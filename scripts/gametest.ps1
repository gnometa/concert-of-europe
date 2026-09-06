<#
.SYNOPSIS
  Smoke-test the DEPLOYED mod: launch v2game.exe with CoE_RoI_R, wait until the
  main menu is reached (PASS) or the process dies / stalls (FAIL), then kill it.
.NOTES
  Reads the deploy target, so run scripts/deploy.ps1 first. Clears the mod's
  logs folder before launching. A FAIL-EXIT(-1073741819) with an empty error.log
  and game.log ending at "Executing History" is a history data-shape problem
  (capital not owned, moved province file) - bisect with this script rather
  than hunting statically. Written during the 2026-09-06 crash bisect (see
  docs/CHANGELOG.md "Post-playtest fixes"). Exit code 0 on PASS, 1 otherwise.
.EXAMPLE
  pwsh -File scripts/gametest.ps1 -Label HEAD
#>
param([string]$Label = "run", [int]$TimeoutSeconds = 150)
$ErrorActionPreference = 'Stop'
$game = 'D:\Steam\steamapps\common\Victoria 2'
$logs = 'E:\OneDrive\Documents\Paradox Interactive\Victoria II\CoE_RoI_R\logs'
Get-Process v2game -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 800
if (Test-Path $logs) { Remove-Item "$logs\*" -Force -ErrorAction SilentlyContinue }
$p = Start-Process -FilePath "$game\v2game.exe" -ArgumentList '-mod=mod/CoE_RoI_R.mod' -WorkingDirectory $game -PassThru
$deadline = (Get-Date).AddSeconds($TimeoutSeconds)
$result = 'TIMEOUT'
$lastLen = -1; $stableSince = Get-Date
while ((Get-Date) -lt $deadline) {
  Start-Sleep -Seconds 5
  $sys = ''
  if (Test-Path "$logs\system.log") { $sys = Get-Content "$logs\system.log" -Raw -ErrorAction SilentlyContinue }
  if ($sys -match 'Creating Checksum|Run Application|entering frontend|done frontend') { $result = 'PASS'; break }
  if ($p.HasExited) { $result = "FAIL-EXIT($($p.ExitCode))"; break }
  $len = $sys.Length
  if ($len -eq $lastLen) { if (((Get-Date) - $stableSince).TotalSeconds -gt 55) { $result = 'FAIL-STUCK'; break } }
  else { $lastLen = $len; $stableSince = Get-Date }
}
Get-Process v2game -ErrorAction SilentlyContinue | Stop-Process -Force
$g = if (Test-Path "$logs\game.log") { (Get-Content "$logs\game.log" -Tail 2) -join ' | ' } else { '(none)' }
$s = if (Test-Path "$logs\system.log") { (Get-Content "$logs\system.log" -Tail 1) } else { '(none)' }
$e = if (Test-Path "$logs\error.log") { (Get-Content "$logs\error.log" | Measure-Object -Line).Lines } else { 0 }
Write-Host "RESULT[$Label]=$result"
Write-Host "game.log: $g"
Write-Host "system.log: $s"
Write-Host "error.log lines: $e"
if ($result -eq 'PASS') { exit 0 } else { exit 1 }
