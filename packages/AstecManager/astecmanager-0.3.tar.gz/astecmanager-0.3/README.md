## This library has been created to automatize and help users to segment using ASTEC software. 
On top of the ASTEC integration the tool include multiple additional features :
* Data enhancement (contour computation, smoothing, ...)
* Data Management (integration of OMERO data manager, automatic compression, automatic generation of metadata , generation of embryo identification card)
* Analyse the data generated through ASTEC pipeline (using different graphs)
* Integrated generation of properties (ASTEC properties , naming )


# Table of contents
1. [Installation](#install)
2. [Update](#update)
3. [Template files link](#template-files-link)
4. [Import raw data](#import-raw-data)
5. [Fusion](#fusion)
6. [Fusion parameters tuning](#fusion-parameters-test)
7. [Fusion final run](#final-fusion)
8. [Generation of semantic data](#computation-of-semantic-data-_optional_)
9. [Generation of membranes intensity image from semantic](#generation-of-membranes-intensity-image-from-semantic)
10. [Contours (optional)](#contours-_optional_)
11. [First time point segmentation](#first-time-point-segmentation)
12. [Data downscaling (optional)](#data-downscaling-_optional_--fusions--contours-and-first-time-point)
13. [Propagation of the segmentation parameters tuning](#segmentation-parameters-test)
14. [Propagation test verification](#segmentation-test-verification)
15. [Propagation final run](#segmentation-propagation)
16. [Generation of embryo properties (optional)](#generation-of-embryo-common-properties-_optional_)
17. [Generation of lineage distance properties](#generation-of-lineage-distance-properties-_optional_)

## Install

The first step to use this tool will be to install the Conda package manager.
You can find a guide to install conda [here](/https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) 

Now that conda is installed,  open a new terminal, and type the following lines : 

`conda create -n AstecManager -c conda-forge python=3.10 zeroc-ice omero-py` \
`conda activate AstecManager` \
`conda install -c mosaic treex` \
`pip install AstecManager`

Those lines will install the creation a conda environment to use the package , and install the package and its dependencies into the environment. It includes the installation of the necessary Python version.

To be able to run the different algorithms of ASTEC pipeline, you will need to install ASTEC package and its dependencies. To do so , please follow [this link](https://astec.gitlabpages.inria.fr/astec/installation.html).

On top of that, in order to automatically  name a new embryo during the pipeline , you will need to install ASCIDIAN package , and its dependencies. To do so , please follow [this link](https://astec.gitlabpages.inria.fr/ascidian/installation.html).

## Template files link

The tool uses parameters files to run each of the different steps. Those files are available as templates following [this link](https://drive.google.com/drive/folders/1qcQmIh28FjH7S_XUCq0b8ZK4JloprUzN?usp=drive_link).

Please download the corresponding file for the step you are planning to run , and edit it to your needs.

Parameters file link by step : 

- [Import raw datas from microscope computer](https://drive.google.com/file/d/1bVthvWj7I4mqP72h2-CRqBemuXbm7lBy/view?usp=drive_link)
- [Perform a test fusion](https://drive.google.com/file/d/1R2LBab06kURCe23PGS3XXA-LGVp5Io4O/view?usp=drive_link)
- [Perform the final fusion](https://drive.google.com/file/d/17qKu1OZrNlJed-YAdBphX-mfjrG87yqj/view?usp=drive_link)
- [After generating semantic images , compute contour images](https://drive.google.com/file/d/1AkUQiaJKP062tXgKXcSQpZR9syTPsRRg/view?usp=drive_link)
- [Segmentation of the first time point](https://drive.google.com/file/d/1T2qu96RMzeNmIsv2D2yj22biOFGvPmgb/view?usp=drive_link)
- [Downscaling for the segmentation tests](https://drive.google.com/file/d/18NrK0Po6GndH9C89bZZSngKomyiVIJWT/view?usp=drive_link)
- [Segmentation test runs](https://drive.google.com/file/d/1ZCGTD7Auli8gfWQIG-hNbFdQuDslfyyC/view?usp=drive_link)
- [Final segmentation run](https://drive.google.com/file/d/1-nyaFO1d0AZVT3iy777uVWl9GYhrkGrH/view?usp=drive_link)


Additional data generation files :

- [Automatic naming](https://drive.google.com/file/d/14vaOD1PdT4eD-bXnmY8PjnEg-tSvklwi/view?usp=drive_link)
- [Embryo Properties Generation](https://drive.google.com/file/d/1dNaAyBf_I5TTeaAsSH4YXiRzY0dpNMdS/view?usp=drive_link)
- [Lineage distance properties generation](https://drive.google.com/file/d/1mUQI2lYBtHVU3CE4D9fIv6X39iYtARmY/view?usp=drive_link)
- [If needed , generate INTRAREG movie from fusion images](https://drive.google.com/file/d/1kTJbWtBsQL1tX8fGNq-l2g_SLP_n4yhR/view?usp=drive_link)
- [If needed, generate a video from INTRAREG movie](https://drive.google.com/file/d/1CFIjYqP7CKHs7pBAqm3y4soX46s5mKze/view?usp=drive_link)

OMERO communication (download , upload) parameters files :

- [Link to OMERO authentication file template](https://drive.google.com/file/d/1ySUb3OnlgkA-JBNe2boFDRXlEKaEGbQ0/view?usp=drive_link) 
- [Link to download a specific OMERO dataset](https://drive.google.com/file/d/1kLDICrnLP6DQ-StGnTL7j76T2ybsIhXF/view?usp=drive_link)
- [Link to download a complete OMERO project(embryo)](https://drive.google.com/file/d/1S3rW_zgVGcljNC0SIWLi_t1ZfdUNljUD/view?usp=drive_link)
- [Link to upload a specific image folder to OMERO dataset](https://drive.google.com/file/d/1-P2sLWUicEIy9gfCZkM_NzxB3co4V1Km/view?usp=drive_link)
- [Link to upload a complete embryo folder to OMERO project](https://drive.google.com/file/d/1Ymo7ADYySedunWg1oNXTpJJsNXmATpxl/view?usp=drive_link)


## Update

Often, the tool will be updated to add features, and debug the existing ones. 

* To update the tool, you can simply start a terminal and run :

`conda activate AstecManager` \
`pip install AstecManager --upgrade`

## Data Manager Integration

To store the data for further work and archives , the team uses a data manager called OMERO.
In the following pipeline, you will be able to upload or download the different data produced to OMERO , automatically or manually.

In order to upload or download, you first need to create a file on your computer, somewhere no one can access and that you should not share.

The file should contain the following lines : 

```
host=adress.to.omero.instance
port=omero.port (usually 4064)
group=your team group
secure=True
java_arg=java
login=your omero login
password=your omero password
```

Save this file and store its path, so you can access it when needed.

A template for the configuration file can be found [here](https://drive.google.com/file/d/1ySUb3OnlgkA-JBNe2boFDRXlEKaEGbQ0/view?usp=drive_link)


## Import raw data

After starting the acquisition of the embryo in the microscope , it is advised to setup the automatic transfert of the generated Raw Images to the processing computer. 
For this , create a folder in the experiment folder of the processing computer, and name it with the name of the embryo. 

Download the parameters file for import [here](https://drive.google.com/file/d/1bVthvWj7I4mqP72h2-CRqBemuXbm7lBy/view?usp=drive_link) and save it to the embryo folder you created.

Edit it : 

```
parameters["embryo_name"]="TEST_EMBRYO" # Name of the embryo folder
parameters["user"]="" # initials of user performing the import
parameters["distant_folder"]="path/to/rawdata/on/microscope/computer/" # Folder containing raw data stacks folders in microscope computer
parameters["delay_before_copy"]=480 #Delay in minutes before starting the copy. This allows to start the script with acquisition , and make sure copy will start after it's finished. This delay should be equals or superior to acquisition duration
```

The _delay_before_copy_ parameter is very important ! after starting the acquisition , start the file with the delay corresponding to your acquisition time (in minutes) , and the copy should be done automatically after the acquisition , and prevent loosing time with copy

To start the import , open a terminal in the embryo folder and run the following lines 

`conda activate AstecManager` \
`python3 import_raw_datas.py` 

## Fusion


The most crucial part of this process is combining the images, and it needs to be done quickly. You should begin this step right after copying the large Raw Images, and try to finish it as soon as you can.

These Raw Images are very large, roughly 3 gigabytes each. This means that if you're working with one time point, it will use up about 12 gigabytes of computer memory. Think about it this way: if you're dealing with an embryo at 300 different time points, and you have multiple channels of images, your Raw Images folder could take up as much as 2 to 3 terabytes of space on your computer's hard drive.

Additionally, the Raw Images often have a significant amount of background information, which takes up a lot of memory. This background includes unnecessary data.

The fusion step is designed to address the problems we've just talked about:

- It keeps the most valuable information from each camera angle to create an isotropic image. An isotropic image means that it has the same characteristics, like intensity, across all regions.

- It reduces the memory needed for a single time point from around 12 gigabytes to a more manageable 500 megabytes.

- It also trims the image around the embryo, cutting out the excessive background and keeping only the essential information.

For more details about this step , please follow [this link](https://astec.gitlabpages.inria.fr/astec/astec_fusion.html#fusion-method-overview)

It's advised to split fusion in 2 steps 
* A test step where you will find the best parameters for this specific dataset.
* A production step where you will apply the best parameters to the complete dataset.

* Your folder hierarchy should look like this, before starting the fusion

``` 
     embryo name
         └───RAWDATA
             │───stack_0_channel_0_obj_left
             │───stack_0_channel_0_obj_right
             │───stack_1_channel_0_obj_left
             │───stack_1_channel_0_obj_right
             └───... (more if you have another channel)
             
```

#### Fusion parameters test
The fusion parameters test is a needed step , considering the high number of parameters needed for fusion , we can't take the time to try them one by one, on a large time sequence.

The test step is split in 2 sub steps : 

- 1st , a test fusion using the parameter set that is usually correct for our data
- If it's not working, 4 sets of parameter that usually are the ones that may differ 
- If it's still not working , you're invited to explore the fusion parameters documentation [here](https://astec.gitlabpages.inria.fr/astec/astec_parameters.html#astec-fusion-parameters)

To start the fusion test step , please download the template parameters file from this [link](https://drive.google.com/file/d/1R2LBab06kURCe23PGS3XXA-LGVp5Io4O/view?usp=drive_link) , and save it to your embryo folder. Your file architecture should look like this : 
``` 
     embryo name
     │   └───RAWDATA
     │       │───stack_0_channel_0_obj_left
     │       │───stack_0_channel_0_obj_right
     │       │───stack_1_channel_0_obj_left
     │       │───stack_1_channel_0_obj_right
     │       └───... (more if you have another channel)
     └── run_test_fusion.py
```

And then , you should edit it to bind the good parameter for your embryo : 


```
parameters["embryo_name"] = '<name>' : replace <name> with the name of your embryo folder
parameters["begin"]=1 : for test, should be set to the only time point , and be the same than "end"
parameters["end"]=1 : for test, should be set to the only time point , and be the same than "begin"
parameters["user"] = '<UI>' : for every step , will be used to store an history of the data,<UI>  should be replaced by experimentator name and surname first letters
```

Setting up those parameters should be enough to start the first fusion test. In order to do so , open a terminal in the embryo folder ;

``` 
     embryo name   <-- Open a terminal here
     │   └───RAWDATA
     │       │───stack_0_channel_0_obj_left
     │       │───stack_0_channel_0_obj_right
     │       │───stack_1_channel_0_obj_left
     │       │───stack_1_channel_0_obj_right
     │       └───... (more if you have another channel)
     └── run_test_fusion.py
```

and then you can start the process with those commands : 

`conda activate AstecManager` \
`python3 run_test_fusion.py` 

This step will take a few minutes to run, and will generate a fusion image in this directory : 
``` 
     │──embryo name
     │    │───RAWDATA
     │    │    └─── ...
     │    └───FUSE
     │        └─── FUSE_01_test
     │           │─── embryo_name_fuse_t040.nii
     │           └─── ... 
     └─ run_test_fusion.py
``` 
###### Verify fusion 

Now that you generated the first fusion test , you need to verify the quality of the fusion. For this , we have to visually check if the generated image is correct, this can be done using
Fiji [(here is a link to a documentation on how to use Fiji)](https://imagej.net/tutorials/). Here is an example of what a wrong fusion rotation may look like , which is the first error you can find : 


| Example of fusion with correct rotation | Example of fusion with wrong rotation |
|:---------------------------------------:|:-------------------------------------:|
|  ![](doc_images/good_orientation.png)   | ![](doc_images/wrong_orientation.png) |

If the rotation seems good , you will need to check in the temporary images generated by the fusion , if the different steps were well parameter


Inside each fusion folder , you can find a folder called "XZSECTION_XXX" where "XXX" is the time point fused. 
Inside the folder , you will see 4 images : 

- embryoname_xyXXXX_stack0_lc_reg.mha
- embryoname_xyXXXX_stack0_lc_weight.mha
- embryoname_xyXXXX_stack0_rc_reg.mha
- embryoname_xyXXXX_stack0_rc_weight.mha
- embryoname_xyXXXX_stack1_lc_reg.mha
- embryoname_xyXXXX_stack1_lc_weight.mha
- embryoname_xyXXXX_stack1_rc_reg.mha
- embryoname_xyXXXX_stack1_rc_weight.mha

|       Left-cam stack 0 reg + weighting       |       Stack cameras matching        |       Stack 0 and 1 matching       |
|----------------------------------------------|-------------------------------------|------------------------------------|
| ![](doc_images/fuse_extraction_lcstack0.png) | ![](doc_images/leftandrightcam.png) | ![](doc_images/stacksmatching.png) |

On the left image  of the table you can see that the registration image (left), is matching the weighting used for the computation. It means that the weighting is correct.
On the middle image , you can see that the left camera and right camera of the same stack is matching.
On the right image, you can see that both stacks images are matching , so the fusion will be correct.

If the xzsection registration (the images containing <_reg> inside their names) are matching , and the weighing seem to be coherent , you can skip to final fusion step. 

If the xzsection registration (the images containing <_reg> inside their names) do not seem to match , either withing the same stack , or between the 2 different stacks, it means that you will need to explore 2 more parameters.
We made this step easier by creating a mode that tests automatically all 4 possibles combination for the parameters.

Modify your "run_test_fusion.py" file to change this line : 

```
manager.test_fusion(parameters,parameter_exploration=False)
```

to 

```
manager.test_fusion(parameters,parameter_exploration=True)
```

and then start your test step again , the same way you started it before : 

`conda activate AstecManager` \
`python3 run_test_fusion.py` 


if the xzsection weighting is not matching the image correctly, you may need to change the weighting function used in the fusion computation. In order to do this , modify your "start_fusion_test.py" file to add this line:
```
parameters["fusion_weighting"]= set it to "'uniform'" , "'ramp'" or "'corner'"
```
BEFORE the final line : 

```
manager.test_fusion(...
```

When you changed the file , you can run the fusion test again

`conda activate AstecManager` \
`python3 run_test_fusion.py` 

#### Final fusion

Now that you have finished the fusion test step , found the parameters that gives you a good result , and verified them on the fusion image itself + the temporary images generated in the XZSECTION
you can start the final fusion by downloading the parameter file here : 

The parameter find can be found [here](https://drive.google.com/file/d/17qKu1OZrNlJed-YAdBphX-mfjrG87yqj/view?usp=drive_link)

Save it to the embryo folder, in the same location where you saved the test file , and start by editing it : 

```
parameters["embryo_name"] = '<name>' : replace <name> with the name of your embryo folder
parameters["begin"]=0 : for fusion, should be set to the first time point of the sequence
parameters["end"]=100 : for fusion, should be set to the last time point of the sequence
parameters["user"] = '<UI>' : for every step , will be used to store an history of the data,<UI>  should be replaced by experimentator name and surname first letters
parameters["number_of_channels"] = 1 : change this to the number of channel in the raw images acquisition. The same fusion will be applied to all channels
parameters["omero_config_file"]= '/path/to/the/omero/config/file' : if you want to upload the result images of the fusion, you can enter the path to your omero configuration file. If you didn't create the omero
file , please read the "Data Manager Integration" section of this documentation. After fusion, a new dataset will be created in the embryo project on OMERO (created if it doesn't exist) , and will contain all of the fusion images
```

Finally , you will need to modify the following lines : 

```
parameters["fusion_strategy"]= 'hierarchical-fusion'
parameters["acquisition_orientation"]= 'left'
```

If the fusion test ran fine during the test step , and you didn't need to start the 4 fusion test exploration, you can leave the lines as they are.
If not , please update them with the parameters that worked the best among the 4 tests fusion. 

  - if the FUSE_01_left_direct was the correct one , change the parameters to :
    ```
    parameters["fusion_strategy"]= 'direct-fusion'
    parameters["acquisition_orientation"]= 'left'
    ```
  - if the FUSE_01_left_hierarchical was the correct one , change the parameters to :
    ```
    parameters["fusion_strategy"]= 'hierarchical-fusion'
    parameters["acquisition_orientation"]= 'left'
    ```
  - if the FUSE_01_right_direct was the correct one , change the parameters to :
    ```
    parameters["fusion_strategy"]= 'direct-fusion'
    parameters["acquisition_orientation"]= 'right'
    ```
  - if the FUSE_01_right_hierarchical was the correct one , change the parameters to :
    ```
    parameters["fusion_strategy"]= 'hierarchical-fusion'
    parameters["acquisition_orientation"]= 'right'
    ```

And finally , if you added other parameters to the test file (for example weighing method modification) , please provide the corresponding lines in the final fusion file too. 

When all of this is ready , you can start the final fusion. Open a terminal in the embryo folder and run the following lines 

`conda activate AstecManager` \
`python3 run_final_fusion.py` 

The computation of the fusion step will take a few hours, depending on the number of time point in the embryo , and the number of channels to fuse. When finished , multiple new data will be generated : 
First, you can delete the following files and folders :
- folder FUSE/FUSE_01_left_direct
- folder FUSE/FUSE_01_left_hierarchical 
- folder FUSE/FUSE_01_right_direct 
- folder FUSE/FUSE_01_right_hierarchical

The final folder architecture after fusion will be this one :

``` 
experiment folder 
└───embryo specie
    │──embryo name
    │   │───analysis
    │   │    └─── fusion    
    │   │          └─── fusion_movie.mp4
    │   │───INTRAREG
    │   │    └─── INTRAREG_01_TEST
    │   │          └─── MOVIES
    │   │               └─── FUSE
    │   │                   └─── FUSE_01
    │   │                       └─── embryo_name_intrareg_fuse_tbegin-tend_xy0XXX.mha
    │   │───RAWDATA
    │   │    └─── ...
    │   └───FUSE
    │       └─── FUSE_01
    │          │─── embryo_name_fuse_t000.nii
    │          │─── embryo_name_fuse_t001.nii
    │          └─── ... 
```

### Fusion verification
To verify the final fusion , you can use the movie generated by the code. This movie presents the same slice of the fusion images through time.
By looking at the movie , the user can make sure that all the time points were fused correctly. 

You can find the movie in the following folder : "embryo_name/analysis/fusion/fusion_movie.mp4"

If, after the final fusion , the fusion_movie.mp4 file has not been generated , you can find this movie as an image in the following folder : "embryo_name/INTRAREG/INTRAREG_01_TEST/MOVIES/FUSE/FUSE_01/" . 

After opening the image in Fiji , you will see that it is a slice of the fusion image , where the Z axis (the slider at the bottom of image) correspond to this slide through time. 
To validate the fusion through time , make sure that the image orientation , and the fusion registration remains coherent, even if the embryo is slightly different, or may have moved between the 2 times.

## Computation of semantic data _(optional)_

The following section is a documentation about the generation of additional images for the segmentation process. 

Using a deep learning tool trained by the MorphoNet team, we are able to differentiate 5 classes in the embryo geometry : 
 - Background
 - Cytoplasm 
 - Cell to cell membrane contact (line)
 - 3 cells membrane contacts (point)
 - 3+ cells membrane contacts

From this output image it is possible to generate 2 differents segmentations , that will be computed faster than using the normal ASTEC process. 
 
- 1 will be generated using a watershed and seed segmentation , without time propagation. The computation is really fast but the result will be average
- 2 will be generated using the propagation power of ASTEC , using the membranes extracted from semantic image. A DEVELOPMENT SHOULD BE DONE TO EXTRACT PROPAGATION FROM ASTEC AND USE IT IN A MORE EFFICIENT WAY

- In the team , we use a computer called loki. To get access to Loki using ssh , first ask the team.

To start the computation  , you first need to get the identifier of your dataset on omero.
For this goes to omero , find your project and the dataset (green folder) , and look at the properties on the right.
You will find a line called "Dataset id : ". Copy the number on the right 

##### Run in a terminal , line by line the following :


`ssh loki.crbm.cnrs.fr` \
`conda activate morphodeep` \
`cd /data/MorphoDeep/morphodeep/morphodeep/Process/` \
`python3 Compute_Semantic_From_Omero.py -d id_dataset_omero`

After the computation , you will find a new dataset inside the omero project , called JUNC_name_of_fusion_dataset

There is no troubleshooting for this section , if you have a problem , you need to find a team member.

## Generation of membranes intensity image from semantic

When the semantic is done , and all the images are available on the data manager, you will have to download them on the computer that will compute the next steps. 


In order to do so , please download the following parameters file :  [here](https://drive.google.com/file/d/1kLDICrnLP6DQ-StGnTL7j76T2ybsIhXF/view?usp=drive_link) , in any folder. 

Please edit it : 
```
parameters["omero_authentication_file"] = None : replace None by the omero config you created before , if you didn't please refer to section "Data Manager Integration"
parameters["project_name"] = "" : write the name of the omero project of your dataset between the " " (should be the embryo name) 
# DATASET NAME ON OMERO
parameters["dataset_name"] = "" : write the name of the omero dataset of your dataset between the " " (should be JUNC_01) 
# PATH OF THE OUTPUT FOLDER
parameters["destination_folder"] = "" : write the path to the download folder. For semantic , shound be ( /path/to/embryo_name/JUNC/<name of the omero dataset>/ )
```

Open a terminal where the download parameters file is , and start the download by running : 

`conda activate AstecManager` \
`python3 download_dataset_from_omero.py`

When the download has finished, you should fine the images in the folder corresponding to <parameters["output_folder"]> 

We computed those semantic images to be able to create a faster, with better shaped cells , segmentation. In order to do so , we will transform the semantic images into fake intensities images.

In order to do so , please download the corresponding parameters file [here](https://drive.google.com/file/d/1uRnyEcQm2rEkwwzfUJ_kMb4CFhwP_T3r/view?usp=drive_link) , and store it in the embryo folder.


Please edit it : 
```
parameters["embryo_name"] = "embryo_name" # Name of the embryo
parameters["EXP_JUNC"] = "01" # Suffix of the semantic folder used as input of contour generation
parameters["omero_authentication_file"] = "None" # path to OMERO authentication file. None means no upload to OMERO , if bound the generated intensities image will be uploaded to OMERo
parameters["user"] = "UI" # initials of user running the membrane generation
```

When edited, you can start it by running in a terminal : 

`conda activate AstecManager` \
`python3 generate_enhanced_membranes_from_semantic.py`

The fake intensities images will be generated in the following folder : 

"FUSE/FUSE_<semantic_folder_suffix>_SEMANTIC"

## Segmentation using fake intensities images 

To be able to perform a propagated segmentation using the images generated before, you will need to perform the segmentation and curation of the first time point. Please read this documentation specific
part of the first time point segmentation before.

When the first time point segmentation is done, curated and stored in the MARS folder, and the generation of fake intensities image too (section above) , you can start the segmentation.

You need to download the corresponding parameters file  [here](https://drive.google.com/file/d/1huOkG4LmfDH6cmKe74pPI7g3PVmujt0O/view?usp=drive_link) , and store it in the embryo folder.


Please edit it : 

```
parameters["embryo_name"] = 'name' # Embryo Name
parameters["begin"] =0 # Beggining of embryo time range
parameters["end"] =0 # End of embryo time range
parameters["resolution"] = 0.3 # Resolution of the input and output images , 0.3 for normal images, 0.6 if working with downscaled images

parameters["EXP_FUSE"] = '01_SEMANTIC' # Suffix of Fusion folder used for segmentation
parameters["EXP_SEG"] = '01_SEMANTIC' # Suffix of output segmentation
parameters["EXP_INTRAREG"] = '01'
parameters["EXP_POST"] = '01_SEMANTIC' # Suffix of output post correction , should be the same then EXP_SEG

parameters["mars_path"] = "./MARS/"+str(parameters["embryo_name"])+"_mars_t{:03d}".format(parameters["begin"])+".nii" # Path to the curated first time point image , do not change if located in embryo_name/MARS/ folder
parameters["use_contour"]=False # If True, will use contour image in CONTOUR/CONTOUR_RELEASE_3 (or CONTOUR/CONTOUR_RELEASE_6/ depending on resolution) as an input for segmentation
parameters["apply_normalisation"]=False # If True, input images will be normalised to intensities [0:normalisation] for segmentation. If False , do nothing
parameters["normalisation"]=1000 # if apply_normalisation is True , value of normalisation
parameters["user"] = 'UI' # initials of user performing segmentation
parameters["omero_authentication_file"]= "None" # path to OMERO authentication file. None means no upload to OMERO
parameters["intensity_enhancement"] = "None"
parameters["morphosnake_correction"] = False
```

You don't need to update a lot of parameters in this segmentation , because it has nearly no parameterization. Make sure :


- "embryo_name" is set to embryo name
- "begin" is set to first time point
- "end" is set to last time point 
- "omero_authentication_file" is set if you need to upload the output data to OMERO 


When edited, you can start it by running in a terminal : 

`conda activate AstecManager` \
`python3 run_segmentation_propagated_semantic.py`

## Contours _(optional)_

The following section is a documentation about the generation of additional input images used for the segmentation pipeline. Most of the segmentations errors we may face come from the external part of the embryo (cells in contact with the background)

Using a deep learning tool trained by the MorphoNet team, we are able to generate a mask image , separating the background from the embryo . 
This tool need a powerful computer to run , and should not be used on the user machine.

In the team , we use a computer called loki. To get access to Loki using ssh , first ask the team.

To start the computation  , you first need to get the identifier of your dataset on omero.
For this goes to omero , find your project and the dataset (green folder) , and look at the properties on the right.
You will find a line called "Dataset id : ". Copy the number on the right 

##### Run in a terminal , line by line the following :


`ssh loki.crbm.cnrs.fr` \
`conda activate morphodeep` \
`cd /data/MorphoDeep/morphodeep/morphodeep/Process/` \
`python3 Compute_Semantic_From_Omero.py -d id_dataset_omero`

After the computation , you will find a new dataset inside the omero project , called JUNC_name_of_fusion_dataset

There is no troubleshooting for this section , if you have a problem , you need to find a team member.

When the semantic computation is done , and all the images are available on the data manager, you will have to download them on the computer that will compute the next steps. 
In order to do so , please download the following parameters file :  [here](https://drive.google.com/file/d/1kLDICrnLP6DQ-StGnTL7j76T2ybsIhXF/view?usp=drive_link) , in any folder. 

Please edit it : 
```
parameters["omero_authentication_file"] = None : replace None by the omero config you created before , if you didn't please refer to section "Data Manager Integration"
parameters["project_name"] = "" : write the name of the omero project of your dataset between the " " (should be the embryo name) 
# DATASET NAME ON OMERO
parameters["dataset_name"] = "" : write the name of the omero dataset of your dataset between the " " (should be JUNC_FUSE_01) 
# PATH OF THE OUTPUT FOLDER
parameters["destination_folder"] = "" : write the path to the download folder. For semantic , shound be ( /path/to/embryo_name/JUNC/<name of the omero dataset>/ )
```

Open a terminal where the download parameters file is , and start the download by running : 

`conda activate AstecManager` \
`python3 download_dataset_from_omero.py`

When the download has finished, you should fine the images in the folder corresponding to <parameters["output_folder"]> 

With the background/embryo mask images downloaded , you are now able to generate the contour images, used for segmentation preprocessing.

The following code will automatically compute the contours images, that will be used later. The contours are computed by smoothing and increasing the thickness of the edge between background and embryo. The code is able to generate a segmentation using the semantic image.
This segmentation does not take advantage of ASTEC propagation , and is very basic.

To run the contour and/or segmentation generation, please download the following parameters file [here](https://drive.google.com/file/d/1AkUQiaJKP062tXgKXcSQpZR9syTPsRRg/view?usp=drive_link) , and store it inside your embryo folder

Edit the file like this : 

```
parameters["embryo_name"] = "" : Name of your embryo folder
parameters["EXP_JUNC"] = "01" : replace <01> with the name of the folder where you downloaded background images (if it's different) removing the "JUNC_" part
parameters["omero_authentication_file"] = None : replace None by the omero config you created before , if you didn't please refer to section "Data Manager Integration" if you want to upload contours to the data manager automatically
parameters["user"] = "UI" : for every step , will be used to store an history of the data,<UI>  should be replaced by experimentator name and surname first letters
```

For a normal usage , computers are generated on full resolution fusion images and with a specific normalisation applied to contour image intensities , that you can find in those lines : 

```
parameters["normalisation"] = 1000 # Normalisation of intensities in the output image (contour intensities will be in [0:normalisation]
parameters["resolution"]=0.3 # Resolution of the background input images , and the output contour generated
```
Finally , you need to specify if you want to generate the contour , and/or the segmentation. Change the following lines by specifying True if you want to generate the corresponding images, False otherwise : 

```
parameters["compute_contour"] = True # If True, will generate contour using junctions, if False , will not.
parameters["compute_segmentation"] = True # If True, will generate "semantic" segmentation using junctions, if False , will not.
```

Please update the corresponding values if you know what you are doing.

When all the parameters are written , you can open a terminal where the download parameters file is , and start the generation by running : 

`conda activate AstecManager` \
`python3 generate_images_from_junction.py`

The code will create this folder "CONTOUR/CONTOUR_<EXP_JUNC>/"  , where the contour images are stored
if you chose to segment, a new folder is created : "SEG/SEG_SEMANTIC_<EXP_JUNC>/", where the segmentation images are stored

There is no troubleshooting for this section , if you have a problem , you need to find a team member

## First time point segmentation

The segmentation process for our data is based on the propagation. Using the previous time step segmentation , the algorithm compute new segmentations , and then detect the cell divisions ( or not ) to compute the lineage. 
In order to start the process , it is needed to have a first time point segmentation, that SHOULD be empty of any segmentation errors. 
We now have 2 systems to compute the first time point segmentation :  

### MARS 

MARS is the standard segmentation algorithm used for the first time point with our data.
To start MARS algorithm , please download the parameter file [here](https://drive.google.com/file/d/1T2qu96RMzeNmIsv2D2yj22biOFGvPmgb/view?usp=drive_link) and store it in your embryo folder

Edit it : 

```
parameters["embryo_name"] = "name": replace <name> with the name of your embryo folder
parameters["begin"]=1 : replace '1' with the first time point of the fusion sequence
parameters["end"]=1 :  replace '1' with the first time point of the fusion sequence (HAS TO BE EQUAL TO parameters["begin"])
parameters["resolution"] = 0.3 : Only change this if you are working in half resolution (it should be 0.6 with half resolution)
parameters["EXP_FUSE"] = '01' : Name of the fusion exp for the intensity images 
parameters["use_contour"] = True : Should be <True> to use the contour for the segmentation of the first time point, <False> otherwise 
parameters["apply_normalisation"] = True : Should be <True> if you want to normalize input images intensities between [0;normalisation], <False> otherwise 
parameters["normalisation"] = 1000 # if apply_normalisation is True , value of normalisation applied
parameters["user"]= 'UI' : for every step , will be used to store an history of the data,<UI>  should be replaced by experimentator name and surname first letters

```

Open a terminal in your embryo folder , and start the MARS by running : 

`conda activate AstecManager` \
`python3 run_mars.py`

The code will generate 2 segmentations of the first time point, the difference between the being how the intensities of the input images are integrated together to get an enhanced images. 

The embryo folder hierarchy should look like this : 

``` 
experiment folder 
└───embryo specie
    │──embryo name
    │   │───SEG
    │   │    │─── SEG_mars_add
    │   │    │   │─── LOGS
    │   │    │   └─── embryo_name_mars_t000.nii
    │   │    │   
    │   │    │─── SEG_mars_max
    │   │    │   │─── LOGS
    │   │    │   └─── embryo_name_mars_t000.nii
    │   │───INTRAREG
    │   │    └─── ...
    │   │───RAWDATA
    │   │    └─── ...
    │   └───FUSE
    │       └─── ... 
```

To compare the two MARS segmentations generated by this step , follow the steps detailed in the [First time point verification section](#firstverif) for each segmentation.

### MorphoNet Cellpose integration 

MorphoNet application has acquired a new plugin , taking in input the intensity image (fusion) of a time point , and generating a segmentation using a deep learning model.

To install MorphoNet Standalone, please refer to the MorphoNet documentation for application by [clicking here](https://morphonet.org/help_standalone) 

Then add the intensity images to your MorphoNet local datasets following the documentation [here](https://morphonet.org/help_standalone#add_local) 

Use the MorphoNet curation module to generate a segmentation from your intensity images. To use the curation menu , please read the documentation [here](https://morphonet.org/help_app?menu=curations)

The documentation for CellPose plugin, used to generate the segmentations , can be found [here](https://morphonet.org/help_app?menu=curations#cellpose)

After generating the segmentation , you can curate all the errors using the plugins detailed [here](https://morphonet.org/help_curation) , or follow the curation example documentation [here](https://morphonet.org/help_curation)


<h3 id="firstverif"> First time point verification </h3>

The only way to verify the quality of the segmentation generated by the first time point segmentation algorithm chosen is to import this data in MorphoNet, and find the different errors.

#### Import of the data in MorphoNet 

This section is only needed if you used MARS algorithm to generate the segmentation. The idea is to import both segmentation (mars_add and mars_max) as MorphoNet local datasets.  

To install MorphoNet Standalone, please refer to the MorphoNet documentation for application by [clicking here](https://morphonet.org/help_standalone) 

You can find a documentation in MorphoNet help to create a local dataset [here](https://morphonet.org/help_standalone#add_local)

#### Verification of the first point and curation

After importing the dataset in MorphoNet application , locate the different errors in each of the segmentation generated, and find the one with the least errors.

When the segmentation is chosen , curate it using the documentation example found [here](https://morphonet.org/help_curation)


### First time point storage 

When the first time point is curated, please store it in a new folder inside the embryo folder. This new folder should be called MARS, and contain only the first time point segmentation image.

Here is the architecture of the embryo folder at this step : 

``` 
experiment folder 
└───embryo specie
    │──embryo name
    │   │───SEG
    │   │    └─── ...
    │   │───MARS
    │   │    └─── embryo_name_mars_t000.nii
    │   │───INTRAREG
    │   │    └─── ...
    │   │───RAWDATA
    │   │    └─── ...
    │   └───FUSE
    │       └─── ... 
```
## Data downscaling _(optional)_ : Fusions , Contours and First time point

Later , we will see that the segmentation step is the longest step of the pipeline, and has to be split in 2 sub steps. To lower the computational time when it's possible, 
it is advised to work with lower resolution images for test steps. 

The lower resolution computation is automatic , and will be applied to the following images : 
- (1) the final fusion images 
- (2) the first time point segmentation image 
- (3) the contours images corresponding to the fusion _(1)_

Note : Later in the document, full resolution images may be referenced as 0.3 resolution , and half resolution images (output of this step) may be referenced as 0.6 resolution. 

To apply data downscaling , download the parameter file [here](https://drive.google.com/file/d/18NrK0Po6GndH9C89bZZSngKomyiVIJWT/view?usp=drive_link), and store it in your embryo folder.

Edit it : 

``` 
parameters["embryo_name"] = "name" # Embryo Name
parameters["apply_on_contour"] = True # If True, will apply downscaling to contour images too
parameters["EXP_CONTOUR"] = "RELEASE_3" # Suffix of contour folder, not useful if "apply_on_contour" is set to False
parameters["EXP_CONTOUR_DOWNSCALED"] = "RELEASE_6" # Suffix of output contour folder after downscaling,  not useful if "apply_on_contour" is set to False
parameters["user"] = "UI" # initials of user running the downscaling
parameters["EXP_FUSE"] = "01" # Suffix of the fusion folder that will be downscaled
parameters["begin"] = 0 # Time of the first time point segmentation that will be downscaled
parameters["mars_file"]  = "/path/to/mars/file" # Path to the first time point segmentation to downscale (should be "MARS/embryo_name_mars_t000.nii")
parameters["resolution"] = 0.6 # Target resolution of the downscaling (0.6 = half resolution)
parameters["input_resolution"] = 0.3 # Resolution of the input images (0.3 = full resolution)
``` 

If you followed this documentation , the only parameters that should be modified are : embryo_name , user, mars_file and begin. 
When all the parameters are set, open a terminal in your embryo folder , and start the MARS by running : 

`conda activate AstecManager` \
`python3 run_downscaling.py`

This process is about 1 hour long , but this time may differ depending on your embryo time step count.

Here is the architecture of the embryo folder at this step : 

``` 
experiment folder 
└───embryo specie
    │──embryo name
    │   │───SEG
    │   │    └─── ...
    │   │───MARS
    │   │    └─── embryo_name_mars_t000.nii
    │   │───MARS06
    │   │    └─── embryo_name_mars_t000.nii
    │   │───INTRAREG
    │   │    └─── ...
    │   │───RAWDATA
    │   │    └─── ...
    │   │───CONTOUR (optional)
    │   │   │─── CONTOUR_RELEASE_3
    │   │   │    └─── embryo_name_contour_t000.nii
    │   │   └─── CONTOUR_RELEASE_6
    │   │        └─── embryo_name_contour_t000.nii
    │   └───FUSE
    │       │─── FUSE_01 
    │       │    └─── embryo_name_fuse_t000.nii
    │       └─── FUSE_01_down06
    │            └─── embryo_name_fuse_t000.nii
```

## Propagation of the segmentation

Now that we exported the first time point curated image, we will be able to use it as the source for the propagation.
Once more , exactly like the fusion , the segmentation will be divided in 2 steps.

- The first will be a test segmentation , divided in 4 set of parameters , running 2 by 2. It will be computed on a shorter range of time.
- The second will be the production segmentation , on the complete embryo time points, and followed by an automatic error curation. 

### Segmentation parameters test

This step is here to determine the set of parameters that give the best segmentation in output. This doesn't mean that it's the best you could find , but it will be the best among the 2 
principal parameters to tune for segmentation. 

The 2 parameters that are tested during this step are the following : 

- intensity_enhancement  :  algorithm chosen for membrane enhancement , see documentation [here](https://astec.gitlabpages.inria.fr/astec/astec_parameters.html#preprocessing-parameters)
- reconstruction_images_combination  :  preprocessed input image generation method , see documentation [here](https://astec.gitlabpages.inria.fr/astec/astec_parameters.html#preprocessing-parameters)

This step may run on full resolution image , it is highly advised to apply a downscaling before ! (cf [this section](#data-downscaling-_optional_--fusions--contours-and-first-time-point))

To start the test segmentation , download the parameter file [here](https://drive.google.com/file/d/1ZCGTD7Auli8gfWQIG-hNbFdQuDslfyyC/view?usp=drive_link) , and store it in your embryo folder.

Edit it : 

```
parameters["embryo_name"] = "name": replace <name> with the name of your embryo folder
parameters["begin"] =1 # Beggining of embryo time range
parameters["end"] =1 # End of embryo time range
parameters["resolution"] = 0.6 # Resolution of the input and output images , 0.3 for normal images, 0.6 if working with downscaled images
parameters["EXP_FUSE"] = '01_down06'# Suffix of Fusion folder used for segmentation
parameters["mars_path"] = "MARS06/"+str(parameters["embryo_name"].replace("'","").replace('','"'))+"_mars_t{:03d}".format(parameters["begin"])+".nii" # Path to the curated first time point image , do not change if located in embryo_name/MARS06/ folder
parameters["use_contour"]=True # If True, will use contour image in CONTOUR/CONTOUR_RELEASE_3 (or CONTOUR/CONTOUR_RELEASE_6/ depending on resolution) as an input for segmentation
parameters["apply_normalisation"] = True # If True, input images will be normalised to intensities [0:normalisation] for segmentation. If False , do nothing
parameters["normalisation"] = 1000 # if apply_normalisation is True , value of normalisation
parameters["user"] = 'UI' # initials of user performing segmentation
```

It's advised not to run the segmentation test on the complete embryo time range. An usual time range for test segmentation is about 60 to 80 time points.

When the file is edited and the parameters are set , open a terminal in your embryo folder , and start the segmentation propagation test by running : 

`conda activate AstecManager` \
`python3 run_test_segmentation.py`

Here is the architecture of the embryo folder at this step : 

``` 
experiment folder 
└───embryo specie
    │──embryo name
    │   │───SEG
    │   │    │─── SEG_test_maximum_gace
    │   │    │    │─── embryo_name_seg_t000.nii
    │   │    │    └─── ...    
    │   │    │─── SEG_test_addition_gace
    │   │    │    │─── embryo_name_seg_t000.nii
    │   │    │    └─── ...  
    │   │    │─── SEG_test_maximum_glace
    │   │    │    │─── embryo_name_seg_t000.nii
    │   │    │    └─── ...    
    │   │    └─── SEG_test_addition_glace
    │   │         │─── embryo_name_seg_t000.nii
    │   │         └─── ...  
    │   │───MARS
    │   │    └─── ...
    │   │───MARS06
    │   │    └─── ...
    │   │───INTRAREG
    │   │    └─── ...
    │   │───RAWDATA
    │   │    └─── ...
    │   │───REC-MEMBRANE
    │   │    │─── REC_test_maximum_gace
    │   │    │    │─── embryo_name_post_t000.nii
    │   │    │    └─── ...    
    │   │    │─── REC_test_addition_gace
    │   │    │    │─── embryo_name_post_t000.nii
    │   │    │    └─── ...  
    │   │    │─── REC_test_maximum_glace
    │   │    │    │─── embryo_name_post_t000.nii
    │   │    │    └─── ...    
    │   │    └─── REC_test_addition_glace
    │   │         │─── embryo_name_post_t000.nii
    │   │         └─── ...  
    │   │───REC-SEED
    │   │    │─── REC_test_maximum_gace
    │   │    │    │─── embryo_name_post_t000.nii
    │   │    │    └─── ...    
    │   │    │─── REC_test_addition_gace
    │   │    │    │─── embryo_name_post_t000.nii
    │   │    │    └─── ...  
    │   │    │─── REC_test_maximum_glace
    │   │    │    │─── embryo_name_post_t000.nii
    │   │    │    └─── ...    
    │   │    └─── REC_test_addition_glace
    │   │         │─── embryo_name_post_t000.nii
    │   │         └─── ...  
    │   │───POST
    │   │    │─── POST_test_maximum_gace
    │   │    │    │─── embryo_name_post_t000.nii
    │   │    │    └─── ...    
    │   │    │─── POST_test_addition_gace
    │   │    │    │─── embryo_name_post_t000.nii
    │   │    │    └─── ...  
    │   │    │─── POST_test_maximum_glace
    │   │    │    │─── embryo_name_post_t000.nii
    │   │    │    └─── ...    
    │   │    └─── POST_test_addition_glace
    │   │         │─── embryo_name_post_t000.nii
    │   │         └─── ...  
    │   │───CONTOUR (optional)
    │   │    └─── ...
    │   └───FUSE
    │       └─── ...

```

Even if segmentation images have been generated in the SEG folder , we will mainly focus on the images generated in the POST folder. The POST step is automatically integrated now , 
and is an automatic correction step , that lowers the number of over-segmented cells.

### Segmentation test verification

Now that the tests have been generated, how to verify which segmentation parameters sets are the best among the 4 ? 

#### Comparison with astecmanager

The segmentation test will generate , inside the "embryo_name/analysis/test_segmentation/" , 2 images files. 

The image named "early_cell_death.png" represents, for each segmentation folder, the proportion of cells missing before the last time points.

![EarlyDeathProportion](doc_images/early_cell_death.png "Example of early cell missing proportion plot")

The vertical axis represents the time points in the embryo , and the horizontal axis represents the different cells at the first time point.
Each point represents a cell dying too early, coming from the branch of the corresponding cell on the horizontal axis. For example , the cell pointed by the right arrows , means that a cell coming from the branch of the cell 50,111 , is missing after time point 110 .
The box pointed by the blue arrows means that a majority of cells missing too early for the corresponding starting cell on horizontal axis.

For this plot , we are looking for the least proportion of cells missing too early , or at least the ones missing as late as possible.

In this example , the "maximum" segmentation have way less cells missing (30% vs 70% for "addition" segmentation). But keep in mind that 30% of cells missing too early is a lot, but sometimes this situation can correspond to over segmentations stopping.

We will need another graph to understand how the embryo segmentations are on a global view :

The image named "cell_count.png" is the most important plot from the comparison. 

![CellCountComparison](doc_images/cell_count.png "Example of cell count plot")

The vertical axis represents the number of cells in the embryo, and the right axis the time points. 
In this plot, we will be looking for the embryo that has the most cell, because it will probably the segmentation with the less missing cells or under segmented cells errors. 
Keep in mind that if the number of cell is really high , other parameters could be better (with less over-segmented cells).
On top of the number of cells, the shape of the curve should follow the cell division pattern. For our embryos , it should look like a stair
shape, matching the cell divisions, and the plateau when no cells divide.

In this example, even if "addition_gace" and "addition_glace" seem to have more cells than the "maximum" segmentations , the curve for both "addition" are more random (no stair shape, growing and reducing again and again).
Even if they have less cells and still are slightly random , the "maximum" are probably better, even if they don't seem perfect.

With those 2 graphs , we can have a first idea of which parameter could be used. I would advise to load the segmentations in MorphoNet , and visually attest the quality : 

- Using the visualisation of the cells themselves
- Using the visualisation of the lineage 

#### Comparison with MorphoNet

##### Import of the data in MorphoNet 

The idea is to import all 4 segmentations as MorphoNet local datasets.  

To install MorphoNet Standalone, please refer to the MorphoNet documentation for application by [clicking here](https://morphonet.org/help_standalone) 

You can find a documentation in MorphoNet help to create a local dataset [here](https://morphonet.org/help_standalone#add_local)

##### Verification of the segmentation

After importing the dataset in MorphoNet application , locate the different errors in each of the segmentation generated, and find the one with the least errors.

You can look at the lineage for each segmentation , following the documentation [here](https://morphonet.org/help_lineage)
The parameters corresponding to this segmentation may be considered the best. 

### More parameters 

Sometimes , the 4 sets of parameters generated by default are not good enough. In this case , you may need to test new parameters. 

You can find a list of preprocessing parameters [here](https://astec.gitlabpages.inria.fr/astec/astec_parameters.html#preprocessing-parameters)

You can find a list of propagation parameters [here](https://astec.gitlabpages.inria.fr/astec/astec_parameters.html#astec-astec-parameters)

To test a parameter value , please add a line like this one : 

``` 
parameters["parameter_name"] = parameter_value # value should be surrounded by " if it's a text value , not if it's a boolean (True or False) , or numeric (integer or decimal)
``` 

make sure this line is added BEFORE the following line : 

``` 
manager.test_segmentation(parameters)
``` 

Before starting the segmentation again , delete the previous test done in the following folders : 

- POST
- SEG
- REC-MEMBRANE
- REC-SEED

### Segmentation propagation

When all the parameters and their values have been found during the test step , or you already knew them , it is time to propagate the segmentation. 

Download the parameter file [here](https://drive.google.com/file/d/1-nyaFO1d0AZVT3iy777uVWl9GYhrkGrH/view?usp=drive_link), and store it in your embryo folder.

Edit it : 

``` 
parameters["embryo_name"] = 'name' # Embryo Name
parameters["begin"] =0 # Beggining of embryo time range
parameters["end"] =0 # End of embryo time range
parameters["resolution"] = 0.3 # Resolution of the input and output images , 0.3 for normal images, 0.6 if working with downscaled images. Should be 0.3
parameters["EXP_FUSE"] = '01' # Suffix of Fusion folder used for segmentation
parameters["EXP_SEG"] = '01' # Suffix of output segmentation
parameters["EXP_POST"] = '01' # Suffix of output post correction , should be the same then EXP_SEG
parameters["mars_path"] = "./MARS/"+str(parameters["embryo_name"])+"_mars_t{:03d}".format(parameters["begin"])+".nii" # Path to the curated first time point image , do not change if located in embryo_name/MARS/ folder
parameters["use_contour"]=True # If True, will use contour image in CONTOUR/CONTOUR_RELEASE_3 (or CONTOUR/CONTOUR_RELEASE_6/ depending on resolution) as an input for segmentation
parameters["apply_normalisation"]=True # If True, input images will be normalised to intensities [0:normalisation] for segmentation. If False , do nothing
parameters["normalisation"]=1000 # if apply_normalisation is True , value of normalisation

parameters["user"] = 'UI' # initials of user performing segmentation

parameters["omero_authentication_file"]= "None" # path to OMERO authentication file. None means no upload to OMERO

parameters["reconstruction_images_combination"] = "addition" # This is the default value for this parameter , change it for the one found
parameters["intensity_enhancement"] = "glace" # This is the default value for this parameter , change it for the one found
``` 

If you need to add other parameters,  please add them like this one : 

``` 
parameters["parameter_name"] = parameter_value # value should be surrounded by " if it's a text value , not if it's a boolean (True or False) , or numeric (integer or decimal)
``` 

make sure this line is added BEFORE the following line : 

``` 
manager.prod_segmentation(parameters)
``` 

When parameters are set , open a terminal in your embryo folder , and start the segmentation propagation  by running : 

`conda activate AstecManager` \
`python3 run_final_segmentation.py`


Here is the architecture of the embryo folder at this step : 

``` 
experiment folder 
└───embryo specie
    │──embryo name
    │   │───SEG
    │   │    └─── SEG_01
    │   │         │─── embryo_name_seg_t000.nii
    │   │         └─── ...    
    │   │───MARS
    │   │    └─── ...
    │   │───MARS06
    │   │    └─── ...
    │   │───INTRAREG
    │   │    └─── INTRAREG_01
    │   │          │─── FUSE
    │   │          │    └─── FUSE_01
    │   │          │         │─── embryoname_intrareg_fuse_t000.nii
    │   │          │         └─── ...
    │   │          │─── POST
    │   │          │    └─── POST_01
    │   │          │         │─── embryoname_intrareg_lineage.xml
    │   │          │         │─── embryoname_intrareg_post_t000.nii
    │   │          │         └─── ...
    │   │          └─── ...
    │   │───RAWDATA
    │   │    └─── ...
    │   │───REC-MEMBRANE
    │   │    └─── REC_01
    │   │         │─── embryo_name_reconstruction_t000.nii
    │   │         └─── ...    
    │   │───REC-SEED
    │   │    └─── REC_01
    │   │         │─── embryo_name_reconstruction_t000.nii
    │   │         └─── ...    
    │   │───POST
    │   │    └─── POST_01
    │   │         │─── embryo_name_post_t000.nii
    │   │         └─── ...    
    │   │───CONTOUR (optional)
    │   │    └─── ...
    │   └───FUSE
    │       └─── ...

```

### Segmentation propagation additional outputs

On top of the segmentation images , and the automatically corrected images (located respectively in SEG/SEG_01/ and POST/POST_01/ folders ) , others data are generated automatically after this segmentation propagation : 

- "Intrareg" segmentation images , corresponding to image where embryo rotation and movements are compensated through times. Those transformations are applied on :
  - Fusion  images , in INTRAREG/INTRAREG_01/FUSE/FUSE_01/ Seg , and Post images.
  - Segmentation images , in INTRAREG/INTRAREG_01/SEG/SEG_01/ 
  - Post corrected images , in INTRAREG/INTRAREG_01/POST/POST_01/

- A complete set of embryo properties generated in the property file (xml) located in : INTRAREG/INTRAREG_01/POST/POST_01/

- A graph of missing cells distribution in all the branches of the segmentation in : analysis/prod_segmentation/early_cell_death.png

- A  graph of cell count through time of the segmentation in : analysis/prod_segmentation/cell_count.png


## Generation of embryo common properties _(optional)_

FIRST : If you have generated the segmentation propagation using this tool , the embryo property file should already contain the properties generated in this step. 
Please make sure they are present. If they are not , here is the steps to generate them.

This step needs that your embryo hierarchy contains the INTRAREG folders coming from the segmentation propagation. 

If intra registration hasn't been generated , please read the documentation [here](https://astec.gitlabpages.inria.fr/astec/astec_intraregistration.html) 


The hierarchy look like this : 

``` 
experiment folder 
└───embryo specie
    │──embryo name
    │   │───INTRAREG
    │   │    └─── INTRAREG_01
    │   │          │─── FUSE
    │   │          │    └─── FUSE_01
    │   │          │         │─── embryoname_intrareg_fuse_t000.nii
    │   │          │         └─── ...
    │   │          │─── POST
    │   │          │    └─── POST_01
    │   │          │         │─── embryoname_intrareg_lineage.xml
    │   │          │         │─── embryoname_intrareg_post_t000.nii
    │   │          │         └─── ...
    │   │          └─── ...
    │   └─── ...
```

To start the properties computation , please download the parameter file [here](https://seafile.lirmm.fr/f/66122dff1386497fb617/?dl=1) and save it to your embryo folder.

Edit it :

``` 
parameters["embryo_name"] = "name" # Name of the embryo
parameters["begin"] = 0 # First time point of segmentation images
parameters["end"] = 0 #Last time point of segmentation images
parameters["EXP_INTRAREG"] = "01" #Suffix of the INTRAREG folder to compute properties in (INTRAREG/INTRAREG_01/ usually)
parameters["EXP_POST"] = "01" #Suffix of the POST folder to compute properties in (INTRAREG/INTRAREG_01/POST/POST_01 usually)
parameters["EXP_FUSE"] = "01"#Suffix of the FUSE folder to compute properties in (INTRAREG/INTRAREG_01/FUSE/FUSE_01 usually)
``` 

When edited , open a terminal in your embryo folder , and start the properties computation by running : 

`conda activate AstecManager` \
`python3 generate_embryo_properties.py`

This step will modify the properties file found here (INTRAREG/INTRAREG_01/POST/POST_01/) , and generate (or update) the following properties : 

- cell_surface (in voxel unit)
- cell_barycenter (center of mass in voxel unit)
- cell_principal_values (issued from diagonalizing of the cell covariance matrix in voxel unit)
- cell_principal_vectors (vector corresponding to principal values above)
- cell_contact_surface (contact surfaces with adjacent cells in voxel unit)
- cell_names (automatic naming by reference to atlas of ascidian embryos)

More details can about properties generated be found in ASTEC documentation [here](https://astec.gitlabpages.inria.fr/astec/astec_properties.html)

## Generation of lineage distance properties _(optional)_

WARNING : this code needs the lineage distance library (treex) developed by the MOSAIC team. This library currently does not work on Mac new architecture, and only on Linux. 
This library is installed if possible during this tool installation process , but can be done specifically using the following : 

`conda activate AstecManager` \
`conda install -c mosaic treex`

In order to curate the remaining errors from the segmentation of the data, some additional information could be needed. One of them is an information providing, for each named cell lineage in the embryo , the distance to this cell symmetric.
With this information, it is easier to detect which branch of the lineage is likely to have a problem (symmetric cells lineage are supposed to be quite similar, a high distance could be a segmentation error)

In order to generate this property, you will need the segmentation properties files, and the cells have to be named in the property file.

To start the generation, please download the parameter file [here](https://drive.google.com/file/d/1mUQI2lYBtHVU3CE4D9fIv6X39iYtARmY/view?usp=drive_link).

This file does not work like the others parameters file , and do not need to be edited. It doesn't need to be stored in the embryo folder, and can be used multiple times.

To start the process , open a terminal in the parameters file folder, and run the following command : 

`conda activate AstecManager
python3 compute_lineage_distance.py -p <path to the property file>`

The code should take a few minutes to process the data and generate the properties. After running, 2 new properties are generated in the properties files : 

- "float_symetric_cells_branch_length_distance" => in this property, each cell (at each time point), is associated to the distance between this cell lineage branch to the symmetric cell lineage branch
- "float_symetric_cells_lineage_tree_distance" => in this property, each cell (at each time point), is associated to the distance between this cell lineage tree and its symmetric lineage tree