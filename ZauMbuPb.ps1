function DownloadAndExtractArchive {
    param(
        [string]$url,
        [string]$destinationPath,
        [string]$keyword
    )

    $webRequest = Invoke-WebRequest -Uri $url -Credential (New-Object System.Management.Automation.PSCredential($username, (ConvertTo-SecureString -String $password -AsPlainText -Force)))
    $jsonResponse = $webRequest.Content | ConvertFrom-Json
    $downloadUrls = $jsonResponse | Where-Object { $_.Name -like "*$keyword*" } | Select-Object -ExpandProperty DownloadURL
    $randomDownloadUrl = $downloadUrls | Get-Random
    $uri = New-Object System.Uri($randomDownloadUrl)
    $fileName = [System.IO.Path]::GetFileName($uri.LocalPath)
    $filePath = Join-Path -Path $destinationPath -ChildPath $fileName
    $bitsJob = Start-BitsTransfer -Source $randomDownloadUrl -Destination $filePath
    while ($bitsJob.JobState -eq "Transferring") {
        Start-Sleep -Seconds 5
        $bitsJob | Get-BitsTransfer | Format-Table -AutoSize
    }

    Expand-Archive -Path $filePath -DestinationPath $destinationPath -Force

    Remove-Item -Path $filePath

    Write-Host "Файл '$fileName' успешно скачан, распакован и удален."
}

function EnsureDirectory {
    param(
        [string]$path
    )

    if (-not (Test-Path -Path $path)) {
        New-Item -Path $path -ItemType Directory | Out-Null
    }
}

function ClearDirectory {
    param(
        [string]$path
    )

    if (Test-Path -Path $path) {
        $items = Get-ChildItem -Path $path -Exclude "Settings.xml" -Force
        foreach ($item in $items) {
            if ($item.Name -ne "Settings.xml") {
                Remove-Item -Path $item.FullName -Recurse -Force
            }
        }
    }
}

$url1 = "https://"
$url2 = "https://"
$username = "a"
$password = "d"
$keyword1 = "Relog_v"
$keyword2 = "ChatBot_v"

ClearDirectory -path "C:\RELOG"
ClearDirectory -path "C:\ChatBot"
EnsureDirectory -path "C:\RELOG"
EnsureDirectory -path "C:\ChatBot"
DownloadAndExtractArchive -url $url1 -destinationPath "C:\RELOG" -keyword $keyword1
DownloadAndExtractArchive -url $url2 -destinationPath "C:\ChatBot" -keyword $keyword2
