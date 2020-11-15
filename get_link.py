from selenium import webdriver
from secrets import login, password
import datetime


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


    def get_activities_with_days(self):
        driver = self.driver
        user_input = driver.find_element_by_xpath("//input[@id='username']")
        user_input.send_keys(login)
        user_password = driver.find_element_by_xpath("//input[@id='password']")
        user_password.send_keys(password)
        submit_btn = driver.find_element_by_xpath("//input[@value='Zaloguj']")
        submit_btn.click()
        driver.get("https://jsos.pwr.edu.pl/index.php/student/zajecia/tydzien")
        activities_data = driver.find_elements_by_xpath(
            "//div[contains(@class,'wyzwalany')]")
        # schedule = {}
        for activity in activities_data:
            text = activity.get_attribute('textContent')
            name_of_activity, time_list = clean_up_list(text.split(' '))
            print(name_of_activity, time_list)

def clean_up_list(splitted_text):
    content = []
    for item in splitted_text:
        item = item.strip()
        if item != '' and item != '-':
            content.append(item)
    print(content)
    day_of_the_week = content[0]
    starting_time = content[1]
    starting_time = str(starting_time)
    if len(starting_time) == 3:
        start_hour = starting_time[0]
        start_minutes = starting_time[1:]
    elif len(starting_time) == 4:
        start_hour = starting_time[0:2]
        start_minutes = starting_time[2:]
    end_hour = content[2]
    end_minutes = content[3]
    name = ''
    for c in content[4:]:
        if c == 's.':
            break
        else:
            name += c.replace(',','')
            name += ' '
    name = name[:len(name)-1]
    day_of_the_week = day_of_week_to_number(day_of_the_week.\
        replace(',',''))
    time_list = [day_of_the_week, start_hour, start_minutes, end_hour, end_minutes]
    return name, time_list

def day_of_week_to_number(day):
    if day == 'Poniedziałek': return 0
    if day == 'Wtorek': return 1
    if day == 'Środa': return 2
    if day == 'Czwartek': return 3
    if day == 'Piątek': return 4
    if day == 'Sobota': return 5
    if day == 'Niedziela': return 6
    

if __name__ == "__main__":
    driver = WebDriver()
    driver.get_activities_with_days()
    del driver