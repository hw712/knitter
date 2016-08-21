# -*- coding: utf-8 -*-

import datetime, sys, os

import xlwt

# from knitter import env
# from knitter import common
# from knitter import htmlreport
try:
    # Python 3
    from knitter import env
    from knitter import common
    from knitter import htmlreport
except ImportError:
    # Python 2
    import env
    import common
    import htmlreport

def generate_result_xls():
    wbk = xlwt.Workbook()
    
    style_red   = xlwt.easyxf('font: colour red,   bold False;')
    style_green = xlwt.easyxf('font: colour green, bold False;')
    style_bold  = xlwt.easyxf('font: colour black, bold True;')
    
    for m in env.EXCEL_REPORT_DATA:
        if m.has_key("Name"):
            sheet = wbk.add_sheet(m["Name"])
            
            sheet.write(0, 0, 'Test Case Name', style_bold)
            sheet.write(0, 1, 'IE', style_bold)
            sheet.write(0, 2, 'Firefox', style_bold)
            sheet.write(0, 3, 'Chrome', style_bold)
            
            sheet.col(0).width = 256 * 80
            sheet.col(1).width = 256 * 20
            sheet.col(2).width = 256 * 20
            sheet.col(3).width = 256 * 20
            
            
            i = 1
            for case in m["TestCases"]:
                sheet.write(i, 0, case["Name"])
                
                if case.has_key("IE"):
                    if case["IE"] == "Pass":
                        sheet.write(i, 1, case["IE"], style_green)
                    if case["IE"] == "Fail":
                        sheet.write(i, 1, case["IE"], style_red)
                
                if case.has_key("Firefox"):
                    if case["Firefox"] == "Pass":
                        sheet.write(i, 2, case["Firefox"], style_green)
                    if case["Firefox"] == "Fail":
                        sheet.write(i, 2, case["Firefox"], style_red)
                
                if case.has_key("Chrome"):
                    if case["Chrome"] == "Pass":
                        sheet.write(i, 3, case["Chrome"], style_green)
                    if case["Chrome"] == "Fail":
                        sheet.write(i, 3, case["Chrome"], style_red)
                
                i = i + 1
    
    wbk.save(common.force_delete_file(os.path.join(env.RESULT_PATH, "result", "result.xls")))



def add_excel_report_data(list_all=[], module_name="TestModule", case_name="TestCase", browser_type="IE", result="Pass"):
    for module in list_all:
        if module_name == module["Name"]:
            
            for case in module["TestCases"]:
                if case_name == case["Name"]:
                    case[browser_type] = result
                    return list_all
            
            module["TestCases"].append({"Name": case_name, browser_type: result})
            return list_all
    
    list_all.append({"Name": module_name, "TestCases": [{"Name": case_name, browser_type: result}]})
    return list_all


def start_test(case_name):
    env.threadlocal.CASE_NAME       = case_name
    env.threadlocal.CASE_START_TIME = datetime.datetime.now().replace(microsecond=0)
    env.threadlocal.CASE_PASS       = True
    env.threadlocal.CASE_WARNINGS   = 0
    
    write_log(os.path.join("testcase", "%s.log" % (case_name)), 
              "\n**************  Test Case [%s] [%s]  ***************\n" %(case_name, env.threadlocal.TESTING_BROWSER))
    
    

def start_total_test():
    env.threadlocal.CASE_START_TIME  = ""
    env.threadlocal.CASE_STOP_TIME   = ""
    env.threadlocal.CASE_NAME        = ""
    env.threadlocal.CASE_PASS        = True
    env.threadlocal.CASE_WARNINGS    = 0
    
    env.threadlocal.MODULE_NAME      = ""
    
    env.threadlocal.BROWSER          = None
    
    env.threadlocal.TESTING_BROWSER  = ""
    env.threadlocal.TESTING_BROWSERS = ""
    
    env.TOTAL_TESTCASE_PASS = 0
    env.TOTAL_TESTCASE_FAIL = 0
    env.HTMLREPORT_TESTCASES[:] = []
    
    common.delete_file_or_folder(os.path.join(env.RESULT_PATH, "result", "testcase"))
    common.delete_file_or_folder(os.path.join(env.RESULT_PATH, "result", "screenshots"))
    
    env.TOTAL_START_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print  (">>>>>>  [%s]  =>  start testing......       <<<<<<" %
              (
               env.TOTAL_START_TIME,
               )
           )
    
    htmlreport.generate_html_report([env.TOTAL_START_TIME, "N/A", "N/A", "N/A", "N/A", "N/A"], [])
    












def finish_total_test():
    env.TOTAL_STOP_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print (">>>>>>  [%s]  =>  [%s], duration [%s], case [%s], pass [%s], fail [%s]       <<<<<<" %
              (
               env.TOTAL_START_TIME,
               env.TOTAL_STOP_TIME,
               datetime.datetime.strptime(env.TOTAL_STOP_TIME, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(env.TOTAL_START_TIME, "%Y-%m-%d %H:%M:%S"),
               env.TOTAL_TESTCASE_PASS + env.TOTAL_TESTCASE_FAIL, 
               env.TOTAL_TESTCASE_PASS,
               env.TOTAL_TESTCASE_FAIL,
               )
            )
    
    print (
           ">>>>>>  [%s]  =>  [%s]" % (env.TOTAL_START_TIME, common.get_version_info())
           )
    
    htmlreport.generate_html_report([env.TOTAL_START_TIME, env.TOTAL_STOP_TIME, datetime.datetime.strptime(env.TOTAL_STOP_TIME, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(env.TOTAL_START_TIME, "%Y-%m-%d %H:%M:%S"), 
                                     env.TOTAL_TESTCASE_PASS+env.TOTAL_TESTCASE_FAIL, env.TOTAL_TESTCASE_PASS, env.TOTAL_TESTCASE_FAIL], 
                                    env.HTMLREPORT_TESTCASES,
                                    countdown=False)
    htmlreport.save_current_report_to_repository()
    htmlreport.generate_report_history()
    htmlreport.generate_html_report([env.TOTAL_START_TIME, env.TOTAL_STOP_TIME, datetime.datetime.strptime(env.TOTAL_STOP_TIME, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(env.TOTAL_START_TIME, "%Y-%m-%d %H:%M:%S"), 
                                     env.TOTAL_TESTCASE_PASS+env.TOTAL_TESTCASE_FAIL, env.TOTAL_TESTCASE_PASS, env.TOTAL_TESTCASE_FAIL], 
                                    env.HTMLREPORT_TESTCASES,
                                    countdown=True)
    
    env.TOTAL_TESTCASE_PASS = 0
    env.TOTAL_TESTCASE_FAIL = 0
    env.HTMLREPORT_TESTCASES[:] = []
    
    print ("\n")
    
        

def stop_test():
    
    try:
        env.THREAD_LOCK.acquire()
        
        env.threadlocal.CASE_STOP_TIME = datetime.datetime.now().replace(microsecond=0)
        env.TOTAL_STOP_TIME            = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if env.threadlocal.CASE_WARNINGS > 0:
            warning_message = ", has [%s] warning(s)!" % env.threadlocal.CASE_WARNINGS
        else:
            warning_message = ""
        
        if env.threadlocal.CASE_PASS == True:
            print (u"%s    [Pass]  =>  [%s] [%s] [%s] [%s]%s" %(common.stamp_datetime(), 
                                                        env.threadlocal.CASE_STOP_TIME - env.threadlocal.CASE_START_TIME, 
                                                        env.threadlocal.MODULE_NAME, 
                                                        env.threadlocal.CASE_NAME, 
                                                        env.threadlocal.TESTING_BROWSER,
                                                        warning_message
                                                        ))
            env.TOTAL_TESTCASE_PASS = env.TOTAL_TESTCASE_PASS + 1
            
            env.HTMLREPORT_TESTCASES.append(["%s =&gt; %s" % (env.threadlocal.CASE_START_TIME.strftime("%m-%d %H:%M:%S"), env.threadlocal.CASE_STOP_TIME.strftime("%m-%d %H:%M:%S")),
                                             '<a href="testcase/%s.log">[%s] - %s</a>' % (env.threadlocal.CASE_NAME, env.threadlocal.MODULE_NAME, env.threadlocal.CASE_NAME),
                                             env.threadlocal.CASE_STOP_TIME - env.threadlocal.CASE_START_TIME, 
                                             env.threadlocal.TESTING_BROWSER, 
                                             '<td>Pass</td>'
                                             ])
            
        else:
            print (u"%s    [Fail]  =>  [%s] [%s] [%s] [%s]%s  :( " %(common.stamp_datetime(), 
                                                                 env.threadlocal.CASE_STOP_TIME - env.threadlocal.CASE_START_TIME, 
                                                                 env.threadlocal.MODULE_NAME, 
                                                                 env.threadlocal.CASE_NAME, 
                                                                 env.threadlocal.TESTING_BROWSER,
                                                                 warning_message
                                                                 ))
            env.TOTAL_TESTCASE_FAIL = env.TOTAL_TESTCASE_FAIL + 1
            
            env.HTMLREPORT_TESTCASES.append(["%s =&gt; %s" % (env.threadlocal.CASE_START_TIME.strftime("%m-%d %H:%M:%S"),env.threadlocal.CASE_STOP_TIME.strftime("%m-%d %H:%M:%S")),
                                             '<a href="testcase/%s.log">[%s] - %s</a>' % (env.threadlocal.CASE_NAME, env.threadlocal.MODULE_NAME, env.threadlocal.CASE_NAME),
                                             env.threadlocal.CASE_STOP_TIME - env.threadlocal.CASE_START_TIME, 
                                             env.threadlocal.TESTING_BROWSER, 
                                             '<td class="tfail"><a href="screenshots/%s">Fail</a></td>' % env.HTMLREPORT_SCREENSHOT_NAME
                                             ])
        
        htmlreport.generate_html_report([env.TOTAL_START_TIME, env.TOTAL_STOP_TIME, datetime.datetime.strptime(env.TOTAL_STOP_TIME, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(env.TOTAL_START_TIME, "%Y-%m-%d %H:%M:%S"), 
                                         env.TOTAL_TESTCASE_PASS+env.TOTAL_TESTCASE_FAIL, env.TOTAL_TESTCASE_PASS, env.TOTAL_TESTCASE_FAIL], 
                                        env.HTMLREPORT_TESTCASES)
        
        env.threadlocal.CASE_PASS     = True
        env.threadlocal.CASE_WARNINGS = 0
    finally:
        env.THREAD_LOCK.release()




def step_section(message):
    write_log(os.path.join("testcase", "%s.log" % (env.threadlocal.CASE_NAME)), 
              "\n%s    Section: %s\n" %(common.stamp_datetime(), message))


def step_normal(message):
    write_log(os.path.join("testcase", "%s.log" % (env.threadlocal.CASE_NAME)), 
              "%s    Step: %s\n" %(common.stamp_datetime(), message))


def step_pass(message):
    write_log(os.path.join("testcase", "%s.log" % (env.threadlocal.CASE_NAME)), 
              "%s    Pass: %s\n" %(common.stamp_datetime(), message))


def step_fail(message):
    
    screenshot_name = "Fail__%s__%s__%s.png" % (common.stamp_datetime_coherent(), env.threadlocal.CASE_NAME, env.threadlocal.TESTING_BROWSER)
    
    write_log(os.path.join("testcase", "%s.log" % (env.threadlocal.CASE_NAME)),  
              "------------ Fail [%s] -------------------\n"%common.stamp_datetime())
    
    write_log(os.path.join("testcase", "%s.log" % (env.threadlocal.CASE_NAME)), 
              "%s    Fail: %s, Check ScreenShot [%s]\n" %(common.stamp_datetime(), message, screenshot_name))
    
    write_log(os.path.join("testcase", "%s.log" % (env.threadlocal.CASE_NAME)), 
              "------------ Fail [%s] --------------------------------------------\n"%common.stamp_datetime())
    
    try:
        save_screen_shot(screenshot_name)
    except:
        step_normal(str(sys.exc_info()))
    
    env.HTMLREPORT_SCREENSHOT_NAME = screenshot_name
    env.threadlocal.CASE_PASS = False
    env.EXIT_STATUS = -1
    
    raise AssertionError(message)


def step_warning(message):
    screenshot_name = "Warning__%s__%s__%s.png" % (common.stamp_datetime_coherent(), env.threadlocal.CASE_NAME, env.threadlocal.TESTING_BROWSER)
    
    write_log(os.path.join("testcase", "%s.log" % (env.threadlocal.CASE_NAME)), 
              "------------ Warning [%s] -------------------\n"%common.stamp_datetime())
    
    write_log(os.path.join("testcase", "%s.log" % (env.threadlocal.CASE_NAME)), 
              "%s    Warning: %s, Check ScreenShot [%s]\n" %(common.stamp_datetime(), message, screenshot_name))
    
    write_log(os.path.join("testcase", "%s.log" % (env.threadlocal.CASE_NAME)), 
              "------------ Warning [%s] --------------------------------------------\n"%common.stamp_datetime())
    
    try:
        save_screen_shot(screenshot_name)
    except:
        step_normal(str(sys.exc_info()))
    
    env.threadlocal.CASE_WARNINGS = env.threadlocal.CASE_WARNINGS + 1




def write_log(relative_path, log_message):
    log_path = os.path.join(env.RESULT_PATH, "result", relative_path)
    common.mkdirs(os.path.dirname(log_path))
    
    with open(log_path, 'a') as f:
        f.write(log_message)


def save_screen_shot(image_name):
    image_path = os.path.join(env.RESULT_PATH, "result", "screenshots")
    common.mkdirs(image_path)
    
    env.threadlocal.BROWSER.save_screenshot(os.path.join(image_path, image_name))
    




def handle_error():
    if env.threadlocal.CASE_PASS == False:
        return
    
    
    if sys.exc_info()[0] != None:
        step_normal(common.exception_error())
        
        screenshot_name = "Fail__%s__%s__%s.png" % (common.stamp_datetime_coherent(), env.threadlocal.CASE_NAME, env.threadlocal.TESTING_BROWSER)
        
        try:
            save_screen_shot(screenshot_name)
        except:
            step_warning(str(sys.exc_info()))
        
        step_normal("Current step screen short [%s]" % (screenshot_name))
        
        env.HTMLREPORT_SCREENSHOT_NAME = screenshot_name
        
        env.threadlocal.CASE_PASS = False
        env.EXIT_STATUS = -1
    













