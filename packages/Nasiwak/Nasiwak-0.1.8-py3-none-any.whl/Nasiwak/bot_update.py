import os
import requests
import sys
import time

class Bot_Update:
    def __init__(self,repo_owner:str,repo_name:str,version:str,access_token:str) -> None:
        """_summary_
         Check for the updates in repo if there are updates, it will automatically updates the bot 

        Args:
            repo_owner  : Enter Your NAME 
            repo_name   : Enter Repo NAME
            version     : Enter the Bot Version
            access_toke : Enter the Access Token
        """
        
        self.REPO_OWNER = repo_owner
        self.REPO_NAME = repo_name
        self.CURRENT_VERSION = version
        self.ACCESS_TOKEN = access_token
        self.NEW_VERSION_FILE = ""
        folder = os.getcwd()
        files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith('.bat')]
        for f in files:
            os.remove(f) 
            time.sleep(2)
        print("Checking for updates...")
        download_url = self.check_for_update()
        if download_url:
            if self.download_update(download_url):
                print(f"{self.NEW_VERSION_FILE} Downloaded Successfully")
                time.sleep(3)
                self.self_delete()
                exit()
            else:
                print("Can't Download the bot")
        
    
    def check_for_update(self):
        
        """Check GitHub for the latest release."""
        url = f"https://api.github.com/repos/{self.REPO_OWNER}/{self.REPO_NAME}/releases/latest"
        headers = {
            "Authorization": f"token {self.ACCESS_TOKEN}",
            
            }
        # print(url)
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                release_info = response.json()
                # print(release_info)
                latest_version = release_info['tag_name']
                # download_url = release_info['assets'][0]['browser_download_url']
                download_url = release_info['assets'][0]['url']
                self.NEW_VERSION_FILE = release_info['assets'][0]['name']
                print(f"Latest version: {latest_version}, Current version: {self.CURRENT_VERSION}")
                if latest_version > self.CURRENT_VERSION:
                    print("Update available!")
                    return download_url
                else:
                    print("No update available.")
            else:
                print(f"Failed to fetch release info: {response.status_code}")
        except Exception as e:
            print(f"Error checking for update: {e}")
        return None

    def download_update(self,download_url):
        
        """Download the latest version."""
        print("Downloading update...")
        try:
            headers = {
            "Authorization": f"token {self.ACCESS_TOKEN}",
            "Accept": "application/octet-stream"
        }
        # Send a GET request to the file URL and follow redirects
            response = requests.get(download_url,headers=headers,stream=True,allow_redirects=True)
            # Check if the request was successful
            print(f'Response Code: {response.status_code}')
            if response.status_code == 200:
                # Open the file in write-binary mode and save the content
                with open(self.NEW_VERSION_FILE, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
                        file.write(chunk)
                print(f"File downloaded successfully")
                return True
            else:
                print("Response code is not 200")
                return False
        except Exception as e:
            print(f"Error downloading update: {e}")
            return False

    def self_delete(self):
        # Get the current script path
        script_path = os.path.abspath(sys.argv[0])
     
        # Properly quote the path to handle spaces
        script_path_quoted = f'"{script_path}"'

        # Create a batch command to delete the script
        delete_command = fr'''
        @echo off
        timeout /t 2 >nul
        del {script_path_quoted}
        exit
        '''

        # Save the batch script in the same directory as the script
        batch_path = "deleter.bat"
        with open(batch_path, "w") as batch_file:
            batch_file.write(delete_command)
        
        # Execute the batch script to delete this script
        os.system(f'start /b {batch_path}')

