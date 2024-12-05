from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Webaccess:
    def __init__(self,webaccess_config) -> None:
        """_summary_

        Args:
            json_config (json): json config of webaccess
        """
        self.config = webaccess_config

    def WebAccess_login(self,driver:object,user_id:str = "NasiwakRobot",password:str = "159753"):
        
        
        """_summary_
        Used To login to WebAccess 
        Args:
            driver : selenium.chrome.WebDriver
            user_id : Userid of your account  default value -> "NasiwakRobot"
            password : Password of your account default value -> "159753"
        """
        
        # webaccess_url = 'https://webaccess.nsk-cad.com/order_list.php'
        webaccess_url = self.config["webaccess_url"]
        driver.get(webaccess_url)
        # user_id = "NasiwakRobot"
        # password = "159753"
        try:
            logid = driver.find_element("name","u")
            logpassword = driver.find_element("name","p")

            logid.clear()
            logpassword.clear()

            logid.send_keys(user_id)
            logpassword.send_keys(password)
            logid.submit()
            driver.implicitly_wait(10)

            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located)
            print("Successfully logged in to Webaccess")
        except:
            print('logged in already')
            



    
    