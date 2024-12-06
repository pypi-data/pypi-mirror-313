import os
import numpy as np
from AstecManager.libs.data import imread,imsave
from scipy import ndimage as nd
def fill_image(imagein, folderin,imagearray=None,vsize=None):
    """ Threshold a given background image and fill the holes in the background using skimage morphology tool

    :param imagein: Name of the image to be filled
    :type imagein: str
    :param folderin: Folder of the image
    :type folderin: str
    :return: The image array after being filled , and the voxel size of the image
    :rtype: tuple

    """
    from skimage import morphology
    voxel_size = None # Useless if we provide voxel_size , but kept for compatibililty
    if imagearray is None:
        arraynp, voxel_size = imread(os.path.join(folderin, imagein), voxel_size=True)
    else:
        arraynp = imagearray
        voxel_size = vsize
    im_bin = (arraynp < 150)
    try :
        im_bin = morphology.remove_small_holes(im_bin)
    except :
        print("skimage morphology not found")
    return im_bin, voxel_size

def membrane_from_junction(junction_array):
    """ Extract the mask background over membrane from junction image
    :param junction_array: Junction image
    :type junction_array: ndarray
    :return: Background image
    :rtype: ndarray

    """

    image_background = np.zeros_like(junction_array)
    #imsave("/home/bgallean/imagebackgroundraw.nii", image_background)
    image_background[junction_array == 0] = 255
    image_background[junction_array > 0] = 0
    image_background[junction_array < 2] = 255
    image_background[junction_array > 1] = 0
    return image_background

def background_from_junction(junction_array):
    """ Extract the mask background over embryo from junction image
    :param junction_array: Junction image
    :type junction_array: ndarray
    :return: Background image
    :rtype: ndarray

    """

    image_background = np.zeros_like(junction_array)
    #imsave("/home/bgallean/imagebackgroundraw.nii", image_background)
    image_background[junction_array == 0] = 255
    image_background[junction_array > 0] = 0
    return image_background
def apply_morphological_changes(condition, type, structural_connectivity=3):
    """ In order to create the  contour from the background image, its needed to erode and dilate the image a certain
    number of times. Depending on a strategy given in parameter, applies the strategy to the image, using a specific
    connectivity.The different strategies change the thickness of the created contour.

    :param condition: The input image where contour is determined
    :type condition: numpy.ndarray
    :param type: The strategy to create contour
    :type type: str
    :param structural_connectivity: The connectivity structuring element  (Default value = 3)
    :type structural_connectivity: int

    :return: The modified image
    :rtype: numpy.ndarray

    """
    # binary structure 6 connectivity  : nd.generate_binary_structure(3, 1)
    struct1 = nd.generate_binary_structure(3, structural_connectivity)
    if type == "twice-d":
        return np.logical_xor(nd.binary_dilation(condition, struct1, iterations=2),
                              nd.binary_dilation(condition, struct1, iterations=1))
    elif type == "identity":
        return condition
    elif type == "noerod":
        return np.logical_xor(nd.binary_dilation(condition, struct1, iterations=1), condition)
    else:
        return np.logical_xor(condition,
                              nd.binary_dilation(condition, struct1, iterations=2))


def generate_contour(imagein, arraydata, voxelsize, folderout, type, sigma=1, connectivity=3,target_normalization_max=255):
    """ Generate the contour for a given image in parameter , using a strategy and a structuring element. This function
    saves the image to a new folder , replacing "background" by "contour" in its name. A normalization should be provided
    for output intensities.

    :param imagein: Path to the input image
    :type imagein: str
    :param arraydata: Numpy array of the image
    :type arraydata: numpy.ndarray
    :param voxelsize: The voxel size of the input image, will be the same for output
    :type voxelsize: float
    :param folderout: Folder where the images will be saved
    :type folderout: str
    :param type: Type of contour generation geometric transform (for contour thickness). Current best is "normal"
    :type type: str
    :param sigma: Value of the gaussian for smoothing of output contour (to simulate membrane intensities (Default value = 1)
    :type sigma: int
    :param connectivity: Size of the structuring element for contour geometric changes (Default value = 3)
    :type connectivity: int
    :param target_normalization_max: Value max for intensities in output contour images (Default value = 255)
    :type target_normalization_max: int

    """
    result = np.zeros(arraydata.shape, dtype=np.float64)
    im_cyto_erod = apply_morphological_changes(arraydata, type, structural_connectivity=connectivity)
    result[im_cyto_erod == True] = 1
    #imsave(os.path.join(folderout, imagein.replace("_background", "_result")), result, voxel_size=voxelsize)
    smoothed = nd.gaussian_filter(result, sigma=sigma)
    smoothed *= target_normalization_max
    del im_cyto_erod
    imsave(os.path.join(folderout, imagein.replace("_junctions", "_contour")), smoothed.astype(np.uint16), voxel_size=voxelsize)
    del result

def junctions_to_segmentation(semantic,footprint=4):
    """ Function forked from MorphoDeep tool. Compute segmentation by labeled components from a junction image

    :param semantic: Junction image
    :type semantic: numpy.ndarray
    :return: Segmentated image
    :rtype: numpy.ndarray

    """
    from skimage.segmentation import watershed
    from skimage.measure import label
    from skimage.morphology import binary_erosion,binary_dilation

    markers = np.uint16(label(np.uint16(binary_erosion(semantic == 1,footprint=np.ones((footprint, footprint,footprint)))), background=0))  # MARKERS
    background = binary_dilation(semantic == 0)  # BACKGROUND
    membrane = np.uint8(semantic > 1)  # NICE MEMBRANE
    return np.uint16(watershed(np.float32(membrane), markers=markers, mask=1 - background))
def update_backgrounds(image_array,old_backgroundg=0,new_background=1):
    """ Change the value of background of a segmented image to a new value
    :param image_array: Input image
    :type image_array: numpy.ndarray
    :param old_backgroundg: Background value in the image
    :type old_backgroundg: int
    :param new_background: New background value in the image
    :type new_background: int
    :return: Segmentation image with new background value
    :rtype: numpy.ndarray

    """
    new_max = np.max(image_array)+1
    image_array[image_array==new_background]=new_max
    image_array[image_array==old_backgroundg]=new_background
    return image_array

def compute_segmentation_from_junctions(embryo_folder,junction_folder_name):
    """ Generate a segmentation from all junction images found in an embryo folder
    :param embryo_folder: Path to the embryo folder
    :type embryo_folder: str
    :param junction_folder_name: Name of the junction folder
    :type junction_folder_name: str
    :return: Segmentation folder name, segmentation folder path
    :rtype: tuple

    """
    semantic_seg_name = "SEG_SEMANTIC_"+junction_folder_name.replace("JUNC_","")
    semantic_seg_path = os.path.join("SEG/",semantic_seg_name)

    junction_folders = os.path.join(embryo_folder, "JUNC/")
    folder_raw = os.path.join(junction_folders, junction_folder_name)
    if not os.path.exists(folder_raw):
        print("Input images path does not exist")
        exit()

    res = []
    for path in os.listdir(folder_raw):  # List all junction images to process
        # check if current path is a file
        if os.path.isfile(os.path.join(folder_raw, path)) and ".mha" in path or ".nii" in path:
            res.append(path)

    res.sort()

    if not os.path.exists(semantic_seg_path):
        os.makedirs(semantic_seg_path)

    for image in res: # Process the contour creation for each image
        output_image = os.path.join(semantic_seg_path,image.replace("_junctions","_seg"))
        if not os.path.isfile(output_image):
            image_junc,vsize = imread(os.path.join(folder_raw, image),voxel_size=True)
            output_image = os.path.join(semantic_seg_path,image.replace("_junctions","_seg"))
            seg_array = junctions_to_segmentation(image_junc)
            updated_background = update_backgrounds(seg_array)
            imsave(output_image, updated_background,voxel_size=vsize)
            print("     -" + str(image))
    return semantic_seg_path, semantic_seg_name


def compute_membranes_from_junctions(embryo_folder, junctionimput, reducvoxelsize=0.3, target_normalization_max=255,
                        correction_vsize=False):
    """ Generate the enhanced membranes images from all the junction images found in an embryo folder. Details on methods and
    parameters are given in the documentation of each specific function

    :param embryo_folder: Path to the embryo folder
    :type embryo_folder: str
    :param junctionimput: Name of the junction folder to compute the contour from
    :type junctionimput: str
    :param reducvoxelsize: If voxel size should be changed (either because it's incorrect or we want to reduce resolution), value of the new voxel size (Default value = 0.3)
    :type reducvoxelsize: float
    :param target_normalization_max: Maximum value for the intensities of the output contour images (Default value = 255)
    :type target_normalization_max: int
    :param correction_vsize: If true , apply the voxel size specified in parameter to the input images (Default value = False)
    :type correction_vsize: bool

    :returns: The path to the contour folder generated
    :rtype: str

    """
    junction_folders = os.path.join(embryo_folder, "JUNC/")
    folder_raw = os.path.join(junction_folders, junctionimput)
    contour_suffix = junctionimput.replace("JUNC_","")
    if not os.path.exists(folder_raw):
        print("Input images path does not exist")
        exit()
    if not os.path.exists(folder_raw):
        print("Input templates path does not exist")

    res = []
    for path in os.listdir(folder_raw):  # List all junction images to process
        # check if current path is a file
        if os.path.isfile(os.path.join(folder_raw, path)) and ".mha" in path or ".nii" in path:
            res.append(path)

    res.sort()
    # Correction of networks voxel size errors
    if correction_vsize:  # If we need to correct voxel size , do it with ASTEC package setVoxelSize command
        print("Correction of the image voxel size")
        for image in res:
            print("     - " + str(image))
            os.system("conda run -n astec setVoxelSize " + str(os.path.join(folder_raw, image)) + " " + str(
                reducvoxelsize) + " " + str(reducvoxelsize) + " " + str(reducvoxelsize))

    folder_contour_name = "FUSE"+str(contour_suffix)+"_MEMBRANES"
    folder_contour = os.path.join(embryo_folder, "FUSE/"+folder_contour_name+"/")
    if not os.path.exists(folder_contour):
        os.makedirs(folder_contour)

    print("Filling and creating contour for normal size")
    for image in res: # Process the contour creation for each image
        image_junc,vsize = imread(os.path.join(folder_raw, image),voxel_size=True)
        background_array = membrane_from_junction(image_junc)
        #imsave("./BACKGROUND/BACKGROUND_TEST/"+image,background_array,voxel_size=vsize)
        print("     -" + str(image))
        image_filled, voxelsize = fill_image("", "",imagearray=background_array,vsize=vsize) # Binarize and fill the holes of the background images
        image_filled = (background_array < 150)
        generate_contour(image, image_filled, voxelsize, folder_contour, "identity", sigma=2, connectivity=1,
                         target_normalization_max=target_normalization_max)  # Generating the contour
    return folder_contour,folder_contour_name

def compute_contour_from_junctions(embryo_folder, junctionimput, reducvoxelsize=0.3, target_normalization_max=255,
                        correction_vsize=False):
    """ Generate the contour images from all the junction images found in an embryo folder. Details on methods and
    parameters are given in the documentation of each specific function

    :param embryo_folder: Path to the embryo folder
    :type embryo_folder: str
    :param junctionimput: Name of the junction folder to compute the contour from
    :type junctionimput: str
    :param reducvoxelsize: If voxel size should be changed (either because it's incorrect or we want to reduce resolution), value of the new voxel size (Default value = 0.3)
    :type reducvoxelsize: float
    :param target_normalization_max: Maximum value for the intensities of the output contour images (Default value = 255)
    :type target_normalization_max: int
    :param correction_vsize: If true , apply the voxel size specified in parameter to the input images (Default value = False)
    :type correction_vsize: bool

    :returns: The path to the contour folder generated
    :rtype: str

    """
    junction_folders = os.path.join(embryo_folder, "JUNC/")
    folder_raw = os.path.join(junction_folders, junctionimput)
    contour_suffix = junctionimput.replace("JUNC_","")
    if not os.path.exists(folder_raw):
        print("Input images path does not exist")
        exit()
    if not os.path.exists(folder_raw):
        print("Input templates path does not exist")

    res = []
    for path in os.listdir(folder_raw):  # List all junction images to process
        # check if current path is a file
        if os.path.isfile(os.path.join(folder_raw, path)) and ".mha" in path or ".nii" in path:
            res.append(path)

    res.sort()
    # Correction of networks voxel size errors
    if correction_vsize:  # If we need to correct voxel size , do it with ASTEC package setVoxelSize command
        print("Correction of the image voxel size")
        for image in res:
            print("     - " + str(image))
            os.system("conda run -n astec setVoxelSize " + str(os.path.join(folder_raw, image)) + " " + str(
                reducvoxelsize) + " " + str(reducvoxelsize) + " " + str(reducvoxelsize))

    folder_contour_name = "CONTOUR_"+str(contour_suffix)
    folder_contour = os.path.join(embryo_folder, "CONTOUR/"+folder_contour_name+"/")
    if not os.path.exists(folder_contour):
        os.makedirs(folder_contour)

    print("Filling and creating contour for normal size")
    for image in res: # Process the contour creation for each image
        image_junc,vsize = imread(os.path.join(folder_raw, image),voxel_size=True)
        background_array = background_from_junction(image_junc)
        print("     -" + str(image))
        image_filled, voxelsize = fill_image("", "",imagearray=background_array,vsize=vsize) # Binarize and fill the holes of the background images
        generate_contour(image, image_filled, voxelsize, folder_contour, "normal", sigma=2, connectivity=1,
                         target_normalization_max=target_normalization_max)  # Generating the contour
    return folder_contour,folder_contour_name
def compute_contour(embryo_folder,backgroundinput,reducvoxelsize=0.3,target_normalization_max=255,correction_vsize=False):
    """ Generate the contour images from all the background images found in an embryo folder. Details on methods and
    parameters are given in the documentation of each specific function

    :param embryo_folder: Path to the embryo folder
    :type embryo_folder: str
    :param backgroundinput: Name of the background folder to compute the contour from
    :type backgroundinput: str
    :param reducvoxelsize: If voxel size should be changed (either because it's incorrect or we want to reduce resolution), value of the new voxel size (Default value = 0.3)
    :type reducvoxelsize: float
    :param target_normalization_max: Maximum value for the intensities of the output contour images (Default value = 255)
    :type target_normalization_max: int
    :param correction_vsize: If true , apply the voxel size specified in parameter to the input images (Default value = False)
    :type correction_vsize: bool

    :returns: The path to the contour folder generated
    :rtype: str

    """
    background_folders = os.path.join(embryo_folder, "BACKGROUND/")
    folder_raw = os.path.join(background_folders, backgroundinput)
    contour_suffix = backgroundinput.replace("Background_","").replace("BACKGROUND_","")
    if not os.path.exists(folder_raw):
        print("Input images path does not exist")
        exit()
    if not os.path.exists(folder_raw):
        print("Input templates path does not exist")

    res = []
    for path in os.listdir(folder_raw): # List all background images to process
        # check if current path is a file
        if os.path.isfile(os.path.join(folder_raw, path)) and ".mha" in path or ".nii" in path:
            res.append(path)


    res.sort()
    # Correction of networks voxel size errors
    if correction_vsize: #If we need to correct voxel size , do it with ASTEC package setVoxelSize command
        print("Correction of the image voxel size")
        for image in res:
            print("     - " + str(image))
            os.system("conda run -n astec setVoxelSize " + str(os.path.join(folder_raw, image)) + " "+str(reducvoxelsize)+" "+str(reducvoxelsize)+" "+str(reducvoxelsize))

    folder_contour_name = "CONTOUR_"+str(contour_suffix)
    folder_contour = os.path.join(embryo_folder, "CONTOUR/"+folder_contour_name+"/")


    if not os.path.exists(folder_contour):
        os.makedirs(folder_contour)

    print("Filling and creating contour for normal size")
    for image in res: # Process the contour creation for each image
        print("     -" + str(image))
        image_filled, voxelsize = fill_image(image, folder_raw) # Binarize and fill the holes of the background images
        generate_contour(image, image_filled, voxelsize, folder_contour, "normal", sigma=2, connectivity=1,target_normalization_max=target_normalization_max) #Generating the contour
    return folder_contour,folder_contour_name



