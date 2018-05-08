from hobby.page import Hobby


def TestCase01_UserInformation():
    Hobby.User.Title.WaitForAppearing()

    Hobby.User.Title.VerifyEnabled(True)
    Hobby.User.Title.VerifyVisible(True)

    Hobby.User.Title.Select("Mrs.")
    Hobby.User.Title.VerifyAttribute("value", "Mrs.")

    Hobby.User.Title.SelectByOrder(3)
    Hobby.User.Title.VerifyAttribute("value", "Ms.")
    Hobby.User.Title.VerifyAttribute("value", "Dr.", action="not equal")

    Hobby.User.Name.Set("Super Man")
    Hobby.User.Name.VerifyAttribute("value", "Super", action="contain")
    Hobby.User.Name.VerifyAttribute("value", "More", action="not contain")
    Hobby.User.Name.VerifyAttribute("value", "Here Comes Super Man!!", action="in")


def TestCase02_Gender():
    Hobby.Gender.Male.VerifyAttribute("checked", None)
    Hobby.Gender.Female.VerifyAttribute("checked", None)

    Hobby.Gender.Male.Click()
    Hobby.Gender.Male.VerifyAttribute("checked", "true")
    Hobby.Gender.Female.VerifyAttribute("checked", None)

    Hobby.Gender.Female.Click()
    Hobby.Gender.Male.VerifyAttribute("checked", None)
    Hobby.Gender.Female.VerifyAttribute("checked", "true")


def TestCase03_Hobbies():
    Hobby.Hobby.Music.VerifyAttribute("checked", None)
    Hobby.Hobby.Sport.VerifyAttribute("checked", None)
    Hobby.Hobby.Travel.VerifyAttribute("checked", None)

    Hobby.Hobby.Music.Click()
    Hobby.Hobby.Travel.Click()

    Hobby.Hobby.Music.VerifyAttribute("checked", "true")
    Hobby.Hobby.Sport.VerifyAttribute("checked", None)
    Hobby.Hobby.Travel.VerifyAttribute("checked", "true")

    Hobby.Hobby.Travel.Click()
    Hobby.Hobby.Travel.VerifyAttribute("checked", None)


def TestCase04_SelectionResult():
    Hobby.Result.VerifyAttribute("innerHTML", "")

    Hobby.User.Title.SelectByOrder(1)
    Hobby.User.Name.Set("Super Man")

    Hobby.Gender.Male.Click()

    Hobby.Hobby.Music.Click()
    Hobby.Hobby.Sport.Click()

    Hobby.SubmitButton.Click()

    Hobby.Result.VerifyAttribute("innerHTML", "Sport", action="contain")
    Hobby.Result.VerifyAttribute("innerHTML", "Male", action="contain")
    Hobby.Result.VerifyAttribute("innerHTML", "Female", action="not contain")
    Hobby.Result.VerifyAttribute("innerHTML", "Travel", action="not contain")


def TestCase05_ThisOneShouldFail():
    Hobby.Result.VerifyAttribute("innerHTML", "")

    Hobby.User.Title.SelectByOrder(1)
    Hobby.User.Name.Set("Super Man")

    Hobby.Gender.Male.Click()

    Hobby.Hobby.Music.Click()
    Hobby.Hobby.Sport.Click()

    Hobby.SubmitButton.Click()

    Hobby.Result.VerifyAttribute("innerHTML", "Sport", action="not contain")
    Hobby.Result.VerifyAttribute("innerHTML", "Male", action="not contain")
    Hobby.Result.VerifyAttribute("innerHTML", "Travel", action="not contain")
