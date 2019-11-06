Set-Location $PSScriptRoot
Get-ChildItem 'result\idt-disp-0-05\I-DT*' -Filter *.csv | Select-Object -ExpandProperty FullName | Import-Csv | Export-Csv .\merged\idt-disp\merged1.csv -NoTypeInformation
Get-ChildItem 'data\' -Filter *.cal | Select-Object Name,FullName | Export-Csv .\merged\idt-disp\merged2.csv -NoTypeInformation
Select-String -Path 'result\idt-disp-0-05\*.log' -Pattern ".*coordX, coordY, timealgorithm, fixationsForPoint, fixations, saccade..*calculateId." |
Select-Object @{
    Name = "Line"
    Expression = {($_.Line -split '\s+')[4]}
} |
#ForEach-Object {Line.Split(" ")} |
Export-Csv .\merged\idt-disp\merged3.csv -NoTypeInformation
