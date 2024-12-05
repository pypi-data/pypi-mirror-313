from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

def create_driver():
        
        """_summary_
        creates a selenium.chrome.WebDriver and returns it

        Returns:
            selenium.chrome.WebDriver : Chrome WebDrivere 
        """
        chrome_options = Options()
        # download_folder = os.path.join(os.getcwd(), f'{id_folder_name}')
        chrome_options.add_experimental_option("prefs", {
        #"download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
        })

        # chrome_options.add_argument("--lang=en")

        # Initialize the WebDriver before the loop
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        
        return driver
    



def create_json_config(url,ACCESS_TOKEN) -> dict: 
    """_summary_

    Args:
        url : git file row url
        ACCESS_TOKEN : your access token

    Returns:
        json response: Returns the json-encoded content of a response, if any.
    """
    headers = {"Authorization": f"token {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    return response.json()