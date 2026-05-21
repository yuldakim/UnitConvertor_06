"""Export agent transcripts to prompting markdown."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT_NAME = "04_UnitConvertor_06_Golden_Master_Refactoring_Progress"
OUT = ROOT / "prompting" / f"{REPORT_NAME}.md"
TRANSCRIPT_DIR = Path(
    r"C:\Users\jyk17\.cursor\projects\c-DEV-BR-UnitConvertor-06\agent-transcripts"
)

MAX_BODY = 15000


def main() -> None:
    lines = [
        f"# Export Transcript — {REPORT_NAME}",
        "",
        f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| 항목 | 값 |",
        "|------|-----|",
        f"| 보고서 | [{REPORT_NAME}.md](../Report/{REPORT_NAME}.md) |",
        "| 브랜치 | `refactoring` → PR 머지 → `B_06` → `refactoring` 재생성 |",
        "| 선행 | [03_UnitConvertor_06_Green_TDD_Implementation_Progress.md]"
        "(03_UnitConvertor_06_Green_TDD_Implementation_Progress.md) |",
        "",
        "---",
        "",
    ]

    turn = 0
    for jsonl_path in sorted(TRANSCRIPT_DIR.rglob("*.jsonl")):
        session_id = jsonl_path.parent.name
        lines.append(f"## Session `{session_id}`")
        lines.append("")
        for raw in jsonl_path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not raw.strip():
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError:
                continue
            role = obj.get("role", "unknown")
            msg = obj.get("message", {})
            parts = msg.get("content", [])
            texts = []
            for part in parts:
                if isinstance(part, dict) and part.get("type") == "text":
                    texts.append(part.get("text", ""))
            body = "\n".join(texts).strip()
            if not body:
                continue
            turn += 1
            label = "user" if role == "user" else "assistant"
            lines.append(f"### Turn {turn} — {label}")
            lines.append("")
            if len(body) > MAX_BODY:
                body = body[:MAX_BODY] + "\n\n[... truncated for export ...]"
            lines.append(body)
            lines.append("")
            lines.append("---")
            lines.append("")

    lines.extend(
        [
            "## Session — Workspace summary (report 04 scope)",
            "",
            "### Topics covered",
            "",
            "1. Git: delete `green` branch; create/push `refactoring` from `B_06`",
            "2. Golden Master: `golden_master_expected.txt`, approve pattern, GM-TC-01~04",
            "3. `tests/test_golden_master.py`, `pytest -m golden_master` (4 passed)",
            "4. README Golden Master To-Do (GM-01~GM-09); GM-08 manual branch protection",
            "5. CI: `.github/workflows/golden_master.yml` (`Golden Master Regression`)",
            "6. approvaltests vs 자체 Golden Master — 자체 방식 유지",
            "7. Report 04 + transcript export + push/PR/merge B_06 + refactoring 재분기",
            "",
        ]
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
