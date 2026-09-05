#!/usr/bin/env python3
"""Factory and artisan profitability report for the CoE_RoI_R Victoria 2 mod.

Reads common/production_types.txt and common/goods.txt and prints, for every
production type of type `factory` or `artisan`:

    inputs        input_goods amounts x base price, summed  (cost per day at
                  full employment, before throughput modifiers)
    output        output_goods amount (`value`) x base price
    ratio         output value / input cost
    rev/worker    output value / workforce

Throughput multipliers, owner output bonuses and the `efficiency` (bonus goods)
blocks are ignored on purpose: throughput scales inputs and output together and
so cancels out of the ratio, and the efficiency block only adds output when the
bonus goods are present in the market. What is left is the base ratio the AI
factory builder and the artisan-promotion code see at base prices.

Usage
  python scripts/balance_factories.py                 the mod
  python scripts/balance_factories.py --vanilla       the vanilla game files
  python scripts/balance_factories.py <folder>        any folder holding common/
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refcheck  # noqa: E402  (parser + paths)

ROOT = refcheck.ROOT
MOD = refcheck.MOD
VANILLA = refcheck.VANILLA


def load(base):
    """Return (prices, production types) from <base>/common/*.txt."""
    goods = refcheck.parse(refcheck.read(Path(base) / "common" / "goods.txt"))
    prices = {}
    for cat in goods:
        for good in cat.children or []:
            cost = good.first("cost")
            if cost is not None:
                prices[good.key] = float(cost)

    nodes = [n for n in refcheck.parse(refcheck.read(Path(base) / "common" / "production_types.txt"))
             if n.children is not None]
    by_name = {n.key: n for n in nodes}

    def field(node, key):
        """Look a field up on the type, falling back to its template."""
        v = node.first(key)
        if v is None:
            tmpl = by_name.get(node.first("template"))
            if tmpl is not None:
                v = tmpl.first(key)
        return v

    types = []
    for node in nodes:
        kind = field(node, "type")
        if kind not in ("factory", "artisan"):
            continue
        inputs = []
        for blk in node.get("input_goods"):
            for g in blk.children or []:
                if g.key and g.value is not None:
                    inputs.append((g.key, float(g.value)))
        out = field(node, "output_goods")
        val = field(node, "value")
        if out is None or val is None:
            continue
        types.append({
            "name": node.key,
            "kind": kind,
            "inputs": inputs,
            "output": out,
            "value": float(val),
            "workforce": float(field(node, "workforce") or 0),
        })
    return prices, types


def report(base, label):
    prices, types = load(base)
    missing = set()
    rows = []
    for t in types:
        cost = 0.0
        for good, qty in t["inputs"]:
            if good not in prices:
                missing.add(good)
            cost += qty * prices.get(good, 0.0)
        if t["output"] not in prices:
            missing.add(t["output"])
        rev = t["value"] * prices.get(t["output"], 0.0)
        wf = t["workforce"] or 1
        rows.append((t, cost, rev, (rev / cost if cost else float("inf")), rev / wf))

    print(f"=== {label}: {base}")
    for kind in ("factory", "artisan"):
        sel = [r for r in rows if r[0]["kind"] == kind]
        if not sel:
            continue
        sel.sort(key=lambda r: -r[3])
        print(f"\n-- {kind} ({len(sel)})")
        print(f"{'name':<28}{'inputs':<46}{'cost':>10}  {'output':<26}{'revenue':>9}{'ratio':>8}{'rev/worker':>12}")
        for t, cost, rev, ratio, per in sel:
            ins = ", ".join(f"{g} {q:g}" for g, q in t["inputs"]) or "-"
            out = f"{t['output']} {t['value']:g}"
            print(f"{t['name']:<28}{ins[:45]:<46}{cost:>10.2f}  {out:<26}{rev:>9.2f}{ratio:>8.2f}{per:>12.5f}")
        r = [x[3] for x in sel if x[3] != float("inf")]
        if r:
            print(f"{'':<28}{'':<46}{'':>10}  {'':<26}{'':>9}{'':>8}   band {min(r):.2f}-{max(r):.2f}")
    if missing:
        print("\n!! goods with no price in goods.txt:", ", ".join(sorted(missing)))
    print()


def main(argv):
    if not argv:
        report(MOD, "mod")
    elif argv[0] in ("--vanilla", "-v"):
        report(VANILLA, "vanilla")
    elif argv[0] in ("--both", "-b"):
        report(MOD, "mod")
        report(VANILLA, "vanilla")
    else:
        report(Path(argv[0]), "folder")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
