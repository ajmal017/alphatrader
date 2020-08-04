from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def do_kite_login():
	opts = FirefoxOptions()
	opts.add_argument("--headless")
	driver = webdriver.Firefox(firefox_options=opts)	
	# driver = webdriver.Firefox()
	# go to the google home page
	driver.get("https://www.erate.in/trade/login/")# find the element that's name attribute is q (the google search box)
	wait = WebDriverWait(driver, 40)

	loginlinkelement = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginlink"]')))
	loginlinkelement.send_keys(Keys.RETURN)
	print "Clicked"
	# driver.quit()
	userid = wait.until(EC.element_to_be_clickable((By.ID, "inputone")))
	password = driver.find_element_by_id("inputtwo")
	submitbtn = driver.find_element_by_xpath('//*[@id="loginform"]/div[1]/div[1]/button')

	# type in the search
	userid.send_keys("ZZ8276")
	password.send_keys("vsappu7")
	submitbtn.send_keys(Keys.RETURN)
	# submit the form (although google automatically searches now without submitting)

	# the page is ajaxy so the title is originally this:
	print driver.title

	try:
		# we have to wait for the page to refresh, the last thing that seems to be updated is the title
		wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="twofaform"]/div[1]/input')))
		q1 = driver.find_element_by_xpath('//*[@id="twofaform"]/div[1]/span').text
		q2 = driver.find_element_by_xpath('//*[@id="twofaform"]/div[2]/span').text
		answer1input = driver.find_element_by_xpath('//*[@id="twofaform"]/div[1]/input')
		answer2input = driver.find_element_by_xpath('//*[@id="twofaform"]/div[2]/input')
		submit2btn = driver.find_element_by_xpath('//*[@id="twofaform"]/div[3]/div[1]/button')
		answer1 = get_kite_answer(q1)
		answer2 = get_kite_answer(q2)
		answer1input.send_keys(answer1)
		answer2input.send_keys(answer2)
		submit2btn.click()
		# You should see "cheese! - Google Search"
		wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="successful_login"]')))

		#Start Collecting ticks here
		# driver.get("https://www.erate.in/trade/dashboard/")# find the element that's name attribute is q (the google search box)
		# startcollectbtn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="start_collect_btn"]')))
		# startcollectbtn.send_keys(Keys.RETURN)

		print driver.title
		driver.quit()
		
	except Exception as e:
		driver.quit()
		time.sleep(5)
		do_kite_login()


def get_kite_answer(question):
	print question
	answer = ""
	if "landmark near your office" in question:
		answer = "Infopark"
	elif "first life insurance provider" in question:
		answer = "ICICI"
	elif "start your career" in question:
		answer = "Pulze"
	elif "your first mobile" in question:
		answer = "Samsung"		
	else:
		answer = "sobha city"
	return answer


do_kite_login()