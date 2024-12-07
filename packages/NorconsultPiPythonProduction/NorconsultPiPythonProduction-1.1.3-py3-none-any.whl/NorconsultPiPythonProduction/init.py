import subprocess
import os
import clr
import sys
import requests
from importlib.metadata import version
import logging


file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from copyFiles import copyAllFiles

#Check for internet connection
def check_internet_connection():
    try:
        requests.get('http://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False

user_has_internet_connection = check_internet_connection()

class refresh_auth: 
    def __init__(self): 
        authPath = "C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Norconsult\\NorconsultPiPython_auth\\PiPython.exe"
        subprocess.check_call([authPath])

#Copy Files & Authentificate
if user_has_internet_connection:
    try: 
        copyAllFiles()
        refresh_auth()
    except Exception as e:
        print("Continuing without VPN connection... Establishing a connection with the API is not possible outside Norconsult firewall. Connect to VPN and restart kernel if you are using notebook.")
        print()
else:
    logging.warning("Running PiPython in offline mode as no internet connection is detected. Establishing a connection with the API is not possible offline.")

##Importing PI libraries and dependencies
referenceFolder = "C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Norconsult\\NorconsultPiPythonProduction"
modellingDllPath = referenceFolder + "\\APIClientModelling.dll" 
analysisDllPath = referenceFolder + "\\APIClientAnalysis.dll" 
commonDllPath = referenceFolder + "\\APIClientCommon.dll" 
piCommonDllPath = referenceFolder + "\\Norconsult.PI.Common.dll"
FEMmodelBuilderPath = referenceFolder + "\\ModelBuilder_FEM_Design.dll";
RobotModelBuilderPath = referenceFolder + "\\ModelBuilder_Robot.dll"
FemIntegratedPath = referenceFolder + "\\FemIntegrated.dll"

clr.AddReference(modellingDllPath)
clr.AddReference(analysisDllPath)
clr.AddReference(commonDllPath)
clr.AddReference(piCommonDllPath)
clr.AddReference(FEMmodelBuilderPath)
clr.AddReference(RobotModelBuilderPath)
clr.AddReference(FemIntegratedPath)


#Imports 
import Norconsult.PI.APIConnect.Analysis as aapi 
import Norconsult.PI.Common.API.Models.Analysis as adto
import Norconsult.PI.APIConnect.Analysis.Extensions as aext
import Norconsult.PI.APIConnect.Helpers.Analysis as ahel

import Norconsult.PI.APIConnect.Modelling as mapi 
import Norconsult.PI.Common.API.Models.Modelling as mdto
import Norconsult.PI.APIConnect.Modelling.Extensions as mext
import Norconsult.PI.APIConnect.Helpers.Modelling as mhel

import Norconsult.PI.Common.API.Models.Common as cdto
import Norconsult.PI.APIConnect.Helpers as chel

import FEMDesign as fem
import Robot as robot
import FEMIntegrated as fi 

adto.__dict__['AdministrativeUnits'] = cdto.AdministrativeUnits
mdto.__dict__['AdministrativeUnits'] = cdto.AdministrativeUnits

#Set Routes 
mhel.RouteBuilder.RequestURI = 'https://pi-db-modelling.norconsult.com/api/modelling'
ahel.RouteBuilder.RequestURI = 'https://pi-db-analysis.norconsult.com/api/analysis'
chel.RouteBuilder.RequestURI = 'https://pi-db-common.norconsult.com/api/common'

#Apperently we have to import clr twice so add Norconsult namespace in clr
import clr

documentationPath = authPath = "C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Norconsult\\NorconsultPiPythonDocumentation\\README.html"
print('Welcome to PiPython!')
print('This is the main version of our package, which means all requests will be directed to our production database.')
print('If you need startup help, check out: https://norconsult365.sharepoint.com/sites/pamintegrated')
print()


def get_latest_version(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        latest_version = data["info"]["version"]
        return latest_version
    else:
        return None


def get_installed_version(package_name):
    try:
        version_number = version(package_name)
        return version_number
    except Exception as e:
        return None
    
if user_has_internet_connection:
    package_name = "NorconsultPiPythonProduction"
    installed_version = get_installed_version(package_name)
    latest_version = get_latest_version(package_name)

    if ((installed_version is not None) and (latest_version is not None)):
        if (installed_version != latest_version): 
            message = f"The most recent release of {package_name} is version {latest_version}. You are currently using version {installed_version}. To upgrade, execute the following command in terminal: pip install {package_name} --upgrade. If you use notebook you might have to restart the kernel."
            logging.warning(message)


