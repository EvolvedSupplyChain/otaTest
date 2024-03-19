#boot stuff
#import otacustom
import json
import secretVars
import os
from machine import reset

with open('config.json','r') as f:
    config = json.load(f)
    
for index, file in enumerate(config['FILEMANIFEST']):
    if file['CHECKFLAG']:
        os.remove(file['FILENAME'])
        os.rename("latest_" + file['FILENAME'], file['FILENAME'])
        config['FILEMANIFEST'][index]['CHECKFLAG'] = False
        
with open('config.json', 'w') as f:
    json.dump(config, f)
    
reset()