import time
import pyautogui


class Aisys:
    def __init__(self,aisys_config) -> None:
        """_summary_
        
        Args:
            Aisys_config (json): Json config of aisys
        """
        self.Aisys_config = aisys_config
        
    def Aisys_login(self,driver):
        driver.get(self.Aisys_config['aisys_url'])
        
        #Log In to Aikomuten
        userId = self.Aisys_config['aisys_userid']
        id = driver.find_element('xpath',self.Aisys_config["login_xpaths"]["ログインID"])
        id.send_keys(userId)

        userPwd = self.Aisys_config['aisys_password']
        pwd = driver.find_element('xpath',self.Aisys_config["login_xpaths"]["パスワード"])
        pwd.send_keys(userPwd)

        print('Entered Username and Password')

        submit1 = driver.find_element('xpath',self.Aisys_config["login_xpaths"]["ログイン"])
        submit1.click()
        
        
        print('Login Successful to Ai-koumuten')
        time.sleep(2)
        pyautogui.press('Enter')
        
        
    
    