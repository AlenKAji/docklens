param(
  [string]$RepoName = "docklens",
  [switch]$Private
)

$ErrorActionPreference = "Stop"

$git = "C:\Program Files\Git\cmd\git.exe"
$gh = "C:\Program Files\GitHub CLI\gh.exe"

if (-not (Test-Path $git)) {
  $git = "git"
}

if (-not (Test-Path $gh)) {
  $gh = "gh"
}

& $gh auth status
if ($LASTEXITCODE -ne 0) {
  Write-Host "GitHub CLI is not authenticated. Run this first:"
  Write-Host "  `"$gh`" auth login --hostname github.com --git-protocol https --web"
  exit 1
}

$visibility = if ($Private) { "--private" } else { "--public" }

& $git status --short
& $gh repo create $RepoName $visibility --source . --remote origin --push
& $gh repo view --web
