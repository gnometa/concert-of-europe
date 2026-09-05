#!/usr/bin/env python3
"""CWTools language-server glue for the CoE_RoI_R mod.

Used two ways:

  python cwtools_lsp.py proxy      stdio LSP proxy between Claude Code and "CWTools Server.exe"
  import cwtools_lsp               helpers shared with scripts/cwtools_check.py

Why a proxy instead of pointing Claude Code at the server directly:
  * the server binary lives inside a versioned editor-extension folder (path discovered here);
  * the server crashes unless workspace/didChangeConfiguration carries every cwtools.* key,
    and it only starts scanning the mod after that notification, so the proxy sends it;
  * the server must be told language=vic2 and the mod folder via initializationOptions/rootUri;
  * the community Victoria 2 rule set is a stub, so ~85k of the diagnostics it emits are
    rule gaps, not mod bugs. The proxy drops those classes so only actionable ones reach Claude.

All logging goes to stderr; stdout is protocol only.
"""
import glob
import json
import os
import re
import subprocess
import sys
import threading
from pathlib import Path
from urllib.request import pathname2url

REPO = Path(__file__).resolve().parents[4]          # .claude/skills/cwtools-lsp/bin -> repo root
MOD = REPO / "CoE_RoI_R"
GAME = Path(r"D:\Steam\steamapps\common\Victoria 2")
RULES = REPO / ".cwtools"

EXT_GLOBS = [
    "~/.antigravity-ide/extensions/tboby.cwtools-vscode-*",
    "~/.vscode/extensions/tboby.cwtools-vscode-*",
    "~/.vscode-insiders/extensions/tboby.cwtools-vscode-*",
    "~/.cursor/extensions/tboby.cwtools-vscode-*",
]


def log(*a):
    print("[cwtools-lsp]", *a, file=sys.stderr, flush=True)


def find_extension():
    for g in EXT_GLOBS:
        hits = sorted(glob.glob(os.path.expanduser(g)))
        if hits:
            return Path(hits[-1])
    return None


def find_server():
    ext = find_extension()
    if not ext:
        return None, None
    exe = ext / "bin" / "server" / "win-x64" / "CWTools Server.exe"
    return (exe if exe.exists() else None), ext


def to_uri(p):
    return "file:" + pathname2url(str(Path(p).resolve()))


def init_options(ext):
    return {
        "language": "vic2",
        "isVanillaFolder": False,
        "rulesCache": str(ext / ".cwtools"),
        "rules_version": "latest",
        "repoPath": "https://github.com/cwtools/cwtools-vic2-config",
        "diagnosticLogging": False,
    }


def settings():
    # Every key is read unconditionally by the server; missing ones throw.
    return {
        "cache": {"eu4": "", "stellaris": "", "hoi4": "", "ck2": "", "imperator": "",
                  "vic2": str(GAME), "ck3": "", "vic3": "", "eu5": ""},
        "rules_folder": str(RULES) if RULES.exists() else "",
        "rules_version": "latest",
        "localisation": {"languages": ["English"], "generated_strings": ':0 "REPLACE_ME"'},
        "errors": {"vanilla": False, "ignore": [], "ignorefiles": ["README.txt", "credits.txt"]},
        "ignore_patterns": ["**/99_README**.txt"],
        "maxFileSize": 5,
        "experimental": True,
        "debug_mode": False,
        "logging": {"diagnostic": False},
        "trace": {"server": "off"},
    }


# --------------------------------------------------------------------------- filtering
# Measured on 2026-09-05 against the full mod: 84,945 diagnostics, of which everything
# below is noise from the incomplete cwtools-vic2-config rule set.
NOISE_CODES = {
    "CW240",  # 'Expecting a "<enum>" value' - enums with no values defined in the rules
    "CW247",  # 'used in wrong scope' - scope rules in the config are wrong
    "CW262", "CW263", "CW264",  # '<key> is unexpected in <block>' - NOT/OR/months/tags/etc.
    "CW998",  # configuration error in the rules themselves
    "CW999",  # 'Unknown type referenced'
}
NOISE_MESSAGE = re.compile(
    r"^(Missing Field of Enum|Missing picture|Missing Field of TypeField|Missing Field of Int"
    r"|Missing (defender_goal|unit_names|factor|days|months|target|ideology|independence"
    r"|demands_enforced_effect|demands_enforced_trigger))\b"
)


def keep_diagnostic(d):
    code = str(d.get("code") or "")
    sev = d.get("severity") or 1
    msg = (d.get("message") or "").strip()
    if sev == 2:                      # warnings ("Too many X") are rare and real
        return True
    if code in NOISE_CODES:
        return False
    if code == "CW242" and NOISE_MESSAGE.match(msg):
        return False
    return True


def filter_diagnostics(params):
    params = dict(params)
    params["diagnostics"] = [d for d in params.get("diagnostics", []) if keep_diagnostic(d)]
    return params


# --------------------------------------------------------------------------- framing
def read_message(stream):
    headers = {}
    line = stream.readline()
    if not line:
        return None
    while line and line.strip():
        k, _, v = line.decode("ascii", "replace").partition(":")
        headers[k.strip().lower()] = v.strip()
        line = stream.readline()
    n = int(headers.get("content-length", 0))
    body = b""
    while len(body) < n:
        chunk = stream.read(n - len(body))
        if not chunk:
            return None
        body += chunk
    return json.loads(body.decode("utf-8"))


def write_message(stream, msg, lock):
    data = json.dumps(msg).encode("utf-8")
    with lock:
        stream.write(f"Content-Length: {len(data)}\r\n\r\n".encode("ascii") + data)
        stream.flush()


# --------------------------------------------------------------------------- proxy
# Server -> client notifications that are CWTools-specific and mean nothing to Claude Code.
CUSTOM_NOTIFICATIONS = {"loadingBar", "debugBar", "createVirtualFile", "promptReload",
                        "forceReload", "promptVanillaPath", "updateFileList"}


def proxy():
    exe, ext = find_server()
    if not exe:
        log("CWTools Server.exe not found; install the CWTools editor extension first")
        return 2
    server = subprocess.Popen([str(exe)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=sys.stderr, bufsize=0)
    client_in = sys.stdin.buffer
    client_out = sys.stdout.buffer
    out_lock = threading.Lock()
    srv_lock = threading.Lock()
    dropped = {"n": 0}

    def to_server(msg):
        write_message(server.stdin, msg, srv_lock)

    def to_client(msg):
        write_message(client_out, msg, out_lock)

    def client_loop():
        try:
            while True:
                msg = read_message(client_in)
                if msg is None:
                    break
                method = msg.get("method")
                if method == "initialize":
                    p = msg.setdefault("params", {})
                    p["rootUri"] = to_uri(MOD)
                    p["rootPath"] = str(MOD)
                    p["workspaceFolders"] = [{"uri": to_uri(MOD), "name": MOD.name}]
                    p["initializationOptions"] = init_options(ext)
                    p.setdefault("capabilities", {}).setdefault("workspace", {})["configuration"] = True
                    log("initialize -> mod root", MOD)
                elif method == "initialized":
                    to_server(msg)
                    to_server({"jsonrpc": "2.0", "method": "workspace/didChangeConfiguration",
                               "params": {"settings": {"cwtools": settings()}}})
                    log("sent cwtools settings; server is scanning the mod")
                    continue
                elif method == "workspace/didChangeConfiguration":
                    msg["params"] = {"settings": {"cwtools": settings()}}
                elif method == "textDocument/didOpen":
                    td = msg.get("params", {}).get("textDocument", {})
                    td["languageId"] = "vic2"
                to_server(msg)
        except Exception as e:  # noqa: BLE001
            log("client loop ended:", e)
        finally:
            try:
                server.stdin.close()
            except Exception:  # noqa: BLE001
                pass

    def server_loop():
        try:
            while True:
                msg = read_message(server.stdout)
                if msg is None:
                    break
                method = msg.get("method")
                if "id" in msg and method:                      # request from server
                    if method == "workspace/configuration":
                        items = msg.get("params", {}).get("items", [])
                        s = {"cwtools": settings()}
                        result = []
                        for it in items:
                            val = s
                            for part in [x for x in (it.get("section") or "").split(".") if x]:
                                val = val.get(part) if isinstance(val, dict) else None
                            result.append(val)
                        to_server({"jsonrpc": "2.0", "id": msg["id"], "result": result})
                        continue
                    to_client(msg)
                    continue
                if method == "textDocument/publishDiagnostics":
                    before = len(msg["params"].get("diagnostics", []))
                    msg["params"] = filter_diagnostics(msg["params"])
                    dropped["n"] += before - len(msg["params"]["diagnostics"])
                elif method in CUSTOM_NOTIFICATIONS:
                    if method == "promptVanillaPath":
                        log("server rejected the vanilla path; check GAME in cwtools_lsp.py")
                    elif method == "loadingBar" and not msg.get("params", {}).get("enable"):
                        log(f"scan finished; suppressed {dropped['n']} rule-gap diagnostics so far")
                    continue
                to_client(msg)
        except Exception as e:  # noqa: BLE001
            log("server loop ended:", e)

    t1 = threading.Thread(target=client_loop, daemon=True)
    t2 = threading.Thread(target=server_loop, daemon=True)
    t1.start()
    t2.start()
    t1.join()
    server.wait(timeout=10) if server.poll() is None else None
    if server.poll() is None:
        server.kill()
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "proxy":
        sys.exit(proxy())
    print(__doc__)
