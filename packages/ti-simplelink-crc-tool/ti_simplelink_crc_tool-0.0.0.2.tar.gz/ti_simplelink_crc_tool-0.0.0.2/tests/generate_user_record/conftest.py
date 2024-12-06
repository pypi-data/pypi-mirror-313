"Common test methods for generate_user_record"
from typing import List

def get_integers_which_sum_to(desired_sum: int, num_integers: int) -> List[int]:
    "Get list of integers which sums to input, with length num_components"
    # Cannot sum to 5 with 100 integers for example
    assert num_integers <= desired_sum

    # Assign each value a minimum
    minimum_value = desired_sum // num_integers
    integer_list = [minimum_value] * num_integers
    counter = 0
    # Iterate through integers and add 1 until we reach desired sum
    while sum(integer_list) < desired_sum:
        integer_list[counter] += 1
        counter += 1
        counter = counter % len(integer_list)
    return integer_list
