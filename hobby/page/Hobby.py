from knitter.webelement import WebElement
from selenium.webdriver.common.by import By


class User:
    class Title(WebElement):
        (by, value) = (By.ID, 'title')

    class Name(WebElement):
        (by, value) = (By.ID, 'name')


class Gender:
    class Male(WebElement):
        (by, value) = (By.ID, 'male')

    class Female(WebElement):
        (by, value) = (By.ID, 'female')


class Hobby:
    class Music(WebElement):
        (by, value) = (By.ID, 'music')

    class Sport(WebElement):
        (by, value) = (By.ID, 'sport')

    class Travel(WebElement):
        (by, value) = (By.ID, 'travel')


class SubmitButton(WebElement):
    (by, value) = (By.XPATH, '//button[@onclick="do_submit();"]')


class ResetButton(WebElement):
    (by, value) = (By.XPATH, '//button[@onclick="do_reset();"]')


class Result(WebElement):
    (by, value) = (By.ID, 'result')

