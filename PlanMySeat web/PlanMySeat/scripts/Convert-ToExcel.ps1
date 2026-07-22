# Creates .xlsx Excel files from CSV reports without Python (uses Excel COM if available, else SpreadsheetML XML)
param(
    [string]$ReportsDir = "$PSScriptRoot\..\reports"
)

$ErrorActionPreference = "Stop"
$excelDir = Join-Path $ReportsDir "excel"
New-Item -ItemType Directory -Force -Path $excelDir | Out-Null

function Convert-CsvToSpreadsheetXml {
    param([string]$CsvPath, [string]$XmlPath, [string]$SheetName)

    $rows = Import-Csv $CsvPath
    $headers = ($rows | Get-Member -MemberType NoteProperty).Name

    $xml = @"
<?xml version="1.0" encoding="UTF-8"?>
<?mso-application progid="Excel.Sheet"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:x="urn:schemas-microsoft-com:office:excel"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">
<Styles>
 <Style ss:ID="Header"><Font ss:Bold="1" ss:Color="#FFFFFF"/><Interior ss:Color="#1A73E8" ss:Pattern="Solid"/></Style>
 <Style ss:ID="Pass"><Font ss:Bold="1" ss:Color="#0D904F"/><Interior ss:Color="#E6F4EA" ss:Pattern="Solid"/></Style>
</Styles>
<Worksheet ss:Name="$SheetName">
<Table>
<Row>
"@

    foreach ($h in $headers) {
        $xml += "<Cell ss:StyleID=`"Header`"><Data ss:Type=`"String`">$([System.Security.SecurityElement]::Escape($h))</Data></Cell>"
    }
    $xml += "</Row>"

    foreach ($row in $rows) {
        $xml += "<Row>"
        foreach ($h in $headers) {
            $val = $row.$h
            $style = if ($h -eq "Status" -and $val -eq "PASSED") { ' ss:StyleID="Pass"' } else { "" }
            $type = if ($val -match '^\d+$') { "Number" } else { "String" }
            $xml += "<Cell$style><Data ss:Type=`"$type`">$([System.Security.SecurityElement]::Escape("$val"))</Data></Cell>"
        }
        $xml += "</Row>"
    }

    $xml += "</Table></Worksheet></Workbook>"
    $xml | Out-File -FilePath $XmlPath -Encoding UTF8
}

function Convert-CsvToXlsxViaExcel {
    param([string]$CsvPath, [string]$XlsxPath, [string]$SheetName)

    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    try {
        $wb = $excel.Workbooks.Open($CsvPath)
        $wb.Worksheets.Item(1).Name = $SheetName
        $wb.SaveAs($XlsxPath, 51) # xlOpenXMLWorkbook
        $wb.Close($false)
    } finally {
        $excel.Quit()
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
    }
}

$pairs = @(
    @{ Csv = "appium-android-report-300.csv"; Xlsx = "appium-android-report-300.xlsx"; Sheet = "Mobile Tests 300" },
    @{ Csv = "selenium-web-report-300.csv"; Xlsx = "selenium-web-report-300.xlsx"; Sheet = "Web Tests 300" }
)

$hasExcel = $false
try {
    $testExcel = New-Object -ComObject Excel.Application -ErrorAction Stop
    $testExcel.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($testExcel) | Out-Null
    $hasExcel = $true
} catch {
    $hasExcel = $false
}

foreach ($p in $pairs) {
    $csvPath = Join-Path $ReportsDir $p.Csv
    if (-not (Test-Path $csvPath)) {
        Write-Warning "Missing $csvPath - run Generate-TestReports.ps1 first"
        continue
    }

    $xlsxPath = Join-Path $excelDir $p.Xlsx
    if ($hasExcel) {
        Convert-CsvToXlsxViaExcel -CsvPath $csvPath -XlsxPath $xlsxPath -SheetName $p.Sheet
        Write-Host "Created $xlsxPath (via Excel COM)"
    } else {
        $xmlPath = $xlsxPath -replace '\.xlsx$', '.xml'
        Convert-CsvToSpreadsheetXml -CsvPath $csvPath -XmlPath $xmlPath -SheetName $p.Sheet
        Write-Host "Created $xmlPath (Excel XML - open with Excel and Save As .xlsx)"
    }
}

Write-Host "`nExcel reports ready in: $excelDir"
