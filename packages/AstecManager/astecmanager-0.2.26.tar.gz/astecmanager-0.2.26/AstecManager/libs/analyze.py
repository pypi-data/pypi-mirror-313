import os
from os import listdir
import numpy as np
import re
from os.path import isfile, join
from AstecManager.libs.data import imread
import matplotlib.pyplot as plt
from AstecManager.libs.lineage import temporal_alignment, get_aligned_time, build_all_leaves, count_cells,Get_Cell_Contact_Surface, Get_Cell_Names, get_id_t
from AstecManager.libs.jsonlib import addDictToMetadata


def apply_analysis(list_lineage, list_noms, folder_out, embryo_name, begin, end,
                   is_test=True, ref_lineage=None, data_path=None):
    """ Generate the 2 plots used to analyze a segmentation for a list of property file

    :param list_lineage: List of properties files for analysis
    :type list_lineage: list
    :param list_noms: List of segmentation instances names
    :type list_noms: list
    :param folder_out: Folder path where to save the plots
    :type folder_out: str
    :param embryo_name: Name of the embryo
    :type embryo_name: str
    :param begin: First time point of segmentations
    :type begin: int
    :param end: Last time point of segmentations
    :type end: int
    :param is_test: If set to true , the plot will be computed for all the list of lineages (because we have 4 tests) , if False only for the first one (Default value = False)
    :type is_test: bool
    :param ref_lineage: If not None, specify a property file used as reference to align embryo (Default value = None)
    :type ref_lineage: str
    :param data_path: If not None, specify where to save the plots raw data csv   (Default value = None)
    :type data_path: str

    """
    print("-> Compute of the cell count plot")
    generate_compare(list_noms, list_lineage, folder_out=folder_out, embryo_name=embryo_name,
                     ref_lineage_path=ref_lineage, data_path=data_path)

    folder_exp = folder_out

    print("-> compute all min max leaves in for ")

    begin_temp = begin
    end_temp = end
    if not is_test:
        plotminmaxleaves_post(list_lineage[0], list_noms[0], begin_temp, end_temp, folder_out, data_path=None)
    else:
        plotminmaxleaves(list_lineage, list_noms, begin_temp, end_temp, embryo_name, folder_out, data_path=None)

    os.system("cd " + folder_exp + ' && `for f in *.py; do python3 "$f"; done`')
    os.system("cd " + folder_out + ' && rm generate_cell_count_multiples_.py')


def is_uncompressed_image(f):
    """ test if a filename correspond to an uncompressed image

    :param f: image name
    :type f: str
    :return: True if the filename correspond to an uncompressed image , false Otherwise
    :rtype: bool

    """
    return ".nii" in f or ".mha" in f or ".h5" in f or ".inr" in f


def generate_compare(input_names, list_lineage, folder_out="DATA/OUT/", embryo_name="",
                     remove_times=None, only_times=None,ref_lineage_path=None,
                     data_path=None):
    """ Generate the cell count plot used for segmentation analysis. Can be generated with a reference property file to
    align embryos segmentation. If multiple property files are given, the cell count will be plotted on the same image.

    :param input_names: List of segmentation instances names
    :type input_names: list
    :param list_lineage: List of properties files to generate cell count
    :type list_lineage: list
    :param folder_out: Path to the folder where plot image will be saved (Default value = "DATA/OUT/")
    :type folder_out: str
    :param embryo_name: Name of the embryo (Default value = "")
    :type embryo_name: str
    :param remove_times: List of time points to remove from the cell count, None means remove nothing (Default value = None)
    :type remove_times: list
    :param only_times: List of time points to plot , excluding all others. None means apply on all times  (Default value = None)
    :type only_times: list
    :param ref_lineage_path: Path to a property file that will be used as reference to align segmentations (Default value = None)
    :type ref_lineage_path: str
    :param data_path: Folder path to save raw plot data (Default value = None)
    :type data_path: str

    """
    folder_exp = ""
    for embryoname in input_names:
        if embryoname is not None:
            folder_exp += embryoname + "_"

    for lineage in list_lineage:
        if not os.path.isfile(lineage):
            print(lineage + " is not a file , check for typos")
            return

    if data_path is not None:
        if not os.path.isdir(data_path):
            os.makedirs(data_path)
    list_count = {}
    list_name = []
    list_histo = []
    ref_cell_count = None
    if ref_lineage_path != None:
        ref_cell_count = count_cells(ref_lineage_path, remove_time=([] if remove_times is None else remove_times),
                                     only_times=[] if only_times is None else only_times) #Generate cell count for reference
    for i in range(0, len(list_lineage)): # Generate cell count for lienages
        count = count_cells(list_lineage[i], remove_time=([] if remove_times is None else remove_times),
                            only_times=[] if only_times is None else only_times)
        txt = "" #Save the raw data to csv
        for key in count:
            txt += str(key) + ":" + str(count[key]) + ";"
        if data_path is not None:
            f = open(os.path.join(data_path, str(input_names[i]) + "-cell-count.csv"), "w+")
            f.write(txt)
            f.close()

        if ref_lineage_path != None:
            a, b = temporal_alignment(ref_lineage_path, list_lineage[i]) #ASTEC temporal alignment for embryos
            temp_count = {}
            for time in count:
                print("aligned time : " + str(get_aligned_time(time, a, b)) + " get count " + str(
                    count[time]) + " from time init : " + str(time))
                # TODO : verifier si on doit pas prendre le temps aligné de l'embryon
                temp_count[get_aligned_time(time, a, b)] = count[time] # cell counts are shifted using alignement
            count = temp_count
        list_histo.append(count)
        for t in count:
            list_count[input_names[i]] = [count[t]]
        list_name.append(input_names[i].replace("SEG_test_", ""))
        parameters = {}
        parameters["list_embryo_name"] = plot_variables(list_name, False)
        parameters["list_cell_count_by_time"] = plot_variables(list_histo, False)
        if embryo_name != "":
            parameters["embryo_name"] = plot_variables(embryo_name, True)
        if ref_lineage_path != None:
            save_cell_count_plot("cell_count_multiples", list_name, list_histo, folder_out,
                                 cell_count_ref=ref_cell_count,embryo_name=embryo_name) # plot with ref
        else:
            save_cell_count_plot("cell_count_multiples", list_name, list_histo, folder_out,embryo_name=embryo_name) # plot without ref


def save_cell_count_plot(plot_title, list_names, list_count, folder_out, cell_count_ref=None,embryo_name=""):
    """ Plot the cell count data given in parameters to a file , used for segmentation analysis

    :param plot_title: Title of the plot (not used anymore)
    :type plot_title: str
    :param list_names: List of segmentation instances names
    :type list_names: list
    :param list_count: List of dict corresponding to cell count by time point in each segmentation
    :type list_count: dict
    :param folder_out: Folder where the the plot image will be saved
    :type folder_out: str
    :param cell_count_ref: If not None, dict of the cell count by time point for the reference  (Default value = None)
    :type cell_count_ref: dict

    """
    list_cell_count_by_time = list_count
    import matplotlib.transforms as transforms
    folder_out = folder_out
    list_embryo_name = list_names
    if not os.path.isdir(folder_out):
        os.makedirs(folder_out)

    print(">>Cells counted, saving to image result")
    title = "cell_count"
    plt.figure(figsize=(10, 6)) # Setup figure
    plt.title("Cell count along time" + " " + embryo_name)
    plt.xlabel("Time")
    plt.ylabel("Cell count")
    for i in range(0, len(list_cell_count_by_time)):# plot each cell count for embryo
        print(str(list_embryo_name[i]) + " -> " + str(list_cell_count_by_time[i]))
        times = []
        cell_counts = []
        cell_count_by_time = list_cell_count_by_time[i]
        for time in cell_count_by_time:
            times.append(time)
            cell_counts.append(cell_count_by_time[time])
        plt.plot(times, cell_counts, '-', label=list_embryo_name[i], alpha=0.5)
    if cell_count_ref is not None: # plot reference cell count
        timesref = []
        cell_countsref = []
        for time in cell_count_ref:
            timesref.append(time)
            cell_countsref.append(cell_count_ref[time])
        plt.plot(timesref, cell_countsref, '-', label="reference", color='grey', alpha=0.5)
    trans = transforms.blended_transform_factory(
        plt.gca().get_yticklabels()[0].get_transform(), plt.gca().transData) #Extract transformations from the Y axis (to plot stages lines) , do not change
    stages = [64,72,116,184]
    for stage in stages: # Plot a line for each stage , where cell count should be constant
        plt.axhline(y=stage,color='grey',alpha=0.3)
        plt.text(0, stage, "{:.0f}".format(stage), color="grey", transform=trans,
                ha="right", va="center")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(folder_out, title + ".png"))
    plt.clf()


def plotminmaxleaves(lineage_list, embryo_name_list, start_time, end_time, embryo_name, folder_out="DATA/OUT/",
                     data_path=None):
    """ Plot the distribution of cells missing during segmentation lineages. This version takes up to 4 segmentation in input
    (used for test segmentation step). A version exist for only one segmentation

    :param lineage_list: List of properties file to get lineage from
    :type lineage_list: list
    :param embryo_name_list: List of embryo names , same order than lineage list
    :type embryo_name_list: list
    :param start_time: First time point of lineage
    :type start_time: int
    :param end_time: Last time point of lineage
    :type end_time: int
    :param embryo_name: Name of the embryo
    :type embryo_name: str
    :param folder_out: If specified , path to the folder where the plot will be stored (Default value = "DATA/OUT/")
    :type folder_out: str
    :param data_path: Path to folder to store the raw plot data(Default value = None)
    :type data_path: str

    """
    if folder_out != "":
        if not os.path.exists(folder_out):
            os.makedirs(folder_out)

    if data_path is not None:
        if not os.path.isdir(data_path):
            os.makedirs(data_path)
    fig, ax = plt.subplots(2, 2)

    fig.suptitle("Early cell death detection in branch")
    cell_keys_info = {}
    timefor64cells = start_time
    finalx = []
    current_axis_x = 0
    current_axis_y = 0
    activate_name_use = False
    for i in range(0, len(lineage_list)): # Plot the missing cells for each properties file
        lineage = lineage_list[i]
        if has_info_lineage(lineage, "cell_name") or has_info_lineage(lineage, "cell_contact_surface") and activate_name_use: #If the lineage has contact surface, we can start the plot at 64 cells for all embryos. Deactivated for now
            timefor64cells = -1
            cellcountfortime = 64
            cellforlineage = dict(sorted(count_cells(lineage).items()))
            for time in cellforlineage:
                if cellforlineage[time] >= 64:
                    timefor64cells = int(time)
                    cellcountfortime = int(cellforlineage[time])
                break
        cell_keys_by_time, final_proportion, mars_ids1, all_leaves = build_all_leaves(lineage, timefor64cells,
                                                                                      end_time)
        txt = "" # save all data to csv
        if data_path is not None:
            for i in range(0, len(all_leaves)):
                txt += str(mars_ids1[i]) + ":" + str(all_leaves[i]) + ";"
            txt += str(final_proportion)
            f = open(os.path.join(data_path, str(embryo_name)) + "-early-cell-death.csv", "w+")
            f.write(txt)
            f.close()
        cell_keys_info[lineage] = cell_keys_by_time

        finalx = []
        lineagepath = None
        if has_info_lineage(lineage, "cell_name") and activate_name_use: #Use names for x axis
            nameinit = get_cell_names(lineage, mars_ids1)
            finalx = nameinit
        elif has_info_lineage(lineage, "cell_contact_surface") and activate_name_use: #if no cell name , auto generate them for x axis
            lineagepath = auto_name_time(lineage, cellcountfortime)
            nameinit = get_cell_names(lineagepath, mars_ids1)
            finalx = nameinit
        else: # X axis use cell ids
            for idcell in mars_ids1:
                finalx.append(format_cell_id(idcell))
        if lineagepath is not None:
            os.system("rm " + str(lineagepath))
        ax[current_axis_x, current_axis_y].plot([], [], ' ',
                                                label="early cell missing:" + str(round(final_proportion, 3)) + "%") # plot to write in legend the proportion
        print(str(len(all_leaves)) + " - " + str(len(finalx)))
        if len(all_leaves) > 0: # Generate the box plots
            ax[current_axis_x, current_axis_y].boxplot(all_leaves, labels=finalx)
        ax[current_axis_x, current_axis_y].set_ylim([start_time, end_time]) #Update the axis labels and limits
        ax[current_axis_x, current_axis_y].set_title(embryo_name_list[i].replace("SEG_test_", ""))
        ax[current_axis_x, current_axis_y].set_xticklabels([])
        if current_axis_y == 0:
            ax[current_axis_x, current_axis_y].set_ylabel("Time of cell missing")
        if current_axis_x == 1:
            ax[current_axis_x, current_axis_y].set_xlabel("Lineage branch")
        ax[current_axis_x, current_axis_y].legend()
        current_axis_x = (current_axis_x + 1) % 2
        if current_axis_x == 0:
            current_axis_y += 1 % 2

    print("Saving to identity card")
    fig.tight_layout()
    fig.set_size_inches(18.5, 10.5)
    fig.suptitle("Early cell missing for " + str(embryo_name), fontsize=14)
    fig.savefig(folder_out + "/early_cell_death.png")


def plotminmaxleaves_post(lineage, embryo_name, start_time, end_time, folder_out="DATA/OUT/", data_path=None,suffix_file=""):
    """ Plot the distribution of cells missing during segmentation lineages. This version takes only 1 segmentation in input
     (used for production segmentation step). A version exist for  test segmentation (up to 4 properties files)

     :param lineage_list: List of properties file to get lineage from
     :type lineage_list: list
     :param embryo_name_list: List of embryo names , same order than lineage list
     :type embryo_name_list: list
     :param start_time: First time point of lineage
     :type start_time: int
     :param end_time: Last time point of lineage
     :type end_time: int
     :param embryo_name: Name of the embryo
     :type embryo_name: str
     :param folder_out: If specified , path to the folder where the plot will be stored (Default value = "DATA/OUT/")
     :type folder_out: str
     :param data_path: Path to folder to store the raw plot data(Default value = None)
     :type data_path: str

     """
    if folder_out != "":
        if not os.path.exists(folder_out):
            os.makedirs(folder_out)
    if data_path is not None:
        if not os.path.isdir(data_path):
            os.makedirs(data_path)
    fig = plt.figure()

    fig.suptitle("Early cell death detection in branch")
    cell_keys_info = {}
    timefor64cells = start_time
    finalx = []
    activate_name_use = False
    if has_info_lineage(lineage, "cell_name") or has_info_lineage(lineage, "cell_contact_surface") and activate_name_use: # if active, the graph starts at 64 cells with named lineage branch. Deactivated for now
        timefor64cells = -1
        cellcountfortime = 64
        cellforlineage = dict(sorted(count_cells(lineage).items()))
        for time in cellforlineage:
            if cellforlineage[time] >= 64:
                timefor64cells = int(time)
                cellcountfortime = int(cellforlineage[time])
            break
    cell_keys_by_time, final_proportion, mars_ids1, all_leaves = build_all_leaves(lineage, timefor64cells,
                                                                                  end_time) # generate the missing cells distribution

    txt = ""
    if data_path is not None: # save raw data to csv
        for i in range(0, len(all_leaves)):
            txt += str(mars_ids1[i]) + ":" + str(all_leaves[i]) + ";"
        txt += str(final_proportion)
        f = open(os.path.join(data_path, str(embryo_name)) + "-early-cell-death.csv", "w+")
        f.write(txt)
        f.close()
        name = lineage.replace("\\", "/").split("/")[-1]
    cell_keys_info[lineage] = cell_keys_by_time

    finalx = []
    lineagepath = None
    if has_info_lineage(lineage, "cell_name") and activate_name_use: # If has cell name , compute them to use them as x axis , deactivate for now
        nameinit = get_cell_names(lineage, mars_ids1)
        finalx = nameinit
    elif has_info_lineage(lineage, "cell_contact_surface") and activate_name_use: # if no cell name , generate them
        lineagepath = auto_name_time(lineage, cellcountfortime)
        nameinit = get_cell_names(lineagepath, mars_ids1)
        finalx = nameinit
    else: # use ids of cell for x axis
        for idcell in mars_ids1:
            finalx.append(format_cell_id(idcell))
    if lineagepath is not None:
        os.system("rm " + str(lineagepath))
    plt.plot([], [], ' ', label="early cell missing:" + str(round(final_proportion, 3)) + "%") # this plot is here to create a legend with proportion of missing cells
    if len(all_leaves) > 0:
        plt.boxplot(all_leaves, labels=finalx) # plot all distributions
    plt.ylim([start_time, end_time]) # setup title , labels and limits
    plt.title(embryo_name.replace("SEG_test_", ""))
    plt.xticks(rotation=90)
    plt.legend()
    plt.xlabel("Lineage branch")
    plt.ylabel("Time of cell missing")

    print("Saving to identity card")
    # fig.tight_layout()
    # fig.set_size_inches(18.5, 10.5)
    plt.title("Early cell missing for " + str(embryo_name), fontsize=14)
    fig.savefig(folder_out + "/early_cell_death_"+suffix_file+".png")


def camerastacksignaltonoise(axis, folder_images, analysisfolder, title, boundaries=None, display_x_label=True,
                             display_y_label=True):
    """ This function is used to generate the intensities profile in RAW DATA, to plot them in analysis. It will try to read the csv if it exists, and if not
    the intensities are generated using numpy and saved to the csv file.

    :param axis: matplolib figure axis where to write the intensities profile
    :type axis: matplotlib figure axis
    :param folder_images: Folder where the images will be found to analyse intensities
    :type folder_images: str
    :param analysisfolder: Folder where the csv file for intensities cache will be stored , or retrieved if exists
    :type analysisfolder: str
    :param title: Title of the figure subplot of intensities
    :type title: str
    :param boundaries: Boundaries for x and y axis on the plot , used to align all camera stacks on same scale on image (Default value = None)
    :type boundaries: list
    :param display_x_label: If true , display the label of x axis (used to prevent to display the same label between 2 axis in image)  (Default value = True)
    :type display_x_label: bool
    :param display_y_label: If true , display the label of y axis (used to prevent to display the same label between 2 axis in image)  (Default value = True)
    :type display_y_label: bool

    :returns: min , max and details of intensities
    :rtype: tuple
    """
    print("     -> Intensities analysis for folder : " + str(folder_images))
    if boundaries is None:
        boundaries = [0, 2000]
    average_by_time = {}
    max_by_time = {}
    if not os.path.isdir(join(analysisfolder, "raw")):
        os.makedirs(join(analysisfolder, "raw"))
    csv_data = join(join(analysisfolder, "raw"), title.replace(" ", "_") + ".csv")
    if os.path.isfile(csv_data): # If we found a csv data file containing intensities , read them directly
        f = open(csv_data, "r")
        datacsv = f.read()
        f.close()
        for line in datacsv.split(":"):
            if line != "":
                data = line.split(";")
                time = int(data[0])
                mean = float(data[1])
                std = float(data[2])
                average_by_time[time] = mean
                max_by_time[time] = std

    else: # if not , generate them using numpy
        image_name_list = [f for f in listdir(folder_images) if isfile(join(folder_images, f)) and is_uncompressed_image(f)]
        image_name_list.sort()
        csv = ""
        for image_name in image_name_list:
            image_path = join(folder_images, image_name)
            image_time = int(re.findall(r'\d+', image_name.split(".")[0])[-1])
            image_np = imread(image_path)
            mean = np.mean(image_np)
            intensities = list(np.unique(image_np.reshape(-1)))
            intensities.sort()
            intensities.reverse()
            cumulated = []
            for intensity in intensities:
                if len(cumulated) < 0.05 * len(intensities): #Construction of 95% cumulated histogram
                    cumulated.append(intensity)
            max_cumulated = min(cumulated)
            maxt = np.max(image_np)
            print("Image max : " + str(maxt) + " cumulated max : " + str(max_cumulated))
            # Get the list of intensities in images
            # Sort them
            # Take the one at 95%
            average_by_time[image_time] = mean
            max_by_time[image_time] = max_cumulated
            csv += str(image_time) + ";" + str(mean) + ";" + str(max_cumulated) + ":" # creation of the intensity csv
        f = open(csv_data, "w+")
        f.write(csv)
        f.close()
    data_means = list(average_by_time.values())
    data_std = list(max_by_time.values())
    times = list(average_by_time.keys())
    axis.plot(times, data_means, '-')
    mins = min([a - b for a, b in zip(data_means, data_std)])
    maxs = max([a + b for a, b in zip(data_means, data_std)])
    axis.fill_between(times, [a + b for a, b in zip(data_means, data_std)], [a for a in data_means], alpha=0.2) #plot intensities
    axis.set_ylim(boundaries)
    if display_x_label:
        axis.set_xlabel("Time")
    if display_y_label:
        axis.set_ylabel("Signal mean (line) and amplitude")
    axis.legend()
    axis.set_title(title)
    return mins, maxs, csv_data

def generate_plots_signal_to_noise(stack_0_left_cam,stack_0_right_cam,stack_1_left_cam,stack_1_right_cam,export_folder):
    """  This function is called by AstecManager to generate a profile of intensities for all 4 cameras of the Raw Data of an embryo.
    It's not needed to provide all 4 cameras folder name, replacing a non-existent one with None is enough to skip it

    :param stack_0_left_cam: Name of the left camera of stack 0 folder
    :type stack_0_left_cam: str
    :param stack_0_right_cam: Name of the right camera of stack 0 folder
    :type stack_0_right_cam: str
    :param stack_1_left_cam: Name of the left camera of stack 1 folder
    :type stack_1_left_cam: str
    :param stack_1_right_cam: Name of the right camera of stack 1 folder
    :type stack_1_right_cam: str
    :param export_folder: Folder where the plot will be saved
    :type export_folder: str
    """
    mins = []
    maxs = []
    if export_folder != "":
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)
        fig, ax = plt.subplots(2, 2)
        if stack_0_left_cam is not None: # If folder name is not none , plot intensities of this folder in first axis of figure (top left)
            miny, maxy, csv = camerastacksignaltonoise(ax[0, 0], stack_0_left_cam, export_folder, "Left camera of stack 0",
                                                       display_x_label=False,
                                                       display_y_label=True)
            mins.append(miny)
            maxs.append(maxy)
        if stack_0_right_cam is not None: # If folder name is not none , plot intensities of this folder in second axis of figure (top right)
            miny, maxy, csv = camerastacksignaltonoise(ax[0, 1], stack_0_right_cam, export_folder, "Right camera of stack 0",
                                                       display_x_label=False,
                                                       display_y_label=False)
            mins.append(miny)
            maxs.append(maxy)
        if stack_1_left_cam is not None: # If folder name is not none , plot intensities of this folder in third axis of figure (bottom left)
            miny, maxy, csv = camerastacksignaltonoise(ax[1, 0], stack_1_left_cam, export_folder, "Left camera of stack 1",
                                                       display_x_label=True,
                                                       display_y_label=True)
            mins.append(miny)
            maxs.append(maxy)
        if stack_1_right_cam is not None: # If folder name is not none , plot intensities of this folder in fourth axis of figure (bottom right)
            miny, maxy, csv = camerastacksignaltonoise(ax[1, 1], stack_1_right_cam, export_folder, "Right camera of stack 1",
                                                       display_x_label=True,
                                                       display_y_label=False)
            mins.append(miny)
            maxs.append(maxy)
        realmin = min(mins)
        realmax = max(maxs)
        ax[0, 0].set_ylim([0, realmax])
        ax[0, 1].set_ylim([0, realmax])
        ax[1, 0].set_ylim([0, realmax])
        ax[1, 1].set_ylim([0, realmax])
        fig.tight_layout()
        fig.set_size_inches(18.5, 10.5) # Save the final plot to image
        fig.suptitle("Signal mean and amplitude though time in raw images", fontsize=14)
        fig.savefig(export_folder, "raw_images_intensities.png")
def plotsignaltonoise(embryo_name, parameters, one_stack_only=False, stack_chosen=0,add_to_metadata=True):
    """ Compute the name of the different raw data cameras folders depending on parameters, and call the generation of intensities plot.
    Have the possibility to save this to the metadata file

    :param embryo_name: Name of the embryo
    :type embryo_name: str
    :param parameters: Dict of parameters coming from the Fusion step
    :type parameters: dict
    :param one_stack_only: If true, only use one stack for the plot  (Default value = False)
    :type one_stack_only: bool
    :param stack_chosen: If one stack only is used, index of the stack that will be plotted (Default value = 0)
    :type stack_chosen: int

    """

    stack_0_left_cam = None
    stack_0_right_cam = None
    stack_1_right_cam = None
    stack_1_left_cam = None
    path = "."
    folder_out = os.path.join(path, "analysis","raw")
    raw_path = os.path.join(path, parameters["DIR_RAWDATA"].replace('"', '').replace("'", ""))
    if (one_stack_only and stack_chosen == 0) or not one_stack_only:
        stack_0_left_cam = os.path.join(raw_path, parameters["DIR_LEFTCAM_STACKZERO"].replace('"', '').replace("'", ""))
        stack_0_right_cam = os.path.join(raw_path,
                                         parameters["DIR_RIGHTCAM_STACKZERO"].replace('"', '').replace("'", ""))
    if (one_stack_only and stack_chosen == 1) or not one_stack_only:
        stack_1_left_cam = os.path.join(raw_path, parameters["DIR_LEFTCAM_STACKONE"].replace('"', '').replace("'", ""))
        stack_1_right_cam = os.path.join(raw_path,
                                         parameters["DIR_RIGHTCAM_STACKONE"].replace('"', '').replace("'", ""))
    generate_plots_signal_to_noise(stack_0_left_cam, stack_0_right_cam, stack_1_left_cam,
                                   stack_1_right_cam, folder_out)
    if add_to_metadata:
        parameters["step"] = "rawdata_intensities_plot"
        parameters["embryo_name "] = embryo_name
        addDictToMetadata(path, parameters)

class plot_variables:
    """ This class is used to store variables for AstecManager run , and store the flag specifying if it's string typed or not.
    Used when writing the python file called when generating the analysis plots.
    """
    def __init__(self, value, isstring):
        self.value = value

        self.isstring = isstring

def format_cell_id(cellid):
    """ Using the cell key, format it to morphonet-like format (cell_t,cell_id).

    :param cellid: Cell key
    :type cellid: int
    :return: Formatted cell key
    :rtype: str
    """
    tc, idc = get_id_t(int(cellid))
    return str(tc) + "," + str(idc)

def has_info_lineage(lineage, info_name):
    """ Detect if a property file given in parameter has the property given by its name

    :param lineage: Path to the property file
    :type lineage: str
    :param info_name: Name of the property to test
    :type info_name: str
    :returs: Has the file the given property
    :rtype: bool

    """
    return Get_Cell_Contact_Surface(lineage, info_name) is not None

def get_cell_names(lineage, cells):
    """ Using a list of cell keys and a property file , retrieve the list of names corresponding to those cells from
     the file, or a list of formatted ids if names are not found

    :param lineage: Path to the property file
    :type lineage: str
    :param cells: List of cells by key
    :type cells: list
    :return: List of cell names
    :rtype: list
    """
    result_names = []
    names = Get_Cell_Names(lineage)
    for cell in cells:
        if cell in names:
            namesplitted = names[cell].split('.')
            result_names.append(namesplitted[0] + "." + namesplitted[1].lstrip("0").replace("_", "-"))
        else:
            result_names.append(str(format_cell_id(cell)))
    return result_names

def lineage_path_with_names(lineagepath):
    """ Format a property file path given in parameter to add the named suffix for a plot

    :param lineagepath: Path to the property file
    :type lineagepath: str
    :return: Formatted property file path
    :rtype: str

    """
    lineagepathsplited = lineagepath.split('.')
    return lineagepathsplited[0] + "_minmaxnamed" + "." + lineagepathsplited[1]


def auto_name_time(lineage, cellcount):
    from AstecManager.Manager import compute_atlas
    """ Generate an automatic naming using the ASTEC naming system for a property file, from a given cell count.

    :param lineage: Path to the property file
    :type lineage: str
    :param cellcount: Cell count used to start naming
    :type cellcount: int
    :return: Path to the new written property file
    :rtype: str

    """
    outlineage = lineage_path_with_names(lineage)
    parameters = ""
    parameters += 'cell_number=' + str(cellcount) + '\n'
    parameters += 'inputFile="' + str(lineage) + '"\n'
    parameters += 'outputFile="' + str(outlineage) + '"\n'
    parameters += "atlasFiles=" + str(compute_atlas()) + "\n"
    f = open("parameters_naming.py", "w+")
    f.write(parameters)
    f.close()
    os.system("conda run -n astec astec_atlas_init_naming -p parameters_naming.py")
    os.remove("parameters_naming.py")
    os.system("rm *.log")
    return outlineage