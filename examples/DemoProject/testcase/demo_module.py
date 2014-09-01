# -*- coding: utf-8 -*-

from knitter import datadriver, log

from page import DemoPage



def TestCase001_Normal_Input_Test():
    
    #### Name ###
    DemoPage.Name.Title.Select("Mr.")
    DemoPage.Name.Name.Set("Henry.Wang")
    
    ### Gender ###
    DemoPage.Gender.Male.Click()
    
    ### Hobbies ###
    DemoPage.Hobby.Music.Click()
    DemoPage.Hobby.Travel.Click()
    
    ###### Result ######
    DemoPage.SubmitButton.Click()
    
    DemoPage.Result.VerifyInnerHTMLContains("Henry.Wang")
    DemoPage.Result.VerifyInnerHTMLContains("Gender: male")
    DemoPage.Result.VerifyInnerHTMLContains("Hobbies: Music Travel")



def TestCase002_Data_In_Excel():
    xls = datadriver.ExcelSheet("TestData.xlsx", "TestCase002")
    
    for i in range(1, xls.nrows()):
        log.step_section("Execute Excel Date: Line [%s]" % i)
        
        title   = xls.cell(i, "Title")
        name    = xls.cell(i, "Name")
        gender  = xls.cell(i, "Gender")
        hobbies = xls.cell(i, "Hobbies")
        
        ### Clear Values of Last Cycle ###
        DemoPage.ResetButton.Click()
        
        #### Name ###
        DemoPage.Name.Title.Select(title)
        DemoPage.Name.Name.Set(name)
        
        ### Gender ###
        if gender == "Male":
            DemoPage.Gender.Male.Click()
        if gender == "Female":
            DemoPage.Gender.Female.Click()
        
        ### Hobbies ###
        if "Travel" in hobbies:
            DemoPage.Hobby.Travel.Click()
        if "Music" in hobbies:
            DemoPage.Hobby.Music.Click()
        if "Sport" in hobbies:
            DemoPage.Hobby.Sport.Click()
        
        ###### Result ######
        DemoPage.SubmitButton.Click()
        
        DemoPage.Result.VerifyInnerHTMLContains("%s%s" % (title, name))
        DemoPage.Result.VerifyInnerHTMLContains("Gender: %s" % gender.lower())
        
        if "Travel" in hobbies:
            DemoPage.Result.VerifyInnerHTMLContains("Travel")
        if "Music" in hobbies:
            DemoPage.Result.VerifyInnerHTMLContains("Music")
        if "Sport" in hobbies:
            DemoPage.Result.VerifyInnerHTMLContains("Sport")
        
        
        
        









def before_launch_browser():
    pass

def before_each_testcase():
    pass

def after_each_testcase():
    pass


