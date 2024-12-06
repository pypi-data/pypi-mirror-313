import random
import secrets
import pytest


@pytest.fixture
def random_name_generator():
    """Pytest fixture to get a method to generate random names."""
    def __gen_random_name() -> str:
        # Generate random hex string
        return secrets.token_hex(10)
    return __gen_random_name


@pytest.fixture
def val_hex_generator():
    """Pytest get a random number between 0 and 100 and its padded hex representation."""
    def __generate_random_val_hex_pair() -> str:
        # Generate random hex string
        rand_num = random.randint(0, 100)
        return (rand_num, f"{rand_num:#010x}")
    return __generate_random_val_hex_pair


@pytest.fixture
def symbol_pair_map_generator(random_name_generator):
    def __gen_random_sym_value_pair(begin=-1, end=-1):
        name = random_name_generator()
        if begin == -1:
            begin = random.randint(0, 100)
        if end == -1:
            end = begin + random.randint(0, 100)
        return {name: (begin, end)}
    return __gen_random_sym_value_pair
