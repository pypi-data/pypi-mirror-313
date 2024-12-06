import os
import numpy as np
from nibabel import load as loadnii
from skimage.io import imread as imreadTIFF
import tifffile as tf
import time
def isfile(filename):
    """ Test if a file exist on the disk. Test for compressed version too

    :param filename: Path of the file to test
    :type filename: str
    :return: True if the file exist (or a compressed version), False otherwise
    :rtype: bool

    """
    return os.path.isfile(filename) or os.path.isfile(filename+".gz") or os.path.isfile(filename+".zip")


def imsave(filename, img, verbose=True,voxel_size=(1,1,1)):
    """Save a numpyarray as an image to filename.
    
    The filewriter is choosen according to the file extension.

    :param filename: Name of the file to save
    :type filename: str
    :param img: Array of the image
    :type img: np.ndarray
    :param verbose: If True, will print the save call (useless) (Default value = True)
    :type verbose: bool
    :param voxel_size: Voxel size of the saved image (Default value = (1,1,1))
    :type voxel_size: tuple
    :return: The path of the image if saved, None otherwise
    :rtype: str
    """

    if verbose:
        print(" --> Save " + filename)
    if filename.find('.inr') > 0 or filename.find('.mha') > 0:
        from AstecManager.libs.ImageHandling import SpatialImage
        from AstecManager.libs.ImageHandling import imsave as imsaveINR
        return imsaveINR(filename, SpatialImage(img),voxel_size=voxel_size)
    elif filename.find('.nii') > 0:
        import nibabel as nib
        from nibabel import save as savenii
        new_img = nib.nifti1.Nifti1Image(img, None)
        new_img.header.set_zooms(voxel_size)
        im_nifti = savenii(new_img, filename)
        return im_nifti
    else:
        from skimage.io import imsave as imsaveTIFF
        if filename.endswith(".gz"):
            filename = filename.replace(".gz", "")
            im = imsaveTIFF(filename, img)
            os.system("cd " + os.path.dirname(filename) + ";gzip " + os.path.basename(filename))
            return im
    return None

def TIFFTryParseVoxelSize(filename):
    """Tries to parse voxel size from TIFF image. default return is (1,1,1)

    :param filename: Path of the image to parse
    :type filename: str
    :return: Voxel size of the image
    :rtype: tuple

    """

    vsx = 1
    vsy = 1
    vsz = 1
    with tf.TiffFile(filename) as tif:

        if len(tif.pages) > 0:
            page = tif.pages[0]
            for tag in page.tags:
                if tag.name == "XResolution":
                    if len(tag.value) >= 2:
                        vsx = round(tag.value[1] / tag.value[0], 5)
                if tag.name == "YResolution":
                    if len(tag.value) >= 2:
                        vsy = round(tag.value[1] / tag.value[0], 5)
                if tag.name == "ImageDescription":
                    subtags = tag.value.split("\n")
                    for t in subtags:
                        if "spacing" in t:
                            if len(t.split("=")) >= 2:
                                vsz = t.split("=")[1]
    vsize = (vsx, vsy, vsz)
    return vsize



def imread(filename, verbose=True,voxel_size=False):
    """Reads an image file completely into memory

    :param filename: Path to the image
    :type filename: str
    :param verbose: If true, print the read process to terminal (useless)  (Default value = True)
    :type verbose: bool
    :param voxel_size: If true, load the voxel size and returns it (Default value = False)
    :type voxel_size: bool
    :return: The array of the image , and the voxel size if requested
    :rtype: np.ndarray or tuple

    """
    if verbose:
        print(" --> Read " + filename)
    if not isfile(filename):
        if verbose:
            print("Miss "+filename)
        return None
    try:

        if filename.find("mha") > 0:
            from AstecManager.libs.ImageHandling import imread as imreadINR #Use Image Handling for mha images
            data, vsize = imreadINR(filename)
            if voxel_size:
                return np.array(data), vsize
            else:
                return np.array(data)
        elif filename.find('.inr') > 0:
            from AstecManager.libs.ImageHandling import imread as imreadINR # Image handling for INR
            data,vsize = imreadINR(filename)
            if voxel_size:
                return np.array(data),vsize
            else:
                return np.array(data)
        elif filename.find('.nii') > 0:
            im_nifti = loadnii(filename) # Use NIFTI if loading a nii image
            if voxel_size:
                sx, sy, sz = im_nifti.header.get_zooms()
                vsize = (sx, sy, sz)
                data = np.array(im_nifti.dataobj).astype(np.dtype(str(im_nifti.get_data_dtype())))
                #data = np.swapaxes(data,0,2)
                return data,vsize
            else :
                data = np.array(im_nifti.dataobj).astype(np.dtype(str(im_nifti.get_data_dtype())))
                return data
        elif filename.find("h5") > 0:
            import h5py # Use H5PY for h5 image, but cant return voxelsize
            with h5py.File(filename, "r") as f:
                return np.array(f["Data"])
        else: # Default is to try reading as a TIFF
            imtiff = imreadTIFF(filename)
            imtiff = np.swapaxes(imtiff,0,2)
            if voxel_size:
                vsize = TIFFTryParseVoxelSize(filename)
                return imtiff,(float(vsize[0]), float(vsize[1]), float(vsize[2]))
            else:
                return imtiff
    except Exception as e:
        if verbose:
            print(" Error Reading " + filename)
            print(str(e))
            if filename.endswith("gz") or filename.endswith("zip"): # If we found a compressed image and the parser is not adapted, uncompress and read again
                temp_path = "TEMP" + str(time.time())
                while os.path.isdir(temp_path):  # JUST IN CASE OF TWISE THE SAME
                    temp_path = "TEMP" + str(time.time())
                os.system("mkdir -p " + temp_path)
                os.system("cp " + filename + " " + temp_path)
                filename = os.path.join(temp_path, os.path.basename(filename))
                os.system("gunzip " + filename)
                filename = filename.replace('.gz', '')
                if voxel_size:
                    arrayim,vsize = imread(filename,verbose,voxel_size)
                    if temp_path is not None:
                        os.system("rm -rf " + temp_path)
                    return arrayim,vsize
                else :
                    arrayim = imread(filename,verbose,voxel_size)
                    if temp_path is not None:
                        os.system("rm -rf " + temp_path)
                    return arrayim

            return None
        # quit()
    return None
class Cell:
    """ Class representing the cells in memory. A cell has a time point (int) , and id (int) , a list of cells being
    their direct mothers (should only contain one) , and a list of cells being their direct daughters (can be 0 to many)
    """
    id = -1
    t = -1
    mothers = []
    daughters = []

    def __init__(self,id_cell,time_cell):
        self.id = id_cell
        self.t = time_cell
        self.mothers = []
        self.daughters = []

    def add_mother(self,cell):
        """ Add a mother to the list of mothers , and add this cell to the mother's daughters list

        :param cell: The cell that will be current cell mother
        :type cell: Cell

        """
        #print("mother len before : " + str(len(self.mothers)))
        #print("add mother for cell : "+str(self.t)+","+str(self.id)+" for mother : "+str(cell.t)+","+str(cell.id))
        if self.mothers is None:
            self.mothers = []
        if not cell in self.mothers:
            self.mothers.append(cell)
        #print("mother len after : " + str(len(self.mothers)))
        cell.add_daughter(self)


    def add_daughter(self,cell):
        """ Add the given cell to current cell daughters. This function should not be called directly ,
        instead use "add_mother" on the parameter cell.

        :param cell: Cell to add as a daughter
        :type cell: Cell

        """
        #print("daughters len before : " + str(len(self.daughters)))
        #print("add daughter for cell : " + str(self.t) + "," + str(self.id) + " for mother : " + str(cell.t) + "," + str(cell.id))
        if self.daughters is None:
            self.daughters = []
        if not cell in self.daughters:
            self.daughters.append(cell)


def get_id_t(idl):
    """Return the cell t,id

    :param idl: 
    :type idl: int
    :return: The cell t,id
    :rtype: tuple

    
    """
    t=int(int(idl)/(10**4))
    cell_id=int(idl)-int(t)*10**4
    return t,cell_id

def get_longid(t,idc):
    """Return the cell key (longid)

    :param t: Cell time point
    :type t: int
    :param idc: Cell id
    :type idc: int
    :return: The cell key
    :rtype: int

    
    """
    if t==0 or  t=="0":
        return idc
    return t*10**4+idc

