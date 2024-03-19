import network
import urequests
import os
import json
import machine
from time import sleep

class OTAUpdater:
    """ This class handles OTA updates. It connects to the Wi-Fi, checks for updates, downloads and installs them."""
    def __init__(self, ssid, password, repo_url, filename, current_version):
        self.filename = filename
        self.ssid = ssid
        self.password = password
        self.repo_url = repo_url
        self.reboot_flag = False
        self.current_version = current_version
        self.tempString = ""
        # self.version_url = repo_url + 'main/version.json'                 # Replacement of the version mechanism by Github's oid
        self.version_url = self.process_version_url(repo_url, filename)     # Process the new version url
        self.firmware_url = repo_url + filename                             # Removal of the 'main' branch to allow different sources

        # get the current version (stored in version.json)
        '''
        if 'version.json' in os.listdir():    
            with open('version.json') as f:
                self.current_version = json.load(f)['version']
            print(f"Current device firmware version is '{self.current_version}'")
        
        
        #Use my custom file manifest instead:
        #with open('config.json

        else:
            self.current_version = "0"
            # save the current version
            with open('version.json', 'w') as f:
                json.dump({'version': self.current_version}, f)
        '''
        #get the latest version from init variables, passed from main loop
        
        
    def process_version_url(self, repo_url, filename):
        """ Convert the file's url to its assoicatied version based on Github's oid management."""

        # Necessary URL manipulations
        version_url = repo_url.replace("raw.githubusercontent.com", "github.com")  # Change the domain
        version_url = version_url.replace("/", "§", 4)                             # Temporary change for upcoming replace
        version_url = version_url.replace("/", "/latest-commit/", 1)                # Replacing for latest commit
        version_url = version_url.replace("§", "/", 4)                             # Rollback Temporary change
        version_url = version_url + filename                                       # Add the targeted filename
        
        return version_url

    def connect_wifi(self):
        """ Connect to Wi-Fi."""

        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(self.ssid, self.password)
        while not sta_if.isconnected():
            print('.', end="")
            sleep(0.25)
        print(f'Connected to WiFi, IP is: {sta_if.ifconfig()[0]}')
        
    def fetch_latest_code(self)->bool:
        """ Fetch the latest code from the repo, returns False if not found."""
        
        # Fetch the latest code from the repo.
        response = urequests.get(self.firmware_url)
        if response.status_code == 200:
            print(f'Fetched latest firmware code, status: {response.status_code}, -  {response.text}')
    
            # Save the fetched code to memory
            self.latest_code = response.text
            return True
        
        elif response.status_code == 404:
            print('Firmware not found.')
            return False

    def update_no_reset(self):
        """ Update the code without resetting the device."""
        self.tempString = 'latest_' + self.filename
        # Save the fetched code and update the version file to latest version.
        try:
            with open(self.tempString, 'w') as f:
                f.write(self.latest_code)
            os.rename(self.tempString, self.filename)
            self.current_version = self.latest_version
            self.latest_code = None
            return True
            
        except Exception as error:
            print(error)
            self.reboot_flag = True
            return False
        
        # update the version in memory
        #self.current_version = self.latest_version
        
        
        '''
        # save the current version
        with open('version.json', 'w') as f:
            json.dump({'version': self.current_version}, f)
        '''
        # free up some memory
        #self.latest_code = None

        # Overwrite the old code.
        #os.rename('latest_code.py', self.filename)

    def update_and_reset(self):
        """ Update the code and reset the device."""
        self.tempString = 'latest_' + self.filename
        print('Updating device...', end='')

        # Overwrite the old code.
        os.rename(self.tempString, self.filename)  

        # Restart the device to run the new code.
        print("Restarting device... (don't worry about an error message after this")
        sleep(0.25)
        machine.reset()  # Reset the device to run the new code.
        
    def check_for_updates(self):
        """ Check if updates are available."""
        
        # Connect to Wi-Fi
        self.connect_wifi()

        print('Checking for latest version...')
        headers = {"accept": "application/json"} 
        response = urequests.get(self.version_url, headers=headers)
        
        data = json.loads(response.text)
       
        self.latest_version = data['oid']                   # Access directly the id managed by GitHub
        print(f'latest version is: {self.latest_version}')
        
        # compare versions
        newer_version_available = True if self.current_version != self.latest_version else False
        
        print(f'Newer version available: {newer_version_available}')    
        return newer_version_available
    
    def download_and_install_update_if_available(self):
        """ Check for updates, download and install them."""
        if self.check_for_updates():
            if self.fetch_latest_code():
                self.update_no_reset()
                #self.update_and_reset()
        else:
            print('No new updates available.')
            
            
    def rolling_check_and_install(self):
        if self.check_for_updates():
            if self.fetch_latest_code():
                if self.update_no_reset():
                    return True
                else:
                    return False