
import os
from pathlib import Path

CONST_LOCATION = Path(__file__).parent

USER_RECORD_EXAMPLE = os.path.join(CONST_LOCATION.parents[2], "docs/examples/generate_user_record/user_record_example.txt")
USER_RECORD_EXAMPLE_EXPECTED_CRC = "52148fe6"

DATA_FOLDER = os.path.join(CONST_LOCATION.parents[0], "data/")
NO_VALUE_USER_RECORD = os.path.join(DATA_FOLDER, "no_value_user_record.txt")
DOUBLE_VALUE_USER_RECORD = os.path.join(DATA_FOLDER, "double_value_user_record.txt")
MULTI_INTEGER_SUPPORT_USER_RECORD = os.path.join(DATA_FOLDER, "multi_integer_support.txt")
ZERO_VALUE_USER_RECORD = os.path.join(DATA_FOLDER, "zero_value_user_record.txt")

SCRATCH_BIN_FILE_NAME = "temp.bin"

EXAMPLE_TXT1 = "000102030405060708090A0B"
EXAMPLE_TXT1_WITH_PREFIX = "0x000102030405060708090A0B"
TXT1_BYTE_ARRAY = [
    0x0B,
    0x0A,
    0x09,
    0x08,
    0x07,
    0x06,
    0x05,
    0x04,
    0x03,
    0x02,
    0x01,
    0x00,
] + [0] * (124 - 12)

TXT1_CRC_BYTE_ARRAY = [0x99, 0x9B, 0xCE, 0x4F]

EXAMPLE_TXT_SHORT1 = "00102034"
SHORT1_BYTE_ARRAY = [0x34, 0x20, 0x10, 0x0, 0x0] + [0] * (124 - 5)
SHORT1_CRC_BYTE_ARRAY = [182, 0x2b, 0xF8, 0x2]
