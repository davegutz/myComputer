Get-ChildItem -File |
    Group-Object Length |
    Where-Object {$_.Count -gt 1} |
    ForEach-Object {$_.Group |
    Get-FileHash} |
    Group-Object Hash |
    Where-Object {$_.Count -gt 1} |
    ForEach-Object { Write-Host "Duplicate files:"; $_.Group.Path; Write-Host "---" }
