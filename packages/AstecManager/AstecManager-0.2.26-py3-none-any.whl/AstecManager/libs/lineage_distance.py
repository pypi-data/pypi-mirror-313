import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
import pickle as pkl
from collections import defaultdict
import re
import os
from AstecManager.libs.data import get_longid,get_id_t
from AstecManager.libs.lineage import Get_Cell_Names,AddNodeToXML,LoadCellList,GetCellWholeLifetime,GetAllCellLifeFutur

def list_ids_with_name(list_names,cell_name):
    """Using a dict of cell key to name coming, retrieve the list of cell keys with the name

    :param list_names: List of names
    :type list_names: dict
    :param cell_name: The cell name to find
    :type cell_name: str
    :return: List of cell keys with the name
    :rtype: list

    """
    list_ids = []
    for cell_key in list_names:
        if cell_name == list_names[cell_key]:
            list_ids.append(cell_key)
    return list_ids
def find_lowest_t_with_cell(list_names, cell_name):
    """Using a dict of cell key to name coming, retrieve the cell with the lowest time point

    :param list_names: List of names
    :type list_names: dict
    :param cell_name: The cell name to find
    :type cell_name: str
    :return: Cell time point, cell id of the cell
    :rtype: tuple

    """
    current_found_time = None
    current_found_id = None
    for cell_key in list_names:
        if cell_name == list_names[cell_key]:
            tc, idc = get_id_t(cell_key)
            if current_found_time is None or current_found_time > int(tc):
                current_found_time = int(tc)
                current_found_id = int(idc)
    return current_found_time,current_found_id



# NEW DEFINITION OF LOCAL COST FUNCTIONS FOR TREE-EDIT DISTANCES
# Definition of a LOCAL COST function.
# this function computes the elementary distance between to any vertices of two trees
def new_local_cost(v1=None,v2=None):
    """Compute distance between two vertices

    :param v1:  (Default value = None)
    :param v2:  (Default value = None)

    
    """
    if isinstance(v1,tuple)==True:
        if v2 == None:
            cost = 0
            v = list(v1)
            for i in range(len(v)):
                cost+=v[i]
            return cost
        else:
            d=len(v1)
            return sum( [abs(v1[i]-v2[i]) for i in range(0,d)])
    else:
        if v2==None:
            return v1
        else:
            return abs(v1-v2)

# A first function to defined an attribute called 'label_for_distance' with a constant value
# on each node of a given tree (to make simple tests)
def give_label_dist_constant(tree,value):
    """

    :param tree:
    :param value: 

    """
    # associate a constant attribute value with all the vertices of the tree
    # Parameters
    # ----------
    # tree: treex tree
    # value: number vector
    tree.add_attribute_to_id('label_for_distance',value)
    for child in tree.my_children:
        give_label_dist_constant(child,value)

# Define a more general function to attach a 'label_for_distance' to a tree
# with more general values (by copying the value of another given attribute in 'label_for_distance')
# and so that the edit-distance can then be used with this tree.

def give_label_dist_attribute(tree,name):
    """

    :param tree: 
    :param name: 

    """
    # associate a constant attribute value with all the vertices of the tree
    # Parameters
    # ----------
    # tree: treex tree
    # value: number vector
    value = tree.get_attribute(name)
    tree.add_attribute_to_id('label_for_distance',value)
    for child in tree.my_children:
        give_label_dist_attribute(child,name)

def time_stamp(cell_id):
    """ Retrieve the time stamp from a cell key

    :param cell_id: Cell key
    :type cell_id: int
    :return: Time stamp
    :rtype: int

    """
    return int(cell_id // 10000)

def cell_lifespan_list(c,cell_lineage):
    """

    :param c: 
    :param cell_lineage: 

    """
    cell_list = [c]
    if c in cell_lineage:
        child = cell_lineage[c]
        while len(child) == 1:
            cell_list.append(child[0])
            if child[0] in cell_lineage:
                child = cell_lineage[child[0]]
            else:
                child = []
    return cell_list

def life_span(cell_id,cell_lineage):
    """

    :param cell_id: 
    :param cell_lineage: 

    """
    lst = cell_lifespan_list(cell_id,cell_lineage)
    return time_stamp(lst[-1])-time_stamp(lst[0])+1

# Two functions to create (Treex) trees from lineage data

# definition of a function to build a tree from astec cell lineages
# Note: this accesses the astec lineage as a global variable, as well as the translation dict from tree to astec
def add_child_tree(t,astec_child,cell_lineage,astec2tree,maxtime=None):
    """

    :param t: 
    :param astec_child: 
    :param cell_lineage: 
    :param astec2tree: 
    :param maxtime:  (Default value = None)

    """
    import treex as tx
    if maxtime == None:
        if astec_child == None :
            return False
    else:
        if astec_child == None or time_stamp(astec_child) > maxtime:
            return False
    ct = tx.Tree()
    ct.add_attribute_to_id('astec_id',astec_child)
    astec2tree[astec_child] = ct.my_id
    t.add_subtree(ct)
    if astec_child in cell_lineage: # astec_child is not terminal
        for c in cell_lineage[astec_child]:
            #print(c)
            add_child_tree(ct, c,cell_lineage,astec2tree,maxtime) # recursive call on children of astec_child
    return True

def daughters(c,cell_lineage):
    """

    :param c: 
    :param cell_lineage: 

    """
    if c in cell_lineage:
        child = cell_lineage[c] #
        if len(child) == 0:
            return None
        elif len(child) == 1:
            return daughters(child[0],cell_lineage)
        else:
            return child
    else:
        return None

def mother(c,cell_lineage):
    """

    :param c: 
    :param cell_lineage: 

    """
    mother_dic = {}
    for c in cell_lineage:
        child = daughters(c,cell_lineage)
        if child is not None:
            mother_dic[child[0]] = c
            mother_dic[child[1]] = c
    if c in mother_dic:
        return mother_dic[c]
    else:
        return None

def has_sister(c,cell_lineage):
    """

    :param c: 
    :param cell_lineage: 

    """
    m = mother(c)
    if m is not None:
        if m in cell_lineage:
            child = cell_lineage[m]
            if len(child) == 1:
                return has_sister(m,cell_lineage)
            else:
                return True
        else:
            return False
    else:
        return False

def sister(c,cell_lineage):
    """

    :param c: 
    :param cell_lineage: 

    """
    m = mother(c)
    if m is not None:
        if m in cell_lineage:
            child = cell_lineage[m]
            if len(child) == 1:
                return has_sister(m,cell_lineage)
            else: # len == 2
                return child[0] if child[0] != c else child[1]
        else:
            return None
    else:
        return None

# Create the lineage tree of the cell given in argument
def create_lineage_tree(astec_id,cell_lineage,maxtime=None):
    """

    :param astec_id: 
    :param cell_lineage: 
    :param maxtime:  (Default value = None)

    """
    import treex as tx
    t = tx.Tree() # create tree (in treex, nodes are actually trees)
    astec2tree = {}
    # setting root data
    t.add_attribute_to_id('astec_id',astec_id)
    # store mapping between vertices
    astec2tree[astec_id] = t.my_id

    if astec_id in cell_lineage:
        for c in cell_lineage[astec_id]:
            #print(c)
            add_child_tree(t,c,cell_lineage,astec2tree,maxtime)
    return t

def create_compressed_lineage_tree(astec_id,cell_lineage,cellnames=None,stop_at_division=False):
    """

    :param astec_id: 
    :param cell_lineage: 
    :param cellnames:  (Default value = None)

    """
    # print(astec_id)
    import treex as tx
    astec2tree = {}
    lifespan = life_span(astec_id,cell_lineage)
    t = tx.Tree()  # create tree (in treex, nodes are actually trees)
    # setting root data
    if cellnames is not None and astec_id in cellnames:
        t.add_attribute_to_id('astec_id', cellnames[astec_id])
    else:
        t.add_attribute_to_id('astec_id', astec_id)
    t.add_attribute_to_id('lifespan', lifespan)
    # store mapping between vertices
    keytree = astec_id
    if cellnames is not None and astec_id in cellnames:
        keytree = cellnames[astec_id]
    astec2tree[keytree] = t.my_id
    if not stop_at_division:
        dlist = daughters(astec_id,cell_lineage)  # find the daughters (cell ids just after a division)
        if dlist != None and dlist != []:
            try:
                assert len(dlist) == 2
                for c in dlist:
                    if c in cell_lineage:
                        tchild = create_compressed_lineage_tree(c,cell_lineage,cellnames)
                        if tchild != None:
                            t.add_subtree(tchild)
            except :
                print("skipping")
    return t

def apply_compressed_compare(lineage_prop1,lineage_prop2,cell_key,cell_key2,stop_at_division=False):
    """

    :param lineage_prop1: 
    :param lineage_prop2: 
    :param cell_key: 
    :param cell_key2: 

    """
    from treex.analysis.edit_distance.zhang_labeled_trees import zhang_edit_distance
    tree1 = create_compressed_lineage_tree(cell_key, lineage_prop1,stop_at_division=stop_at_division)
    tree2 = create_compressed_lineage_tree(cell_key2, lineage_prop2,stop_at_division=stop_at_division)
    give_label_dist_attribute(tree1, 'lifespan')
    give_label_dist_attribute(tree2, 'lifespan')

    # Compute the zhang edit-distance between them (then making use of the information 'lifespan' on the nodes)
    d = zhang_edit_distance(tree1, tree2, "lifespan", new_local_cost)
    return d

def apply_compare(lineage_prop1,lineage_prop2,cell_key,cell_key2,stop_at_divison=False):
    """

    :param lineage_prop1: 
    :param lineage_prop2: 
    :param cell_key: 
    :param cell_key2: 

    """
    from treex.analysis.edit_distance.zhang_labeled_trees import zhang_edit_distance
    tree1 = create_lineage_tree(cell_key, lineage_prop1)
    tree2 = create_lineage_tree(cell_key2, lineage_prop2)
    give_label_dist_constant(tree1, (1))
    give_label_dist_constant(tree2, (1))
    d = zhang_edit_distance(tree1, tree2, "label_for_distance", new_local_cost)
    return d

def read_lineage(lineage):
    """

    :param lineage: 

    """
    import os
    converted = False
    lineagepkl = None
    if lineage.endswith(".xml"):
        lineagepkl = lineage.replace(".xml",".pkl")
        os.system("conda run -n astec astec_embryoproperties -i "+lineage+" -o "+lineagepkl)
        converted = True
        lineage = lineagepkl
    f = open(lineage, 'rb')
    astec_output1 = pkl.load(f)  # astec_output is the set of all dictionary returned by ASTEC (itself a dic)
    f.close()
    if converted and lineagepkl is not None:
        if os.path.isfile(lineagepkl):
            os.system("rm "+lineagepkl)
    return astec_output1
def get_id_t(idl):
    """Return the cell t,id

    :param idl:
    :type idl: int


    """
    t = int(int(idl) / (10 ** 4))
    cell_id = int(idl) - int(t) * 10 ** 4
    return t, cell_id
def load_cell_names(lineage):
    """

    :param lineage: 

    """
    astec_output = read_lineage(lineage)
    if not 'cell_name' in astec_output:
        print("Name information is missing")
        exit()
    return astec_output['cell_name']
def name_to_id(output_astec,namecell):
    """

    :param output_astec: 
    :param namecell: 

    """
    if not 'cell_name' in output_astec:
        print("Name information is missing")
        exit()

    cell_names1 = output_astec['cell_name']
    cell_key_1 =""
    for keyc in cell_names1:
        if cell_names1[keyc] == namecell:
            tc, idc = get_id_t(keyc)
            previoust = None
            if cell_key_1 != "":
                previoust, previousid = get_id_t(cell_key_1)
            if previoust is None or previoust > tc:
                cell_key_1 = keyc

    return cell_key_1


def compare_cells_by_name(lineage_path_1,lineage_path_2,cell_names_pairs,stop_at_division=False):
    """

    :param lineage_path_1:
    :param lineage_path_2:
    :param cell_name1:
    :param cell_name2:

    """
    distances_by_names = {}
    tested_names = []
    astec_output1 = read_lineage(
        lineage_path_1)  # astec_output is the set of all dictionary returned by ASTEC (itself a dic)
    astec_output2 = read_lineage(
        lineage_path_2)  # astec_output is the set of all dictionary returned by ASTEC (itself a dic)
    cell_lineage1 = astec_output1['cell_lineage']
    cell_lineage2 = astec_output2['cell_lineage']
    for cell_name1, cell_name2 in cell_names_pairs:
        if not cell_name1 in tested_names:
            cell_key_1 = name_to_id(astec_output1,cell_name1)
            cell_key_2 = name_to_id(astec_output2,cell_name2)
            if cell_key_1 != "" and cell_key_2 != "":
                cell_key_1_int = int(cell_key_1)
                cell_key_2_int = int(cell_key_2)
                distance_found = apply_compressed_compare(cell_lineage1, cell_lineage2, cell_key_1_int,cell_key_2_int,stop_at_division=stop_at_division)
                distances_by_names[cell_name1] = distance_found
                distances_by_names[cell_name2] = distance_found
                tested_names.append(cell_name1)
                tested_names.append(cell_name2)
    return distances_by_names

def compare_cell_by_name(lineage_path_1,lineage_path_2,cell_name1,cell_name2):
    """

    :param lineage_path_1: 
    :param lineage_path_2: 
    :param cell_name1: 
    :param cell_name2: 

    """
    astec_output1 = read_lineage(
        lineage_path_1)  # astec_output is the set of all dictionary returned by ASTEC (itself a dic)
    astec_output2 = read_lineage(
        lineage_path_2)  # astec_output is the set of all dictionary returned by ASTEC (itself a dic)
    cell_lineage1 = astec_output1['cell_lineage']
    cell_lineage2 = astec_output2['cell_lineage']
    cell_key_1 = name_to_id(astec_output1,cell_name1)
    cell_key_2 = name_to_id(astec_output2,cell_name2)

    return apply_compressed_compare(cell_lineage1, cell_lineage2, cell_key_1,cell_key_2)

def compare_cell_by_key(lineage_path_1,lineage_path_2,cell_key_1,cell_key_2):
    """

    :param lineage_path_1: 
    :param lineage_path_2: 
    :param cell_key_1: 
    :param cell_key_2: 

    """
    astec_output1 = read_lineage(lineage_path_1)  # astec_output is the set of all dictionary returned by ASTEC (itself a dic)
    astec_output2 = read_lineage(lineage_path_2)  # astec_output is the set of all dictionary returned by ASTEC (itself a dic)
    cell_lineage1 = astec_output1['cell_lineage']
    cell_lineage2 = astec_output2['cell_lineage']

    return apply_compare(cell_lineage1,cell_lineage2,cell_key_1,cell_key_2)

def print_tree(lineage,cell_key,compressed=False,name=None):
    """

    :param lineage: 
    :param cell_key: 
    :param compressed:  (Default value = False)
    :param name:  (Default value = None)

    """
    from treex.visualization.matplotlib_plot import view_tree
    astec_output = read_lineage(lineage)
    cell_lineage = astec_output['cell_lineage']
    treeforcell = None
    if compressed:
        treeforcell=create_compressed_lineage_tree(cell_key, cell_lineage)
    else :
        treeforcell=create_lineage_tree(cell_key, cell_lineage)
    fig = view_tree(treeforcell)
    displayname = cell_key
    if name is not None:
        displayname = name
    prefixfig = "dendogram_plots/"
    if compressed:
        prefixfig=prefixfig+"compressed_tree_"
    else:
        prefixfig = prefixfig + "tree_"
    fig.savefig(prefixfig+lineage.split('.')[0].replace('/','_')+"_"+displayname.replace(".","")+".png")

def print_tree_by_name(lineage,cell_name,compressed=False):
    """

    :param lineage: 
    :param cell_name: 
    :param compressed:  (Default value = False)

    """
    astec_output = read_lineage(lineage)
    cell_key_1 = name_to_id(astec_output,cell_name)
    print_tree(lineage,cell_key_1,compressed,cell_name)



# Transform distance matrix into a condensed matrix (used by linkage function below)
# (= vector array made from upper triangular part of the distance matrix)
# i<j<m, where m is the number of original observations
# m * i + j - ((i + 2) * (i + 1)) // 2.
def condensed_matrix(dist_mat):
    """

    :param dist_mat: 

    """
    m = np.shape(dist_mat)[0]
    cm = np.zeros(m*(m-1)//2)
    for j in range(m):
        for i in range(j):
            cm[m * i + j - ((i + 2) * (i + 1)) // 2] = dist_mat[j][i]
    return cm
def count_cells(cell_list,remove_time=[]):
    """

    :param cell_list: 
    :param remove_time:  (Default value = [])

    """
    cell_count_by_time = {}
    for cell_key in cell_list:
        cell_obj_t = time_stamp(cell_key)
        if not cell_obj_t in remove_time:
            if not cell_obj_t in cell_count_by_time:
                cell_count_by_time[cell_obj_t] = 0
            cell_count_by_time[cell_obj_t] += 1
    return cell_count_by_time

def get_cell_generation(cell_names,cellkey):
    """

    :param cell_names: 
    :param cellkey: 

    """
    if cell_names is None or len(cell_names)==0:
        return None
    if not cellkey in cell_names:
        return None
    findgenin = cell_names[cellkey].split(".")[0]
    return int(re.findall(r'\d+', findgenin)[-1])


def compute_dendogram(lineage_trees):
    """

    :param lineage_trees: 

    """
    from treex.analysis.edit_distance.zhang_labeled_trees import zhang_edit_distance
    nbcell=len(lineage_trees)
    dist_array = np.zeros((nbcell, nbcell))
    for i in range(nbcell):
        for j in range(i, nbcell):
            dist_array[i][j] = zhang_edit_distance(lineage_trees[i], lineage_trees[j], "lifespan", new_local_cost)
            dist_array[j][i] = dist_array[i][j]
    return hierarchy.linkage(condensed_matrix(dist_array), method='average', optimal_ordering=True)

def compute_cluster_for_names(lineage_list,namelist,lineage_names):
    """

    :param lineage_list: 
    :param namelist: 
    :param lineage_names: 

    """
    mapping_index={}
    i=0
    lineage_trees = []
    lin=0
    for lineage in lineage_list:
        cells_to_compute = []
        workedids = []
        astec_output = read_lineage(lineage)  # astec_output is the set of all dictionary returned by ASTEC (itself a dic)
        cell_lineage = astec_output['cell_lineage']
        cellnames = None
        if 'cell_name' in astec_output:
            cellnames = astec_output['cell_name']
        if cellnames is None:
            print("No names found in : "+lineage)
        filteredlineage = list(filter(lambda x: (cellnames is not None and x in cellnames and cellnames[x] in namelist), cell_lineage))
        for cell in filteredlineage:
                if cellnames[cell] in namelist:
                    mother_cell = get_direct_mother(cell, cell_lineage,cellnames)
                    if mother_cell is not None and not mother_cell in workedids:
                        if mother_cell in cellnames and cellnames[mother_cell] in namelist:
                            print("Added cell "+str(mother_cell)+" with name "+str(cellnames[mother_cell]))
                            cells_to_compute.append(mother_cell)
                            workedids.append(mother_cell)
        # Compute the lineage trees:
        for cellc in cells_to_compute:
            print("cell "+str(cellc)+" found name : "+str(cellnames[cellc])+" at index "+str(i))
            mapping_index[i]=cellnames[cellc]+" "+lineage_names[lin]
            t = create_compressed_lineage_tree(cellc,cell_lineage,cellnames)
            give_label_dist_attribute(t, 'lifespan')
            lineage_trees.append(t)
            i+=1
        lin+=1
    Z = compute_dendogram(lineage_trees)
    return mapping_index, lineage_trees, Z

def get_next_mother(cell,cell_lineage):
    """

    :param cell: 
    :param cell_lineage: 

    """
    for celltest in cell_lineage:
        for cellval in cell_lineage[celltest]:
            if cellval==cell:
                return celltest
    return None

def get_daughters(cell,cell_lineage):
    """

    :param cell: 
    :param cell_lineage: 

    """
    d = []
    for celltest in cell_lineage:
        if celltest==cell:
            d=cell_lineage[celltest]
    return d

def get_direct_mother(cell,cell_lineage,cellnames=None):
    """

    :param cell: 
    :param cell_lineage: 
    :param cellnames:  (Default value = None)

    """
    if not cell in cell_lineage:
        return None
    directmother = get_next_mother(cell,cell_lineage)
    if directmother is None:
        return cell
    daughters = get_daughters(directmother,cell_lineage)
    directmothertwice = get_next_mother(directmother, cell_lineage)
    if directmothertwice is None or len(daughters) > 1:
        return directmother
    return get_direct_mother(directmother,cell_lineage)

def compute_cluster_for_generation(lineage_list,generation_list,lineage_names):
    """

    :param lineage_list: 
    :param generation_list: 
    :param lineage_names: 

    """
    mapping_index={}
    i=0
    lineage_trees = []
    lin=0
    for lineage in lineage_list:
        workedids = []
        cells_to_compute = []
        astec_output = read_lineage(lineage)  # astec_output is the set of all dictionary returned by ASTEC (itself a dic)
        cell_lineage = astec_output['cell_lineage']
        cellnames = None
        if 'cell_name' in astec_output:
            cellnames = astec_output['cell_name']
        if cellnames is None:
            print("No names found in : "+lineage)
        filtered_lineage=list(filter(lambda x: (x in cellnames and int(get_cell_generation(cellnames,x)) in generation_list), cell_lineage))
        for cell in filtered_lineage:
            mother_cell = get_direct_mother(cell,cell_lineage,cellnames)
            if mother_cell is not None and not mother_cell in workedids:
                cells_to_compute.append(mother_cell)
                workedids.append(mother_cell)
        # Compute the lineage trees:
        for cellc in cells_to_compute:
            mapping_index[i] = cellnames[cellc] + " " + lineage_names[lin]
            t = create_compressed_lineage_tree(cellc,cell_lineage,cellnames)
            give_label_dist_attribute(t, 'lifespan')
            lineage_trees.append(t)
            i+=1
        lin += 1
    Z = compute_dendogram(lineage_trees)
    return mapping_index, lineage_trees, Z


def compute_cluster_for_stage(lineage_list,cell_count,lineage_names):
    """

    :param lineage_list: 
    :param cell_count: 
    :param lineage_names: 

    """

    mapping_index={}
    i=0
    lineage_trees = []
    lin=0
    for lineage in lineage_list:
        workedids = []
        cells_to_compute = []
        astec_output = read_lineage(lineage)  # astec_output is the set of all dictionary returned by ASTEC (itself a dic)
        cell_lineage = astec_output['cell_lineage']
        cell_count_time=dict(sorted(count_cells(cell_lineage).items()))
        cellnames = None
        if 'cell_name' in astec_output:
            cellnames = astec_output['cell_name']
        timepoint = None
        for time in cell_count_time:
            if timepoint is None and cell_count_time[time] == cell_count:
                timepoint=int(time)
        if timepoint is None:
            for time in cell_count_time:
                if timepoint is None and cell_count_time[time] >= cell_count:
                    timepoint = int(time)
        filteredlineage = list(filter(lambda x: (int(time_stamp(x))==timepoint), cell_lineage))
        for cell in filteredlineage:
            mother_cell = get_direct_mother(cell,cell_lineage,cellnames)
            if mother_cell is not None and not mother_cell in workedids:
                cells_to_compute.append(mother_cell)
                workedids.append(mother_cell)
        # Compute the lineage trees:
        for cellc in cells_to_compute:
            mapping_index[i] = cellnames[cellc] + " " + lineage_names[lin]
            t = create_compressed_lineage_tree(cellc,cell_lineage,cellnames)
            give_label_dist_attribute(t, 'lifespan')
            lineage_trees.append(t)
            i+=1
        lin += 1
    Z = compute_dendogram(lineage_trees)
    return mapping_index, lineage_trees, Z

def compute_cluster_for_time(lineage_list,timepoint_list,lineage_names):
    """

    :param lineage_list: 
    :param timepoint_list: 
    :param lineage_names: 

    """
    cells_to_compute = []
    mapping_index={}
    i=0
    lineage_trees = []
    lin=0
    for lineage in lineage_list:
        workedids = []
        astec_output = read_lineage(lineage)  # astec_output is the set of all dictionary returned by ASTEC (itself a dic)
        cell_lineage = astec_output['cell_lineage']
        cellnames = None
        if 'cell_name' in astec_output:
            cellnames = astec_output['cell_name']
        filteredlineage = list(filter(lambda x: (time_stamp(x) is not None and int(time_stamp(x)) in timepoint_list), cell_lineage))
        for cell in filteredlineage:
            if cell is not None and not cell in workedids:
                cells_to_compute.append(cell)
                workedids.append(cell)
        # Compute the lineage trees:
        for cellc in cells_to_compute:
            cname = str(cellc)
            if cellc in cellnames:
                cname=cellnames[cellc]
            mapping_index[i] = cname + " " + lineage_names[lin]
            t = create_compressed_lineage_tree(cellc,cell_lineage,cellnames)
            give_label_dist_attribute(t, 'lifespan')
            lineage_trees.append(t)
            i+=1
        lin += 1
    Z = compute_dendogram(lineage_trees)
    return mapping_index, lineage_trees, Z
def compute_cluster_for_time_single_lineage(lineage,timepoint):
    """

    :param lineage: 
    :param timepoint: 

    """
    cells_to_compute = []
    mapping_index={}
    astec_output = read_lineage(lineage)  # astec_output is the set of all dictionary returned by ASTEC (itself a dic)
    cell_lineage = astec_output['cell_lineage']
    cellnames = None
    if 'cell_name' in astec_output:
        cellnames = astec_output['cell_name']
    for cell in cell_lineage:
        timecell = time_stamp(cell)
        if timecell==timepoint:
            cells_to_compute.append(cell)
    nbcell = len(cells_to_compute)
    lineage_trees = []
    # Compute the lineage trees:
    for i in range(nbcell):
        cname=cells_to_compute[i]
        if cellnames is not None and cname in cellnames:
            cname = cellnames[cname]
        mapping_index[i]=cname
        t = create_compressed_lineage_tree(cells_to_compute[i],cell_lineage,cellnames)
        give_label_dist_attribute(t, 'lifespan')
        lineage_trees.append(t)
    Z = compute_dendogram(lineage_trees)
    return mapping_index,lineage_trees,Z
def plot_cluster(dendogram,filename,axismapping=None,title=None,figxsize=None,figysize=None):
    """

    :param dendogram: 
    :param filename: 
    :param axismapping:  (Default value = None)
    :param title:  (Default value = None)
    :param figxsize:  (Default value = None)
    :param figysize:  (Default value = None)

    """
    dist_threshold = 350  # this is used to define the grain of the classes (see horizontal dashed line on the figure)

    # Function linkage performs the hirarchical clustering based on a condensed version of the distance matrix
    # print(Z)

    # - Then the cell hierarchy is computed as a dendrogram data-structure
    # It contains the labels of the points, their color code and more (see scipy doc)

    fig = plt.figure()
    curr_axis = fig.gca()  # current viewport (called axis) in the fig window (fig)

    # prepare the plot of the dendrogram and select the level of the classes see: 'color_threshold'
    dn = hierarchy.dendrogram(dendogram, color_threshold=dist_threshold, ax=curr_axis, leaf_font_size=14)

    curr_axis.axhline(y=dist_threshold, linestyle='--', linewidth=1)
    curr_axis.set_title(title if title is not None else 'Hierarchical Clustering Dendrogram', size=24)
    curr_axis.set_xlabel("cell lineage", size=18)
    curr_axis.set_ylabel("edit-distance", size=18)
    labels = [item.get_text() for item in curr_axis.get_xticklabels()]
    for i in range(0,len(labels)):
        previouslabs = labels[i]
        if int(previouslabs) in axismapping:
            print("Working on id : "+str(previouslabs)+" with label "+ str(axismapping[int(previouslabs)]))
            writtenname = str(axismapping[int(previouslabs)])
            if "." in writtenname:
                namesplitted=writtenname.split('.')
                labels[i]=namesplitted[0]+"."+namesplitted[1].lstrip("0").replace("_","-")
            else :
                labels[i] = writtenname
    curr_axis.set_xticklabels(labels)
    plt.xticks(fontsize=8)
    fig.set_size_inches(figxsize if figxsize is not None else 40,figysize if figysize is not None else 15)  # size of the plot
    #fig.set_size_inches(figxsize if figxsize is not None else 40, figysize if figysize is not None else 15)  # size of the plot
    plt.savefig(filename)
    plt.clf()
def compute_classes_dendogram(dendogram,lineage_trees):
    """

    :param dendogram: 
    :param lineage_trees: 

    """
    # - Finally Extract the classes from the dendrogram:
    dist_threshold = 350
    fig = plt.figure()
    curr_axis = fig.gca()
    classes = hierarchy.fcluster(dendogram, t=dist_threshold, criterion='distance')
    dn = hierarchy.dendrogram(dendogram, color_threshold=dist_threshold, ax=curr_axis, leaf_font_size=14)

    # and print the detailed results corresponding to the above figure
    classlist = {}
    for i in range(0,len(classes)):
        k = dn['leaves'][i]
        if not k in classlist:
            classlist[k] = []
        cell_id = lineage_trees[k].get_attribute('astec_id')
        classlist[k].append(cell_id)
    for k in classlist:
        print("> Cells in class "+str(k))
        for cell in classlist[k]:
            print('     -> ', cell)

def generate_lineage_comparison(lineage_file,begin_time_point,info_name_1="float_symetric_cells_branch_length_distance",info_name_2="float_symetric_cells_lineage_tree_distance",info_name_3="float_symetric_cells_lineage_subtree_distance"):
    """
    Using a named lineage , generates properties representing the distance between symetric cells in lineage
    The generated properties :
    - name1 : the distance between symetric cells branch length
    - name2 : the distance between symetric cells complete lineage tree
    - name3 : the distance between symetric cells sub lineage tree

    :param dendogram:
    :param lineage_trees:
    """
    if not os.path.isfile(lineage_file):
        raise Exception("The lineage file does not exist !")
    names = Get_Cell_Names(lineage_file)

    # Build names lists
    names_tuples = [] #List of tuples that will compute a distance
    tested_names = [] #buffer to prevent multiples testing
    name_to_tid = {} #Used to retrieve ids for information generation
    for idc in names:
        current_name = names[idc]
        mint, minid = find_lowest_t_with_cell(names, current_name) #Find first cell of branch
        name_to_tid[current_name] = str(mint) + "," + str(minid)
        other_name = None
        if "_" in current_name:
            other_name = current_name.replace("_", "*")
        elif "*" in current_name:
            other_name = current_name.replace("*", "_")
        if other_name is not None and not current_name in tested_names and not other_name in tested_names and current_name != "" and other_name != "":
            mint, minid = find_lowest_t_with_cell(names, other_name) # Find the first cell of symetric branch
            name_to_tid[other_name] = str(mint) + "," + str(minid)
            names_tuples.append((current_name, other_name)) #  Add to compute distance
            names_tuples.append((other_name, current_name))
            tested_names.append(current_name) # prevent adding it again
            tested_names.append(other_name)

    # build branch to branch length
    distance_by_names = compare_cells_by_name(lineage_file, lineage_file, names_tuples, stop_at_division=True) #build distance
    info_distance = {}
    distance_by_names = dict(sorted(distance_by_names.items(), key=lambda key_val: key_val[1]))
    for name in distance_by_names: # loop is here to fill the whole property (add the proeprty to each snapshot)
        idscells = list_ids_with_name(names, name)
        for cell in idscells:
            if cell not in info_distance:
                info_distance[cell] = distance_by_names[name]
    AddNodeToXML(lineage_file, info_distance, info_name_1, "cell", identifier_text="cell-id") #Save in property file


    all_cells = LoadCellList(lineage_file)    #compute lineage for both next info
    distance_by_names = compare_cells_by_name(lineage_file, lineage_file, names_tuples, stop_at_division=False) #compute whole distance
    info_distance = {}
    distance_by_names = dict(sorted(distance_by_names.items(), key=lambda key_val: key_val[1]))

    #Build subtree distances
    for name in distance_by_names:
        idscells = list_ids_with_name(names, name)
        begin_t = 100000
        begin_key = None
        for cell in idscells:
            tc, idcell = get_id_t(cell)
            if tc < begin_t:
                begin_t = tc
                begin_key = cell
        if begin_key is not None:
            idscells = GetAllCellLifeFutur(all_cells[begin_key])
            if not all_cells[begin_key] in idscells:
                idscells.append(all_cells[begin_key])
            for cellc in idscells:
                longcellid = get_longid(cellc.t, cellc.id)
                if longcellid not in info_distance:
                    info_distance[longcellid] = distance_by_names[name]
    AddNodeToXML(lineage_file, info_distance, info_name_3, "cell", identifier_text="cell-id")
    # Build whole tree distance
    info_distance = {}
    for name in distance_by_names:
        idscells = list_ids_with_name(names, name)
        t_begin_key = None
        for cell in idscells:
            tc, idcell = get_id_t(cell)
            if tc == begin_time_point:
                t_begin_key = cell
        if t_begin_key is not None:
            idscells = GetCellWholeLifetime(all_cells[t_begin_key])
            for cellc in idscells:
                longcellid = get_longid(cellc.t, cellc.id)
                if longcellid not in info_distance:
                    info_distance[longcellid] = distance_by_names[name]
    AddNodeToXML(lineage_file, info_distance, info_name_2, "cell", identifier_text="cell-id")