import os
from datetime import datetime

from knitter import library
from knitter.configure import General


def html_source_header(title="Web UI Automation Test Report"):
    return """
     <!DOCTYPE HTML>
        <html>

        <head>
            <title>%s</title>

            <style>
                a {
                    color: #034CAC;
                    overflow: hidden;
                    text-decoration: none;
                    display: inline; /* do not show the dot of list */
                }

                a:hover {
                    text-decoration: underline;
                    color: #034CAC;
                }
                a:visited {
                    color: #034CAC;
                }
                body {
                    width: 100%%;
                    color: #5a5a5a;
                    font-size: 13px;
                    font-family: Verdana, Courier New;
                    text-align: center;
                }
                table, td, th {
                    border: 1px solid rgb(119, 119, 119);
                    border-collapse: collapse;
                    width: 1400px;
                    text-align: center;
                }
                .tcaption {
                    background-color: rgb(116, 162, 179);
                }
                .theader {
                    background-color: rgba(186, 216, 221, 0.61);
                }
                .tfail{
                    background-color: #FF6F6F;
                }
                h1{
                    text-align: center;
                }
                table {
                    box-shadow: 3px 3px 2px #d3d3d3;
                }
                
                .report-link{
                    color: #5a5a5a !important;
                    font-family: Courier New, Courier, monospace;
                    background-color:#f7f7f7; 
                    border-radius: 2px; 
                    box-shadow: 2px 2px 2px #d3d3d3;
                    margin: 10px;
                    padding: 5px 20px 5px 20px;
                }
                a.report-link:hover{
                    font-family: Courier New, Courier, monospace;
                    color: #5a5a5a;
                    background-color:#f1f1f1; 
                    text-decoration: none;
                    box-shadow: 4px 4px 2px #d3d3d3;
                    border-radius: 2px; 
                }
                hr{
                    margin: 20px;
                }
            </style>
        </head>    
    """ % title


def html_source_body(title="Web UI Automation Test Report", countdown=True):
    if countdown is False:
        return """
        <body> 
        <h1>%s</h1> 
        <p style="text-align: center">
            <a href="..\index.html" class="report-link">Latest Test Report</a>
            &nbsp;&nbsp;&nbsp;
            <a href="..\history.html" class="report-link">History Test Reports</a>
        </p>
        <br />
        """ % title
    
    return """
    <body>
    <script>
        function countdown(){
            var timer = 9;
            setInterval(function() {
                timer--;
                document.getElementById('timer').innerHTML = timer;
        
            }, 1000);
        }
        function autorefresh(){
            window.location.reload(); 
        } 
        
        countdown();
        window.setTimeout('autorefresh()', 9000);
    </script>
    
    <h1>%s</h1>
    <p style="text-align: center">
        <a href="index.html" class="report-link">Latest Test Report</a>
        &nbsp;&nbsp;&nbsp;
        <a href="history.html" class="report-link">History Test Reports</a>
    </p>
    <br />
    
""" % title


def html_source_table1(args):
    return """
    <table style="margin: auto">
        <tr class="tcaption"><th colspan="5">Summary</th></tr>
        
        <tr class="theader">
            <th>Start Time/Stop Time</th>
            <th>Duration</th>
            <th>Total Cases</th>
            <th>Passed Cases</th>
            <th>Failed Cases</th>
        </tr>
        <tr>
            <td style='width: 27%%'>%s =&gt; %s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
        </tr>
    </table>
""" % tuple(args)


def html_source_table_history_header():
    return """
    <table style="margin: auto">
        <tr class="tcaption"><th colspan="5">History Reports</th></tr>
        
        <tr class="theader">
            <th>Folder</th>
            <th>Duration</th>
            <th>Total Cases</th>
            <th>Passed Cases</th>
            <th>Failed Cases</th>
        </tr>
""" 


def html_source_table_history(*args):
    return """
        <tr>
            <td style='width: 50%%; text-align: left; padding-left: 20px;'><a href="%s/index.html">%s</a></td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
        </tr>
""" % args


def html_source_table2():
    return """
    <br />
    <br />
    <table style="margin: auto">
        <tr class="tcaption"><th colspan="5">Details</th></tr>
        <tr class="theader">
            <th>Start Time/Stop Time</th>
            <th>Test Case</th>
            <th>Duration</th>
            <th>Browser</th>
            <th>Result</th>
        </tr>

"""


def html_source_test_cases(test_cases):
    return_src_code = ""
    
    for test_case in test_cases:
        return_src_code += """
                <tr>
                    <td style="width: 20%%">%s</td>
                    <td style="width: 52%%; text-align: left;">&nbsp;%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    %s
                </tr>
        """ % tuple(test_case)
    
    return return_src_code


def html_source_end_table():
    return """
    </table> 
<br />
<br />
<br />
"""


def html_source_version_info():
    return u"""
<p style="text-align: center">%s</p>
""" % library.version_info()


def html_source_foot():
    return u"""
<hr />
<p style="text-align: center">@2014-2018 Powered by <a href="https://pypi.python.org/pypi/knitter">Knitter</a></p>
<br />
</body>
</html>
"""


def generate_html_report(test_status, test_cases=[], countdown=True):
    if General.QuickTest is True:
        return
    
    library.create_folder(General.Path.Result)
    
    with open(os.path.join(General.Path.Result, "index.html"), "w") as f:
        f.write(html_source_header())
        f.write(html_source_body(countdown=countdown))
        
        f.write(html_source_table1(test_status))
        f.write(html_source_table2())
         
        f.write(html_source_test_cases(test_cases))
        
        f.write(html_source_end_table())
        f.write(html_source_version_info())
        f.write(html_source_foot())


def save_current_report_to_repository():
    if General.QuickTest is True:
        return

    report_dir = os.path.join(General.Path.Result,
                              "%s__%s" % (datetime.strptime(General.Total.StartTime, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d_%H%M%S"),
                                         datetime.strptime(General.Total.EndTime, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d_%H%M%S")))
    library.delete_folder(report_dir)
    library.create_folder(report_dir)

    if os.path.exists(os.path.join(General.Path.Result, "testcase")):
        library.copy(os.path.join(General.Path.Result, "testcase"), os.path.join(report_dir, "testcase"))

    if os.path.exists(os.path.join(General.Path.Result, "screenshots")):
        library.copy(os.path.join(General.Path.Result, "screenshots"), os.path.join(report_dir, "screenshots"))

    if os.path.exists(os.path.join(General.Path.Result, "index.html")):
        library.copy(os.path.join(General.Path.Result, "index.html"), report_dir)
    
    with open(os.path.join(report_dir, "status.ini"), "w") as f:
        f.write("Duration=%s\n" % str(datetime.strptime(General.Total.EndTime, "%Y-%m-%d %H:%M:%S") -
                                      datetime.strptime(General.Total.StartTime, "%Y-%m-%d %H:%M:%S")))
        f.write("TotalCases=%s\n" % str(General.Total.NumberOfTestCasePass + General.Total.NumberOfTestCaseFail))
        f.write("PassedCases=%s\n" % str(General.Total.NumberOfTestCasePass))
        f.write("FailedCases=%s\n" % str(General.Total.NumberOfTestCaseFail))


def generate_report_history():
    if General.QuickTest is True:
        return

    folders = library.get_sub_folder_names(General.Path.Result)
    
    reports = []
    for folder in folders:
        if folder.startswith("testcase") or folder.startswith("screenshot"):
            continue
        reports.append(folder)

    with open(os.path.join(General.Path.Result, "history.html"), "w") as f:
        f.write(html_source_header(title="Web UI Automation Test History Reports"))
        f.write(html_source_body(title="Web UI Automation Test History Reports"))
        f.write(html_source_table_history_header())
        
        i = 0
        for report in sorted(reports, reverse=True):
            
            Duration = library.get_value_from_conf(os.path.join(General.Path.Result, report, "status.ini"), "Duration")
            TotalCases = library.get_value_from_conf(os.path.join(General.Path.Result, report, "status.ini"), "TotalCases")
            PassedCases = library.get_value_from_conf(os.path.join(General.Path.Result, report, "status.ini"), "PassedCases")
            FailedCases = library.get_value_from_conf(os.path.join(General.Path.Result, report, "status.ini"), "FailedCases")
            
            f.write(html_source_table_history(report, report, Duration, TotalCases, PassedCases, FailedCases))
            
            i = i + 1

        f.write(html_source_end_table())
        f.write(html_source_foot())


if __name__ == "__main__":
    General.Path.Result = "D:/"
    generate_report_history()







