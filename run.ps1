Set-Location $PSScriptRoot
$files = Get-ChildItem "data" -Filter *.cal
for ($i=0; $i -lt 10; $i++) {
    $name = $files[$i].Name
    Write-Host $name
    python main.py -i $name 'I-DT' -d
}
    
pause