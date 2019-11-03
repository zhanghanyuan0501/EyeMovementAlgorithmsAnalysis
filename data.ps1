Set-Location $PSScriptRoot
Get-ChildItem 'result\idt-time-200\I-DT*' -Filter *.csv | Select-Object -ExpandProperty FullName | Import-Csv | Export-Csv .\merged\idt-time\merged1.csv -NoTypeInformation
Get-ChildItem 'data\' -Filter *.cal | Select-Object Name,FullName | Export-Csv .\merged\idt-time\merged2.csv -NoTypeInformation
Select-String -Path 'result\idt-time-200\*.log' -Pattern ".*coordX, coordY, timealgorithm, fixationsForPoint, fixations..*calculateIdtAlgorithm." |
Select-Object @{
    Name = "Line"
    Expression = {($_.Line -split '\s+')[4]}
} |
#ForEach-Object {Line.Split(" ")} |
Export-Csv .\merged\idt-time\merged3.csv -NoTypeInformation
