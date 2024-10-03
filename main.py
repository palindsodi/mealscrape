from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from datetime import datetime, timedelta

print("||||||||||||| STANFORDHUNGRY |||||||||||||")

# hall filtering
HALLS = ["Arrillaga", "Branner", "EVGR", "FlorenceMoore", "GerhardCasper", "Lakeside", "Ricker", "Stern", "Wilbur"]

target_hall = ""
hall_chosen = False
while hall_chosen == False:
    target_hall = input("\nSelect hall(s):\n(0) Arrillaga\n(1) Branner\n(2) EVGR\n(3) FloMo\n(4) Casper\n(5) Lakeside\n(6) Ricker\n(7) Stern\n(8) Wilbur\nExample input: 70\n\t-> Stern, Arrillaga\nPress ENTER to skip\n")
    hall_chosen = True
    for i in target_hall:
        if i not in ["0","1","2","3","4","5","6","7","8"]:
            print("Invalid input ...")
            hall_chosen = False
halls_search = []
for i in target_hall:
    halls_search.append(HALLS[int(i)])
if len(target_hall) == 0: target_hall = HALLS

# day filtering
DAYS = []

current_time = datetime.now()
for i in range(7): 
    DAYS.append(current_time.strftime('%-m/%-d/%Y'))
    current_time += timedelta(days=1)

datestring = "\nSelect date(s):\n"
for i in range(0,6):
    datestring += "("+str(i)+") "+ DAYS[i] + "\n"

target_day = ""
day_chosen = False
while day_chosen == False:
    target_day = input(datestring + "Press ENTER to skip\n")
    day_chosen = True
    for i in target_day:
        if i not in ["0","1","2","3","4","5","6"]:
            print("Invalid input ...")
            day_chosen = False
days_search = []
for i in target_day:
    days_search.append(DAYS[int(i)])
if len(target_day) == 0: target_day = DAYS

# meal filtering
MEALS = ["Breakfast", "Lunch", "Dinner", "Brunch"]

target_meal = ""
meal_chosen = False
while meal_chosen == False:
    target_meal = input("\nSelect meal(s):\n(0) Breakfast\n(1) Lunch\n(2) Dinner\n(3) Brunch\nExample input: 12\n\t-> Lunch, Dinner\nPress ENTER to skip\n")
    meal_chosen = True
    for i in target_meal:
        if i not in ["0","1","2","3"]:
            print("Invalid input ...")
            meal_chosen = False
meals_search = []
for i in target_meal:
    meals_search.append(MEALS[int(i)])
if len(target_meal) == 0: target_meal = MEALS

# speed choice
drowsy = -1
while drowsy not in [0,1,2]:
    try:
        drowsy = int(input("\nSelect speed:\n(0) Normal\n(1) Fast\n(2) Faster (beware IP bans)\n"))
        if drowsy not in [0,1,2]:
            print("Invalid input ...")
    except:
        print("Invalid input ...")

# prepare driver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
url = "https://rdeapps.stanford.edu/dininghallmenu/"
driver.get(url)

# for repeat dropdown operations 
def selector(element_id, option_value):
    # according to speed choice 
    if drowsy == 0: time.sleep(random.randint(100,200)*0.01+1)
    if drowsy == 1: time.sleep(random.randint(100,200)*0.0015+0.5)
    dropdown = wait.until(EC.presence_of_element_located((By.ID, element_id)))
    for option in dropdown.find_elements(By.TAG_NAME, "option"):
        # find the matching name in dropdown 
        if option.get_attribute("value") == option_value:
            option.click()
            # if staleness anticipated for last dropdown (meal)
            # if element_id == "MainContent_lstMealType":
                # wait.until(EC.staleness_of(dropdown))  
            break


hall_dropdown = driver.find_element(By.ID, "MainContent_lstLocations")
# list names of halls
halls = [h.get_attribute("value") for h in hall_dropdown.find_elements(By.TAG_NAME, "option") if h.get_attribute("value") in halls_search]
for hall in halls:
    print("|||||||| DINING HALL: " + hall + " ||||||||")
    selector("MainContent_lstLocations", hall)

    day_dropdown = driver.find_element(By.ID, "MainContent_lstDay")
    # list names of days
    days = [d.get_attribute("value") for d in day_dropdown.find_elements(By.TAG_NAME, "option") if d.get_attribute("value") in days_search]
    for day in days:
        print("\t• " + day)
        selector("MainContent_lstDay", day)

        meal_dropdown = driver.find_element(By.ID, "MainContent_lstMealType")
        # list names of meals
        meals = [m.get_attribute("value") for m in meal_dropdown.find_elements(By.TAG_NAME, "option") if m.get_attribute("value") in meals_search]
        for meal in meals:
            print("\t\t------- " + ''.join(meal).upper() + " -------")
            selector("MainContent_lstMealType", meal)

            # collect food
            foods = driver.find_elements(By.CSS_SELECTOR, "div[class^='clsMenuItem']")
            if foods:
                for food in foods: 
                    food_text = food.text.replace("\n", "\n\t\t\t")
                    print('\t\t\t• ' + ''.join(food_text) + '\n')
                    # grab linked image information to determine food qualifications
                    for category in food.find_elements(By.TAG_NAME, "img"):
                        image_string = category.get_attribute("src")
                        if "png" in image_string:
                            if "H" in image_string: print("\t\t\tHALAL\n")
                            if "K" in image_string: print("\t\t\tKOSHER\n")
                            if "GF" in image_string: print("\t\t\tGLUTEN FREE\n")
                            if "VGN" in image_string: print("\t\t\tVEGAN\n")
                            elif "V" in image_string: print("\t\t\tVEGETARIAN\n")
print("||||||||||||| RETRIEVAL FINISHED! |||||||||||||")
driver.quit()
