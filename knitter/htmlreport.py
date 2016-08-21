# -*- coding: utf-8 -*-

import os, shutil, datetime
# from knitter import env, common
try:
    # Python 3
    from knitter import env
    from knitter import common
except ImportError:
    # Python 2
    import env
    import common

def html_source_header(title="Knitter Web Automation Test Result"):
    return """<!DOCTYPE HTML>
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
            color: #000000;
        }
        button {
            width: 120px;
        }
        body {
            width: 100%%;
            color: #000000;
            font-size: 13px;
            font-family: verdana, Courier New;
            text-align: center;
        }
        table, td, th {
            border: 1px solid black;
            border-collapse: collapse;
            width: 1260px;
            text-align: center;
        }
        .tcaption {
            background-color: #65ACCA;
        }
        .theader {
            background-color: #D7EAF2;
        }
        .tfail{
            background-color: #FF6F6F;
        }
        h1{
            text-align: center;
        }
            
    </style>
</head>
""" % title


def html_source_body(title="Knitter Web Automation Test Result", countdown=True):
    if countdown == False:
        return """<body> <h1>%s</h1> <p>[<a href="..\index.html">Last Test</a>]&nbsp;[<a href="..\history.html">History Tests</a>]""" % title
    
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
    [<a href="index.html">Last Test</a>]&nbsp;[<a href="history.html">History Tests</a>]
    </p>
    <p style="text-align: center">
    Pending to do auto-refresh in [<span id='timer'>9</span>] seconds. &nbsp;&nbsp;&nbsp;&nbsp;<button onclick="window.location.reload();">Refresh Now</button></p>
    
""" % title


def html_source_table1(args):
    return """
    <table>
        <tr class="tcaption"><th colspan="5">Test Status</th></tr>
        
        <tr class="theader">
            <th>Time</th>
            <th>Duration</th>
            <th>Total Cases</th>
            <th>Passed Cases</th>
            <th>Failed Cases</th>
        </tr>
        <tr>
            <td style='width: 35%%'>%s =&gt; %s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
        </tr>
    </table>
""" % tuple(args)


def html_source_table_history_header():
    return """
    <table>
        <tr class="tcaption"><th colspan="5">History Results (Latest 100 Results)</th></tr>
        
        <tr class="theader">
            <th>Result Folder</th>
            <th>Duration</th>
            <th>Total Cases</th>
            <th>Passed Cases</th>
            <th>Failed Cases</th>
        </tr>
""" 

def html_source_table_history(*args):
    return """
        <tr>
            <td style='width: 36%%'><a href="%s/index.html">%s</a></td>
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
    <table>
        <tr class="tcaption"><th colspan="5">Test Cases</th></tr>
        <tr class="theader">
            <th>Time</th>
            <th>Case</th>
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
""" % common.get_version_info()

def html_source_foot():
    return u"""
<hr />
<p style="text-align: center">2016 Powered by Knitter</p>
<br />
<body>
</html>
"""

def generate_html_report(test_status, test_cases=[], countdown=True):
    
    common.mkdirs(os.path.join(env.RESULT_PATH, "result"))
    
    with open(os.path.join(env.RESULT_PATH, "result", "index.html"), "w") as f:
        f.write(html_source_header())
        f.write(html_source_body(countdown=countdown))
        
        f.write(html_source_table1(test_status))
        f.write(html_source_table2())
         
        f.write(html_source_test_cases(test_cases))
        
        f.write(html_source_end_table())
        f.write(html_source_version_info())
        f.write(html_source_foot())
    


def save_current_report_to_repository():
    report_dir = os.path.join(env.RESULT_PATH, 
                              "result", 
                              "%s__%s" % (datetime.datetime.strptime(env.TOTAL_START_TIME, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d_%H%M%S"),
                                         datetime.datetime.strptime(env.TOTAL_STOP_TIME, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d_%H%M%S")))
    common.delete_then_mkdir(report_dir)
    
    common.copy(os.path.join(env.RESULT_PATH, "result", "testcase"), os.path.join(report_dir, "testcase"))
    common.copy(os.path.join(env.RESULT_PATH, "result", "screenshots"), os.path.join(report_dir, "screenshots"))
    common.copy(os.path.join(env.RESULT_PATH, "result", "index.html"), report_dir)
    
    with open(os.path.join(report_dir, "status.ini"), "w") as f:
        f.write("Duration=%s\n" % str(datetime.datetime.strptime(env.TOTAL_STOP_TIME, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(env.TOTAL_START_TIME, "%Y-%m-%d %H:%M:%S")))
        f.write("TotalCases=%s\n" % str(env.TOTAL_TESTCASE_PASS+env.TOTAL_TESTCASE_FAIL))
        f.write("PassedCases=%s\n" % str(env.TOTAL_TESTCASE_PASS))
        f.write("FailedCases=%s\n" % str(env.TOTAL_TESTCASE_FAIL))
    


def generate_report_history():
    folders = common.get_sub_folder_names(os.path.join(env.RESULT_PATH, "result"))
    
    reports = []
    for folder in folders:
        if len(folder) == 36:
            reports.append(folder)
    
    
    with open(os.path.join(env.RESULT_PATH, "result", "history.html"), "w") as f:
        f.write(html_source_header(title="Knitter Web Automation Test History"))
        f.write(html_source_body(title="Knitter Web Automation Test History"))
        f.write(html_source_table_history_header())
        
        i = 0
        for report in sorted(reports, reverse=True):
            
            Duration     = common.get_value_from_conf(os.path.join(env.RESULT_PATH, "result", report, "status.ini"), "Duration")
            TotalCases   = common.get_value_from_conf(os.path.join(env.RESULT_PATH, "result", report, "status.ini"), "TotalCases")
            PassedCases  = common.get_value_from_conf(os.path.join(env.RESULT_PATH, "result", report, "status.ini"), "PassedCases")
            FailedCases  = common.get_value_from_conf(os.path.join(env.RESULT_PATH, "result", report, "status.ini"), "FailedCases")
            
            f.write(html_source_table_history(report, report, Duration, TotalCases, PassedCases, FailedCases))
            
            i = i + 1
            if i > 100: break
         
        
        f.write(html_source_end_table())
        f.write(html_source_foot())
    



if __name__ == "__main__":
    pass
    env.RESULT_PATH = r"E:\EclipseWorkspace\claims-qa-test"
    generate_report_history()

#===============================================================================
#     generate_html_report(["2015-03-05 09:54:06", "2015-03-05 09:59:17", "11:05:12", "1", "1", "0"],
#                          [
#                            ["2015-03-03 17:28:23", "claims", "WC2TC0047_CreateNewPreliminaryWithMandatoryFieldsSuccessfullyMandatoryFieldsSuccessfully", 
#         "0:07:05", "Firefox", '<td class="tfail"><a href="#">Fail</a></td>', '<a href="#">Check Image</a>'],
#                            ["2015-03-03 17:28:23", "claims", "WC2TC0047_CreateNewPreliminaryWithMandatoryFieldsSuccessfully", 
#         "0:07:05", "Firefox", '<td class="tfail"><a href="#">Fail</a></td>', '<a href="#">Check Image</a>'],
#                          ]
# 
#                          
#                          )
#===============================================================================

















