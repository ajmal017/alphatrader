from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import time
import threading
import schedule

def start_rdp_purge():
	opts = FirefoxOptions()
	opts.add_argument("--headless")
	# driver = webdriver.Firefox(firefox_options=opts)	
	fp = webdriver.FirefoxProfile('/home/kris/.mozilla/firefox/xvjz362f.default')
	driver = webdriver.Firefox(firefox_profile=fp,firefox_options=opts)

	# driver = webdriver.Firefox()
	# go to the google home page

	while 1:
		scheduled_task(driver)
  		time.sleep(1)

def scheduled_task(driver):
	driver.get("https://www.causematch.com/wp-admin/admin.php?page=cm-rdp-cache")# find the element that's name attribute is q (the google search box)

	wait = WebDriverWait(driver, 40)

	purgeelement = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cm_rdp_purge"]')))
	dropelement = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="camp_post_id"]')))
	select=Select(dropelement)
	select.select_by_value('8307')
	purgeelement.send_keys(Keys.RETURN)
	print "Clicked"
	print "Purged cache"

	# the page is ajaxy so the title is originally this:
	print driver.title

	try:
		thread1 = threading.Thread(target = threaded_function, args = ("https://www.causematch.com/en/projects/belz-en/",driver,))
		thread2 = threading.Thread(target = threaded_function, args = ("https://www.causematch.com/he/projects/belz-offline/",driver, ))
		thread3 = threading.Thread(target = threaded_function, args = ("https://www.causematch.com/he/projects/belz/",driver, ))
		thread4 = threading.Thread(target = threaded_function, args = ("https://www.causematch.com/he/projects/belz-israel/",driver, ))
		thread1.start()
		thread1.join()


   		thread2.start()
		thread2.join()

		thread3.start()
		thread3.join()

   		thread4.start()

  		
 		thread4.join()


		#driver.quit()
		
	except Exception as e:
		driver.quit()	

def threaded_function(link,driver):
	driver.get(link)# find the element that's name attribute is q (the google search box)
	print driver.title


start_rdp_purge()

