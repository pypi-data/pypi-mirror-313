import os
import numpy as np
import pickle as pkl
import xml.etree.ElementTree as ElementTree

########################################################################################
#
# key correspondences
#
# Examples
# - from 'full_properties_Samson_MN20.pkl', keys are
#   ['volumes information',
#    'Cells labels in time',
#    'Barycenters',
#    'Fate',
#    'All Cells',
#    'Principal values',
#    'Names',
#    'cell_cell_contact_information',
#    'Lineage tree',
#    'Cells history',
#    'Principal vectors']
# - from 'new_lineage_tree_MN20.pkl', keys are cell labels
# - from '140317-Patrick-St8_seg_lineage.pkl', keys are
#   ['h_mins_information', 'lin_tree', 'volumes_information', 'sigmas_information']
#
#
########################################################################################

keydictionary = {'lineage': {'output_key': 'cell_lineage',
                             'input_keys': ['lineage_tree', 'lin_tree', 'Lineage tree', 'cell_lineage']},
                 'h_min': {'output_key': 'cell_h_min',
                           'input_keys': ['cell_h_min', 'h_mins_information']},
                 'volume': {'output_key': 'cell_volume',
                            'input_keys': ['cell_volume', 'volumes_information', 'volumes information', 'vol']},
                 'surface': {'output_key': 'cell_surface',
                             'input_keys': ['cell_surface', 'cell surface']},
                 'compactness': {'output_key': 'cell_compactness',
                                 'input_keys': ['cell_compactness', 'Cell Compactness', 'compacity',
                                                'cell_sphericity']},
                 'sigma': {'output_key': 'cell_sigma',
                           'input_keys': ['cell_sigma', 'sigmas_information', 'sigmas']},
                 'label_in_time': {'output_key': 'cell_labels_in_time',
                                   'input_keys': ['cell_labels_in_time', 'Cells labels in time', 'time_labels']},
                 'barycenter': {'output_key': 'cell_barycenter',
                                'input_keys': ['cell_barycenter', 'Barycenters', 'barycenters']},
                 'fate': {'output_key': 'cell_fate',
                          'input_keys': ['cell_fate', 'Fate']},
                 'fate2': {'output_key': 'cell_fate_2',
                           'input_keys': ['cell_fate_2', 'Fate2']},
                 'fate3': {'output_key': 'cell_fate_3',
                           'input_keys': ['cell_fate_3', 'Fate3']},
                 'fate4': {'output_key': 'cell_fate_4',
                           'input_keys': ['cell_fate_4', 'Fate4']},
                 'all-cells': {'output_key': 'all_cells',
                               'input_keys': ['all_cells', 'All Cells', 'All_Cells', 'all cells', 'tot_cells']},
                 'principal-value': {'output_key': 'cell_principal_values',
                                     'input_keys': ['cell_principal_values', 'Principal values']},
                 'apicobasal-length': {'output_key': 'cell_apicobasal_length',
                                     'input_keys': ['cell_apicobasal_length']},
                 'name': {'output_key': 'cell_name',
                          'input_keys': ['cell_name', 'Names', 'names', 'cell_names']},
                 'contact': {'output_key': 'cell_contact_surface',
                             'input_keys': ['cell_contact_surface', 'cell_cell_contact_information']},
                 'contact-edge': {'output_key': 'cell_contact_edge',
                             'input_keys': ['cell_contact_edge']},
                 'contact-edge-length': {'output_key': 'cell_contact_edge_length',
                             'input_keys': ['cell_contact_edge_length']},
                 'contact-edge-segment': {'output_key': 'cell_contact_edge_segment',
                             'input_keys': ['cell_contact_edge_segment']},
                 'history': {'output_key': 'cell_history',
                             'input_keys': ['cell_history', 'Cells history', 'cell_life', 'life']},
                 'principal-vector': {'output_key': 'cell_principal_vectors',
                                      'input_keys': ['cell_principal_vectors', 'Principal vectors']},
                 'name-score': {'output_key': 'cell_naming_score',
                                'input_keys': ['cell_naming_score', 'Scores', 'scores']},
                 'problems': {'output_key': 'problematic_cells',
                              'input_keys': ['problematic_cells']},
                 'urchin_apicobasal_length': {'output_key': 'urchin_cell_apicobasal_length',
                              'input_keys': ['urchin_cell_apicobasal_length']},
                 'urchin_apicobasal_segment': {'output_key': 'urchin_cell_apicobasal_segment',
                              'input_keys': ['urchin_cell_apicobasal_segment']},
                 'urchin_adjacency': {'output_key': 'urchin_cell_adjacency',
                                       'input_keys': ['urchin_cell_adjacency']},
                 'urchin_apical_surface': {'output_key': 'urchin_apical_surface',
                              'input_keys': ['urchin_apical_surface']},
                 'urchin_apical_surface_barycenter': {'output_key': 'urchin_apical_surface_barycenter',
                              'input_keys': ['urchin_apical_surface_barycenter']},
                 'urchin_basal_surface': {'output_key': 'urchin_basal_surface',
                              'input_keys': ['urchin_basal_surface']},
                 'urchin_basal_surface_barycenter': {'output_key': 'urchin_basal_surface_barycenter',
                              'input_keys': ['urchin_basal_surface_barycenter']},
                 'urchin_apical_contact_edge_length': {'output_key': 'urchin_apical_contact_edge_length',
                              'input_keys': ['urchin_apical_contact_edge_length']},
                 'urchin_apical_contact_edge_segment': {'output_key': 'urchin_apical_contact_edge_segment',
                              'input_keys': ['urchin_apical_contact_edge_segment']},
                 'urchin_basal_contact_edge_length': {'output_key': 'urchin_basal_contact_edge_length',
                              'input_keys': ['urchin_basal_contact_edge_length']},
                 'urchin_basal_contact_edge_segment': {'output_key': 'urchin_basal_contact_edge_segment',
                              'input_keys': ['urchin_basal_contact_edge_segment']},
                 'urchin_vegetal_distance': {'output_key': 'urchin_vegetal_distance',
                              'input_keys': ['urchin_vegetal_distance']},
                 'unknown': {'output_key': 'unknown_key',
                             'input_keys': ['unknown_key']}}


def _normalize_dictionary_keys(inputdict):
    """

    :param inputdict: return:

    """

    if inputdict == {}:
        return {}

    outputdict = {}

    for inputkey in inputdict:
        foundkey = False
        for k in keydictionary:
            # print "       compare '" + str(tmpkey) + "' with '" + str(k) + "'"
            if inputkey in keydictionary[k]['input_keys']:
                outputkey = keydictionary[k]['output_key']
                outputdict[outputkey] = inputdict[inputkey]
                foundkey = True
                break

        if foundkey is False:
            outputdict[inputkey] = inputdict[inputkey]

    return outputdict


########################################################################################
#
# to translate a dictionary into XML
#
########################################################################################

#
# from stackoverflow.com
# questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
#
#
# used for pretty printing
#

########################################################################################
#
# types
# 'lineage':  'lineage_tree' :
#     dictionary de liste de int
#     lineage_tree.590002 = <type 'list'>
# 'h_min' : 'cell_h_min' :
# 'volume' : 'cell_volume' :
#     dictionary de int
#     cell_volume.590002 = <type 'int'>
#     590002: 236936
# 'sigma': 'cell_sigma':
# 'label_in_time': 'cell_labels_in_time'
#     dictionary de liste de numpy.int64
#     cell_labels_in_time.1 = <type 'list'>
#     1: [10002, 10003, 10004, ..., 10082]
# 'barycenter': 'cell_barycenter'
#     dictionary de numpy.ndarray de numpy.float64
#     cell_barycenter.590002 = <type 'numpy.ndarray'>
#     590002: array([ 258.41037242,  226.74975943,  303.67167927])
# 'fate': 'cell_fate'
#     dictionary de str
#     cell_fate.590002 = <type 'str'>
#     590002: 'Mesoderm Notochord 1'
# 'all-cells': 'all_cells'  # liste de toutes les cellules ?
#     liste de numpy.int64
#     all_cells = <type 'list'>
# 'principal-value': 'cell_principal_values'
#     dictionary de liste de numpy.float64
#     cell_principal_values.590002 = <type 'list'>
#     590002: [1526.0489371146978, 230.60881177650205, 91.063513300019849]
# 'name': 'cell_name'
#     dictionary de str
#     cell_name.590002 = <type 'str'>
#     590002: 'a9.0012_'
# 'contact': 'cell_contact_surface',
#     dictionary de dictionary de int
#     cell_contact_surface.590002.590019 = <type 'int'>
#     590002: {590001: 1808, 590003: 1436, 590004: 5012, ..., 590225: 2579}
# 'history': 'cell_history'
#     dictionary de numpy.ndarray de numpy.int64
#     cell_history.590002 = <type 'numpy.ndarray'>
#     590002: array([510002, 520002, 530002, 540002, 550002, 560002, 570002, 580002,
#         590002, 600002, 610002, 620002, 630002, 640002, 650002, 660002,
#         670002, 680002, 690002, 700002, 710002, 720002, 730002, 740002,
#         750002, 760002, 770002, 780002, 790002, 800002, 810002, 820002,
#         830002, 840002, 850002, 860002, 870002, 880002])
# 'principal-vector': 'cell_principal_vectors'    # liste de numpy.ndarray
#     dictionary de liste de numpy.ndarray de numpy.float64
#     cell_principal_vectors.590002 = <type 'list'>
#     590002: [array([ 0.17420991, -0.74923203,  0.63898534]),
#         array([-0.24877611,  0.59437038,  0.7647446 ]),
#         array([ 0.95276511,  0.29219037,  0.08284582])]
#
########################################################################################

def _list_to_text(value):
    """

    :param value: 

    """
    proc = "_list_to_text"

    #
    # list of numbers
    #
    if type(value[0]) in (int, float, np.int64, np.float64):
        # element.text = str(value)
        # GM: why sorting
        # value.sort()
        return repr(value)

    #
    # list of strings
    #
    elif isinstance(value[0], str):
        value.sort()
        text = "["
        for i in range(len(value)):
            text += "'" + value[i] + "'"
            if i < len(value) - 1:
                text += ", "
                if i > 0 and i % 5 == 0:
                    text += "\n  "
        text += "]"
        return text
    #
    # 'principal-vector' case
    #  liste de numpy.ndarray de numpy.float64
    #
    elif type(value[0]) == np.ndarray:
        text = "["
        for i in range(len(value)):
            # text += str(list(value[i]))
            text += repr(list(value[i]))
            if i < len(value) - 1:
                text += ", "
                if i > 0 and i % 10 == 0:
                    text += "\n  "
        text += "]"
        return text

    elif type(value[0]) == list:
        text = "["
        for i in range(len(value)):
            # text += str(list(value[i]))
            text += _list_to_text(value[i])
            if i < len(value) - 1:
                text += ", "
                if i > 0 and i % 5 == 0:
                    text += "\n  "
        text += "]"
        return text
    return ""

def _set_xml_element_text(element, value):
    """

    :param element: param value:
    :param value: 

    """
    proc = "_set_xml_element_text"

    #
    # dictionary : recursive call
    #   dictionary element may be list, int, numpy.ndarray, str
    # list : may be int, numpy.int64, numpy.float64, numpy.ndarray
    #

    if type(value) == dict:
        # print proc + ": type is dict"
        keylist = list(value.keys())
        keylist.sort()
        for k in keylist:
            _dict2xml(element, k, value[k])

    elif type(value) == list:

        #
        # empty list
        #

        if len(value) == 0:
            element.text = repr(value)
        #
        # 'lineage', 'label_in_time', 'all-cells', 'principal-value'
        #

        else:
            element.text = _list_to_text(value)

    #
    # 'barycenter', 'cell_history'
    #
    elif type(value) == np.ndarray:
        # element.text = str(list(value))
        element.text = repr(list(value))

    #
    # 'volume', 'contact'
    #
    elif type(value) in (int, float, np.int64, np.float64):
        # element.text = str(value)
        element.text = repr(value)

    #
    # 'fate', 'name'
    #
    elif type(value) == str:
        element.text = repr(value)



#
#
#


def _dict2xml(parent, tag, value):
    """

    :param parent: param tag:
    :param value: return:
    :param tag: 

    """

    #
    # integers can not be XML tags
    #
    if type(tag) in (int, np.int64):
        child = ElementTree.Element('cell', attrib={'cell-id': str(tag)})
    else:
        mn_type, name = _get_morphonet_type_name(str(tag))
        if mn_type is not None:
            child = ElementTree.Element(name, attrib={'mn_type': str(mn_type)})
        else:
            child = ElementTree.Element(str(tag))

    _set_xml_element_text(child, value)

    parent.append(child)
    return parent


#
# procedure d'appel et creation de la racine
#


########################################################################################
#
# to translate a XML tree into dictionary
#
########################################################################################


def _set_dictionary_value(root):
    """

    :param root: return:

    """

    if len(root) == 0:

        #
        # pas de branche, on renvoie la valeur
        #

        # return ast.literal_eval(root.text)
        if root.text is None:
            return None
        else:
            return eval(root.text)

    else:

        dictionary = {}

        for child in root:

            # print("child.tag=" + str(child.tag))
            # print "len(child)=" + str(len(child))
            # print "child.text=" + str(child.text)

            key = child.tag
            if child.tag == 'cell':
                key = np.int64(child.attrib['cell-id'])
            elif 'mn_type' in child.attrib:
                key = 'morphonet_' + child.attrib['mn_type'] + "_" + str(child.tag)
            dictionary[key] = _set_dictionary_value(child)

    return dictionary


def xml2dict(tree):
    """

    :param tree: return:

    """

    proc = "xml2dict"

    root = tree.getroot()

    dictionary = {}

    for k, v in keydictionary.items():

        if root.tag == v['output_key']:
            dictionary[str(root.tag)] = _set_dictionary_value(root)
            break
    else:
        for child in root:
            value = _set_dictionary_value(child)
            if value is None:
                print("value is none for xml2dict")
            else:
                key = child.tag
                if child.tag == 'cell':
                    key = np.int64(child.attrib['cell-id'])
                elif 'mn_type' in child.attrib:
                    key = 'morphonet_' + child.attrib['mn_type'] + "_" + str(child.tag)
                dictionary[key] = value

    return dictionary


########################################################################################
#
# to read a set of files into a dictionary
#
########################################################################################


#
# update dictionary from what has been read
#

def _update_read_dictionary(propertiesdict, tmpdict, filename):
    """

    :param propertiesdict: param tmpdict:
    :param tmpdict: 
    :param filename: 

    """
    proc = "_update_read_dictionary"
    unknownkeys = []

    for tmpkey in tmpdict:
        foundkey = False

        for k in keydictionary:
            # print "       compare '" + str(tmpkey) + "' with '" + str(k) + "'"
            if tmpkey in keydictionary[k]['input_keys']:
                outputkey = keydictionary[k]['output_key']
                #
                # update if key already exists, else just create the dictionary entry
                #
                if outputkey in propertiesdict:
                    if type(propertiesdict[outputkey]) is dict and type(tmpdict[tmpkey]) is dict:
                        propertiesdict[outputkey].update(tmpdict[tmpkey])
                    elif type(propertiesdict[outputkey]) is list and type(tmpdict[tmpkey]) is list:
                        propertiesdict[outputkey] += tmpdict[tmpkey]
                else:
                    propertiesdict[outputkey] = tmpdict[tmpkey]
                foundkey = True
                break

        if foundkey is False:
            unknownkeys.append(tmpkey)

    if len(unknownkeys) > 0 and len(unknownkeys) == len(list(tmpdict.keys())):
        #
        # no key was found
        # it is assumed it's a lineage tree: add some test here ?
        #
        outputkey = keydictionary['lineage']['output_key']
        if outputkey in propertiesdict:
            if type(propertiesdict[outputkey]) is dict and type(tmpdict) is dict:
                propertiesdict[outputkey].update(tmpdict)
        else:
            propertiesdict[outputkey] = tmpdict

    elif len(unknownkeys) > 0:
        for k in unknownkeys:
            propertiesdict[k] = tmpdict[k]

    return propertiesdict


#
# types issued from the reading of xml files may be erroneous
# fix it
#

def _set_types_from_xml(propertiesdict):
    """

    :param propertiesdict: return:

    """

    if propertiesdict == {}:
        return {}

    if 'cell_barycenter' in propertiesdict:
        for c in propertiesdict['cell_barycenter']:
            propertiesdict['cell_barycenter'][c] = np.array(propertiesdict['cell_barycenter'][c])

    if 'cell_history' in propertiesdict:
        for c in propertiesdict['cell_history']:
            propertiesdict['cell_history'][c] = np.array(propertiesdict['cell_history'][c])

    if 'cell_principal_vectors' in propertiesdict:
        for c in propertiesdict['cell_principal_vectors']:
            for v in range(len(propertiesdict['cell_principal_vectors'][c])):
                propertiesdict['cell_principal_vectors'][c][v] \
                    = np.array(propertiesdict['cell_principal_vectors'][c][v])

    return propertiesdict


#
#
#

def _read_xml_file(filename, propertiesdict):
    """

    :param filename: 
    :param propertiesdict: 

    """
    inputxmltree = ElementTree.parse(filename)
    tmpdict = xml2dict(inputxmltree)
    propertiesdict = _update_read_dictionary(propertiesdict, tmpdict, filename)
    del tmpdict
    return propertiesdict


#
#
#

def _read_pkl_file(filename, propertiesdict):
    """

    :param filename: 
    :param propertiesdict: 

    """
    inputfile = open(filename, 'rb')
    tmpdict = pkl.load(inputfile)
    inputfile.close()
    propertiesdict = _update_read_dictionary(propertiesdict, tmpdict, filename)
    del tmpdict
    return propertiesdict


#
#
#

def read_dictionary(inputfilenames, inputpropertiesdict={}):
    """

    :param inputfilenames: param inputpropertiesdict:
    :param inputpropertiesdict:  (Default value = {})

    """
    proc = 'read_dictionary'

    if inputfilenames is None:
        return {}

    propertiesdict = inputpropertiesdict

    #
    #
    #

    if type(inputfilenames) == str:
        if not os.path.isfile(inputfilenames):
            return propertiesdict

        if inputfilenames.endswith("xml") is True:
            propertiesdict = _read_xml_file(inputfilenames, propertiesdict)
            propertiesdict = _set_types_from_xml(propertiesdict)
        elif inputfilenames.endswith("pkl") is True:
            propertiesdict = _read_pkl_file(inputfilenames, propertiesdict)

        propertiesdict = _normalize_dictionary_keys(propertiesdict)
        return propertiesdict

    #
    # here, we assume type(inputfilenames) == list
    #

    #
    # read xml files
    #

    for filename in inputfilenames:

        if not os.path.isfile(filename):
            continue

        if filename.endswith("xml") is True:
            propertiesdict = _read_xml_file(filename, propertiesdict)

    #
    # translation of xml may take place here
    #

    propertiesdict = _set_types_from_xml(propertiesdict)

    #
    # read pkl files
    #

    for filename in inputfilenames:

        if not os.path.isfile(filename):
            continue

        if filename.endswith("pkl") is True:
            propertiesdict = _read_pkl_file(filename, propertiesdict)

    #
    #
    #

    for filename in inputfilenames:
        if filename[len(filename) - 3:len(filename)] == "xml":
            continue
        elif filename[len(filename) - 3:len(filename)] == "pkl":
            continue

    propertiesdict = _normalize_dictionary_keys(propertiesdict)
    return propertiesdict


########################################################################################
#
#
#
########################################################################################

def _get_morphonet_type_name(key):
    """

    :param key: 

    """
    mn_type = None
    if key[:10] == 'morphonet_' or key[:10] == 'selection_':
        if key[10:20] == 'selection_':
            mn_type = 'selection'
            name = key[20:]
        elif key[10:16] == 'float_':
            mn_type = 'float'
            name = key[16:]
        else:
            name = key[10:]
    else:
        name = key
    return mn_type, name
