$levels = 1
foreach ($u in $levels) {
    & "C:\Users\filip\Downloads\apache-jmeter-5.6.3\bin\jmeter.bat" -n -t .\movies.jmx `
        -Jusers=$u `
        -l "results_${u}u.jtl" `
        -e -o "report_${u}u"
}