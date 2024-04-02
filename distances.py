# 3rd party
from Levenshtein import distance

# standard library

def calculate_relative_distance(str1: str, str2: str,
        distance_func: callable=distance,
        use_shorter_str_len_as_denominator: bool=True) -> float:
    """Return edit distance between strings accounting for length

    :param str1: first string to compare against the other string
    :type str1: string
    :param str2: second string to comparse against the other string
    :type str2: string
    :param distance_func: function to calculate string distance, defaults to Levenshtein.distance
    :type distance_func: callable
    :param use_shorter_str_len_as_denominator: flag to choose which string length to use in relative distance calculation, defaults to True or use the shorter string as the denominator in the calculation
    :type use_shorter_str_len_as_denominator: boolean
    :return: relative distance from 0-1 with 1 being the largest distance
    :rtype: float"""
    # get the relative distance denominator 
    # compare edits from shorter str perspective
    if use_shorter_str_len_as_denominator:
        str_denominator = min(len(str1), len(str2))
    else:
        str_denominator = max(len(str1), len(str2))

    edit_distance = distance_func(str1, str2)

    # calulate and return the relative distance
    return edit_distance / str_denominator

def calculate_list_distance(lst1: list, lst2: list,
                            make_lower_case: bool=True) -> int:
    """Calculate the distance between the two lists treating each item as a single character then running levenshtein distance
    :param lst1: list of items
    :type lst1: list
    :param lst2: list of items
    :type lst2: list
    :return: int of edit distance
    :rtype: int

    # Algorithm from - https://www.geeksforgeeks.org/introduction-to-levenshtein-distance/
    # Credit to Susobhan Akhuli for this implementation of the levenshtein distance
    """
    # edge case of no list
    if not lst1 or not lst2:
        return len(lst1) or len(lst2)
    # fails if the list contains non-string data
    if make_lower_case:
        lst1 = [x.lower() for x in lst1]
        lst2 = [x.lower() for x in lst2]
    # lengths of lists 
    m = len(lst1)
    n = len(lst2)
 
    # Initialize two rows for dynamic programming
    prev_row = [j for j in range(n + 1)]
    curr_row = [0] * (n + 1)
 
    # Dynamic programming to fill the matrix
    for i in range(1, m + 1):
        # Initialize the first element of the current row
        curr_row[0] = i
 
        for j in range(1, n + 1):
            if lst1[i - 1] == lst2[j - 1]:
                # items match, no operation needed
                curr_row[j] = prev_row[j - 1]
            else:
                # Choose minimum cost operation
                curr_row[j] = 1 + min(
                    curr_row[j - 1],  # Insert
                    prev_row[j],      # Remove
                    prev_row[j - 1]    # Replace
                )
 
        # Update the previous row with the current row
        prev_row = curr_row.copy()
 
    # The final element in the last row contains the Levenshtein distance
    return curr_row[n]
