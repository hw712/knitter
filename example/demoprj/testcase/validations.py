# -*- coding: utf-8 -*-

from knitter import datadriver, log
from demoprj.page import KnitterDemo



def TestCase001_NormalInputTest():
    #### Name ###
    KnitterDemo.Name.Title.Select("Mr.")
    KnitterDemo.Name.Name.Set("Henry.Wang")
    
    ### Gender ###
    KnitterDemo.Gender.Male.Click()
    
    ### Hobbies ###
    KnitterDemo.Hobby.Music.Click()
    KnitterDemo.Hobby.Travel.Click()
    
    ###### Result ######
    KnitterDemo.SubmitButton.Click()
    
    KnitterDemo.Result.VerifyInnerHTMLContains("Henry.Wang")
    KnitterDemo.Result.VerifyAttribute("innerHTML", "Music", method="contain")



def TestCase002_Data_In_Excel():
    xls = datadriver.ExcelSheet("TestData.xlsx", "TestCase002")
    
    for i in range(1, xls.nrows()):
        log.step_section("Execute Excel Date: Line [%s]" % i)
        
        title   = xls.cell(i, "Title")
        name    = xls.cell(i, "Name")
        gender  = xls.cell(i, "Gender")
        hobbies = xls.cell(i, "Hobbies")
        
        ### Clear Values of Last Cycle ###
        KnitterDemo.ResetButton.Click()
        
        #### Name ###
        KnitterDemo.Name.Title.Select(title)
        KnitterDemo.Name.Name.Set(name)
        
        ### Gender ###
        if gender == "Male":
            KnitterDemo.Gender.Male.Click()
        if gender == "Female":
            KnitterDemo.Gender.Female.Click()
        
        ### Hobbies ###
        if "Travel" in hobbies:
            KnitterDemo.Hobby.Travel.Click()
        if "Music" in hobbies:
            KnitterDemo.Hobby.Music.Click()
        if "Sport" in hobbies:
            KnitterDemo.Hobby.Sport.Click()
        
        ###### Result ######
        KnitterDemo.SubmitButton.Click()
        
        KnitterDemo.Result.VerifyInnerHTMLContains("%s%s" % (title, name))
        KnitterDemo.Result.VerifyInnerHTMLContains("Gender: %s" % gender.lower())
        
        if "Travel" in hobbies:
            KnitterDemo.Result.VerifyInnerHTMLContains("Travel")
        if "Music" in hobbies:
            KnitterDemo.Result.VerifyInnerHTMLContains("Music")
        if "Sport" in hobbies:
            KnitterDemo.Result.VerifyInnerHTMLContains("Sport")










