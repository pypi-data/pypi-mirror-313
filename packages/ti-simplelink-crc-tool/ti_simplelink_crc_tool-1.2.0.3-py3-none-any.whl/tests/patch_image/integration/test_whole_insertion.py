from crc_tool.util.consts import CRC_BYTE_COUNT
import pytest
from typing import List

import lief

from crc_tool.input_file_handlers.elf_handler import ElfHandler
from crc_tool.main import app

from tests.patch_image.util.consts import (
    VALID_IAR_ELF_FILE,
    VALID_TICLANG_ELF_FILE,
    VALID_GCC_ELF_FILE,
    INVALID_IAR_ELF_FILE,
    INVALID_TICLANG_ELF_FILE,
    INVALID_GCC_ELF_FILE,
    EXPECTED_ELF_FILE_SYMBOLS,
    SCRATCH_ELF_FILE_NAME
)
from crc_tool.util.util import get_crc_bytes
from tests.patch_image.util.consts import CCFG_WHOLE_LENGTH
from tests.patch_image.util.consts import EXAMPLE_ELF_CCFG_BEGIN


def __get_expected_with_crc(input_file: str, begin: int, end: int) -> List[int]:
    elf_file = lief.parse(input_file)
    length = end + 1 - begin
    prev_bytes = elf_file.get_content_from_virtual_address(begin, length)

    crc_bytes = get_crc_bytes(
        elf_file.get_content_from_virtual_address(begin, length)
    )
    return prev_bytes + crc_bytes


@pytest.mark.parametrize("input_elf", [VALID_GCC_ELF_FILE, VALID_IAR_ELF_FILE, VALID_TICLANG_ELF_FILE])
def test_can_add_crc_to_stated_elf_file(tmpdir, input_elf, caplog):
    # Arrange
    output_file = str(tmpdir / SCRATCH_ELF_FILE_NAME)
    original_elf_file = ElfHandler(input_elf)

    original_elf_file = lief.parse(input_elf)

    expected_crc_values = {}

    # Calculate expected crc values
    for key, item in EXPECTED_ELF_FILE_SYMBOLS.items():
        expected_crc_values[item[0]] = __get_expected_with_crc(
            input_elf,
            begin=item[0],
            end=item[1]
        )

    # act
    app(["patch-image", "--elf", input_elf, "-o", output_file, "-p", "__ccfg"])

    # assert
    output_elf_file = lief.parse(output_file)

    # Make sure check is actually run
    assert 0 < len(expected_crc_values)

    for key, item in expected_crc_values.items():
        section_length = len(item)

        generated_section = output_elf_file.get_content_from_virtual_address(key, section_length)
        unmodified_section = original_elf_file.get_content_from_virtual_address(key, section_length)
        # Check that non-crc section has not changed
        assert unmodified_section[:section_length - 4] == generated_section[:section_length - 4]
        # Check that whole section, including crc, is as we expect
        assert item == generated_section
    assert "No CRC was inserted into file" not in caplog.text


@pytest.mark.parametrize("input_elf", [VALID_GCC_ELF_FILE, VALID_IAR_ELF_FILE, VALID_TICLANG_ELF_FILE])
def test_assert_ccfg_does_not_change_when_no_symbol_is_found(tmpdir, input_elf, caplog):
    # Arrange
    output_file = str(tmpdir / SCRATCH_ELF_FILE_NAME)

    original_elf_file = lief.parse(input_elf)

    expected_crc_values = {}

    # Calculate expected crc values
    for key, item in EXPECTED_ELF_FILE_SYMBOLS.items():
        expected_crc_values[item[0]] = __get_expected_with_crc(
            input_elf,
            begin=item[0],
            end=item[1]
        )

    # act
    app(["patch-image", "--elf", input_elf, "-o", output_file, "-p", "__ccfg_invalid"])

    # assert
    output_elf_file = lief.parse(output_file)

    generated_section = output_elf_file.get_content_from_virtual_address(EXAMPLE_ELF_CCFG_BEGIN, CCFG_WHOLE_LENGTH)
    unmodified_section = original_elf_file.get_content_from_virtual_address(EXAMPLE_ELF_CCFG_BEGIN, CCFG_WHOLE_LENGTH)
    # Check that non-crc section has not changed
    assert unmodified_section == generated_section
    assert "No CRC was inserted into file" in caplog.text
