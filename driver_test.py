# Test to see if webdriver is working (should show youtube in chrome)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()
driver.get("https://www.google.com/travel/flights")
#elem = driver.find_element(By.NAME, "q")
#elem = driver.find_element(By.XPATH("//input[@placeholder='Where to?']"))
elem = driver.find_element(By.XPATH,"//input[@placeholder='Where to?']")

elem.clear()
elem.send_keys("Seattle")
elem.send_keys(Keys.TAB)
elem.send_keys(Keys.RETURN)
#elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
time.sleep(30)
#driver.close()


# Test to see if webdriver is working (should show )
# import time
# from selenium import webdriver

# driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
# driver.get('http://www.youtube.com/');
# time.sleep(5) # Let the user actually see something!
# search_box = driver.find_element_by_name('q')
# search_box.send_keys('ChromeDriver')
# search_box.submit()
# time.sleep(5) # Let the user actually see something!
# driver.quit()