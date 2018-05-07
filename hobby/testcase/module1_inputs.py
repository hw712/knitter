from hobby.page import Hobby

def TestCase01_BasicVerify():
    Hobby.User.Title.SelectByOrder(1)
    Hobby.User.Name.Set("Henry Wang")

