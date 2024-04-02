# 3rd party

# standard
from pathlib import Path

# internal
import distances

def calculate_file_name_distance(filename1: str, filename2: str,
                                 distance_function: callable=distances.calculate_relative_distance,
                                 split_file_extension: bool=True,
                                 weights: tuple=(1, 0.2),
                                 make_lower_case: bool=True) -> float:
    """Calculate the distance between the two raw filenames with no paths
    :param filename1: first filename
    :type filename1: string
    :param filename2: second filename
    :type filename2: string
    :param distance_function: function to calculate the distance between the two strings, defaults to the relative distance metric
    :type distance_function: callable 
    :param split_file_extension: whether to split and treat the file extension as one character, defaults to True
    :type split_file_extension: boolean
    :param weights: weight of filename and weight of extension, defaults to (1, 0.2) or full weight on filename and 1/5 weight on file extension
    :type tuple: tuple of floats
    :param make_lower_case: flag on whether the filename should be lowercased, defaults to True or normalizing the filename case
    :type make_lower_case: boolean
    :return: addition of the distance times weight of filename and extension portions if split_file_extension is True, otherwise takes the levenshtein distance between the two strings
    :rtype: float
    """
    # calculate the weight of the file extension
    file_extension_distance = 0
    filename_weight = 1
    if split_file_extension:
        filename_weight = weights[0]
        filename1_extension_index = filename1.rfind('.')
        filename1, filename1_extension = filename1[:filename1_extension_index], filename1[filename1_extension_index:].lower()
        filename2_extension_index = filename2.rfind('.')
        filename2, filename2_extension = filename2[:filename2_extension_index], filename2[filename2_extension_index:].lower()
        file_extension_distance = (filename1_extension != filename2_extension) * weights[1]

    # normalize the filename if make_lower_case flag enabled
    if make_lower_case:
        filename1, filename2 = filename1.lower(), filename2.lower()

    # calculate the weight of the file name
    filename_distance = distance_function(filename1, filename2) * filename_weight

    return filename_distance + file_extension_distance

def calculate_full_path_distance(path1: str, path2: str,
                                 path_distance_function: callable=distances.calculate_list_distance,
                                 file_distance_function: callable=calculate_file_name_distance,
                                 weights: tuple=(0.2, 1)) -> float:
    path1, path2 = Path(path1), Path(path2)
    path_distance = 0
    if path1.parts[:-1] or path2.parts[:-1]:
        path_distance = path_distance_function(path1.parts[:-1], path2.parts[:-1]) * weights[0]
    file_distance = file_distance_function(path1.name, path2.name) * weights[1]

    return path_distance + file_distance
