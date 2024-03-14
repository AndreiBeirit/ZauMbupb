function GenerateRandomSuffix {
    $characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    $suffix = -join ((0..5) | ForEach-Object { $characters[(Get-Random -Maximum $characters.Length)] })
    return $suffix
}
$scriptFiles = Get-ChildItem "C:/Users/vagrant/Downloads/" -Filter *.ps1
if ($scriptFiles.Count -gt 0) {
    $firstTwoLetters = $scriptFiles[0].BaseName.Substring(0, 2)
} else {
    $firstTwoLetters = -join ((0..1) | ForEach-Object { $characters[(Get-Random -Maximum $characters.Length)] })
}
$newDeviceName = "PC-" + $firstTwoLetters + (GenerateRandomSuffix)
Rename-Computer -NewName $newDeviceName -Force -Restart
