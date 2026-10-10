# Read-only inventory of a legally installed copy; exports metadata only.
param(
    [Parameter(Mandatory=$true)][string]$GameDir,
    [string]$Output = './zomboid-inventory.json'
)
$ErrorActionPreference = 'Stop'
$folder = (Resolve-Path -LiteralPath $GameDir).Path
$important = @('.jar', '.dll', '.so', '.dylib', '.json', '.exe')
$items = @(Get-ChildItem -LiteralPath $folder -Recurse -File -ErrorAction Stop)
$files = @($items | Where-Object { $important -contains $_.Extension.ToLowerInvariant() } | ForEach-Object {
    $relative = $_.FullName.Substring($folder.Length).TrimStart('\','/')
    [PSCustomObject]@{ path = ($relative -replace '\','/'); bytes = $_.Length }
})
$launchers = @($files | Where-Object { $_.path -match 'ProjectZomboid|projectzomboid|lwjgl|fmod|java' } | Select-Object -First 80)
$report = [ordered]@{
    report_format = 'zomboidnx-inventory-v1'
    created_utc = [DateTime]::UtcNow.ToString('o')
    total_files = $items.Count
    total_size_bytes = [long](($items | Measure-Object Length -Sum).Sum)
    selected_files = $files
    candidate_runtime_files = $launchers
    note = 'Metadata only; no game binaries, code or assets exported.'
}
$report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $Output -Encoding UTF8
Write-Host ('Inventory saved: ' + (Resolve-Path -LiteralPath $Output).Path)
Write-Host ('Total files: ' + $items.Count)
Write-Host ('Selected metadata files: ' + $files.Count)
