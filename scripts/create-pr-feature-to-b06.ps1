# Create PR: feature -> B_06 (requires: gh auth login once)
$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$ghCandidates = @(
    "$env:ProgramFiles\GitHub CLI\gh.exe",
    "$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe",
    (Get-ChildItem -Path "$env:TEMP\gh-cli" -Recurse -Filter "gh.exe" -ErrorAction SilentlyContinue |
        Select-Object -First 1).FullName
)
$gh = $ghCandidates | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
if (-not $gh) {
    Write-Host "gh not found. Install: https://cli.github.com/ or run: winget install GitHub.cli"
    Write-Host "Or open in browser:"
    Write-Host "https://github.com/yuldakim/UnitConvertor_06/compare/B_06...feature?expand=1"
    exit 1
}

& $gh auth status 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Run GitHub login first:"
    & $gh auth login --hostname github.com --git-protocol https --web
}

$bodyFile = Join-Path $repoRoot "pr-body-feature-b06.md"
& $gh pr create `
    --base B_06 `
    --head feature `
    --title "feat: Bonus registerUnit (cubit) + Report 06" `
    --body-file $bodyFile

Write-Host ""
Write-Host "Or open in browser:"
Write-Host "https://github.com/yuldakim/UnitConvertor_06/compare/B_06...feature?expand=1"
