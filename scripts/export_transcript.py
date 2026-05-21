"""Export agent transcripts to prompting markdown."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT_NAME = "03_UnitConvertor_06_Green_TDD_Implementation_Progress"
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
        "| 브랜치 | `B_06` (GREEN TC별 커밋 + `green` PR 머지) |",
        "| 선행 | [02_UnitConvertor_06_Red_TDD_Implementation_Progress.md]"
        "(02_UnitConvertor_06_Red_TDD_Implementation_Progress.md) |",
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
            "## Session — Workspace summary (report 03 scope)",
            "",
            "### Topics covered",
            "",
            "1. Dual-Track TDD one-commit-per-TC (TC-B-01~09, TC-A-01~07)",
            "2. `green` branch bulk GREEN + `B_06` incremental commits",
            "3. PR #1 merge and conflict resolution on `tests/red/`",
            "4. JSON renderer, UnitConverter → ConverterApp delegation",
            "5. README RED vs GREEN To-Do checklists",
            "6. pytest 50 passed, coverage entity/boundary targets",
            "7. Report 03 + transcript export + GitHub push",
            "",
        ]
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
