from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
url = "https://rdeapps.stanford.edu/dininghallmenu/"
driver.get(url)

def selector(element_id, option_value):
    dropdown = wait.until(EC.presence_of_element_located((By.ID, element_id)))
    for option in dropdown.find_elements(By.TAG_NAME, "option"):
        # find the matching name in dropdown 
        if option.get_attribute("value") == option_value:
            option.click()
            # staleness anticipated for last dropdown (meal)
            if element_id == "MainContent_lstMealType":
                wait.until(EC.staleness_of(dropdown))  
            break


hall_dropdown = driver.find_element(By.ID, "MainContent_lstLocations")
# list names of halls
halls = [h.get_attribute("value") for h in hall_dropdown.find_elements(By.TAG_NAME, "option") if h.get_attribute("value") != '']
for hall in halls:
    print(hall)
    selector("MainContent_lstLocations", hall)

    day_dropdown = driver.find_element(By.ID, "MainContent_lstDay")
    # list names of days
    days = [d.get_attribute("value") for d in day_dropdown.find_elements(By.TAG_NAME, "option") if d.get_attribute("value") != '']
    for day in days:
        print(day)
        selector("MainContent_lstDay", day)

        meal_dropdown = driver.find_element(By.ID, "MainContent_lstMealType")
        # list names of meals
        meals = [m.get_attribute("value") for m in meal_dropdown.find_elements(By.TAG_NAME, "option") if m.get_attribute("value") != '']
        for meal in meals:
            print(meal)
            selector("MainContent_lstMealType", meal)

            # collect food
            food = driver.find_elements(By.CSS_SELECTOR, "div[class^='clsMenuItem']")
            if food:
                print([f.text for f in food])

driver.quit()
