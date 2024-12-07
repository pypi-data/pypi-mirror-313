import os 
from serverPaths import getServerPaths
import shutil
import glob

def copyAllFiles(): 
    try: 
        serverPaths = getServerPaths()
    except Exception as e:
        raise e 

    destinationFolder = "C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Norconsult\\NorconsultPiPythonProduction\\"
    destinationFolderAuth =  "C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Norconsult\\NorconsultPiPython_auth\\"

    if not os.path.exists(destinationFolder):
        os.makedirs(destinationFolder)
        
    if not os.path.exists(destinationFolderAuth):
        os.makedirs(destinationFolderAuth)
        
    try:
        analysisPath = serverPaths["Analysis"]
        modellingPath = serverPaths["Modelling"]
        modelBuilderFEMPath = serverPaths['ModelBuilder_FEM']
        modelBuilderRobotPath = serverPaths["ModelBuilder_Robot"]
        auth_python_Path = serverPaths["auth_python"]
        stubsPath = serverPaths["stubs"]
        femIntegratedPath = serverPaths["FemIntegrated"]
    except Exception as e: 
        raise e
    
    filesToCopyAnalysis = os.listdir(analysisPath)
    filesToCopyModelling = os.listdir(modellingPath)
    filesToCopyFEM = os.listdir(modelBuilderFEMPath)
    filesToCopyRobot = os.listdir(modelBuilderRobotPath)
    filesToCopy_auth_python = os.listdir(auth_python_Path)
    filesToCopyStubs = os.listdir(stubsPath)
    filesToCopyFemIntegrated = os.listdir(femIntegratedPath)

    
    directoryPiPython = os.path.dirname(os.path.abspath(__file__))
    #check for multiple stubs file in the folder (in case we change the name of the stub file) and select the newest
    if len(filesToCopyStubs) > 0: 
        # get all files in the folder that end with '.pyi'
        files = glob.glob(os.path.join(stubsPath, '*.pyi'))
        # sort the files by creation time and get the newest one
        stubsFileToCopy = max(files, key=os.path.getctime)
        stubsFileDestination = os.path.join(directoryPiPython, "init.pyi")
        shutil.copy2(stubsFileToCopy, stubsFileDestination)
    else: 
        print("Unable to find a stub file for copying. This may result in outdated or missing code-help and IntelliSense.")

    for file in filesToCopyFemIntegrated: 
        if requiresUpdate(femIntegratedPath + file, destinationFolder + file): 
            shutil.copyfile(femIntegratedPath + file, destinationFolder + file)
            
    for file in filesToCopyFEM: 
        if requiresUpdate(modelBuilderFEMPath + file, destinationFolder + file): 
            shutil.copyfile(modelBuilderFEMPath + file, destinationFolder + file)
                
    for file in filesToCopyRobot: 
        if requiresUpdate(modelBuilderRobotPath + file, destinationFolder + file): 
            shutil.copyfile(modelBuilderRobotPath + file, destinationFolder + file)
    
    for file in filesToCopy_auth_python:
        if requiresUpdate(auth_python_Path + file, destinationFolderAuth + file):
            shutil.copyfile(auth_python_Path + file, destinationFolderAuth + file)
    

    for file in filesToCopyAnalysis: 
        if requiresUpdate(analysisPath + file, destinationFolder + file): 
            shutil.copyfile(analysisPath + file, destinationFolder + file)
            
    for file in filesToCopyModelling: 
        if requiresUpdate(modellingPath + file, destinationFolder + file): 
            shutil.copyfile(modellingPath + file, destinationFolder + file)


def requiresUpdate(serverFilePath, destFilePath):
    if not os.path.isfile(destFilePath): 
        return True 
    
    serverFilePathCreatedDate = os.path.getmtime(serverFilePath)
    destFilePathCreatedDate = os.path.getmtime(destFilePath)
    if serverFilePathCreatedDate >  destFilePathCreatedDate: 
        return True

    return False