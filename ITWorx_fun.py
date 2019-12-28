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
	driver.get_screenshot_as_file("screenshots//application_when_opened.png")
	print("*** Application has been opened. \n")
	file.write("*** Application has been opened. \n")
	
######### Another way to check if page has been loaded #########
def check_element_to_be_clickable(file, driver):
	try:
		WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "add")))
		driver.get_screenshot_as_file("screenshots//application_when_opened.png")
		print("*** Application has been opened. \n")
		file.write("*** Application has been opened. \n")
	except:
		driver.close()
		print("*** Application has not been opened. \n")
		file.write("*** Application has not been opened. \n")

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
		driver.get_screenshot_as_file("screenshots//check_not_exist.png")
		print("*** Test case: Pass, Computer not found.\n")
		file.write("*** Test case: Pass, Computer not found.\n")
		searchbox = driver.find_element_by_id("searchbox")
		searchbox.clear()
		searchbox.send_keys("Test Pass") #type on searchbox
	except:
		driver.get_screenshot_as_file("screenshots//check_not_exist.png")
		print("*** Test case: Fail, Computer already exist please delete it or run test by unique computer name\n")
		file.write("*** Test case: Fail, Computer already exist please delete it or run test by unique computer name\n")
	sleep(2)

######### check search result on existing computer  #########
def check_exist(file, driver):
	searchbox = driver.find_element_by_id("searchbox")
	try:
		WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.ID, "main"), "Nothing to display"))
		driver.get_screenshot_as_file("screenshots//check_exist.png")
		print("*** Test case: Fail, Search results not found\n")
		file.write("*** Test case: Fail, Search results not found\n")
		searchbox.clear()
		searchbox.send_keys("Test Fail") #type on searchbox
	except:
		driver.get_screenshot_as_file("screenshots//check_exist.png")
		print("*** Test case: Pass, Search results has been found.\n")
		file.write("*** Test case: Pass, Search results has been found.\n")
		searchbox.clear()
		searchbox.send_keys("Test Pass") #type on searchbox
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
	company.click() #Open companies list
	sleep(1)
	asus = driver.find_element_by_xpath("//option[contains(text(),'" + c_company + "')]")
	asus.click()  #Choose Company
	sleep(1)
	company.click() #Close list
	sleep(1)
	driver.get_screenshot_as_file("screenshots//added_computer_data.png")
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
		driver.get_screenshot_as_file("screenshots//check_creation_message.png")
		print("*** Test case: Pass, Correct creation message appeared\n")
		file.write("*** Test case: Pass, Correct creation message appeared\n")
		searchbox.clear()
		searchbox.send_keys("Test Pass") #type on searchbox
	except:
		print("*** Test case: Fail in creation message.\n")
		file.write("*** Test case: Fail in creation message.\n")
		searchbox.clear()
		searchbox.send_keys("Test Fail") #type on searchbox

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
	search_by_computer_name(file, driver, c_name) # Search on the computer to delete
	elem1 = driver.find_element_by_xpath("/html/body/section/table/tbody/tr[1]/td[1]/a")
	elem1.click()
	sleep(1)
	driver.get_screenshot_as_file("screenshots//computer_data_before_delete.png")
	del_btn = driver.find_element_by_class_name("topRight")
	del_btn.click()
	sleep(1)

######### Check deletion message #########
def check_deletion_message(file, driver, c_name):
	try:
		msg= "Done! Computer has been deleted"
		searchbox = driver.find_element_by_id("searchbox")
		WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.ID, "main"), msg))
		driver.get_screenshot_as_file("screenshots//check_deletion_message.png")
		print("*** Test case: Pass, Correct deletion message appeared\n")
		file.write("*** Test case: Pass, Correct deletion message appeared\n")
		searchbox.clear()
		searchbox.send_keys("Test Pass") #type on searchbox
	except:
		driver.get_screenshot_as_file("screenshots//check_deletion_message.png")
		print("*** Test case: Fail in deletion message\n")
		file.write("*** Test case: Fail in deletion message\n")
		searchbox.clear()
		searchbox.send_keys("Test Fail") #type on searchbox
	sleep(2)

######### Edit computer data #########
# old_c_name:name of commputer you want to edit
# c_name, I_date, D_date, c_company: new data to replace old data by it.
# if you want any parameter without change put it by the old data.
def edit_computer(file,  driver, old_c_name, c_name, I_date, D_date, c_company): 
	search_by_computer_name(file, driver, old_c_name) # Search on the computer to edit
	elem1 = driver.find_element_by_xpath("/html/body/section/table/tbody/tr[1]/td[1]/a")
	elem1.click()
	sleep(1)
	driver.get_screenshot_as_file("screenshots//Edit_Computer_Old_Data.png")
	name = driver.find_element_by_id("name")
	name.clear()  # clear Computer name
	name.send_keys(c_name) #type Computer name
	sleep(1)
	introduced = driver.find_element_by_id("introduced")
	introduced.clear()  # clear Introduced date
	introduced.send_keys(I_date) #type Introduced date
	sleep(1)
	discontinued = driver.find_element_by_id("discontinued")
	discontinued.clear()  # clear Discontinued date
	discontinued.send_keys(D_date) #type Discontinued date
	sleep(1)
	company = driver.find_element_by_id("company") #find Company
	company.click() #Open companies list
	sleep(1)
	asus = driver.find_element_by_xpath("//option[contains(text(),'" + c_company + "')]")
	asus.click()  #Choose Company
	sleep(1)
	company.click() #Close list
	sleep(1)
	driver.get_screenshot_as_file("screenshots//Edit_Computer_New_Data.png")
	sleep(1)

######### Check edition message #########
def check_edition_message(file, driver, new_c_name):
	try:
		msg= "Done! Computer " + new_c_name + " has been updated"
		searchbox = driver.find_element_by_id("searchbox")
		WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.ID, "main"), msg))
		driver.get_screenshot_as_file("screenshots//check_edition_message.png")
		print("*** Test case: Pass, Correct edition message appeared\n")
		file.write("*** Test case: Pass, Correct edition message appeared\n")
		searchbox.clear()
		searchbox.send_keys("Test Pass") #type on searchbox
	except:
		driver.get_screenshot_as_file("screenshots//check_edition_message.png")
		print("*** Test case: Fail in edition message\n")
		file.write("*** Test case: Fail in edition message\n")
		searchbox.clear()
		searchbox.send_keys("Test Fail") #type on searchbox
	sleep(2)


def check_computer_data(file,  driver, c_name, I_date, D_date, c_company): 
	search_by_computer_name(file, driver, c_name) # Search on the computer to check his data
	elem1 = driver.find_element_by_xpath("/html/body/section/table/tbody/tr[1]/td[1]/a")
	elem1.click()
	name = driver.find_element_by_id("name").get_attribute('value')
	introduced = driver.find_element_by_id("introduced").get_attribute('value')
	discontinued = driver.find_element_by_id("discontinued").get_attribute('value')
	company_list = driver.find_element_by_id("company").get_attribute('value')
	switcher = {"1": "Apple Inc.", "2": "Thinking Machines", "3": "RCA", "4": "Netronics", "5": "Tandy Corporation", "6": "Commodore International", "7": "MOS Technology", "8": "Micro Instrumentation and Telemetry Systems", "9": "IMS Associates, Inc.", "10": "Digital Equipment Corporation", "11": "Lincoln Laboratory", "12": "Moore School of Electrical Engineering", "13": "IBM", "14": "Amiga Corporation", "15": "Canon", "16": "Nokia", "17": "Sony", "18": "OQO", "19": "NeXT", "20": "Atari", "22": "Acorn computer", "23": "Timex Sinclair", "24": "Nintendo", "25": "Sinclair Research Ltd", "26": "Xerox", "27": "Hewlett-Packard", "28": "Zemmix", "29": "ACVS", "30": "Sanyo", "31": "Cray", "32": "Evans &amp; Sutherland", "33": "E.S.R. Inc.", "34": "OMRON", "35": "BBN Technologies", "36": "Lenovo Group", "37": "ASUS", "38": "Amstrad", "39": "Sun Microsystems", "40": "Texas Instruments", "41": "HTC Corporation", "42": "Research In Motion", "43": "Samsung Electronics"}
	company = switcher.get(company_list, "")
	if (name == c_name and introduced == I_date and discontinued == D_date and company == c_company):
		driver.get_screenshot_as_file("screenshots//check_computer_data.png")
		print("*** Computer data are the same as expected\n")
		file.write("*** Computer data are the same as expected\n")
		res=1
	else:
		driver.get_screenshot_as_file("screenshots//check_computer_data.png")
		print("*** Computer data are not the same as expected\n")
		file.write("*** Computer data are not the same as expected\n")
		res=2
	cancel_it(file, driver)
	return res


######### End test & close results file #########
def end_test(file, driver):
	time_now = datetime.now()
	# dd/mm/YY H:M:S
	time_now_string = time_now.strftime("%d/%m/%Y %H:%M:%S")
	driver.get_screenshot_as_file("screenshots//application_at_the_end.png")
	print("*** Application has been closed. \n")
	file.write("*** Application has been closed. \n")
	print("*** Test End time: " + time_now_string + "\n")
	file.write("\nTest End time: " + time_now_string + "\n")
	file.close()
	sleep(5)
	driver.close()