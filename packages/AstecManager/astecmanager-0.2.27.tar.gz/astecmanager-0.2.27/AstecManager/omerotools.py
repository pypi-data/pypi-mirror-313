import subprocess

import omero
import ezomero
import os
import numpy as np
from os.path import join,isfile
from threading import Thread
from multiprocessing import cpu_count

def run_command(command):
    """Run a command in a subprocess

    :param command: the command to run
    :type command: str
    
    """
    splitted = command.split(" ")
    subcommand = []
    for s in splitted:
        subcommand.append(s.replace('"',''))
    subprocess.run(subcommand)

def is_image(file_name):
    """Test if file is an image and not compressed

    :param file_name: name of the image file
    :type file_name: string

    
    """
    splited_name = file_name.split('.')
    return not ".bak" in file_name and splited_name[1] is not None and splited_name[1] in ['mha','nii','inr']

class process_upload_image(Thread):
    """Thread processing the upload of an image to dataset on  OMERO , if doesn't exist."""
    def __init__(self, dataset_id,image_path,omeroinstance):
        super(process_upload_image, self).__init__()
        self.image_path = image_path
        self.dataset_id = dataset_id
        self.omeroinstance = omeroinstance

    def run(self):
        """ """

        tries = 0
        final_image_name = self.image_path.split("/")[-1]
        image_name_list = self.omeroinstance.get_images_filename(self.dataset_id)
        found_image = (final_image_name in image_name_list)
        while tries < 3:
            if not found_image:
                self.omeroinstance.add_image_to_dataset_java(self.image_path,self.dataset_id)
                image_name_list = self.omeroinstance.get_images_filename(self.dataset_id)
                found_image = (final_image_name in image_name_list)
            tries += 1

class process_upload_annotation_file(Thread):
    """Thread processing the upload of a file to OMERO dataset attachment , if doesn't exist."""
    def __init__(self, dataset_id,file_path,omeroinstance):
        super(process_upload_annotation_file,self).__init__()
        self.image_path = file_path
        self.dataset_id = dataset_id
        self.omeroinstance = omeroinstance

    def run(self):
        """ """
        self.omeroinstance.add_file_to_dataset(self.dataset_id,self.image_path)

class process_download(Thread):
    """Thread processing the download of an image file from OMERO dataset."""
    def __init__(self, folder_out, image_id, omeroinstance):
        super(process_download, self).__init__()
        self.folder_out = folder_out
        self.image_id = image_id
        self.omeroinstance = omeroinstance

    def run(self):
        """ """
        tries = 0
        found_image = False
        self.image_name_compress = self.omeroinstance.get_image_object(self.image_id).getName()
        self.image_name = join(self.folder_out, self.image_name_compress.replace(".gz", ""))
        if isfile(self.image_name):
            print(" --> already download " + self.image_name)
        else:
            while tries < 3:
                if not found_image:
                    self.omeroinstance.export_image(self.image_id, self.image_name)
                    found_image = isfile(self.image_name)
                tries += 1

def parse_parameters_file(filename):
    """Parse file lines  in the OMERO authentication file . The file is composed of 1 line by parameter, with the value separated by a "="

    :param filename: path to the omero authentication file
    :type filename: string

    
    """
    result = {}
    try:
        f = open(filename, "r+")
    except:
        print("Unable to open file" + str(filename))
        return None
    else:
        lines = f.readlines()
        for line in lines:
            if line != "" and line != "\n" and not line.startswith("#"):
                tab = line.replace("\n", "").split("=")
                result[tab[0]] = tab[1]
        f.close()
    return result

class connect:
    """Class containing the different functions to communicate with an OMERO instance. The class auto connect at creation"""
    def __init__(self, login=None, passwd=None, server=None, port=None, group=None, secure=False,file_path=None):
        if file_path is None:
            self.params_connect(login,passwd,server,port,group)
        else :
            self.file_connect(file_path)

    def params_connect(self,login=None, passwd=None, server=None, port=None, group=None, secure=False):
        """Bind omero communication parameters using parameters and connect to omero instance

        :param login: User login on OMERO (Default value = None)
        :type login: string
        :param passwd: User password on OMERO  (Default value = None)
        :type passwd: string
        :param server: OMERO server instance (Default value = None)
        :type server: string
        :param port: OMERO instance communication port (Default value = None)
        :type port: int
        :param group: Working group in OMERO (Default value = None)
        :type group: string
        :param secure: Secure connection communication (Default value = False)
        :type secure: bool

        
        """
        if login is not None:
            self.login = login

        self.secure = False
        if secure is not None:
            self.secure = secure

        if passwd is not None:
            self.o_passwd = passwd

        if server is not None:
            self.server = server

        if port is not None:
            self.port = port

        if group is not None:
            self.group = group

        self.omero_cmd="omero"

        self.connection = None
        self.connected = False
        self.o_connect()

    def file_connect(self,file_path):
        """Bind omero communication parameters using the content of an OMERO authentication file

        :param file_path: Path to the omero authentication file
        :type file_path: string

        
        """
        parameters = parse_parameters_file(file_path)

        self.login = ""
        if parameters['login'] is not None:
            self.login = parameters['login']
        self.secure = False
        if parameters['secure'] is not None:
            self.secure = bool(parameters['secure'])
        self.o_passwd = ""
        if parameters['password'] is not None:
            self.o_passwd = parameters['password']
        self.server = ""
        if parameters['host'] is not None:
            self.server = parameters['host']
        self.port = -1
        if parameters['port'] is not None:
            self.port = int(parameters['port'])
        self.group = ""
        if parameters['group'] is not None:
            self.group = parameters['group']
        self.omero_cmd = "omero"

        self.connection = None
        self.connected = False
        self.o_connect()

    def o_connect(self):
        """Try to connect to OMERO instance using parameters stored"""
        self.connection = ezomero.connect(user=self.login, group=self.group, password=self.o_passwd, host=self.server,
                                          port=self.port, secure=self.secure)
        if self.connection is None:
            self.connected = False
        else:
            self.connected = True
            #self.connection.c.enableKeepAlive(60)
            #self.connection.keepAlive()
        return self.connected

    def o_reconnect(self):
        """Renew connection if failed"""
        self.connected = False
        try:
            self.connection.connect()
            self.connected = True
        except Exception as e:
            print("ERROR during omero connection " + str(e))
            raise e
        return self.connection

    def o_close(self):
        """ """
        if self.connection is not None:
            self.connected = False
            self.connection.close()



    def download_omero_set(self, project_name, dataset_name, folder_output):
        """Download a dataset from OMERO using the project name and dataset name. The download is processed
        3 images by 3 images in threads.

        :param project_name: Name of the project containing the dataset on OMERO
        :type project_name: string
        :param dataset_name: Name of the dataset to download on OMERO
        :type dataset_name: string
        :param folder_output: Path to the folder where images and files will be stored on disk
        :type folder_output: string

        
        """
        cpuCount = cpu_count()
        maxNumberOfThreads =3
        threads = []
        found = False
        found_path = False
        run_command("mkdir " + str(folder_output).replace('"','').replace(",",""))
        for p in self.list_projects():
            if not found and p.getName().lower() == project_name.lower():
                found = True
                for path in p.listChildren():
                    if not found_path and path.getName().lower() == dataset_name.lower():
                        found_path = True
                        list_files = self.get_images_ids(path.getId())
                        for image in list_files:
                            if len(threads) >= maxNumberOfThreads:  # Waitfor a free process if too much threads
                                tc = threads.pop(0)
                                tc.join()
                            tc = process_download(folder_output.replace('"','').replace(",",""), image, self)
                            tc.start()
                            threads.append(tc)
                        while len(threads) > 0:
                            tc = threads.pop(0)
                            tc.join()

    def download_omero_set_by_id(self, dataset_id, folder_output):
        """Download a dataset from OMERO using the dataset id. The download is processed
        3 images by 3 images in threads

        :param dataset_id: ID of the dataset to download on OMERO
        :type dataset_id: string
        :param folder_output: Path to the folder where images and files will be stored on disk
        :type folder_output: string

        
        """
        maxNumberOfThreads =3
        threads = []
        run_command("mkdir " + str(folder_output).replace('"','').replace(",",""))
        list_files = self.get_images_ids(dataset_id)
        for image in list_files:
            if len(threads) >= maxNumberOfThreads:  # Waitfor a free process if too much threads
                tc = threads.pop(0)
                tc.join()
            tc = process_download(folder_output.replace('"','').replace(",",""), image, self)
            tc.start()
            threads.append(tc)
        while len(threads) > 0:
            tc = threads.pop(0)
            tc.join()

    def upload_omero_set(self,project_name,dataset_name,input_folder,mintime=None,maxtime=None,tag_list=None,include_logs=False):
        """Upload the content of a folder (image files and non image files) to a OMERO dataset given by name , in project given by name
        Bind key value pair of the dataset for minTime if mintime is not None, same for maxTime.
        If tag_list if not None, add the tags to the dataset. If include_logs is True , upload content of the LOGS folder to attachments

        :param project_name: Name of the project where dataset will be uploaded (created if does not exist)
        :type project_name: string
        :param dataset_name: Name of the dataset where images and files will be uploaded (created if does not exist)
        :type dataset_name: string
        :param input_folder: Path to the folder containing images and files on disk
        :type input_folder: string
        :param mintime:  (Default value = None) Value of dataset min time point in images , for OMERO metadata
        :type mintime: int
        :param maxtime:  (Default value = None) Value of dataset max time point in images , for OMERO metadata
        :type maxtime: int
        :param tag_list:  (Default value = None) List of tags to be added to OMERO metadata
        :type tag_list: list of strings
        :param include_logs:  (Default value = False) If True, content of "LOGS" folder will be uploaded to attachments
        :type include_logs: boolean

        
        """
        cpuCount = cpu_count()
        maxNumberOfThreads = 3
        imagefiles = [f for f in os.listdir(input_folder) if
                      isfile(join(input_folder, f)) and is_image(f) and not ".mha" in f]
        logfiles = []
        if os.path.isdir(os.path.join(input_folder,"LOGS")):
            logfiles = [f for f in os.listdir(os.path.join(input_folder,"LOGS")) if
                          isfile(join(join(input_folder,"LOGS"), f)) and not f.lower() == ".ds_store"]
        nonimagefiles = [f for f in os.listdir(input_folder) if
                         isfile(join(input_folder, f)) and not is_image(f) and not ".mha" in f and not f.lower() == ".ds_store"]

        embryolist = self.list_projects()
        dataset = None
        project = None
        if embryolist is not None:
            for o_emb in embryolist:
                if o_emb.getName()==project_name:
                    project = o_emb
                    for path in self.get_datasets(o_emb.getid()):
                        if path.getName() == dataset_name:
                            dataset = path

        if project is None:
            # create it
            project_id = self.create_project(project_name)
            # store in project
            project = self.get_project_by_id(project_id)
        else:
            project_id = project.getId()
        # find dataset id
        if dataset is None:
            print("Didn't find dataset with name : "+str(dataset_name))
            dataset_id = self.create_dataset(dataset_name, project_id=project_id)
            dataset = self.get_dataset_by_id(dataset_id)
        else :
            dataset_id = dataset.getId()
        # if doesnt exist , create it
        # for each image
        # start thread and upload image

        image_name_list = self.get_images_filename(dataset_id)

        threads = []
        for image_f in imagefiles:
            if len(threads) >= maxNumberOfThreads:  # Waitfor a free process if too much threads
                tc = threads.pop(0)
                tc.join()
            if not image_f in image_name_list:
                tc = process_upload_image(dataset_id, os.path.join(input_folder, image_f), self)
                tc.start()
                threads.append(tc)
        while len(threads) > 0:
            tc = threads.pop(0)
            tc.join()

        already_existing_files = self.list_files(dataset)
        # for each non image
        # start thread and upload it like attachment
        threads = []
        maxNumberOfThreads = 1
        print(nonimagefiles)
        for file_f in nonimagefiles:
            if len(threads) >= maxNumberOfThreads:  # Waitfor a free process if too much threads
                tc = threads.pop(0)
                tc.join()
            if not file_f in already_existing_files:
                tc = process_upload_annotation_file(dataset_id, os.path.join(input_folder, file_f), self)
                tc.start()
                threads.append(tc)
        while len(threads) > 0:
            tc = threads.pop(0)
            tc.join()
        if include_logs:
            print(logfiles)
            threads = []
            for file_f in logfiles:
                print("Upload non image log : " + str(os.path.join(input_folder, file_f)))
                if len(threads) >= maxNumberOfThreads:  # Waitfor a free process if too much threads
                    tc = threads.pop(0)
                    tc.join()
                if not file_f in already_existing_files:
                    tc = process_upload_annotation_file(dataset_id, os.path.join(os.path.join(input_folder,"LOGS"), file_f), self)
                    tc.start()
                    threads.append(tc)
            while len(threads) > 0:
                tc = threads.pop(0)
                tc.join()

        # add KVP minTime
        if maxtime is not None:
            if not self.has_kvp(project, "maxTime", int(maxtime)):
                self.add_kvp(project, "maxTime", int(maxtime))
        # add KVP maxTime
        if maxtime is not None:
            if not self.has_kvp(project, "minTime", int(mintime)):
                self.add_kvp(project, "minTime", int(mintime))
        if tag_list is not None:
            for tag in tag_list:
                self.add_tag(project,tag)
    def get_images_ids(self, dataset_id):
        """Retrive list of image ids associated to the dataset_id

        :param dataset_id: id of the dataset in omero to get images and files from
        :type dataset_id: int

        
        """
        return ezomero.get_image_ids(self.connection, dataset=dataset_id)

    def get_image_object(self, image_id):
        """retrieve OMERO image object for the given image_id

        :param image_id: id of the image in omero to retrieve image object for
        :type image_id: int

        
        """
        image_obj, pixels = ezomero.get_image(self.connection, image_id, no_pixels=True)
        return image_obj

    def get_image_data(self, image_id):
        """Retrieve pixels for the given image id

        :param image_id: id of the image in omero to get pixels for
        :type image_id: int

        
        """
        image_obj, pixels = ezomero.get_image(self.connection, image_id, dim_order="xyztc")
        return pixels

    def add_file_to_project(self, project_name, filepath):
        """Add the file from path to the project given by its name as an annotation
        
        :param project_name: name of the project to add the file to
        :type project_name: str
        :param filepath: path of the file to add
        :type filepath: str


        """
        project = self.get_project_by_name(project_name)
        if project is not None:
            project_id = project.getId()
            namespace = omero.constants.metadata.NSCLIENTMAPANNOTATION
            ezomero.post_file_annotation(self.connection, "Project", project_id, filepath, namespace)

    def add_file_to_dataset(self, dataset_id, file):
        """Add the file from path to the dataset given by its id as an annotation

        :param dataset_id: ID of the dataset in omero to add the annotation file to
        :type dataset_id: int
        :param file: Path of the file on the disk
        :type file: str

        
        """
        print("Post : "+str(file)+" to dataset id "+str(dataset_id))
        namespace = omero.constants.metadata.NSCLIENTMAPANNOTATION
        ezomero.post_file_annotation(self.connection, "Dataset", dataset_id, file, namespace)

    def add_image_to_dataset_java(self, image_path, dataset_id):
        """Upload image using path to a dataset by its id , through Java Omero Lib (jar)

        :param image_path: Path of the image on the disk
        :type image_path: str
        :param dataset_id: ID of the dataset in omero to add the image file to
        :type dataset_id: int

        
        """
        #First Login
        run_command(self.omero_cmd + ' -s ' + self.server + ' -u ' + self.login + ' -w ' + self.o_passwd + ' login')
        return run_command(
            self.omero_cmd  + ' import --skip minmax --skip thumbnails --skip upgrade -d ' + str(
                dataset_id) + ' ' + image_path)

    def add_image_to_dataset_cli(self, image_path, dataset_id):
        """Upload image using path to a dataset by its id , through the cli command interface

        :param image_path: Path of the image on the disk
        :type image_path: str
        :param dataset_id: ID of the dataset in omero to add the image file to
        :type dataset_id: int

        
        """
        from omero.cli import CLI
        args = ["login"]
        args += ["-s",self.server]
        args += ["-u", self.login]
        args += ["-w",self.o_passwd]
        cli = CLI()
        cli.load_plugins()
        cli.invoke(args)
        # First Login
        #run_command(self.omero_cmd + ' -s ' + self.server + ' -u ' + self.login + ' -w ' + self.o_passwd + ' login')
        args = ["import"]
        args += ["--skip","minmax"]
        args += ["--skip","thumbnails"]
        args += ["--skip","upgrade"]
        args += ["-d", dataset_id]
        args += [image_path]
        cliupload = CLI()
        cliupload.load_plugins()
        cliupload.invoke(args)
        #return run_command(
        #    self.omero_cmd + ' import --skip minmax --skip thumbnails --skip upgrade -d ' + str(
        #        dataset_id) + ' ' + image_path)
    def imread(self, filename, verbose=True):
        """Reads an image file completely into memory

        ::param filename: Path on disk of the image to load in memory
        :type filename: str
        :param verbose:  (Default value = True) Print read to console or not
        :type verbose: bool
        :return: The image file content as a numpy array
        :rtype: ndarray

        """
        if verbose:
            print(" --> Read " + filename)
        if filename.find('.inr') > 0 or filename.find('mha') > 0:
            # from morphonet.ImageHandling import SpatialImage
            from morphonet.ImageHandling import imread as imreadINR
            data = imreadINR(filename)
            return np.array(data)
        elif filename.find('.nii') > 0:
            from nibabel import load as loadnii
            im_nifti = loadnii(filename)
            return np.array(im_nifti.dataobj).astype(np.dtype(str(im_nifti.get_data_dtype())))
        else:
            from skimage.io import imread as imreadTIFF
            return imreadTIFF(filename)
        return None

    def add_image_to_dataset_ezomero(self, image_path, dataset_id, source_image_id=None):
        """Upload image using path to a dataset by its id , through EZOmero python library. Copy existing image if source_image_id param is not None

        :param image_path: Path to the image on the disk
        :type image_path: str
        :param dataset_id: ID of the dataset in omero to add the image file to
        :type dataset_id: int
        :param source_image_id:  (Default value = None) ID of a source image data to be duplicated (unclear)
        :type source_image_id: int

        
        """
        image_np = np.asarray(self.imread(image_path))
        if source_image_id is not None:
            ezomero.post_image(self.connection, image_np, image_path.split('/')[-1], dataset_id=dataset_id)
        else:
            ezomero.post_image(self.connection, image_np, image_path.split('/')[-1], dataset_id=dataset_id, source_image_id=source_image_id)

    def add_image_to_dataset(self, image_path, dataset_id, source_image_id=None):
        """Upload image using path to a dataset by its id. Copy existing image if source_image_id param is not None
         NOTE : this function is just a bridge to ezomero upload, but it should be kept in case we change the system

        :param image_path: Path to the image on the disk
        :type image_path: str
        :param dataset_id: ID of the dataset in omero to add the image file to
        :type dataset_id: int
        :param source_image_id:  (Default value = None) ID of a source image data to be duplicated (unclear)
        :type source_image_id: int

        
        """
        if self.omero_cmd == "" or self.omero_cmd is None:
            self.add_image_to_dataset_ezomero(image_path,dataset_id)
        else :
            self.add_image_to_dataset_java(image_path, dataset_id)

    def export_image_with_java(self, image_id, path_image):
        """Download image by it's ID to a path , using Java Omero Library (jar)

        :param image_id: id of the image in omero to download on disk
        :type image_id: int
        :param path_image: path where to store the image to (including image name)
        :type path_image: string

        
        """
        # print("export_image_with_java lien Download "+str(Imageid))
        cmd = self.omero_cmd+' -s ' + self.server + ' -u ' + self.login + ' -w ' + self.o_passwd + ' -p ' + str(
            self.port) + ' download Image:' + str(image_id) + ' "' + os.path.dirname(os.path.abspath(path_image))+'"'
        run_command(cmd)
        if not os.path.isfile(path_image):
            print("--> ERROR Omero Import ID " + str(image_id))
            return False
        return True


    def export_image(self, image_id, path_image):
        """Download image by it's ID to a path

        :param image_id: id of the image in omero to download on disk
        :type image_id: int
        :param path_image: path where to store the image to (including image name)
        :type path_image: string

        
        """
        # print(" export_image"+str(Imageid))
        java_succes = self.export_image_with_java(image_id, path_image)
        if java_succes:
            return True
        else:
            print("---> Unable to use java command to download image")
            return False
            print("---> trying using ezomero")
            self.save_image_to_file_ezomero(image_id, path_image)

    def imsave(self, filename, img):
        """Save a numpyarray as an image to filename.

        :param filename: Path on disk to save the image to
        :type filename: string
        :param img: Image content to be saved
        :type img: ndarray

        """

        if filename.find('.inr') > 0 or filename.find('mha') > 0:
            from morphonet.ImageHandling import SpatialImage
            from morphonet.ImageHandling import imsave as imsaveINR
            return imsaveINR(filename, SpatialImage(img))
        elif filename.find('.nii') > 0:
            import nibabel as nib
            from nibabel import save as savenii
            print("new save")
            new_img = nib.Nifti1Image(img, np.eye(4))
            im_nifti = savenii(new_img, filename)
            return im_nifti

        else:
            from skimage.io import imsave as imsaveTIFF
            return imsaveTIFF(filename, img)
        return None

    def save_image_to_file_ezomero(self, image_id, file_path):
        """Download image by its ID to a path, using ezomero

        :param image_id: ID of the image in omero to download on disk
        :type image_id: int
        :param file_path: path where to store the image to (including image name)
        :type file_path: string

        
        """
        pixels = self.get_image_data(image_id)
        self.imsave(file_path, pixels)


    def get_data_from_image_path(self, image_name):
        """retrieve time and clean path from an image_name

        :param image_name: image_name used to compute data
        :type image_name: string
        :return: time and clean path
        :rtype: tuple (int , str)

        
        """
        import re
        image = image_name
        s = "###."
        splitted_name = image.split(".")
        time = int(splitted_name[0][-3:len(splitted_name[0])])
        new_path = re.sub('\d\d\d\.', s, image)
        return time, new_path

    def get_project_by_name(self,project_name):
        """Get OMERO project object using name

        :param project_name: Name of the project to find on OMERO
        :type project_name: string
        :return: OMERO project object
        :rtype: OMERO project object

        
        """
        projects = self.list_projects()
        for p in projects:
            if p.getName().lower() == project_name.lower():
                return p
        return None

    def get_project_by_id(self,project_id):
        """Get OMERO project object using id

        :param project_id: ID of the project to find on OMERO
        :type project_id: int
        :return: OMERO project object
        :rtype: OMERO project object

        
        """
        projects = self.list_projects()
        for p in projects:
            if p.getid() == project_id:
                return p
        return None

    def get_datasets(self,project=None):
        """Retrieve list of datasets for a defined project, if project is None look for Orphans datasets

        :param project: Name of the project on OMERO, If set to None, retrieve Orphans (Default value = None)
        :type project: OMERO project
        :return: List of datasets
        :rtype: list of dataset objects

        
        """
        if project is not None:
            p = self.connection.getObject("Project", project)
            datasets = p.listChildren()
        else:
            datasets = self.connection.listOrphans("Dataset")
        return datasets

    def get_dataset_by_name(self,dataset_name,project=None):
        """Retrieve the dataset object by its name for a defined project, if project is None look for Orphans datasets

        :param dataset_name: Name of the dataset to retrive from OMERO
        :type dataset_name: string
        :param project: project to list dataset from (Default value = None), if None dataset will be searched among Orphans
        :type project: project or None
        :return: The found dataset by name
        :rtype: OMERO dataset object

        
        """
        if dataset_name is None or dataset_name == "":
            print("The dataset name is None or empty , can't find the dataset")
            return None
        datasets = self.get_datasets(project=project)
        for p in datasets:
            if p is not None:
                if p.getName().lower() == dataset_name.lower():
                    return p
        return None

    def get_dataset_by_id(self,dataset_id,project=None):
        """Retrieve the dataset object by its id for a defined project, if project is None look for Orphans datasets

        :param dataset_id: ID of the dataset to retrive from OMERO
        :type dataset_id: int
        :param project: project to list dataset from (Default value = None), if None dataset will be searched among Orphans
        :type project: project or None
        :return: The found dataset by name
        :rtype: OMERO dataset object

        
        """
        datasets = self.get_datasets(project=project)
        for p in datasets:
            if p.getid() == dataset_id:
                return p
        return None

    def create_dataset(self,dataset_name,project_id=None,dataset_description=None):
        """Create a dataset in OMERO , attached to a project or not (given by its id) , with provided description or not

        :param dataset_name: name of the dataset to create
        :type dataset_name: string
        :param project_id: if exists, link the created dataset to this project (Default value = None)
        :type project_id: int
        :param dataset_description: if exists, add the description to the dataset (Default value = None)
        :type dataset_description: string
        :return: created dataset
        :rtype: OMERO dataset object
        
        """
        return ezomero.post_dataset(self.connection,dataset_name,project_id=project_id,description=dataset_description)

    def create_project(self,project_name,project_description=None):
        """Create a project in OMERO , with provided description or not

        :param project_name: name of the project to create
        :type project_name: string
        :param project_description: if exists, add the description to the dataset (Default value = None)
        :type project_description: string
        :return: created dataset
        :rtype: OMERO dataset object
        
        """
        return ezomero.post_project(self.connection,project_name,description=project_description)

    def list_projects(self):
        """Return a list of all projects currently available for the connection

        :return: List of all projects accessible
        :rtype: list omero dataset objects
        """

        if self.connection is not None:
            return self.connection.listProjects()

    def create_tag(self, tag, description):
        """Create a tag in OMERO if it does not exist already

        :param tag: name of the tag to create
        :type tag: string
        :param description: description of the tag
        :type description: string
        :return: the created tag on OMERO
        :rtype: OMERO annotation

        
        """
        tag_ann = self.get_tag(tag)  # Check if the tag already exyst
        if tag_ann is None:  # Create a new TAG
            print(" --> Create tag " + tag)
            tag_ann = omero.gateway.TagAnnotationWrapper(self.connection)
            tag_ann.setValue(tag)
            if description is not None:
                tag_ann.setDescription(description)
            tag_ann.save()
        return tag_ann

    def get_tag_name(self,connection,tag_id):
        """Retrieve name for a tag id

        :param connection: 
        :type connection: omero connection object
        :param tag_id: id of the tag
        :type tag_id: int
        :return: name of the tag
        :rtype: string

        
        """
        return ezomero.get_tag(connection,tag_id)

    def has_dataset_tag_id(self,connection,tag_id,dataset_id):
        """Verify if a dataset has a tag by its id

        :param connection: 
        :type connection: omero connection object
        :param tag_id: id of the tag
        :type tag_id: int
        :param dataset_id: id of the dataset
        :type dataset_id: int
        :return: True if the dataset has the given tag
        :rtype: bool

        
        """
        list_ids = self.get_tag_id_list(connection,"Dataset",dataset_id)
        return tag_id in list_ids

    def has_dataset_tag_name(self,connection,tag_name,dataset_id):
        """Verify if a dataset has a tag by its name

        :param connection: 
        :type connection: omero connection object
        :param tag_name: name of the tag
        :type tag_name: string
        :param dataset_id: id of the dataset
        :type dataset_id: int
        :return: True if the dataset has the given tag
        :rtype: bool

        
        """
        list_names = self.get_tag_name_list(connection,"Dataset",dataset_id)
        return tag_name in list_names

    def has_project_tag_id(self,connection,tag_id,project_id):
        """Verify if a project has a tag by its id

        :param connection: 
        :type connection: omero connection object
        :param tag_id: id of the tag
        :type tag_id: int
        :param project_id: id of the project
        :type project_id: int
        :return: True if the project has the given tag
        :rtype: bool

        
        """
        list_ids = self.get_tag_id_list(connection,"Project",project_id)
        return tag_id in list_ids

    def find_associated_rawdata_path(self, project,raw_tag_name="fuse"):
        """Find the rawdata path in the project, and retrieve it

        :param project: id of the project object
        :type project: OMERO project object
        :returns: Dataset corresponding to fused data
        :rtype: OMERO dataset object
        
        """
        final_dataset = None
        p = self.connection.getObject("Project", project.getId())
        datasets = p.listChildren()
        for dataset_obj in datasets:
            if self.has_set_tag(dataset_obj, raw_tag_name):
                final_dataset = dataset_obj
                break
        return final_dataset


    def has_project_tag_name(self,connection,tag_name,project_id):
        """Verify if a project has a tag by its name

        :param connection: 
        :type connection: omero connection objects
        :param tag_name: name of the tag
        :type tag_name: string
        :param project_id: id of the project
        :type project_id: int
        :returns: Has the project a tag with this name
        :rtype: bool

        
        """
        list_names = self.get_tag_name_list(connection,"Project",project_id)
        return tag_name in list_names

    def get_tag_id_list(self,connection,object_type,id):
        """Get list of tags id for an object

        :param connection: 
        :type connection: omero connection object
        :param object_type: type of the object to retrieve tags from ("Image","Dataset", "Project")
        :type object_type: basestring
        :param id: id of the object with type object_type
        :type id: int
        :returns: List of tag names associated with the object
        :rtype: list of string

        
        """
        list_ids = ezomero.get_tag_ids(connection,object_type,id)
        list_name = []
        for tag_id in list_ids:
            list_name.append(self.get_tag_name(connection,tag_id))
        return list_name

    def get_tag_name_list(self,connection,object_type,id):
        """Get list of tags name for an object

        :param connection: 
        :type connection: omero connection object
        :param object_type: type of the object to retrieve tags from ("Image","Dataset", "Project")
        :type object_type: basestring
        :param id: id of the object with type object_type
        :type id: int
        :returns: List of tag names associated with the object
        :rtype: list of string

        
        """
        list_ids = ezomero.get_tag_ids(connection,object_type,id)
        list_name = []
        for tag_id in list_ids:
            list_name.append(self.get_tag_name(connection,tag_id))
        return list_name

    def get_tag(self, name):
        """Get a tag in OMERO

        :param name: name of the tag to find
        :type name: string
        :returns: A OMERO annotation object or None
        :rtype: OMERO annotation

        
        """
        listTag = self.connection.getObjects("Annotation")
        for t in listTag:
            #if t.OMERO_TYPE == omero.model.TagAnnot  #AttributeError: module 'omero.model' has no attribute 'TagAnnot'
            if t.getValue() == name:
                return t
        return None

    def get_user_id(self, username):
        """Get user id by it's username

        :param username: name of the user to find
        :type username: string
        :returns: The user id corresponding to the username
        :rtype: int

        
        """
        return ezomero.get_user_id(self.connection, username)

    def get_connected_user_id(self):
        """Get user id for current logged-in user

        :returns: The current connected user id
        :rtype: int
        """
        return self.get_user_id(self.login)

    def get_annotation(self, project, map_ann):
        """Get annotation instance on the project using annotation object

        :param project: project to list annotation from
        :type project: OMERO project object
        :param map_ann: annotation to find on this project
        :type map_ann: OMERO annotation object
        
        """
        try:
            for ann in project.listAnnotations():
                if ann.getId() == map_ann.getId():
                    return ann
        except ValueError:
            print(" PyOmero : Error getting annotation " + ValueError)
        return None

    def remove_annotations_startswith(self, project, startswith):
        """Remove all annotation from project that begins with a name expression

        :param project: 
        :param startswith:
        
        """
        try:
            annotations_toremove = []
            for ann in project.listAnnotations():
                if ann is not None and type(ann) == omero.gateway.TagAnnotationWrapper and ann.getValue().startswith(
                        startswith):
                    annotations_toremove.append(ann)
            for ann in annotations_toremove:
                self.connection.deleteObjects('Annotation', [ann.id], wait=True)
        except ValueError:
            print(" PyOmero : Error remove annotation " + ValueError)

    def get_all_annotations(self, project):
        """Get annotations instance on the project

        :param project: project to list annotation from
        :type project: OMERO project object
        :returns:  All the annotations on the project
        :rtype: List of OMERO annotation object
        
        """
        annotations = []
        try:
            for ann in project.listAnnotations():
                annotations.append(ann)
        except ValueError:
            print(" PyOmero : Error getting annotation " + ValueError)
        return annotations

    def add_tag(self, dataset, tag, description=None):
        """Add tag to dataset using tag name , create it if needed

        :param dataset: 
        :param tag: 
        :param description:  (Default value = None)

        
        """
        if tag.strip() == "":
            print(" --> tag is empty")
            return False
        tag_ann = self.create_tag(tag, description)  # Check if the tag already exyst
        ann = self.get_annotation(dataset, tag_ann)
        if ann is None:
            print(" --> link tag " + tag + " to " + dataset.getName())
            dataset.linkAnnotation(tag_ann)
        else:
            print(" --> tag " + tag + " already linked to " + dataset.getName())

    def has_set_tag(self, dataset, tag_name):
        """check if given dataset has a tag

        :param dataset: dataset to list annotation from
        :type dataset: OMERO dataset object
        :param tag_name: name of the tag
        :type tag_name: string
        :returns:  Has the dataset the given tag
        :rtype: bool
        
        """
        target_object = self.connection.getObject("Dataset", dataset.getId())
        morphonet_tag_id = -1
        for tag_v in self.connection.getObjects("TagAnnotation", attributes={"textValue": tag_name}):
            morphonet_tag_id = tag_v.getId()
        # print(str(morphonet_tag_id.getId()))
        for ann in target_object.listAnnotations():
            if ann.getId() == morphonet_tag_id:
                return True
        return False

    def list_tags(self,dataset):
        """list all tags for dataset

        :param dataset: dataset to list annotation from
        :type dataset: OMERO dataset object
        :returns:  All the tags on the dataset
        :rtype: List of OMERO annotation object

        
        """
        target_object = self.connection.getObject("Dataset", dataset.getId())
        return target_object.listAnnotations()

    def list_tags_name(self,dataset):
        """list all tags names for dataset

        :param dataset: dataset to list annotation from
        :type dataset: OMERO dataset object
        :returns:  All the tags names on the dataset
        :rtype: List of string
        
        """
        names = []
        target_object = self.connection.getObject("Dataset", dataset.getId())
        for t_o in target_object.listAnnotations():
            if t_o is not None and t_o.getName() is not None:
                names.append(t_o.getName())
        return names

    def remove_tag(self, dataset, name ):
        """Remove tag from the dataset by name

        :param dataset: dataset to list annotation from
        :type dataset: OMERO dataset object
        :param name: name of the tag
        :type name: string
        :returns:  Is the remove successful
        :rtype: bool
        
        """
        tag_ann = self.get_tag(name)
        if tag_ann is None:
            return False
        ann = self.get_annotation(dataset, tag_ann)
        if ann is None:
            return False
        self.connection.deleteObjects('Annotation', [ann.id], wait=True)
        print(" --> tab " + name + " removed ")
        return True


    def get_file(self, dataset, file_to_download, path_to_write=""):
        """Download a file from dataset

        :param dataset: dataset to get file annotation from
        :type dataset: OMERO dataset object
        :param file_to_download: name of the file
        :type file_to_download: string
        :param path_to_write: folder where to write file in (Default value = "")
        :type path_to_write: string
        :returns:  Was file wrote successfully
        :rtype: bool
        
        """
        try:
            for ann in dataset.listAnnotations():
                if isinstance(ann, omero.gateway.FileAnnotationWrapper):
                    if ann.getFileName() == os.path.basename(file_to_download):
                        # print("File ID:", ann.getFile().getId(), ann.getFile().getName(), "Size:", ann.getFile().getSize())
                        print(" Download Annotation File " + file_to_download)
                        file_path = os.path.join(path_to_write, ann.getFileName())
                        with open(str(file_path), 'wb') as f:
                            # print("\nDownloading file to", file_path, "...")
                            for chunk in ann.getFileInChunks():
                                f.write(chunk)
                        # print("File downloaded!")
                        return True
        except ValueError:
            print(" PyOmero : Error getting file " + ValueError)
        return False


    def get_images_filename(self, dataset_id):
        """Retrive list of image filename associated to the dataset_id

        :param path_id: id of the dataset in omero to get image from
        :type path_id: int
        :param dataset_id: 
        :returns:  All the images names associated to the dataset
        :rtype: Dict of images id by name
        
        """
        list_images = {}
        for im_id in self.get_images_ids(dataset_id):
            f = self.get_image_object(im_id).getName()
            list_images[f] = im_id
        return list_images
    def list_files(self, dataset):
        """List annotations file for dataset

        :param dataset: dataset to get file annotation from
        :type dataset: OMERO dataset object
        :returns:  All the files annotation on the dataset
        :rtype: List of OMERO file annotation object
        
        """
        list_annotation = []
        if dataset is not None:
            try:
                for ann in dataset.listAnnotations():
                    if isinstance(ann, omero.gateway.FileAnnotationWrapper):
                        list_annotation.append(ann.getFileName())
            except ValueError:
                print(" PyOmero : Error listing file " + ValueError)
        return list_annotation

    def add_kvp(self, project, key_data, value_data):
        """Add a key value pair for the project

        :param project: 
        :param key_data: 
        :param value_data: 

        
        """
        map_ann = self.create_kvp(key_data, value_data)
        ann = self.get_annotation(project, map_ann)
        if ann is None:
            project.linkAnnotation(map_ann)
        # else:
        #    print(" --> link already exist " + key_data + " to " + project.getName())

    def create_kvp(self, key_data, value_data):
        """Create key vale pair

        :param key_data: key of the pair
        :type key_data: string
        :param key_value: value of the pair
        :type key_value: any
        :param value_data: 
        :returns:  The created Key Value pair
        :rtype: OMERO KVP annotation object
        
        """
        try:
            t = self.get_kvp(key_data, value_data)
            if t is not None:
                return t

            # Create KVP
            map_ann = omero.gateway.MapAnnotationWrapper(self.connection)
            namespace = omero.constants.metadata.NSCLIENTMAPANNOTATION
            map_ann.setNs(namespace)
            map_ann.setValue([[key_data, value_data]])
            map_ann.save()
            return map_ann
        except ValueError:
            print(" PyOmero : Error creating key value pair " + ValueError)
        return None

    def get_kvp(self, key_data, value_data):
        """Get key value pair

        :param key_data: key of the pair
        :type key_data: string
        :param key_value: value of the pair
        :type key_value: any
        :param value_data: 
        :returns: The key value pair matching key and value
        :rtype: OMERO KVP annotation object
        
        """
        try:
            listKV = self.connection.getObjects("Annotation")
            for t in listKV:
                if t.OMERO_TYPE == omero.model.MapAnnotationI:
                    tkv = t.getValue()[0]
                    if tkv[0] == key_data and tkv[1] == value_data:
                        return t
        except ValueError:
            print(" PyOmero : Error has get key value pair " + ValueError)
        return None

    def get_ks(self, key_data):
        """

        :param key_data:

        """
        listKS = []
        try:
            listKV = self.connection.getObjects("Annotation")
            for t in listKV:
                if t.OMERO_TYPE == omero.model.MapAnnotationI:
                    tkv = t.getValue()[0]
                    if tkv[0] == key_data:
                        listKS.append(t)
        except ValueError:
            print(" PyOmero : Error has get key annotation " + ValueError)
        return listKS

    def has_kvp(self, project, key_data, value_data):
        """Check if project has key value pair

        :param project: project to check KVP from
        :type project: OMERO project object
        :param key_data: key of the pair
        :type key_data: string
        :param value_data: value of the pair
        :type value_data: any
        :returns:  Does the project have the key value pair
        :rtype: bool
        
        """
        try:
            t = self.get_kvp(key_data, value_data)
            if t is None:  # KV does not exist at all
                return False

            ann = self.get_annotation(project, t)
            if ann is None:  # KV does not exist at all
                return False
        except ValueError:
            print(" PyOmero : Error has key pair value" + ValueError)
        return True

    def get_v(self, project, key_data):
        """Get value for a KVP in a given project

        :param project: project to check KVP from
        :type project: OMERO project object
        :param key_data: key of the pair
        :type key_data: string

        
        """
        try:
            listKS = self.get_ks(key_data)
            for k in listKS:
                ann = self.get_annotation(project, k)
                if ann is not None:
                    tkv = ann.getValue()[0]
                    return tkv[1]
        except ValueError:
            print(" PyOmero : Error getting value of key pair " + ValueError)
        return None


