# -*- coding: utf-8 -*-

import datetime, sys

import xlwt

import environment
import common


def generate_result_xls():
    wbk = xlwt.Workbook()
    
    style_red   = xlwt.easyxf('font: colour red,   bold False;')
    style_green = xlwt.easyxf('font: colour green, bold False;')
    style_bold  = xlwt.easyxf('font: colour black, bold True;')
    
    for m in environment.EXCEL_REPORT_DATA:
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
    
    wbk.save(common.force_delete_file(u"%s\\result\\Result.xls" % environment.PROJECT_PATH))



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
    environment.CASE_NAME       = case_name
    environment.CASE_START_TIME = datetime.datetime.now().replace(microsecond=0)
    environment.CASE_PASS       = True
    
    common.mkdirs("%s\\result\\screenshots\\" % environment.PROJECT_PATH)
    common.mkdirs("%s\\result\\testcase\\" % environment.PROJECT_PATH)
    
    with open(u"%s\\result\\testcase\\%s_%s.TXT" % (environment.PROJECT_PATH, environment.CASE_NAME, common.stamp_date()), "a") as f:
        f.write(u"\n**************  Test Case [%s] [%s]  ***************\n" %(environment.CASE_NAME, environment.RUNNING_BROWSER))


def stop_test():
    environment.CASE_STOP_TIME = datetime.datetime.now().replace(microsecond=0)
    
    with open(u"%s\\result\\summary.txt" % environment.PROJECT_PATH, "a") as f:
        if environment.CASE_PASS == True:
            add_excel_report_data(environment.EXCEL_REPORT_DATA, environment.MODULE_NAME, environment.CASE_NAME, environment.RUNNING_BROWSER, "Pass")
            f.write(u"%s    [%s]  =>  [Pass] [%s] [%s]\n" %(common.stamp_datetime(), environment.CASE_NAME, environment.CASE_STOP_TIME - environment.CASE_START_TIME, environment.RUNNING_BROWSER))
        else:
            add_excel_report_data(environment.EXCEL_REPORT_DATA, environment.MODULE_NAME, environment.CASE_NAME, environment.RUNNING_BROWSER, "Fail")
            f.write(u"%s    [%s]  =>  [Fail] [%s] [%s] :( \n" %(common.stamp_datetime(), environment.CASE_NAME, environment.CASE_STOP_TIME - environment.CASE_START_TIME, environment.RUNNING_BROWSER))
    
    generate_result_xls()
    environment.CASE_PASS = True



def step_section(message):
    with open(u"%s\\result\\testcase\%s_%s.TXT" % (environment.PROJECT_PATH, environment.CASE_NAME, common.stamp_date()), "a") as f:
        f.write(u"\n%s    Section: %s\n" %(common.stamp_datetime(), message))


def step_normal(message):
    with open(u"%s\\result\\testcase\\%s_%s.TXT" % (environment.PROJECT_PATH, environment.CASE_NAME, common.stamp_date()), "a") as f:
        f.write(u"%s    Step: %s\n" %(common.stamp_datetime(), message))


def step_pass(message):
    with open(u"%s\\result\\testcase\\%s_%s.TXT" % (environment.PROJECT_PATH, environment.CASE_NAME, common.stamp_date()), "a") as f:
        f.write(u"%s    Pass: %s\n" %(common.stamp_datetime(), message))


def step_fail(message):
    screenshot_name = "%s_fail_%s.png" % (environment.RUNNING_BROWSER, common.stamp_datetime_coherent())
    
    with open(u"%s\\result\\testcase\\%s_%s.TXT" % (environment.PROJECT_PATH, environment.CASE_NAME, common.stamp_date()), "a") as f:
        f.write(u"------------ Fail [%s] -------------------\n"%common.stamp_datetime())
        f.write(u"%s    Fail: %s, Check ScreenShot [%s]\n" %(common.stamp_datetime(), message, screenshot_name))
        f.write(u"------------ Fail [%s] --------------------------------------------\n"%common.stamp_datetime())
    
    common.mkdirs("%s\\result\\screenshots\\" % environment.PROJECT_PATH)
    environment.BROWSER.save_screenshot(u"%s\\result\\screenshots\\%s" % (environment.PROJECT_PATH, screenshot_name))
    
    environment.CASE_PASS = False
    
    raise AssertionError(message)



def handle_error():
    if environment.CASE_PASS == False:
        return
    
    
    if sys.exc_info()[0] != None:
        step_normal(common.exception_error())
        
        screenshot_name = "%s_error_%s.png" % (environment.RUNNING_BROWSER, common.stamp_datetime_coherent())
        
        common.mkdirs("%s\\result\\screenshots\\" % environment.PROJECT_PATH)
        environment.BROWSER.save_screenshot(u"%s\\result\\screenshots\\%s" % (environment.PROJECT_PATH, screenshot_name))
        
        step_normal("Please check screen short [%s]" % (screenshot_name))
        
        
        environment.CASE_PASS = False












