# Run AFTER: gh auth login (web browser recommended)
# Usage: powershell -ExecutionPolicy Bypass -File scripts/pr_merge_refactoring_to_B06.ps1

$ErrorActionPreference = "Stop"
$gh = if (Get-Command gh -ErrorAction SilentlyContinue) { "gh" }
      else { Join-Path $env:LOCALAPPDATA "gh-cli\bin\gh.exe" }

if (-not (Test-Path $gh)) { throw "gh not found. Install GitHub CLI or use portable gh-cli." }

& $gh auth status | Out-Host
if ($LASTEXITCODE -ne 0) { throw "Run: `"$gh`" auth login" }

Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "Creating PR refactoring -> B_06 ..."
$prUrl = & $gh pr create --base B_06 --head refactoring `
    --title "refactor: Dual-Track BCE cleanup (CLI adapter, GM subprocess, boundary cov 100%)" `
    --body-file pr-body-refactoring.md 2>&1
$prUrl | Out-Host
if ($LASTEXITCODE -ne 0) { throw "pr create failed" }

$prNum = (& $gh pr list --base B_06 --head refactoring --json number -q ".[0].number")
Write-Host "PR #$prNum"

Write-Host "Posting review comment ..."
& $gh pr comment $prNum --body-file docs/pr-review-refactoring.md
if ($LASTEXITCODE -ne 0) { throw "pr comment failed" }

Write-Host "Waiting for checks (60s) ..."
Start-Sleep -Seconds 60
& $gh pr checks $prNum

Write-Host "Merging squash into B_06 ..."
& $gh pr merge $prNum --squash --delete-branch=false
if ($LASTEXITCODE -ne 0) { throw "pr merge failed: fix CI or branch protection first" }

Write-Host "Done. Merged PR #$prNum into B_06."
