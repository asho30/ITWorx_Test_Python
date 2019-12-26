from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from time import sleep
from datetime import datetime
import pyperclip

######### Used Functions #########
######### Create file to save results #########
def start_test(file):
	time_now = datetime.now()
	# dd/mm/YY H:M:S
	time_now_string = time_now.strftime("%d/%m/%Y %H:%M:%S")
	print("*** Test start time: " + time_now_string + "\n")
	file.write("Test start time: " + time_now_string + "\n\n")
	no_comp = "0" # initiate global variable

######### Open Application Home page #########
def goto_home(driver):
	driver.get("http://computer-database.herokuapp.com/computers")

######### Check if page has been loaded #########
def check_page_title(file, driver):
	wait = WebDriverWait( driver, 5 )
	page_title = driver.title
	assert page_title == "Computers database"
	print("*** Page opened \n")
	file.write("*** Page opened \n")
	
######### Another way to check if page has been loaded #########
def check_element_to_be_clickable(file, driver):
	try:
		WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "add")))
		print("*** Page opened \n")
		file.write("*** Page opened \n")
	except:
		driver.close()
		print("*** Page not opened \n")
		file.write("*** Page not opened \n")

######### Search on non Existing computer #########
def search_by_computer_name(file, driver, c_name):
	searchbox = driver.find_element_by_id("searchbox")
	searchbox.clear()
	sleep(1)
	searchbox.send_keys(c_name) #type on searchbox
	sleep(1)
	searchsubmit = driver.find_element_by_id("searchsubmit")
	searchsubmit.click() #filter by name
	sleep(1)

######### check result "Nothing to display" #########
def check_not_exist(file, driver):
	try:
		WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.ID, "main"), "Nothing to display"))
		print("*** Test case: Pass, Computer not found.\n")
		file.write("*** Test case: Pass, Computer not found.\n")
		searchbox = driver.find_element_by_id("searchbox")
		searchbox.clear()
		searchbox.send_keys("Test Pass") #type on searchbox
	except:
		searchbox.clear()
		searchbox.send_keys("Test Fail") #type on searchbox
		print("*** Test case: Fail, Computer already exist please delete it or run test by unique computer name\n")
		file.write("*** Test case: Fail, Computer already exist please delete it or run test by unique computer name\n")
	sleep(2)

######### check search result on existing computer  #########
def check_exist(file, driver):
	try:
		searchbox = driver.find_element_by_id("searchbox")
		WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.ID, "main"), "Nothing to display"))
		print("*** Test case: Fail, Search results not found\n")
		file.write("*** Test case: Fail, Search results not found\n")
		searchbox.clear()
		searchbox.send_keys("Test Fail") #type on searchbox
	except:
		searchbox.clear()
		searchbox.send_keys("Test Pass") #type on searchbox
		print("*** Test case: Pass, Search results has been found.\n")
		file.write("*** Test case: Pass, Search results has been found.\n")
	sleep(2)

######### Add computer #########
def add_computer_data(file, driver, c_name, I_date, D_date, c_company):
	add = driver.find_element_by_id("add")
	add.click() #Add a new computer
	sleep(1)
	name = driver.find_element_by_id("name")
	name.send_keys(c_name) #type Computer name
	sleep(1)
	introduced = driver.find_element_by_id("introduced")
	introduced.send_keys(I_date) #type Introduced date
	sleep(1)
	discontinued = driver.find_element_by_id("discontinued")
	discontinued.send_keys(D_date) #type Discontinued date
	sleep(1)
	company = driver.find_element_by_id("company") #find Company
	company.click() #Choose Company
	sleep(1)
	asus = driver.find_element_by_xpath("//option[contains(text(),'" + c_company + "')]")
	asus.click()  #Choose ASUS
	sleep(1)
	company.click() #Close list
	sleep(1)
 
######### create Computer #########
def create_it(file, driver):
	createcomputer = driver.find_elements_by_class_name("btn")[0] # Create Button
	createcomputer.click()  #Create this computer

######### cancel computer after add data #########
def cancel_it(file, driver):
	cancel = driver.find_elements_by_class_name("btn")[1] # Cancel Button
	cancel.click()  #cancel this computer

######### Check creation message #########
def check_creation_message(file, driver, c_name):
	try:
		msg= "Done! Computer " + c_name + " has been created"
		searchbox = driver.find_element_by_id("searchbox")
		WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.ID, "main"), msg))
		print("*** Test case: Pass, Correct creation message appeared\n")
		file.write("*** Test case: Pass, Correct creation message appeared\n")
		searchbox.clear()
		searchbox.send_keys("Test Pass") #type on searchbox
	except:
		searchbox.clear()
		searchbox.send_keys("Test Fail") #type on searchbox
		print("*** Test case: Fail in creation message.\n")
		file.write("*** Test case: Fail in creation message.\n")
	sleep(2)

######### Get number of computers before add #########
def get_no_computers(file, driver):
	no_comp_str = driver.find_element_by_id("main").text[0:9].split(' ')[0]
	print(no_comp_str + " Computers")
	file.write(no_comp_str + " Computers")
	no_comp = int(no_comp_str)
	return no_comp

######### Check number of computers after add #########
def check_N_computers(file, driver, no_comp1):
	no_comp_str = driver.find_element_by_id("main").text[0:9].split(' ')[0]
	print(no_comp_str + " Computers.\n")
	file.write(no_comp_str + " Computers.\n")
	no_comp2 = int(no_comp_str)
	assert no_comp2 == no_comp1
	print("*** Test case: Pass, Number of computers has been changed to " + no_comp_str +" computers.\n")
	file.write("*** Test case: Pass, Number of computers has been changed to " + no_comp_str +" computers.\n")

######### Sort by Computer name
def sort_by_Computer_name(file, driver, ad): # ad=1 ascending, ad=2 descending
	if ad == 1:
		print("# Test case to sort main table by Computer name in ascending order\n")
		file.write("# Test case to sort main table by Computer name in ascending order\n")
	elif ad == 2:
		print("# Test case to sort main table by Computer name in descending order\n")
		file.write("# Test case to sort main table by Computer name in descending order\n")
	else:
		print("Wrong parameter in sort function\n")
		file.write("Wrong parameter in sort function\n")
		return
	try:
		arrow = driver.find_element_by_xpath("/html/body/section/table/thead/tr/th[1]/a") # Computer_name arrow down by defulte
		arrow2 = driver.find_element_by_xpath("/html/body/section/table/thead/tr/th[2]/a")
		if ad == 1:
			arrow2.click()
			sleep(1)
			arrow.click()
			sleep(1)
		elif ad == 2:
			sleep(1)
			arrow.click()
			sleep(1)
		elem1 = driver.find_element_by_xpath("/html/body/section/table/tbody/tr[1]/td[1]/a")
		elem2 = driver.find_element_by_xpath("/html/body/section/table/tbody/tr[2]/td[1]")
		if ad == 1:
			if elem2 > elem1:
				print("*** Test case: Pass, Table has been sorted by company name ascending\n")
				file.write("*** Test case: Pass, Table has been sorted by company name ascending\n")
			else:
				print("*** Test case: Fail, Table has not been sorted by company name ascending\n")
				file.write("*** Test case: Fail, Table has not been sorted by company name ascending\n")
		elif ad == 2:
			if elem2 < elem1:
				print("*** Test case: Pass, Table has been sorted by company name descending\n")
				file.write("*** Test case: Pass, Table has been sorted by company name descending\n")
			else:
				print("*** Test case: Fail, Table has not been sorted by company name descending\n")
				file.write("*** Test case: Fail, Table has not been sorted by company name descending\n")
	except:
		print("*** Test case: Fail, Table has not been sorted\n")
		file.write("*** Test case: Fail, Table has not been sorted\n")

######### Sort by Introduced
def sort_by_Introduced(file, driver, ad): # ad=1 ascending, ad=2 descending 
	if ad == 1:
		print("# Test case to sort main table by Introduced in ascending order\n")
		file.write("# Test case to sort main table by Introduced in ascending order\n")
	elif ad == 2:
		print("# Test case to sort main table by Introduced in descending order\n")
		file.write("# Test case to sort main table by Introduced in descending order\n")
	else:
		print("Wrong parameter in sort function\n")
		file.write("Wrong parameter in sort function\n")
		return
	try:
		arrow = driver.find_element_by_xpath("/html/body/section/table/thead/tr/th[2]/a") # Introduced arrow up by defulte
		sleep(1)
		arrow.click()
		if ad == 1:
			sleep(1)
			arrow.click()
			sleep(1)
		elif ad == 2:
			sleep(1)
			arrow.click()
			sleep(1)
			sleep(1)
			arrow.click()
			sleep(1)
		elem1 = driver.find_element_by_xpath("/html/body/section/table/tbody/tr[1]/td[1]/a")
		elem2 = driver.find_element_by_xpath("/html/body/section/table/tbody/tr[2]/td[1]")
		if ad == 1:
			if elem2 > elem1:
				print("*** Test case: Pass, Table has been sorted by Introduced ascending\n")
				file.write("*** Test case: Pass, Table has been sorted by Introduced ascending\n")
			else:
				print("*** Test case: Fail, Table has not been sorted by Introduced ascending\n")
				file.write("*** Test case: Fail, Table has not been sorted by Introduced ascending\n")
		elif ad == 2:
			if elem2 < elem1:
				print("*** Test case: Pass, Table has been sorted by Introduced descending\n")
				file.write("*** Test case: Pass, Table has been sorted by Introduced descending\n")
			else:
				print("*** Test case: Fail, Table has not been sorted by Introduced descending\n")
				file.write("*** Test case: Fail, Table has not been sorted by Introduced descending\n")
	except:
		print("*** Test case: Fail, Table has not been sorted\n")
		file.write("*** Test case: Fail, Table has not been sorted\n")

######### Sort by Discontinued
def sort_by_Discontinued(file, driver, ad): # ad=1 ascending, ad=2 descending 
	if ad == 1:
		print("# Test case to sort main table by Discontinued in ascending order\n")
		file.write("# Test case to sort main table by Discontinued in ascending order\n")
	elif ad == 2:
		print("# Test case to sort main table by Discontinued in descending order\n")
		file.write("# Test case to sort main table by Discontinued in descending order\n")
	else:
		print("Wrong parameter in sort function\n")
		file.write("Wrong parameter in sort function\n")
		return
	try:
		arrow = driver.find_element_by_xpath("/html/body/section/table/thead/tr/th[3]/a") # Discontinued arrow up by defulte
		sleep(1)
		arrow.click()
		if ad == 1:
			sleep(1)
			arrow.click()
			sleep(1)
		elif ad == 2:
			sleep(1)
			arrow.click()
			sleep(1)
			sleep(1)
			arrow.click()
			sleep(1)
		elem1 = driver.find_element_by_xpath("/html/body/section/table/tbody/tr[1]/td[1]/a")
		elem2 = driver.find_element_by_xpath("/html/body/section/table/tbody/tr[2]/td[1]")
		if ad == 1:
			if elem2 > elem1:
				print("*** Test case: Pass, Table has been sorted by Discontinued ascending\n")
				file.write("*** Test case: Pass, Table has been sorted by Discontinued ascending\n")
			else:
				print("*** Test case: Fail, Table has not been sorted by Discontinued ascending\n")
				file.write("*** Test case: Fail, Table has not been sorted by Discontinued ascending\n")
		elif ad == 2:
			if elem2 < elem1:
				print("*** Test case: Pass, Table has been sorted by Discontinued descending\n")
				file.write("*** Test case: Pass, Table has been sorted by Discontinued descending\n")
			else:
				print("*** Test case: Fail, Table has not been sorted by Discontinued descending\n")
				file.write("*** Test case: Fail, Table has not been sorted by Discontinued descending\n")
	except:
		print("*** Test case: Fail, Table has not been sorted\n")
		file.write("*** Test case: Fail, Table has not been sorted\n")

######### Sort by Company
def sort_by_Company(file,  driver, ad): # ad=1 ascending, ad=2 descending 
	if ad == 1:
		print("# Test case to sort main table by Company in ascending order\n")
		file.write("# Test case to sort main table by Company in ascending order\n")
	elif ad == 2:
		print("# Test case to sort main table by Company in descending order\n")
		file.write("# Test case to sort main table by Company in descending order\n")
	else:
		print("Wrong parameter in sort function\n")
		file.write("Wrong parameter in sort function\n")
		return
	try:
		arrow = driver.find_element_by_xpath("/html/body/section/table/thead/tr/th[4]/a") # Company arrow up by defulte
		sleep(1)
		arrow.click()
		if ad == 1:
			sleep(1)
			arrow.click()
			sleep(1)
		elif ad == 2:
			sleep(1)
			arrow.click()
			sleep(1)
			sleep(1)
			arrow.click()
			sleep(1)
		elem1 = driver.find_element_by_xpath("/html/body/section/table/tbody/tr[1]/td[1]/a")
		elem2 = driver.find_element_by_xpath("/html/body/section/table/tbody/tr[2]/td[1]")
		if ad == 1:
			if elem2 > elem1:
				print("*** Test case: Pass, Table has been sorted by Company ascending\n")
				file.write("*** Test case: Pass, Table has been sorted by Company ascending\n")
			else:
				print("*** Test case: Fail, Table has not been sorted by Company ascending\n")
				file.write("*** Test case: Fail, Table has not been sorted by Company ascending\n")
		elif ad == 2:
			if elem2 < elem1:
				print("*** Test case: Pass, Table has been sorted by Company descending\n")
				file.write("*** Test case: Pass, Table has been sorted by Company descending\n")
			else:
				print("*** Test case: Fail, Table has not been sorted by Company descending\n")
				file.write("*** Test case: Fail, Table has not been sorted by Company descending\n")
	except:
		print("*** Test case: Fail, Table has not been sorted\n")
		file.write("*** Test case: Fail, Table has not been sorted\n")

######### delete_computer #########
def delete_computer(file,  driver, c_name):
	search_by_computer_name(file, driver, c_name) # Search on non Existing computer
	elem1 = driver.find_element_by_xpath("/html/body/section/table/tbody/tr[1]/td[1]/a")
	elem1.click()
	del_btn = driver.find_element_by_class_name("topRight")
	del_btn.click()

######### Check deletion message #########
def check_deletion_message(file, driver, c_name):
	try:
		msg= "Done! Computer has been deleted"
		searchbox = driver.find_element_by_id("searchbox")
		WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.ID, "main"), msg))
		print("*** Test case: Pass, Correct creation message appeared\n")
		file.write("*** Test case: Pass, Correct creation message appeared\n")
		searchbox.clear()
		searchbox.send_keys("Test Pass") #type on searchbox
	except:
		searchbox.clear()
		searchbox.send_keys("Test Fail") #type on searchbox
		print("*** Test case: Fail in creation message\n")
		file.write("*** Test case: Fail in creation message\n")
	sleep(2)

######### End test & close results file #########
def end_test(file, driver):
	time_now = datetime.now()
	# dd/mm/YY H:M:S
	time_now_string = time_now.strftime("%d/%m/%Y %H:%M:%S")
	print("*** Test End time: " + time_now_string + "\n")
	file.write("\nTest End time: " + time_now_string + "\n")
	file.close()
	sleep(5)
	driver.close()
