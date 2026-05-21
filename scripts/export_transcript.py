"""Export agent transcripts to prompting markdown."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT_NAME = "06_UnitConvertor_06_Bonus_RegisterUnit_Progress"
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
        "| 브랜치 | `feature` → PR 머지 → `B_06` |",
        "| 선행 | [05_UnitConvertor_06_Dual_Track_Refactoring_Progress.md]"
        "(05_UnitConvertor_06_Dual_Track_Refactoring_Progress.md) |",
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
            "## Session — Workspace summary (report 06 scope)",
            "",
            "### Topics covered",
            "",
            "1. Bonus RED: decaying_unit.py stub + tests/test_decaying_unit.py (BT-01~06, @pytest.mark.bonus)",
            "2. Bonus GREEN: UnitRegistry + ConversionEngine facade in decaying_unit.py",
            "3. Verification: pytest 69 passed, GM 8 passed, entity 95% / boundary 100% cov",
            "4. registerUnit negative ratio → InvalidRatioError (ValueError subclass)",
            "5. Report 06 + transcript export; commit/push feature → PR to B_06",
            "",
        ]
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
