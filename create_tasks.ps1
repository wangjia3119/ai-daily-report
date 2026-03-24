$action1 = New-ScheduledTaskAction -Execute "C:\Users\jiawa\ai-daily-report\run_daily.bat"
$trigger1 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday -At "08:00"
Register-ScheduledTask -TaskName "AI-Daily" -Action $action1 -Trigger $trigger1 -Force | Out-Null
Write-Host "OK: AI-Daily created"

$action2 = New-ScheduledTaskAction -Execute "C:\Users\jiawa\ai-daily-report\run_weekly.bat"
$trigger2 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday -At "08:00"
Register-ScheduledTask -TaskName "AI-Weekly" -Action $action2 -Trigger $trigger2 -Force | Out-Null
Write-Host "OK: AI-Weekly created"
