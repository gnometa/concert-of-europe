#!/usr/bin/env python3
"""Run the CWTools language server headless against the mod and print its diagnostics.

Usage:
  python scripts/cwtools_check.py [--all] [--json] [--summary] [--via-proxy] [--timeout S] [--debug] [file ...]

Default output is filtered the same way the Claude Code LSP plugin filters it (see
.claude/skills/cwtools-lsp/bin/cwtools_lsp.py): rule-gap noise from the stub Victoria 2
rule set is dropped. --all shows everything. --via-proxy talks to the plugin's proxy exactly
as Claude Code would (bare initialize, no settings) to prove the plugin wiring works.

Requires the CWTools editor extension to be installed; the server binary ships with it.
"""
import argparse
import collections
import json
import os
import re
import subprocess
import sys
import threading
import time
from pathlib import Path
from urllib.request import url2pathname

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "cwtools-lsp" / "bin"))
import cwtools_lsp as cw  # noqa: E402

SEVERITY = {1: "error", 2: "warning", 3: "info", 4: "hint"}


class Client:
    def __init__(self, cmd, debug=False):
        self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=None if debug else subprocess.DEVNULL, bufsize=0)
        self.debug = debug
        self.next_id = 1
        self.pending = {}
        self.diagnostics = {}
        self.loading = None          # None = never seen, True = loading, False = finished
        self.rejected_vanilla = False
        self.lock = threading.Lock()
        self.alive = True
        threading.Thread(target=self._reader, daemon=True).start()

    def request(self, method, params):
        mid = self.next_id
        self.next_id += 1
        ev = threading.Event()
        self.pending[mid] = [ev, None]
        cw.write_message(self.proc.stdin, {"jsonrpc": "2.0", "id": mid, "method": method, "params": params}, self.lock)
        return mid, ev

    def notify(self, method, params):
        cw.write_message(self.proc.stdin, {"jsonrpc": "2.0", "method": method, "params": params}, self.lock)

    def _reader(self):
        try:
            while True:
                msg = cw.read_message(self.proc.stdout)
                if msg is None:
                    break
                if "id" in msg and "method" in msg:
                    self._server_request(msg)
                elif "id" in msg:
                    slot = self.pending.get(msg["id"])
                    if slot:
                        slot[1] = msg
                        slot[0].set()
                else:
                    m, p = msg.get("method"), msg.get("params") or {}
                    if m == "textDocument/publishDiagnostics":
                        self.diagnostics[p["uri"]] = p.get("diagnostics", [])
                    elif m == "loadingBar":
                        self.loading = bool(p.get("enable"))
                    elif m == "promptVanillaPath":
                        self.rejected_vanilla = True
        finally:
            self.alive = False

    def _server_request(self, msg):
        result = None
        if msg["method"] == "workspace/configuration":
            s = {"cwtools": cw.settings()}
            result = []
            for it in msg["params"].get("items", []):
                val = s
                for part in [x for x in (it.get("section") or "").split(".") if x]:
                    val = val.get(part) if isinstance(val, dict) else None
                result.append(val)
        cw.write_message(self.proc.stdin, {"jsonrpc": "2.0", "id": msg["id"], "result": result}, self.lock)


def summarise(rows):
    msgs = collections.Counter((r["code"], re.sub(r"\b\d+\b", "N", r["message"])[:100]) for r in rows)
    print("TOP MESSAGES")
    for (code, m), c in msgs.most_common(30):
        print(f"{c:7d}  {code:6}  {m}")
    dirs = collections.Counter(re.split(r"[\\/]", r["file"])[1] if re.search(r"[\\/]", r["file"]) else "?" for r in rows)
    print("BY FOLDER", dirs.most_common(12))
    print("BY SEVERITY", collections.Counter(r["severity"] for r in rows))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--all", action="store_true", help="do not filter rule-gap noise")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--via-proxy", action="store_true", help="drive the plugin proxy like Claude Code would")
    ap.add_argument("--timeout", type=float, default=600)
    ap.add_argument("--quiet-after", type=float, default=15)
    ap.add_argument("--debug", action="store_true")
    args = ap.parse_args()

    exe, ext = cw.find_server()
    if not exe:
        print("CWTools extension / server not found; install the CWTools editor extension first", file=sys.stderr)
        return 2

    if args.via_proxy:
        cmd = [sys.executable, str(ROOT / ".claude/skills/cwtools-lsp/bin/cwtools_lsp.py"), "proxy"]
        init = {"processId": os.getpid(), "rootUri": cw.to_uri(ROOT), "capabilities": {}}
    else:
        cmd = [str(exe)]
        init = {
            "processId": os.getpid(),
            "rootUri": cw.to_uri(cw.MOD),
            "rootPath": str(cw.MOD),
            "workspaceFolders": [{"uri": cw.to_uri(cw.MOD), "name": cw.MOD.name}],
            "capabilities": {"workspace": {"configuration": True}},
            "initializationOptions": cw.init_options(ext),
        }

    c = Client(cmd, debug=args.debug)
    mid, ev = c.request("initialize", init)
    if not ev.wait(120):
        print("initialize timed out", file=sys.stderr)
        c.proc.kill()
        return 2
    resp = c.pending[mid][1]
    if "error" in resp:
        print("initialize error:", resp["error"], file=sys.stderr)
        c.proc.kill()
        return 2
    c.notify("initialized", {})
    if not args.via_proxy:
        c.notify("workspace/didChangeConfiguration", {"settings": {"cwtools": cw.settings()}})

    start = time.time()
    last_change = time.time()
    last_count = -1
    while time.time() - start < args.timeout and c.alive:
        time.sleep(1)
        count = sum(len(v) for v in c.diagnostics.values())
        if count != last_count:
            last_count, last_change = count, time.time()
        if c.rejected_vanilla:
            print("server rejected the vanilla path; check GAME in cwtools_lsp.py", file=sys.stderr)
            break
        quiet = time.time() - last_change > args.quiet_after
        if c.loading is False and quiet:
            break
        if c.loading is None and args.via_proxy and count and quiet:
            break  # proxy swallows loadingBar; rely on quiet period
        if c.loading is None and time.time() - start > 120 and quiet:
            break

    wanted = None
    if args.files:
        wanted = {cw.to_uri(f).lower() for f in args.files}
        for f in args.files:
            p = Path(f)
            c.notify("textDocument/didOpen", {"textDocument": {
                "uri": cw.to_uri(p), "languageId": "vic2", "version": 1,
                "text": p.read_bytes().decode("cp1252", errors="replace")}})
        time.sleep(5)

    rows = []
    for uri, diags in sorted(c.diagnostics.items()):
        if wanted is not None and uri.lower() not in wanted:
            continue
        path = uri
        if uri.startswith("file:"):
            path = url2pathname(uri[5:]).lstrip("\\/")
            try:
                path = str(Path(path).resolve().relative_to(ROOT))
            except (ValueError, OSError):
                pass
        for d in diags:
            if not args.all and not args.via_proxy and not cw.keep_diagnostic(d):
                continue
            r = d.get("range", {}).get("start", {})
            rows.append({"file": path, "line": r.get("line", 0) + 1, "col": r.get("character", 0) + 1,
                         "severity": SEVERITY.get(d.get("severity"), "unknown"),
                         "code": d.get("code"), "message": d.get("message", "").strip()})

    try:
        c.request("shutdown", None)
        c.notify("exit", None)
    except Exception:  # noqa: BLE001
        pass
    time.sleep(0.5)
    if c.proc.poll() is None:
        c.proc.kill()

    if args.json:
        print(json.dumps(rows, indent=1))
    elif args.summary:
        summarise(rows)
    else:
        for r in rows:
            print(f"{r['file']}:{r['line']}:{r['col']}: {r['severity']} {r['code']}: {r['message'].splitlines()[0]}")
    errs = sum(1 for r in rows if r["severity"] == "error")
    warns = sum(1 for r in rows if r["severity"] == "warning")
    print(f"{len(rows)} diagnostic(s): {errs} error(s), {warns} warning(s); "
          f"{len(c.diagnostics)} file(s) reported; {time.time() - start:.0f}s"
          f"{'' if args.all or args.via_proxy else ' (filtered; use --all for everything)'}", file=sys.stderr)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
