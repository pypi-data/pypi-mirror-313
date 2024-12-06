class Maildealer:
    
    def login(self,driver:object) -> None:
        """_summary_
        Used to Login to Maildealer 
        
        Args:
            driver : selenium.chrome.WebDriver
        """
        
        Maildealerurl = "https://md29.maildealer.jp/index.php"
        driver.get(Maildealerurl)
        
        logid = driver.find_element("name","fUName")#ログインIDの要素読み込み
        logpassword = driver.find_element("name","fPassword")#パスワードの要素読み込み

        logid.send_keys("チラント")
        logpassword.send_keys("7iww6vqp")

        # driver.find_element("xpath", '/html/body/div/div[1]/div[2]/div/form/div/input[2]')

        #Click on the Login button
        driver.find_element("xpath", "/html/body/div/div[1]/div[2]/div/form/div/input[2]").click()

        print("Login successful")