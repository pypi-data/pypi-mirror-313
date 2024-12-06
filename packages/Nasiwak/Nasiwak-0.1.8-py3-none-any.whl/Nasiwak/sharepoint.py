import time
from selenium.webdriver.common.by import By
import pyautogui
import pyperclip


class SharePoint:
    
    search = ""
    
    def __init__(self,sharepoint_config):
        """_summary_

        Args:
            sharepoint_config (json): Json config of sharepoint
        """
        self.sharepoint_config =  sharepoint_config
        
    
    def upload_folder(self,driver:object,url:str,folder_path:str):
        """_summary_

        Args:
            driver: selenium.chrome.WebDriver
            url : Url of the Sharepoint Folder 
            folder_path : Folder Path to be Uploaded 

        Returns:
            True if the folder Uploaded Succcessfully 
        """
        
        self.driver = driver
        
        self.driver.get(url)
        time.sleep(2)
        
        upload_button = self.driver.find_element(By.XPATH,self.sharepoint_config["xpaths"]["upload"])
        upload_button.click()
        time.sleep(1)
        
        folder_button = self.driver.find_element(By.XPATH,self.sharepoint_config["xpaths"]["folder"])
        folder_button.click()
        time.sleep(2)
        
        pyperclip.copy(folder_path)
        print("folder path is:", folder_path)
        pyautogui.hotkey('ctrl','v')
        print('ctrl v pressed')
        time.sleep(2)
        pyautogui.hotkey('enter')
        time.sleep(2)
        # pyautogui.click(645, 450)
        # pyautogui.hotkey('ctrl','a')
        # time.sleep(2)
        pyautogui.hotkey('enter')
        time.sleep(2)
        pyautogui.press('left')
        time.sleep(2)
        pyautogui.hotkey('enter')
        time.sleep(10)
        print("success")
        return True

        
    def handle_login(self,driver:object):
        """_summary_

        Args:
            driver : selenium.chrome.WebDriver
        """
        
        url=self.sharepoint_config["sharepoint_url"]
        
        self.driver = driver
        # Assuming the login page has input fields with IDs 'username' and 'password'
        self.driver.get(url)

        # username = "kushalnasiwak@nskkogyo.onmicrosoft.com"
        # password = "Vay32135"
        
        username = self.sharepoint_config["username"]
        password = self.sharepoint_config["password"]
        time.sleep(2.5)
        # Find the username input field on the login page
        email_field = self.driver.find_element(By.XPATH, self.sharepoint_config['login_xpaths']['email'])
        email_field.clear()
        email_field.send_keys(username)
        self.driver.find_element(By.XPATH, self.sharepoint_config['login_xpaths']['loggin_button']).click()
        time.sleep(1.5)
        password_field = self.driver.find_element(By.XPATH, self.sharepoint_config['login_xpaths']['password'])
        password_field.clear()
        password_field.send_keys(password)
        self.driver.find_element(By.XPATH, self.sharepoint_config['login_xpaths']['loggin_button']).click()
        time.sleep(1.5)
        
        self.driver.find_element(By.XPATH,self.sharepoint_config['login_xpaths']['checkbox']).click()
        self.driver.find_element(By.XPATH,self.sharepoint_config['login_xpaths']['yes_button']).click()
        time.sleep(2)
        
        print('Logged in to Sharepoint\nPlease wait.....')


    