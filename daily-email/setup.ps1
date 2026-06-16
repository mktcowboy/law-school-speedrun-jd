<#
  Interactive setup for the daily law-school reading email.

  What it does:
    1. Asks for your recipient email, Gmail sender + app password, start date, and send time.
    2. Writes config.json (kept out of git).
    3. Sends a test email so you can confirm delivery.
    4. Registers a Windows Scheduled Task that runs send_daily.py every day.

  Run from this folder:
    powershell -ExecutionPolicy Bypass -File .\setup.ps1
#>

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

# --- Find Python ---
$python = $null
foreach ($cmd in @("py", "python")) {
    $found = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($found) { $python = $found.Source; break }
}
if (-not $python) { throw "Python not found on PATH. Install Python 3.10+ and re-run." }
Write-Host "Using Python: $python" -ForegroundColor Cyan

# --- Collect settings ---
Write-Host ""
Write-Host "=== Daily Law-School Reading Email setup ===" -ForegroundColor Green
Write-Host ""
$recipient = Read-Host "Email address to RECEIVE the daily reading"
$sender    = Read-Host "Gmail address to SEND from (can be the same)"
Write-Host ""
Write-Host "You need a Gmail APP PASSWORD (not your normal password)." -ForegroundColor Yellow
Write-Host "Get one at: https://myaccount.google.com/apppasswords" -ForegroundColor Yellow
Write-Host "(Requires 2-Step Verification enabled. It is 16 letters; spaces are removed automatically.)"
$securePw = Read-Host "Gmail app password" -AsSecureString
$appPassword = ([System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePw))) -replace '\s',''

Write-Host ""
$startDefault = (Get-Date).ToString("yyyy-MM-dd")
$startInput = Read-Host "Start date (Day 1 of 90) [default: today $startDefault]"
if ([string]::IsNullOrWhiteSpace($startInput)) { $startInput = $startDefault }

$timeInput = Read-Host "Daily send time, 24h HH:mm [default: 07:00]"
if ([string]::IsNullOrWhiteSpace($timeInput)) { $timeInput = "07:00" }

# --- Write config.json ---
$config = [ordered]@{
    recipient    = $recipient
    sender       = $sender
    app_password = $appPassword
    start_date   = $startInput
    smtp_host    = "smtp.gmail.com"
    smtp_port    = 587
}
$configPath = Join-Path $here "config.json"
($config | ConvertTo-Json) | Out-File -FilePath $configPath -Encoding utf8
Write-Host "Wrote $configPath" -ForegroundColor Cyan

# --- Send a test email (day 1) ---
Write-Host ""
Write-Host "Sending a test email (Day 1)..." -ForegroundColor Green
& $python (Join-Path $here "send_daily.py") --day 1
if ($LASTEXITCODE -ne 0) {
    throw "Test send failed. Check the app password and sender address, then re-run."
}
Write-Host "Test email sent. Check your inbox (and spam)." -ForegroundColor Green

# --- Register the scheduled task ---
Write-Host ""
$taskName = "LawSchoolDailyReading"
$action = New-ScheduledTaskAction -Execute $python `
    -Argument ("`"{0}`"" -f (Join-Path $here "send_daily.py")) `
    -WorkingDirectory $here
$trigger = New-ScheduledTaskTrigger -Daily -At $timeInput
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun `
    -DontStopOnIdleEnd -ExecutionTimeLimit (New-TimeSpan -Minutes 10)

Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger `
    -Settings $settings -Description "Daily JD speedrun reading assignment email" | Out-Null

Write-Host ""
Write-Host "Scheduled task '$taskName' registered: runs daily at $timeInput." -ForegroundColor Green
Write-Host "If your PC is asleep/off at that time, it runs at the next wake (StartWhenAvailable)." -ForegroundColor Gray
Write-Host ""
Write-Host "Done. You'll get Day 1 today and a new assignment each day through Day 90." -ForegroundColor Green
Write-Host "To stop it later:  Unregister-ScheduledTask -TaskName $taskName -Confirm:`$false" -ForegroundColor Gray
