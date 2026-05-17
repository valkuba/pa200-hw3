param($QueueItem, $TriggerMetadata)

# Zpráva přišla jako objekt (Azure Functions deserializuje JSON automaticky)
$email   = $QueueItem.email
$message = $QueueItem.message

Write-Host "=== Newsletter zpracován ==="
Write-Host "Komu:  $email"
Write-Host "Text:  $message"
Write-Host "Čas:   $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host ">>> Simulace odeslání emailu OK <<<"
