"""Export agent transcripts to prompting markdown."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "prompting" / "02_UnitConvertor_06_Red_TDD_Implementation_Progress.md"
TRANSCRIPT_DIR = Path(
    r"C:\Users\jyk17\.cursor\projects\c-DEV-BR-UnitConvertor-06\agent-transcripts"
)

MAX_BODY = 15000


def main() -> None:
    lines = [
        "# Export Transcript — UnitConvertor_06",
        "",
        f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| 항목 | 값 |",
        "|------|-----|",
        "| 보고서 | "
        "[02_UnitConvertor_06_Red_TDD_Implementation_Progress.md]"
        "(../Report/02_UnitConvertor_06_Red_TDD_Implementation_Progress.md) |",
        "| 브랜치 | `red` |",
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
            "## Session — Workspace summary (report 02 scope)",
            "",
            "### Supplement — Topics covered in red-branch session",
            "",
            "1. Git branch strategy (Dual-Track TDD, RED/GREEN/refactor)",
            "2. Test plan sample `meter:2.5` → `docs/test_plan.md`",
            "3. README RED To-Do list",
            "4. pytest GREEN suite (33) + BCE layers",
            "5. `docs/defect_list.md` (DEF-001~008)",
            "6. Defect analysis template (no failure log pasted)",
            "7. `docs/testing/RED-dual-track-tests.md`",
            "8. `tests/red/` pytest skeleton (17, `pytest.fail(\"RED\")`)",
            "9. Report 02 + this transcript + GitHub push",
            "",
        ]
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
