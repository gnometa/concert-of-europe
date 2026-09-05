# Mirrors the mod from this repo into the Victoria 2 mod folder, exactly 1:1.
# Run manually:  pwsh -File scripts/deploy.ps1
# Also run automatically by .githooks/pre-push on every git push.
$ErrorActionPreference = 'Stop'
$repo   = Split-Path -Parent $PSScriptRoot
$game   = 'D:\Steam\steamapps\common\Victoria 2'
$target = Join-Path $game 'mod'
$src    = Join-Path $repo 'CoE_RoI_R'
$dst    = Join-Path $target 'CoE_RoI_R'

if (-not (Test-Path $game)) { throw "Game folder not found: $game" }
New-Item -ItemType Directory -Force $dst | Out-Null

# /MIR = copy everything, delete anything in the target that is not in the source.
# Exit codes 0-7 are success; 8+ are failures.
robocopy $src $dst /MIR /NJH /NJS /NDL /NFL /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy failed with exit code $LASTEXITCODE" }
Copy-Item (Join-Path $repo 'CoE_RoI_R.mod') $target -Force

# Verify: a second /MIR in list-only mode must find nothing left to copy or delete.
$pending = robocopy $src $dst /MIR /L /NJH /NJS /NDL /NP /NS /NC | Where-Object { $_.Trim() }
if ($pending) {
    $pending | ForEach-Object { Write-Host "  $_" }
    throw "Deploy target is not 1:1 with the repo (see list above)"
}

# Verify contents byte-for-byte via hashes.
$srcHash = Get-ChildItem $src -Recurse -File | ForEach-Object {
    "$($_.FullName.Substring($src.Length))|$((Get-FileHash $_.FullName -Algorithm SHA256).Hash)" } | Sort-Object
$dstHash = Get-ChildItem $dst -Recurse -File | ForEach-Object {
    "$($_.FullName.Substring($dst.Length))|$((Get-FileHash $_.FullName -Algorithm SHA256).Hash)" } | Sort-Object
$diff = Compare-Object $srcHash $dstHash
if ($diff) {
    $diff | ForEach-Object { Write-Host "  $($_.SideIndicator) $($_.InputObject.Split('|')[0])" }
    throw "Hash mismatch between repo and deploy target"
}
if ((Get-FileHash (Join-Path $repo 'CoE_RoI_R.mod')).Hash -ne (Get-FileHash (Join-Path $target 'CoE_RoI_R.mod')).Hash) {
    throw "CoE_RoI_R.mod differs in deploy target"
}

Write-Host "Deployed 1:1 to $dst ($($srcHash.Count) files verified)"
exit 0
