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
	file = open("Test_Report.txt","w")
except:
	print("*** Test Fail: Can't write in result file, Close it if opened.\n")
	file.write("*** Test Fail: Can't write in result file, Close it if opened.\n")
######### Open application #########
itworx.goto_home(driver)
######### start_test #########
itworx.start_test(file)
itworx.check_page_title(file, driver) # Check if page has been loaded
no_comp = itworx.get_no_computers(file, driver) # Save number of computers before test

## Test Case " Search about non existing Computer"
print("# Test Case: Search about non existing Computer\n")
file.write("# Test Case: Search about non existing Computer\n")
itworx.search_by_computer_name(file, driver, "Ashour") # Search on non Existing computer
itworx.check_not_exist(file, driver) # check result "Nothing to display"

## Test Case: Add New Computer (cancel then Add)
print("# Test Case: Add New Computer\n")
file.write("# Test Case: Add New Computer\n")
print("# Test Cancel Button after Adding the New Computer data\n")
file.write("# Test Cancel Button after Adding the New Computer data\n")
itworx.add_computer_data(file, driver,"Ashour","2019-04-13","2019-04-13","ASUS") # Add computer
itworx.cancel_it(file, driver) # press cancel Button after add data
itworx.search_by_computer_name(file, driver, "Ashour") # Search on non Existing computer as per cancel
itworx.check_not_exist(file, driver) # check result "Nothing to display"
itworx.add_computer_data(file, driver,"Ashour","2019-04-13","2019-04-13","ASUS") # Add computer
itworx.create_it(file, driver) # press create Button
itworx.check_creation_message(file, driver, "Ashour") # check creation message
itworx.check_N_computers(file, driver, no_comp+1) # Check number of computers after add

## Test Case " Search about existing Computer"
print("# Test Case: Search about existing Computer\n")
file.write("# Test Case: Search about existing Computer\n")
itworx.search_by_computer_name(file, driver, "Ashour") # Search on it
itworx.check_exist(file, driver) # check if Search results has been found

## Edit Computer
print("# Test Case: Edit Computer\n")
file.write("# Test Case: Edit Computer\n")
print("# Test Cancel Button after Adding the New Computer data\n")
file.write("# Test Cancel Button after Adding the New Computer data\n")
itworx.edit_computer(file, driver, "Ashour", "Ashour2", "2020-05-14","2020-06-13","IBM")
itworx.cancel_it(file, driver) # press cancel Button after add data
res = 0 # 0:Default. 1:Same as parameter 2:Not the same.
res = itworx.check_computer_data(file, driver, "Ashour","2019-04-13","2019-04-13","ASUS") # check data of computer
if res == 1:
	print("*** Test Case: Pass Computer data has not been changed\n")
	file.write("*** Test Case: Pass Computer data has not been changed\n")
elif res == 2:
	print("*** Test Case: Fail Computer data has been changed\n")
	file.write("*** Test Case: Fail Computer data has been changed\n")
itworx.edit_computer(file, driver, "Ashour", "Ashour2", "2020-05-14","2020-06-13","IBM")
itworx.create_it(file, driver) # press create Button
itworx.check_edition_message(file, driver, "Ashour2") # check creation message
itworx.check_computer_data(file, driver, "Ashour2", "2020-05-14","2020-06-13","IBM") # check new data of computer
if res == 1:
	print("*** Test Case: Pass Computer data has been changed\n")
	file.write("*** Test Case: Pass Computer data has been changed\n")
elif res == 2:
	print("*** Test Case: Fail Computer data has not been changed\n")
	file.write("*** Test Case: Fail Computer data has not been changed\n")

## Test Case: Delete Computer
print("# Test Case: Delete Computer\n")
file.write("# Test Case: Delete Computer\n")
itworx.delete_computer(file,  driver, "Ashour")
itworx.check_deletion_message(file, driver, "Ashour") # check creation message
itworx.check_N_computers(file, driver, no_comp) # Check number of computers after delete
itworx.search_by_computer_name(file, driver, "Ashour") # Search on non Existing computer
itworx.check_not_exist(file, driver) # check result "Nothing to display"

## Test Cases of all supported sort
print("# Test Cases of all supported sort:(Note:All sort test cases are fail as per a bug in the Application)\n")
file.write("# Test Cases of all supported sort:(Note:All sort test cases are fail as per a bug in the Application)\n")
itworx.goto_home(driver)
itworx.sort_by_Computer_name(file, driver, 1) # ad=1 ascending
itworx.sort_by_Computer_name(file, driver, 2) # ad=2 descending
itworx.sort_by_Introduced(file, driver, 1) # ad=1 ascending
itworx.sort_by_Introduced(file, driver, 2) # ad=2 descending
itworx.sort_by_Discontinued(file, driver, 1) # ad=1 ascending
itworx.sort_by_Discontinued(file, driver, 2) # ad=2 descending
itworx.sort_by_Company(file, driver, 1) # ad=1 ascending
itworx.sort_by_Company(file, driver, 2) # ad=2 descending
######### end_test #########
itworx.end_test(file, driver)