---
name: cwtools-lsp
description: Background knowledge about the CWTools language server plugin and how to read its diagnostics for this Victoria 2 mod. Not a task.
user-invocable: false
---

# CWTools LSP plugin

This plugin runs the CWTools Paradox language server behind `bin/cwtools_lsp.py proxy`, so diagnostics arrive automatically after edits to `.txt`, `.gui`, `.gfx`, and `.map` files.

What reaches you has already been filtered. The community Victoria 2 rule set is a stub from 2020, so the proxy drops these classes as rule gaps, not mod bugs:

- "X is unexpected in Y" (it does not know `NOT`, `OR`, `months`, unit names, tags, ...)
- "Expecting a "<enum>" value" (enums with no values in the rules)
- "used in wrong scope", "Unknown type referenced", configuration errors
- "Missing picture", "Missing Field of Enum/TypeField/Int", and similar required-field errors

Trust what remains: parse errors (unbalanced braces, code CW001), "Too many <key>, expecting at most 1" duplicates, and any warning or info item.

For a whole-mod run outside the editor use:

```
python scripts/cwtools_check.py            # filtered, whole mod
python scripts/cwtools_check.py --all      # unfiltered, tens of thousands of lines
python scripts/cwtools_check.py <file>...  # only those files
```

Prerequisite: the CWTools editor extension must be installed (Antigravity or VS Code); the proxy locates `CWTools Server.exe` inside it. If it is missing, the plugin shows "Executable not found" in the `/plugin` Errors tab.
