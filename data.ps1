Set-Location $PSScriptRoot
Get-ChildItem 'result\ml-prop-0-5\ML*' -Filter *.csv | Select-Object -ExpandProperty FullName | Import-Csv | Export-Csv .\merged\ml-prop\merged1.csv -NoTypeInformation
Get-ChildItem 'data\' -Filter *.cal | Select-Object Name,FullName | Export-Csv .\merged\ml-prop\merged2.csv -NoTypeInformation
Select-String -Path 'result\ml-prop-0-5\*.log' -Pattern ".*coordX, coordY, fixationsForPoint, timealgorithm, ite, measurementFixations, saccadeCount..*calculateMl." |
Select-Object @{
    Name = "Line"
    Expression = {($_.Line -split '\s+')[4]}
} |
#ForEach-Object {Line.Split(" ")} |
Export-Csv .\merged\ml-prop\merged3.csv -NoTypeInformation
