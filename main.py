#main stuff
import secretVars
import json

with open("config.json",'r') as f:
    config = json.load(f)
    
def updater():
    import otacustom
    from machine import reset
    
    checkList = []
    global config
    
    for index, files in enumerate(config['FILEMANIFEST']):
        ota_updater = otacustom.OTAUpdater(secretVars.ssid, secretVars.wifiPassword, updatePath, files['FILENAME'], files['VERSION'])
        
        if ota_updater.rolling_check_and_install():
            config["FILEMANIFEST"][index]["CHECKFLAG"] = True
            checkList.append(True)
        else:
            config["FILEMANIFEST"][index]["CHECKFLAG"] = False
            checkList.append(False)
            
        del ota_updater
        
    with open("config.json",'w') as f:
        json.dump(config, f)
    
    if all(checkList):
        return True
    else:
        machine.reset()
        
        
if updater():
    import logger
        
        
    
    
        