import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import zipfile
import os
import argparse
import re
import copy
from zipfile import ZipFile
from io import BytesIO
from struct import unpack

def plot_values(xvalues, yvalues,title = "Real-Time Float Data Plot", xlabel="Sample Number", ylabel="eV"):
    """
    Plots the values in a line graph and saves it as a PDF file.
    """
    plt.figure(figsize=(10, 5))
    plt.ticklabel_format(axis='y', style='sci', scilimits=(3,3))
    plt.plot(xvalues, yvalues, color="blue")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.gca().invert_xaxis()
    buf = BytesIO()
    plt.savefig(buf, format='pdf')
    plt.close()
    return buf.getbuffer()


def find_delimiters(file_bytes, start_str="SOFH\r\n", end_str="EOFH\r\n"):
    """
    Finds the start and end positions of relevant content in the file bytes.
    """
    start_bytes = start_str.encode("utf-8")
    end_bytes = end_str.encode("utf-8")

    start_pos = file_bytes.find(start_bytes)

    end_start = file_bytes.find(end_bytes, start_pos + len(start_bytes))
    end_pos = end_start + len(end_bytes)

    if start_pos == -1 or end_pos == -1:
        raise ValueError("Start or end delimiter not found in file.")

    return start_pos, end_pos


def parse_key_value(line):
    """
    Splits a line into a key-value pair.
    """
    if ':' in line:
        key, value = line.split(":", 1)
        return key.strip(), value.strip()
    return None, None


def split_camel_case(key):
    # Helper function to split camelCase into parts
    return re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', key)


def check_and_split(value):
    # Regular expression to match a float followed by a space and a unit
    pattern = r"^(-?\d+(\.\d+)?)(?:[eE][-+]?\d+)?\s+([a-zA-Z\/]+)$"

    match = re.match(pattern, value)
    if match:
        # Extract the numeric value and the unit
        numeric_part = match.group(1)
        unit_part = match.group(3)
        return numeric_part, unit_part
    else:
        return None, None


def add_to_xml(root, hierarchy, value):
    # Function to add a value to the XML structure
    current_element = root
    parent_element = root
    for part in hierarchy:
        # Check if the element already exists
        child = current_element.find(part)
        if child is None:
            # Create new element if it doesn't exist
            child = ET.SubElement(current_element, part)
        parent_element = current_element
        current_element = child

    numeric_part, unit_part = check_and_split(value)
    # Set the text for the last element in the hierarchy
    if not (current_element.get("value") is None):
        current_element = ET.SubElement(parent_element, current_element.tag)

    if (numeric_part is None):
        current_element.set("value", value)
    else:
        current_element.set("value", numeric_part)
        current_element.set("unit", unit_part)


def process_lines(lines, root, spectral_regs):
    """
    Processes lines to populate the XML structure.
    """
    counters = {"NoSpectralReg": 0, "NoDPDataCyc": 1, "NoPreSputterCyc": 0}

    for line in lines:
        key, value = parse_key_value(line)
        if not key:
            continue

        if key in counters:
            counters[key] = int(value)

        key_parts = split_camel_case(key)
        add_to_xml(root, key_parts, value)

    return counters

def extract_float_image(zip_archive, file_bytes, start_pos, root, counters,
                       file_prefix, filedate, create_plot, create_csv):
    mapPixelsXY = root.find('No').find("Map-Pixels-XY")
    
    if not (mapPixelsXY is None):
        x = int(mapPixelsXY.get("x"))
        y = int(mapPixelsXY.get("y"))
        count_values = x * y
        plot_bytes = file_bytes[start_pos:start_pos + count_values * 4]
        start_pos += start_pos + count_values * 4
            
        yvalues = unpack("<"+str(count_values)+"f",plot_bytes)
        
        if create_csv:
            filename = zipfile.ZipInfo(filename=f"{file_prefix}_sxi.csv", date_time=filedate)
            with zip_archive.open(filename, 'w') as csv_file:
                count = 1
                for value in yvalues:
                    csv_file.write(str.encode(f"{value}"))
                    if count < x:
                        count = count + 1
                        csv_file.write(str.encode("\t"))
                    elif count == x:
                        csv_file.write(str.encode("\n"))
                        count = 1
                        
        if create_plot:
            filename = zipfile.ZipInfo(filename=f"{file_prefix}_sxi.pfm", date_time=filedate)
            with zip_archive.open(filename, 'w') as img_file:
                img_file.write(str.encode(f"Pf\n{x} {y}\n-1.0\n"))
                img_file.write(plot_bytes);
            

    
def extract_float_data(zip_archive, file_bytes, start_pos, spectral_regs, counters,
                       file_prefix, filedate, create_plot, create_csv):
    """
    Extracts and processes float data for spectral regions.
    """
    no_all = counters["NoSpectralReg"] + counters["NoPreSputterCyc"]
    
    ylabel = "Photoelectron Count per Second (#)"
    xlabel = "Binding Energy (eV)"
    
    # erste 4 byte integer 1 2e 4 byte integer anzahl columns und 3e 4 byte integer anzal zu übersringende bytes + 16
    skip_bytes = unpack('i', file_bytes[start_pos+8:start_pos+12])
    start_pos += (skip_bytes[0] + 16)    

    for reg_def in spectral_regs:
        if not(reg_def.find('step') is None):
            step = float(reg_def.find('step').get("value"))
            start = float(reg_def.find('lower-range').get("value"))
            count = int(reg_def.find('count').get("value"))
            reg_name = reg_def.find('name').get("value")
            ev = reg_def.find('pass-energy').get("value")
            for cycle in range(counters["NoDPDataCyc"]):
                xvalues = [step * i + start for i in range(count)]
                plot_bytes = file_bytes[start_pos:start_pos + count * 4]
                start_pos += count * 4
    
                unpackformat = "<"+str(len(plot_bytes)>>2)+"f"
                yvalues = unpack(unpackformat,plot_bytes)
    
                if create_plot:
                    filename = zipfile.ZipInfo(filename=f"{file_prefix}_plot_{reg_name}_{cycle}.pdf", date_time=filedate)
                    img_data = plot_values(xvalues, yvalues, reg_name, xlabel,ylabel)
                    with zip_archive.open(filename, 'w') as file1:
                        file1.write(img_data)
    
                if create_csv:
                    filename = zipfile.ZipInfo(filename=f"{file_prefix}_data_{reg_name}_{cycle}.csv", date_time=filedate)
                    with zip_archive.open(filename, 'w') as csv_file:
                        csv_file.write(str.encode("BE/eV\tPE: "+ev+" eV\n"))
                        for x, y in zip(xvalues, yvalues):
                            csv_file.write(str.encode(f"{x}\t{y}\n"))
                            
    return start_pos;


def zip_directory(directory_path, output_zip):
    """Zips an entire directory."""
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                full_path = os.path.join(root, file)
                # Add the file to the zip archive with a relative path
                relative_path = os.path.relpath(full_path, directory_path)
                zipf.write(full_path, arcname=relative_path)
    print(f"Directory {directory_path} zipped into {output_zip}")


def remove_elements_by_name(root, name):
    """
    Recursively removes all elements with the specified name.

    Parameters:
    - root: The root element of the XML tree.
    - name: The name of the elements to remove.
    """
    # Create a list of elements to remove (direct children)
    to_remove = [child for child in root if child.tag == name]

    # Remove those elements
    for child in to_remove:
        root.remove(child)

    # Recurse into remaining children
    for child in root:
        remove_elements_by_name(child, name)


def remove_attributes_except_full(root):
    """
    Removes all attributes from XML elements that are not named "Full".

    Parameters:
    - root: The root element of the XML tree.
    """
    # Traverse all elements in the tree
    for elem in root.iter():
        # If the element is not named "Full", clear its attributes
        if elem.tag != "Full":
            elem.attrib.clear()


def remove_empty_elements(root, parent=None):
    """
    Recursively removes all elements with no children,
    no attributes, and empty/whitespace-only text.

    Parameters:
    - root: The current element being processed.
    - parent: The parent of the current element.
    """
    # Iterate over a copy of the child list
    # to avoid modification issues during iteration
    for child in list(root):
        remove_empty_elements(child, root)

    # If the element has no children, no attributes, and empty text,
    # remove it from the parent
    if (len(root) == 0 and not root.attrib and
            (root.text is None or root.text.strip() == "")):
        if parent is not None:
            parent.remove(root)


def has_attribute_starting_with(element, prefix):
    """
    Check if the element has attributes,
    and if any attribute's value starts with '1'.

    Parameters:
    - element: The XML element to check.

    Returns:
    - True if the element has attributes,
      and any attribute's value starts with '1'.
    - False otherwise.
    """
    # Check if the element has any attributes
    if element.attrib:
        # Iterate through the attributes and check if any value starts with '1'
        for value in element.attrib.values():
            if value.startswith(prefix):
                return True
    return False


def duplicate_and_keep(root, parent=None, prefix='1'):
    copiedTree = copy.deepcopy(root.find('Reg'))
    if not(copiedTree is None):
        for elem in copiedTree.iter():
            # If the element is not named "Full", clear its attributes
            if not (has_attribute_starting_with(elem, prefix)):
                elem.attrib.clear()
        remove_empty_elements(copiedTree)
        copiedTree.set("index", prefix)
        root.append(copiedTree)
    return copiedTree


def replace_attribute_with_subelements(root, count=2, separator=' '):
    """
    Replace attributes with more than two spaces with indexed subelements.

    Parameters:
    - root: The root element of the XML tree.
    """
    for elem in root.iter():
        # Iterate over a copy of the element's attributes
        # to avoid modification issues during iteration
        for attr_name, attr_value in list(elem.attrib.items()):
            # Check if the attribute contains more than two spaces
            if attr_value.count(separator) > count:
                # Split the attribute value into space-separated parts
                parts = attr_value.split(separator)

                # Create indexed sub-elements
                for index, part in enumerate(parts, 1):
                    sub_elem = ET.SubElement(elem, "value")
                    sub_elem.set("index", str(index))
                    sub_elem.set("value", part)

                # Remove the original attribute
                del elem.attrib[attr_name]


def collect_def_elements_with_many_attributes(root, threshold=7):
    """
    Collects all elements named 'Def' with more than 'threshold' attributes.

    Parameters:
    - root: The root element of the XML tree.
    - threshold: The minimum number of attributes an element must
                 have to be collected (default is 7).

    Returns:
    - A list of elements that are named 'Def' and
      have more than the specified threshold of attributes.
    """
    matching_elements = []

    for elem in root.iter():
        if elem.tag == "Def" and len(elem) > threshold:
            matching_elements.append(elem)
            elem.tag = "Def-Detail"
        if elem.tag == "Full" and len(elem) > threshold:
            matching_elements.append(elem)
            elem.tag = "Full-Detail"

    return matching_elements


def compact_element_structure(root):
    """
    Combines all elements that contain only a sigle element.
    """
    for elem in root.iter():
        child = root
        while child is not None:
            child = None
            if (not elem.attrib or len(elem.attrib) == 0) and len(elem) == 1:
                child = elem[0]
                elem.tag = elem.tag + "-" + child.tag
                elem.attrib = child.attrib
                elem[:] = child[:]
            if (len(elem) == 1 and
                    (not elem[0].attrib or len(elem[0].attrib) == 0)):
                child = elem[0]
                elem.tag = elem.tag + "-" + child.tag
                elem[:] = child[:]


def rename_replace_known_values(root):
    if root.attrib['index'] == '1':
        root.tag = 'column'
    if root.attrib['index'] == '2':
        root.tag = 'cycle'
    if root.attrib['index'] == '3':
        root.tag = 'name'
    if root.attrib['index'] == '4':
        root.tag = 'atomic-number'
        if root.attrib['value'] == '111':
            root.set('value','')
    if root.attrib['index'] == '5':
        root.tag = 'count'
    if root.attrib['index'] == '6':
        root.tag = 'step'
        root.set('unit','eV')
    if root.attrib['index'] == '7':
        root.tag = 'lower-range'
        root.set('unit','eV')
    if root.attrib['index'] == '8':
        root.tag = 'upper-range'
        root.set('unit','eV')
    if root.attrib['index'] == '9':
        root.tag = 'analysis-lower-range'
        root.set('unit','eV')
    if root.attrib['index'] == '10':
        root.tag = 'analysis-upper-range'
        root.set('unit','eV')
    if root.attrib['index'] == '11':
        root.tag = 'time-data-point'
        root.set('unit','s')
    if root.attrib['index'] == '12':
        root.tag = 'pass-energy'
        root.set('unit','eV')
    if root.tag != 'value':
        del root.attrib['index']


def replace_known_values(root, parent=None, grand_parent=None):
    """
    Replace known values with named ones
    """
    if root.tag == 'value' and parent.tag == 'Full-Detail' and grand_parent.tag == 'Def':
        rename_replace_known_values(root)
    if root.tag == 'value' and parent.tag == 'Def-Detail' and grand_parent.tag == 'Reg':
        rename_replace_known_values(root)

    for child in root:
        replace_known_values(child, root, parent)


def replace_known_x_y_unit_attrib(root):
    """
    Replace known values with named ones
    """
    if ('value' in root.attrib) and len(root.attrib['value'].split()) > 1:
        parts = root.attrib['value'].split()
        root.attrib.clear()
        root.set("x",parts[0])
        root.set("y",parts[1])
        if len(parts)>2:
            root.set("unit",parts[2])

def replace_known_position(value,position):
    if value.attrib['index'] == '1':
        position.set("x",value.attrib['value'])
        position.remove(value)
    if value.attrib['index'] == '2':
        position.set("y",value.attrib['value'])
        position.remove(value)
    if value.attrib['index'] == '3':
        position.set("z",value.attrib['value'])
        position.remove(value)
    if value.attrib['index'] == '4':
        position.set("tilt",value.attrib['value'])
        position.remove(value)
    if value.attrib['index'] == '5':
        position.set("rotation",value.attrib['value'])
        position.remove(value)


def split_string(input_str):
    """
    Splits a string into the part before the brackets and the part within the brackets.

    Parameters:
    - input_str: The input string to split.

    Returns:
    - A tuple (before_brackets, within_brackets).
    """
    # Split at the opening parenthesis
    parts = input_str.split('(', 1)
    before_brackets = parts[0].strip()  # Part before the brackets
    within_brackets = parts[1].strip(')') if len(parts) > 1 else ""  # Part within the brackets
    return before_brackets, within_brackets


def replace_known_spatial(root):
    first , second = split_string(root.attrib['value'])
    root.set('set-point',first.split()[1])
    values = second.split()
    # (U V Z Tilt Rotation) 
    root.set('u', values[0])
    root.set('v', values[1])
    root.set('z', values[2])
    root.set('tilt', values[3])
    root.set('rotation', values[3])
    root.set('value','')


def replace_known_x_y_unit(root, parent=None, grand_parent=None):
    """
    Replace known values with named ones
    """
    if root.tag == 'Def':
        root.tag = 'Def'
    if root.tag == 'Raster' or root.tag == 'Image-Size-XY':
        replace_known_x_y_unit_attrib(root)
    if root.tag == 'Size' and parent.tag == 'Raster':
        replace_known_x_y_unit_attrib(root)
    if root.tag == 'Offset' and parent.tag == 'Raster':
        replace_known_x_y_unit_attrib(root)
    if root.tag == 'value' and parent.tag == 'Position' and grand_parent.tag == 'Stage':
        replace_known_position(root,parent)
    if root.tag == 'Def' and parent.tag == 'Area' and grand_parent.tag == 'Spatial':
        replace_known_spatial(root)
    if root.tag == 'Map-Pixels-XY' and parent.tag == 'No':
        replace_known_x_y_unit_attrib(root)
    
    for child in list(root):
        replace_known_x_y_unit(child, root, parent)



def parse_file_to_xml(input_file, output_file,
                      create_plot=True, create_csv=True):
    """
    Parses a binary file into XML format
    and optionally generates plots and CSV files.
    """
    with open(input_file, "rb") as f:
        file_bytes = f.read()

    start_pos, end_pos = find_delimiters(file_bytes)
    content_bytes = file_bytes[start_pos + len("SOFH\r\n"):end_pos]
    content_str = content_bytes.decode("utf-8")
    lines = content_str.splitlines()

    # Initialize XML structure
    root = ET.Element("XpsMetaData")
    # spectral_regs[0] for Full, spectral_regs[1] for others
    spectral_regs = ([None] * 100, [None] * 100)

    # Process lines and populate XML
    counters = process_lines(lines, root, spectral_regs)

    spectral = root.find("Spectral")
    duplicated_subtree = copy.deepcopy(spectral)
    remove_elements_by_name(duplicated_subtree, "Full")
    remove_attributes_except_full(spectral)
    spectral.tag = "Spectral-Full"
    remove_empty_elements(spectral)
    remove_empty_elements(duplicated_subtree)
    for index in range(1, counters["NoSpectralReg"]+1):
        duplicate_and_keep(spectral, None, str(index))
    toDelete = spectral.find('Reg')
    if not(toDelete is None):
        spectral.remove(toDelete)
    for index in range(1, counters["NoSpectralReg"]+1):
        duplicate_and_keep(duplicated_subtree, None, str(index))
    duplicated_subtree.remove(duplicated_subtree.find('Reg'))
    root.append(duplicated_subtree)
    replace_attribute_with_subelements(spectral)
    replace_attribute_with_subelements(duplicated_subtree)
    compact_element_structure(root)

    replace_attribute_with_subelements(root.find('Channel'),1)
    replace_attribute_with_subelements(root.find('Stage'),1) 
    replace_attribute_with_subelements(root.find('TFC-Parameters'),1,',')

    defs = collect_def_elements_with_many_attributes(duplicated_subtree)
    collect_def_elements_with_many_attributes(spectral)
    replace_known_values(root)
    replace_known_x_y_unit(root)

    ftype = root.find('File').find('Type').attrib['value']
    fdesc = root.find('File').find('Desc').attrib['value']
    fdate = root.find('Acq').find('File-Date').attrib['value'].split()
    
    filedate = (int(fdate[0]), int(fdate[1])-1, int(fdate[2])-1, 0, 0, 0) 
    fdate = "" + fdate[0] + "."+  str(int(fdate[1])-1)+ "."+ str(int(fdate[2])-1)
  
    file_prefix = re.sub('[^0-9a-zA-Z]+', '_',f"{ftype}_{fdesc}_{fdate}")
    
    archive = BytesIO()

    with ZipFile(archive, 'w') as zip_archive:
        # Write XML to file
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ", level=0)
        
        file_info = zipfile.ZipInfo(filename=f"metadata.xml", date_time=filedate)
        
        with zip_archive.open(name=file_info,mode='w') as xml_file:
            xml_file.write(ET.tostring(tree.getroot(), encoding='UTF-8'))
                        
        # Extract and process float data
        position = extract_float_data(zip_archive,file_bytes, end_pos, defs,
                           counters, file_prefix, filedate, create_plot, create_csv)
        
        extract_float_image(zip_archive,file_bytes, position, root,
                           counters, file_prefix, filedate, create_plot, create_csv)
        

    with open(f"{output_file}.zip", 'wb') as f:
        f.write(archive.getbuffer())

