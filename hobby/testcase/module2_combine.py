from hobby.page import Hobby
from knitter import logger
from knitter import datadriver


def TestCase01_AllCombinations():
    sheet = datadriver.ExcelSheet("hobby/data/TestData.xlsx", "Combinations")

    for i in range(1, sheet.nrows()):
        logger.step_section("Execute Excel Data of Line [" + str(i) + "]")
        title = sheet.cell_by_colname(i, "Title")
        name = sheet.cell_by_colname(i, "Name")
        gender = sheet.cell_by_colname(i, "Gender")
        hobbies = sheet.cell_by_colname(i, "Hobbies")

        Hobby.ResetButton.Click()

        Hobby.User.Title.Select(title)
        Hobby.User.Name.Set(name)

        if gender == "Male":
            Hobby.Gender.Male.Click()
        if gender == "Female":
            Hobby.Gender.Female.Click()

        if "Travel" in hobbies:
            Hobby.Hobby.Travel.Click()
        if "Music" in hobbies:
            Hobby.Hobby.Music.Click()
        if "Sport" in hobbies:
            Hobby.Hobby.Sport.Click()

        Hobby.SubmitButton.Click()
        Hobby.Result.VerifyAttribute("innerHTML", gender, "contain")
        Hobby.Result.VerifyAttribute("innerHTML", title + " " + name, "contain")
