import json
import os
import re
from os.path import isdir, join, isfile,getctime
from datetime import datetime
metadata_file = "metadata.json"
logFolderName = "LOGS"
steps_key = "steps"
general_key = "general"
def isFolderAnEmbryo(embryoPath):
    """ Read the directory and subdirectories to determine by directory names if it's an embryo folder

    :param embryoPath: Folder to test
    :type embryoPath: str
    :return: True if folder is an embryo folder , False otherwise
    :rtype: bool

    """
    subfolders = [f for f in os.listdir(embryoPath) if os.path.isdir(join(embryoPath, f))]
    for folder in subfolders:
        if folder in ["RAWDATA","FUSE","SEG","POST","INTRAREG"]: #List of directories names to determine if it's an embryo folder
            return True
    return False

def getEXPFromParams(itemJson):
    """ Try to determine the experiment folder from the instance parameters , using the step

    :param itemJson: JSON object containing the experiment parameters and metadata
    :type itemJson: dict
    :return: Experiment folder name if found
    :rtype: str

    """
    if itemJson["step"] == "fusion":
        if "EXP_FUSE" in itemJson:
            return "FUSE_"+itemJson["EXP_FUSE"]
    if itemJson["step"] == "segmentation":
        if "EXP_SEG" in itemJson:
            return "SEG_"+itemJson["EXP_SEG"]
    if itemJson["step"] == "post_correction":
        if "EXP_POST" in itemJson:
            return "POST_"+itemJson["EXP_POST"]
    if itemJson["step"] == "embryo_properties" or itemJson["step"] == "intraregistration":
        if "EXP_INTRAREG" in itemJson:
            return "INTRAREG_"+itemJson["EXP_INTRAREG"]
    return ""

def loadSortedMetadata(embryoPath):
    """ Try to  read the metadata file from an embryo folder, sorted by date

    :param embryoPath: Path of the embryo folder to find metadata file
    :type embryoPath: str
    :return: Sorted metadata file
    :rtype: dict

    """
    jsonData = loadMetaData(embryoPath)
    if jsonData is None:
        print("No metadata was found for the embryo")
        return None
    if steps_key in jsonData:
        for jdata in jsonData[steps_key]:
            if not "date" in jdata:
                jdata["date"] = ""
    sortedByDateTEMP = sorted(jsonData[steps_key], key=lambda x: x["date"])
    return list(sortedByDateTEMP)

def is_float(string):
    """ Determine if a string is a float by trying to parse it

    :param string: string to test
    :type string: str
    :return: True if string is a float, False otherwise
    :rtype: bool

    """
    try:
        float(string)
        return True
    except ValueError:
        return False
def is_integer(string):
    """ Determine if a string is an integer by trying to parse it

    :param string: string to test
    :type string: str
    :return: True if string is an integer, False otherwise
    :rtype: bool

    """
    try:
        int(string)
        return True
    except ValueError:
        return False

def parseLogFileName(logFile):
    """ Parse a log file name given in parameter, to extract the command and the date of the process

    :param logFile: Name of the log file to parse
    :type logFile: str
    :return: ASTEC Command from the log file and date of the process
    :rtype: tuple

    """
    import re
    filename = logFile.split("/")[-1]
    if filename is not None:
        prefixName = filename
        astec_command = match_name_to_command(prefixName.split("-")[0].split(".")[0])
        print(prefixName.lower())
        x = re.search('^\d', prefixName.lower()) #Test if start by a digit
        if x!=None or prefixName.lower().startswith("x-"): # Some files start by x-
            astec_command = match_name_to_command(prefixName.split("-")[1].split(".")[0])
        found_date = None
        match = re.search(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}', prefixName)
        if match is not None:
            found_date = datetime.strptime(match.group(), '%Y-%m-%d-%H-%M-%S').strftime("%d/%m/%Y %H:%M:%S")
        return astec_command,found_date
    else:
        return None,None

def match_name_to_command(name):
    """ Taking the name of a file in parameter, try to match it with an Astec pipeline step by parsing it

    :param name:  Name of the file
    :type name: str
    :return: ASTEC Command found
    :rtype: str

    """
    command_lower = name.lower()
    if "property" in command_lower or "propertie" in command_lower:  # The mispelling is here to cover 2 cases
        return "astec_fusion"
    elif "intra" in command_lower:
        return "astec_intraregistration"
    elif "post" in command_lower:
        return "astec_postcorrection"
    elif "astec_astec" in command_lower or "seg" in command_lower:
        return "astec_astec"
    elif "mars" in command_lower:
        return "astec_mars"
    elif "fuse" in command_lower or "fusion" in command_lower:
        return "astec_fusion"
    return ""
def match_command_to_step(command):
    """ Using the ASTEC pipeline command given , try to determine the metadata step value corresponding

    :param command: ASTEC Command to be parsed
    :type command: str
    :return: Metadata step name
    :rtype: str

    """
    command_lower = command.lower()
    print(command_lower)
    if "property" in command_lower or "propertie" in command_lower:  # The mispelling is here to cover 2 cases
        return "embryo_properties"
    elif "intra" in command_lower:
        return "intraregistration"
    elif "post" in command_lower:
        return "post_correction"
    elif "astec_astec" in command_lower or "mars" in command_lower or "seg" in command_lower:
        return "segmentation"
    elif "fuse" in command_lower or "fusion" in command_lower:
        return "fusion"
    return ""


def parseHistoryFile(logFile):
    """ Try to parse the content the ASTEC history file and extract the packages used , the channel the packages are
    coming from , and the packages versions.

    :param logFile: Path to the ASTEC history file
    :type logFile: str
    :return: Packages used metadata for the file
    :rtype: dict

    """
    output = {}
    if logFile is not None and logFile != "":
        if os.path.isfile(logFile):
            f = open(logFile, "r")
            log_content = f.read()
            f.close()
            working_directory_line = None
            for idx, line in enumerate(log_content.split("\n")):
                if "conda version of package" in line.lower():
                    package_found = None
                    package_version = None
                    package_channel = None
                    splitted_line = line.split(" is ")
                    if len(splitted_line) > 1:
                        package_found = splitted_line[0].replace("# CONDA version of package ","")
                        version_split = splitted_line[1].split(" issued from channel ")
                        if len(version_split) > 0:
                            package_version = version_split[0]
                        if len(version_split) > 1:
                            package_channel = version_split[1]
                    if package_found is not None:
                        if package_version is not None:
                            output[package_found+"_version"]=package_version
                        if package_channel is not None:
                            output[package_found+"_channel"]=package_channel
    return output





def parseLogFile(filePath):
    """ Using a log file given in parameter, try to read metadata from its name and its content.

    :param filePath: Path to the log file
    :type filePath: str
    :return: metadata found in the file
    :rtype: dict

    """
    output = {}
    if not os.path.isfile(filePath):
        return None
    output["log_file"] = filePath
    astec_command,str_date = parseLogFileName(filePath) #try to parse astec pipeline command and date
    if astec_command is not None:
        output["step"] = match_command_to_step(astec_command) # extract step from the found command
    if str_date is not None:
        output["date"] = str_date
    f = open(filePath,"r")
    log_content = f.read()
    f.close()
    working_directory_line = None
    for idx,line in enumerate(log_content.split("\n")):
        strippedline = line.strip().replace(" ","")
        if strippedline != "\n":
            if "first_time_point" in strippedline: # parse first time point
                try:
                    if "=" in strippedline:
                        output["begin"] = int(strippedline.split("=")[-1])
                    else :
                        output["begin"] = int(strippedline.split("is")[-1])
                except:
                    a = 1
            if "last_time_point" in strippedline: # parse last time point
                try:
                    if "=" in strippedline:
                        output["end"] = int(strippedline.split("=")[-1])
                    else :
                        output["end"] = int(strippedline.split("is")[-1])
                except:
                    a = 1
            if "Totalexecutiontime" in strippedline: # found that the process has completed in a time , read this time
                output["process_time_seconds"] = int(strippedline.split("=")[-1].replace("sec","").split(".")[0])
                output["process_crashed"] = False
            if "embryo_nameis" in strippedline:# parse embryo name
                output["embryo_name"] = strippedline.split("is")[-1]
            if "workingdirectoryis":
                working_directory_line = idx
            if "sub_directory_suffix" in line and (working_directory_line is not None and idx > working_directory_line): # If we are reading working directory lines
                splittedSuffix = strippedline.split("=")[-1]
                dictkey = ""
                if output["step"] == "fusion":
                    dictkey = "EXP_FUSE"
                elif output["step"] == "segmentation":
                    dictkey = "EXP_SEG"
                elif output["step"] == "post_correction":
                    dictkey = "EXP_POST"
                elif output["step"] == "intraregistration" or output["step"] == "embryo_properties":
                    dictkey = "EXP_INTRAREG"
                output[dictkey] = splittedSuffix
            if "result_image_suffix" in strippedline:
                output["image_format"] = strippedline.split("=")[-1]
            if "result_lineage_suffix" in strippedline:
                output["lineage_format"] = strippedline.split("=")[-1]

    if not "process_crashed" in output:
        output["process_crashed"] = True

    return output


def isFileImage(fileName):
    """ Test is file is an image that can be read for metadata extraction (TODO : duplicate that should be fixed..).
    Image can be compressed too.

    :param fileName: Name of the file to test
    :type fileName: str
    :return: True if the file is an image , False otherwise
    :rtype: bool

    """
    return fileName is not None and (fileName.endswith(".mha") or fileName.endswith(".mha.gz") or fileName.endswith(".mha.tar.gz") or fileName.endswith(".nii") or fileName.endswith(".nii.gz") or fileName.endswith(".nii.tar.gz") or fileName.endswith(".inr") or fileName.endswith(".inr.gz") or fileName.endswith(".inr.tar.gz") or fileName.endswith(".tif") or fileName.endswith(".tif.gz") or fileName.endswith(".tif.tar.gz") or fileName.endswith(".tiff") or fileName.endswith(".tiff.gz") or fileName.endswith(".tiff.tar.gz"))

def parseDateFromLogPath(log_path):
    """ Using the name of the log path , try to extract the date by parsing it using found date format. (may be updated
    with new date formats).

    :param log_path: Name of the log file
    :type log_path: str
    :return: Date and time extracted formatted to string
    :rtype: str

    """
    match = re.search(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}', log_path)
    if match is not None:
        found_date = datetime.strptime(match.group(), '%Y-%m-%d-%H-%M-%S')
        return found_date.strftime("%d/%m/%Y %H:%M:%S")
    else:
        match = re.search(r'\d{4}-\d{2}-\d{2}-\d{2}:\d{2}:\d{2}', log_path)
        if match is not None:
            found_date = datetime.strptime(match.group(), '%Y-%m-%d-%H:%M:%S')
            return found_date.strftime("%d/%m/%Y %H:%M:%S")
        else:
            found_date = datetime.fromtimestamp(getctime(log_path))
            return found_date.strftime("%d/%m/%Y %H:%M:%S")

def FindLogForParameters(paramName,logFolder):
    """ Given a log file name , try to find a parameter file  and an history file in the same folder by the date. (log and params have the
    same dates in name).

    :param paramName: Name of the log file
    :type paramName: str
    :param logFolder: Folder of the log file to search for parameter file
    :type logFolder: str

    :return: Parameter file name if found, and history file name if found. None if not found
    :rtype: str

    """
    date = parseDateFromLogPath(paramName)
    logfiles = [join(logFolder, f) for f in os.listdir(logFolder) if
               os.path.isfile(join(logFolder, f)) and f.endswith(".log") and not "-history" in f]  # all params files
    historyfiles = [join(logFolder, f) for f in os.listdir(logFolder) if
               os.path.isfile(join(logFolder, f)) and f.endswith(".log") and "-history" in f]
    historyfile = None
    logfile = None
    if len(historyfiles) > 0:
        historyfile = historyfiles[0]
    for file in logfiles:
        datelog = parseDateFromLogPath(file)
        if datelog == date and logfile is None:
            logfile = file
    return logfile,historyfile

def load_data_from_files(path,embryo_suffix,embryo_suffix_2 = None):
    """ Using the list of images found a directory , try to extract metadata : date, time points and embryo name.
    This takes name suffix in parameters that can be found, and are used to parse the values.

    :param path: Path to the images folder
    :type path: str
    :param embryo_suffix: Suffix to find and split , that determine position of embryo name and time points
    :type embryo_suffix: str
    :param embryo_suffix_2: May need to use a second suffix if multi suffix (Default value = None)
    :type embryo_suffix_2: str
    :return: Dictionary of metadata extracted from files
    :rtype: dict

    """
    jsonObject = {}
    files = [f for f in os.listdir(path) if os.path.isfile(join(path, f)) and isFileImage(f)]
    begin = 1000000
    end = -1000000
    embryoName = ""
    fuseDate = None
    firstTimeFile = None
    for file in files: # Split name using step or other suffix to find embryo name
        if embryoName == "":
            if embryo_suffix in file:
                embryoName = file.split(embryo_suffix)[0]
            elif embryo_suffix_2 is not None:
                embryoName = file.split(embryo_suffix_2)[0]

        fileTimeSplit = file.split("_t") # Time is located after the _t , and before the extension of the image
        if len(fileTimeSplit) > 1:
            time = int(fileTimeSplit[1].split(".")[0])
            if time > end:
                end = time
            if time < begin:
                firstTimeFile = join(path, file)
                begin = time
    if firstTimeFile is not None: # Read the image created file timestamps from os
        fuseDate = datetime.fromtimestamp(getctime(firstTimeFile)).strftime("%d/%m/%Y %H:%M:%S")
        jsonObject["date"] = fuseDate
    jsonObject["begin"] = begin
    jsonObject["end"] = end
    jsonObject["embryo_name"] = embryoName
    jsonObject["loaded_from_images"]=True
    return jsonObject

def loadJsonForContour(postPath, postFolderName):# CODE DUPLICATE TODO LATER
    """ Parse the contour folder given in parameter to extract contour specific metadata

    :param postPath: Path to the folder of contour
    :type postPath: str
    :param postFolderName: Name of the folder
    :type postFolderName: str

    return: Dictionary of metadata extracted from contour folder
    :rtype: dict

    """

    jsonObjects = []
    fuseEXP = postFolderName.replace("CONTOUR_", "")
    jsonObject = load_data_from_files(postPath,"_contour_")
    jsonObject["step"] = "compute_contour"
    try : # Resolution is most of the time stored in the name of contour folder
        floatval = float("0."+fuseEXP.split("_")[-1])
        jsonObject["resolution"] = floatval
    except:
        a = 1
    jsonObject["EXP_CONTOUR"] = fuseEXP
    jsonObject["loaded_from_images"]=True
    jsonObjects.append(jsonObject)
    return jsonObjects
def loadJsonForBackground(postPath, postFolderName):# CODE DUPLICATE TODO LATER
    """ Parse the background folder given in parameter to extract background specific metadata

    :param postPath: Path to the folder of backgrounds
    :type postPath: str
    :param postFolderName: Name of the folder
    :type postFolderName: str

    return: Dictionary of metadata extracted from background folder
    :rtype: dict

    """
    from datetime import date
    jsonObjects = []
    fuseEXP = postFolderName.replace("BACKGROUND_", "").replace("Background_","")
    # read with image and name
    jsonObject = load_data_from_files(postPath,"_background_")
    jsonObject["step"] = "background"
    jsonObject["EXP_FUSE"] = fuseEXP
    jsonObject["loaded_from_images"]=True
    jsonObjects.append(jsonObject)
    return jsonObjects

def parseParamsAndLog(lastParameterFile,logFolder):
    """ This function load all the metadata possible from a parameter file. It compute the log and history files
    corresponding to the param file, and parse them.

    :param lastParameterFile: Path of the parameter file
    :type lastParameterFile: str
    :param logFolder: Folder containing the log files
    :type logFolder: str
    :return: Dictionary of metadata extracted from files
    :rtype: dict

    """
    jsonObject= {}
    jsonObject["loaded_from_images"]=False
    jsonObject["step_path"] = logFolder.replace("/LOGS/","").replace("/LOGS","") # Step folder is parent folder of LOGS input folder
    jsonObject["parameter_file"] = lastParameterFile
    correspondinglogfile,historyfile = FindLogForParameters(lastParameterFile, logFolder) # find log and history files for the same step
    if correspondinglogfile is not None:
        firstparams = parseLogFile(join(logFolder, correspondinglogfile)) # Parse metadata from the log file
        if firstparams is not None:
            for param in firstparams:
                jsonObject[param] = firstparams[param]
    if historyfile is not None:
        firstparams = parseHistoryFile(join(logFolder,historyfile))# Parse package version and names from the history file
        if firstparams is not None:
            for param in firstparams:
                jsonObject[param] = firstparams[param]
    astec_command, str_date = parseLogFileName(join(logFolder,lastParameterFile)) # extract astec step and date from names
    if not "step" in jsonObject and astec_command is not None:
        jsonObject["step"] = match_command_to_step(astec_command)
    if not "date" in jsonObject and str_date is not None:
        jsonObject["date"] = str_date
    if not "date" in jsonObject or jsonObject["date"] is None or jsonObject["date"] == "":
        jsonObject["date"] = parseDateFromLogPath(lastParameterFile)
    # jsonObject["date"] = datetime.fromtimestamp(getctime(lastParameterFile)).strftime("%d/%m/%Y %H:%M:%S")
    f = open(lastParameterFile, "r")
    linesfull = f.read()
    lines = linesfull.split("\n")
    f.close()
    for line in lines: # Read the parameter file and extract parameters
        shortline = line.strip().replace("\n", "").replace(" ", "")
        if not shortline.startswith("#") and shortline != "":
            keyval = shortline.split("=")
            if keyval[0] in ["PATH_EMBRYO"] or len(keyval) < 2:  # We dont want this line
                continue
            if keyval[0] == "EN":
                jsonObject["embryo_name"] = keyval[1]
            elif keyval[1] == "True" or keyval[1] == "False":  # If we find a bool
                jsonObject[keyval[0]] = bool(keyval[1])
            elif is_float(keyval[1]):  # If we find a float
                jsonObject[keyval[0]] = float(keyval[1])
            elif is_integer(keyval[1]):  # If we find a float
                jsonObject[keyval[0]] = int(keyval[1])
            else:  # If its string
                jsonObject[keyval[0]] = keyval[1].replace("'", "").replace('"', '')
    return jsonObject

def parseAllLogs(logFolder):
    """ Get all the python log and params files found from the logs folder , and parse them to get all instances metadata

    :param logFolder: Folder to find the files in
    :type logFolder: str
    :return: Dictionary of metadata extracted from logs folder and the flag to say if we found log or not
    :rtype: tuple

    """
    readImages = True
    jsonObjects = []
    pyfiles = [join(logFolder, f) for f in os.listdir(logFolder) if
               os.path.isfile(join(logFolder, f)) and f.endswith(".py")]  # all params files
    if len(pyfiles) > 0:
        pyfiles.sort(key=lambda x: getctime(x))
        readImages = False
        for lastParameterFile in pyfiles:
            jsondata = parseParamsAndLog(lastParameterFile, logFolder)
            jsonObjects.append(jsondata)
            print("---------")
    return jsonObjects,readImages

def parseLastLog(logFolder):
    """ Get the last  python log and params files found from the logs folder , and parse it to get instance metadata

    :param logFolder:  Folder to find the file in
    :type logFolder: str
    :return: Dictionary of metadata extracted from logs folder and the flag to say if we found log or not
    :rtype: tuple
    """
    readImages = True
    jsonObject = {}
    pyfiles = [join(logFolder, f) for f in os.listdir(logFolder) if
               os.path.isfile(join(logFolder, f)) and f.endswith(".py")]  # all params files
    if len(pyfiles) > 0:
        pyfiles.sort(key=lambda x: getctime(x))
        lastParameterFile = pyfiles[-1]
        jsonObject = parseParamsAndLog(lastParameterFile, logFolder)
    return jsonObject,readImages

def loadJsonForPost(postPath, postFolderName):# CODE DUPLICATE TODO LATER
    """ Parse the post folder given in parameter to extract post specific metadata (including logs folder)

    :param postPath: Path to the folder of post correction
    :type postPath: str
    :param postFolderName: Name of the folder
    :type postFolderName: str

    return: Dictionary of metadata extracted from post folder
    :rtype: dict

    """
    jsonObjects = []
    readImages = True
    fuseEXP = postFolderName.replace("POST_", "")
    logFolder = join(postPath, logFolderName)
    if isdir(logFolder):
        # read logs
        jsonObjectsTemp,readImages = parseAllLogs(logFolder)
        for jsonObj in jsonObjectsTemp:
            if not "EXP_POST" in jsonObj:
                jsonObj["EXP_POST"] = fuseEXP
            if not "step" in jsonObj or jsonObj["step"] is None or jsonObj["step"] == "":
                jsonObj["step"] = "post_correction"
            jsonObjects.append(jsonObj)
    if not isdir(logFolder) or readImages:
        # read with image and name
        jsonObject = load_data_from_files(postPath, "_post_")
        jsonObject["step"] = "post_correction"
        jsonObject["EXP_POST"] = fuseEXP
        jsonObjects.append(jsonObject)
    return jsonObjects

def loadJsonForSeg(segPath, segFolderName): # CODE DUPLICATE TODO LATER
    """ Parse the segmentation folder given in parameter to extract post specific metadata (including logs folder)

    :param segPath: Path to the folder of segmentation
    :type segPath: str
    :param segFolderName: Name of the folder
    :type segFolderName: str

    return: Dictionary of metadata extracted from segmentation folder
    :rtype: dict

    """
    jsonObjects = []
    readImages = True
    fuseEXP = segFolderName.replace("SEG_", "")
    logFolder = join(segPath, logFolderName)
    if isdir(logFolder):
        # read logs
        jsonObjectsTemp, readImages = parseAllLogs(logFolder)
        for jsonObj in jsonObjectsTemp:
            if not "EXP_SEG" in jsonObj:
                jsonObj["EXP_SEG"] = fuseEXP
            if not "step" in jsonObj or jsonObj["step"] is None or jsonObj["step"] == "":
                jsonObj["step"] = "segmentation"
            jsonObjects.append(jsonObj)
    if not isdir(logFolder) or readImages:
        jsonObject = load_data_from_files(segPath, "_seg_",embryo_suffix_2="_mars_")
        jsonObject["step"] = "segmentation"
        jsonObject["EXP_SEG"] = fuseEXP
        jsonObjects.append(jsonObject)
    return jsonObjects

def loadJsonFromIntraregLogs(intraregPath, intraregFolderName):# CODE DUPLICATE TODO LATER
    """ Read all the logs files from an intrareg folder , to compute metadata of all steps processed in the intrareg

    :param intraregPath: Path to the folder of intrareg
    :type intraregPath: str
    :param intraregFolderName: Name of the folder
    :type intraregFolderName: str

    return: Dictionary of metadata extracted from intrareg logs folder
    :rtype: dict

    """
    jsonObjects = []
    fuseEXP = intraregFolderName.replace("INTRAREG_", "")
    logFolder = join(intraregPath, logFolderName)
    if isdir(logFolder):
        # read logs
        jsonObjectsTemp, readImages = parseAllLogs(logFolder)
        for jsonObj in jsonObjectsTemp:
            if not "EXP_INTRAREG" in jsonObj:
                jsonObj["EXP_INTRAREG"] = fuseEXP
            if not "step" in jsonObj or jsonObj["step"] is None or jsonObj["step"] == "":
                jsonObj["step"] = "unknown_in_intraregistration"
            jsonObjects.append(jsonObj)
    return jsonObjects
def loadJsonForFuse(fusePath, fuseFolderName):# CODE DUPLICATE TODO LATER
    """ Parse the fusion folder given in parameter to extract post specific metadata (including logs folder)

    :param fusePath: Path to the folder of fusion
    :type fusePath: str
    :param fuseFolderName: Name of the folder
    :type fuseFolderName: str

    return: Dictionary of metadata extracted from fusion folder
    :rtype: dict

    """
    from datetime import date
    jsonObjects = []
    readImages = True
    fuseEXP = fuseFolderName.replace("FUSE_","")
    logFolder = join(fusePath,logFolderName)
    if isdir(logFolder):
        # read logs
        jsonObjectsTemp, readImages = parseAllLogs(logFolder)
        for jsonObj in jsonObjectsTemp:
            if not "EXP_FUSE" in jsonObj:
                jsonObj["EXP_FUSE"] = fuseEXP
            if not "step" in jsonObj or jsonObj["step"] is None or jsonObj["step"] == "":
                jsonObj["step"] = "fusion"
            jsonObjects.append(jsonObj)
    if not isdir(logFolder) or readImages:
        jsonObject = load_data_from_files(fusePath, "_fuse_")
        jsonObject["step"] = "fusion"
        jsonObject["EXP_FUSE"] = fuseEXP
        jsonObjects.append(jsonObject)
    return jsonObjects


def isEmpty(path):
    """ Test if the given folder exists and if it contains at least a file

    :param path: Path to the folder
    :type path: str
    :return: True if folder exists and is not empty, else False
    :rtype: bool

    """
    if os.path.exists(path) and not os.path.isfile(path):
        # Checking if the directory is empty or not
        if not os.listdir(path):
            return True
        else:
            return False
    return True
def loadJsonFromSubFolder(inputFolder):
    """ Taking an embryo folder in parameter, parse all the subfolders found to extract all metadatas for
    all instances that were run .

    :param inputFolder: Embryo folder path
    :type inputFolder: str
    :return: Dictionary of metadata extracted from embryo folder
    :rtype: dict

    """
    finalJsonList = []
    found_raw = False
    subdirs = [f for f in os.listdir(inputFolder) if os.path.isdir(join(inputFolder, f))]
    for subdir in subdirs:
        if subdir == "RAWDATA":
            if not isEmpty(join(inputFolder,subdir)):
                found_raw = True
        if subdir == "FUSE":
            fusesubdirs = [f for f in os.listdir(join(inputFolder, subdir)) if
                           os.path.isdir(join(join(inputFolder, subdir), f))]
            for fusesubdir in fusesubdirs:
                if fusesubdir.startswith("FUSE_"):
                    jsonvals = loadJsonForFuse(join(join(inputFolder, subdir), fusesubdir), fusesubdir)
                    for jsoninstance in jsonvals:
                        finalJsonList.append(jsoninstance)
        if subdir == "SEG":
            fusesubdirs = [f for f in os.listdir(join(inputFolder, subdir)) if
                           os.path.isdir(join(join(inputFolder, subdir), f))]
            for fusesubdir in fusesubdirs:
                if fusesubdir.startswith("SEG_"):
                    jsonvals = loadJsonForSeg(join(join(inputFolder, subdir), fusesubdir), fusesubdir)
                    for jsoninstance in jsonvals:
                        finalJsonList.append(jsoninstance)
        if subdir == "POST":
            fusesubdirs = [f for f in os.listdir(join(inputFolder, subdir)) if
                           os.path.isdir(join(join(inputFolder, subdir), f))]
            for fusesubdir in fusesubdirs:
                if fusesubdir.startswith("POST_"):
                    jsonvals = loadJsonForPost(join(join(inputFolder, subdir), fusesubdir), fusesubdir)
                    for jsoninstance in jsonvals:
                        finalJsonList.append(jsoninstance)
        if subdir == "BACKGROUND":
            fusesubdirs = [f for f in os.listdir(join(inputFolder, subdir)) if
                           os.path.isdir(join(join(inputFolder, subdir), f))]
            for fusesubdir in fusesubdirs:
                if fusesubdir.startswith("BACKGROUND_") or fusesubdir.startswith(
                        "Background_"):  # the 2 exist , should use lower but keep the 2 tests for clarity
                    jsonvals = loadJsonForBackground(join(join(inputFolder, subdir), fusesubdir), fusesubdir)
                    for jsoninstance in jsonvals:
                        finalJsonList.append(jsoninstance)
        if subdir == "CONTOUR":
            fusesubdirs = [f for f in os.listdir(join(inputFolder, subdir)) if
                           os.path.isdir(join(join(inputFolder, subdir), f))]
            for fusesubdir in fusesubdirs:
                if fusesubdir.startswith("CONTOUR_"):
                    jsonvals = loadJsonForContour(join(join(inputFolder, subdir), fusesubdir), fusesubdir)
                    for jsoninstance in jsonvals:
                        finalJsonList.append(jsoninstance)
        if subdir == "INTRAREG":
            fusesubdirs = [f for f in os.listdir(join(inputFolder, subdir)) if
                           os.path.isdir(join(join(inputFolder, subdir), f))]
            for fusesubdir in fusesubdirs:
                if fusesubdir.startswith("INTRAREG_"):
                    jsonvals = loadJsonFromIntraregLogs(join(join(inputFolder, subdir), fusesubdir), fusesubdir)
                    for jsoninstance in jsonvals:
                        finalJsonList.append(jsoninstance)
                    #jsonvals = loadJsonFromSubFolder(join(join(inputFolder, subdir), fusesubdir))
                    #for jsoninstance in jsonvals:
                    #    finalJsonList.append(jsoninstance)
    for json_instance in finalJsonList:
        json_instance["raw_found"] = found_raw
    return finalJsonList

def createMetadataFromFolder(embryoPath):
    """ If found an embryo folder that does not contain metadata , this functions creates an empty  metadata file inside

    :param embryoPath: Path to the embryo folder
    :type embryoPath: str

    """
    empty_json = {general_key:{},steps_key:[]}
    if isFolderAnEmbryo(embryoPath):
        empty_json[steps_key] = loadJsonFromSubFolder(embryoPath)
        with open(join(embryoPath,metadata_file), 'w+') as openJson:
            json.dump(empty_json, openJson)
def getMetaDataFile():
    """Return the used name for metadata files in AstecManager


    :returns: name of the file

    """
    return metadata_file


def loadMetaData(embryoPath):
    """Using an embryo path , this function load the metadata file corresponding to the embryo , and returns it

    :param embryoPath: string, path to the embryo folder
    :returns: list of dicts , the content of the json metadatas  , or None if it doesn't exist

    """
    if not isdir(embryoPath):
        print(" ! Embryo path not found !")
        return None

    jsonMetaData = join(embryoPath, getMetaDataFile())
    if not isfile(jsonMetaData):
        print(" ! Embryo metadata file not existing !")
        return None
    with open(jsonMetaData, 'r') as openJson:
        jsonObject = json.load(openJson)
    return jsonObject


def createMetaDataFile(embryoPath):
    """ Create an empty metadata file in embryo folder

    :param embryoPath: Embryo folder path
    :type embryoPath: str
    :returns: True if created, False otherwise
    :rtype: bool

    """
    empty_metadata = {general_key:{},steps_key:[]}
    if not isdir(embryoPath):
        os.makedirs(embryoPath)
    if not isfile(join(embryoPath, getMetaDataFile())):
        with open(join(embryoPath, getMetaDataFile()), "w+") as outfile:
            json.dump(empty_metadata, outfile)
            return True
    return False


def writeMetaData(embryoPath, jsonDict):
    """Using an embryo path , this function write the content of the given json dict to the metadata f
    ile corresponding to the embryo

    :param embryoPath: string, path to the embryo folder
    :type embryoPath: str
    :param jsonDict: dict, data to write (overwrite the content)
    :type jsonDict: dict

    """
    jsonMetaData = join(embryoPath, getMetaDataFile())
    if not isdir(embryoPath) or not isfile(jsonMetaData):
        createMetaDataFile(embryoPath)

    jsonMetaData = join(embryoPath, getMetaDataFile())

    with open(jsonMetaData, 'w') as openJson:
        json.dump(jsonDict, openJson)

def AddMultiToMetadata(embryoPath,dict,output_path=None):
    """ Write multiple metadatas given by a dictionary to an embryo folder. If no metadata file is found , create it.

    :param embryoPath: Path to the embryo folder
    :type embryoPath: str
    :param dict: List of metadata by key value
    :type dict: dict
    :param output_path: If not None, write the metadata file to the given path (Default value = None)
    :type output_path: str

    """
    jsonObjects = loadMetaData(embryoPath)
    if output_path is None:
        output_path = embryoPath
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    for key in dict:
        if not key in jsonObjects["general"]:
            jsonObjects["general"][key] = dict[key]
        writeMetaData(output_path,jsonObjects)
def convert_metadata_to_new_format(embryoPath,embryo_name,output_path=None):
    """ Metadata format has changed during development. This function converts metadata from an embryo if in the wrong
    format.

    :param embryoPath: Path to the embryo folder
    :type embryoPath: str
    :param embryo_name: Name of the embryo
    :type embryo_name: str
    :param output_path: If not None, write the metadata file to the specified folder (Default value = None)
    :type output_path: str

    """
    jsonObjects = loadMetaData(embryoPath)
    if output_path is None:
        output_path = embryoPath
    print("Converting "+str(embryoPath)+" to : "+output_path)
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    if "general" in jsonObjects:
        return jsonObjects
    else :
        min_embryo = 10000
        max_embryo = -10000
        for json_instance in jsonObjects:
            if "begin" in json_instance:
                if json_instance["begin"] < min_embryo:
                    min_embryo = json_instance["begin"]
            if "end" in json_instance:
                if json_instance["end"]> max_embryo:
                    max_embryo = json_instance["end"]
        jsonobj = {"general":{"embryo_name":embryo_name},"steps":jsonObjects}
        if min_embryo < 10000:
            if not "begin" in jsonobj["general"]:
                jsonobj["general"]["begin"] = min_embryo
        if max_embryo > -10000:
            if not "end" in jsonobj["general"]:
                jsonobj["general"]["end"] = max_embryo
        writeMetaData(output_path,jsonobj)
    return

def load_csv_python(csv_path):
    """ Function used to parse the csv file coming from Mattermost to be able to extract metadata

    :param csv_path: Path to the mattermost exported csv file
    :type csv_path: str
    :returns: dict of dicts , the content of the mattermost metadatas by embryo name
    :rtype: dict

    """
    import csv
    embryos = {}
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            embryo = {}
            for key in row:
                if key != "Name":
                    embryo[key] = row[key]
            embryos[row['Name']] = embryo
    return embryos
def convert_all_metadatas(data_path,output_path=None):
    """ Using the path to a folder containing embryo folders, convert all of the metadata found that are in the old format

    :param data_path: Path to the folder ocntaining embryos folder
    :type data_path: str
    :param output_path: If not None, write each metadata to a specific folder (Default value = None)
    :type output_path: str

    """
    embryos = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path,f)) and os.path.isfile(os.path.join(os.path.join(data_path,f),metadata_file))]
    for embryo_name in embryos:
        convert_metadata_to_new_format(os.path.join(data_path,embryo_name),embryo_name,output_path=os.path.join(output_path,embryo_name))

def addDictToMetadata(embryoPath, jsonDict, addDate=True,logFolder=None):
    """Add a dict to the json metadata file

    :param embryoPath: string, path to the embryo folder
    :param jsonDict: dict, dict to add to the metadata
    :param addDate: boolean,  if True, a new key is added to the dict , corresponding to now's date (Default value = True)
    :param logFolder:  (Default value = None)
    :returns: bool , True if the dict was added to the json metadata , False otherwise

    """
    if jsonDict is None:
        print("! Input json dict is None , can not add it to file")
        return False

    if type(jsonDict) is not dict:
        print(" ! input json is not a dictionary ! ")
        return False
    json_copy = {}
    for key in jsonDict:
        json_copy[key] = jsonDict[key]
    jsonMetadata = loadMetaData(embryoPath)
    if jsonMetadata is None:
        createMetaDataFile(embryoPath)
        jsonMetadata = {general_key:{},steps_key:[]}

    if logFolder is not None:
        logJson,readimages = parseLastLog(logFolder)
        for keyJson in logJson:
            print(str(keyJson))
            json_copy[keyJson] = logJson[keyJson]
    if addDate and not "date" in json_copy:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        json_copy["date"] = now
    jsonMetadata[steps_key].append(json_copy)
    writeMetaData(embryoPath, jsonMetadata)
