from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from time import sleep
import pyperclip
import ITWorx_fun as itworx
######### Initiation #########
driver = webdriver.Chrome()
driver.maximize_window()
try:
	file = open("Test_Report_add20.txt","w")
	inputfile = open("Add20computers.csv","r")
except:
	print("*** Test Fail: Can't open data file, Close it if opened.\n")
	file.write("*** Test Fail: Can't open data file, Close it if opened.\n")
####### Open application #########
itworx.goto_home(driver)
######### start_test #########
itworx.start_test(file)
itworx.check_page_title(file, driver) # Check if page has been loaded
print("# Number of computers before @ the beginning of the test:")
file.write("# Number of computers before @ the beginning of the test:")
itworx.get_no_computers(file, driver) # Save number of computers before test

text = inputfile.read()
lines = text.split("\n")
i=0
for line in lines:
	if i==0:
		i += 1
	else:
		print("*** Addtion: (" + str(i) + ") data: " + line + ".\n")
		file.write("*** Addtion: (" + str(i) + ") data: " + line + ".\n")
		i += 1
		parameters_list = line.split(",")
		c_name = parameters_list[0]
		I_date = parameters_list[1]
		D_date = parameters_list[2]
		c_company = parameters_list[3]
		## Test Case: Add New Computer (cancel then Add)
		no_comp = itworx.get_no_computers(file, driver) # Save number of computers before test
		print("# Test Case: Add New Computer\n")
		file.write("# Test Case: Add New Computer\n")
		itworx.add_computer_data(file, driver,c_name,I_date,D_date,c_company) # Add computer
		itworx.create_it(file, driver) # press create Button
		itworx.check_creation_message(file, driver, c_name) # check creation message
		print("# Number of computers after addtion:")
		file.write("# Number of computers after addtion:")
		itworx.check_N_computers(file, driver, no_comp+1) # Check number of computers after add
		## Test Case " Search about existing Computer"
		print("# Test Case: Search about existing Computer\n")
		file.write("# Test Case: Search about existing Computer\n")
		itworx.search_by_computer_name(file, driver, c_name) # Search on it
		itworx.check_exist(file, driver) # check if Search results has been found
		itworx.goto_home(driver)

######### end_test #########
print("# Number of computers before @ the end of the test:")
file.write("# Number of computers before @ the end of the test:")
no_comp = itworx.get_no_computers(file, driver)
itworx.end_test(file, driver)