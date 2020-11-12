from selenium import webdriver
from secrets import login, password
import datetime
from time import sleep


class WebDriver():
    def __init__(self):
        options = webdriver.chrome.options.Options()
        options.add_argument("--headless")
        self.driver = webdriver.chrome.webdriver.WebDriver(options=options)
        self.driver.get(
            "https://jsos.pwr.edu.pl/index.php/site/loginAsStudent")

    def __del__(self):
        self.driver.quit()

    def get_activities(self):
        driver = self.driver
        user_input = driver.find_element_by_xpath("//input[@id='username']")
        user_input.send_keys(login)
        user_password = driver.find_element_by_xpath("//input[@id='password']")
        user_password.send_keys(password)
        submit_btn = driver.find_element_by_xpath("//input[@value='Zaloguj']")
        submit_btn.click()
        driver.get("https://jsos.pwr.edu.pl/index.php/student/zajecia/tydzien")
        activities = driver.find_elements_by_xpath(
            "//div[contains(@class,'wyzwalacz')]/p")
        schedule = {}
        for i in range(0, len(activities), 3):
            if activities[i+1].text not in schedule:
                schedule[activities[i+1].text] = activities[i].text
            else:
                schedule[activities[i+1].text + " +"] = activities[i].text
        print(schedule)


driver = WebDriver()
driver.get_activities()
del driver
