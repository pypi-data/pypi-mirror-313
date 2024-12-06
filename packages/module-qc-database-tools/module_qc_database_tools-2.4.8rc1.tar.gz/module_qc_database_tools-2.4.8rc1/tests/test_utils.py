from __future__ import annotations

import module_qc_database_tools


def test_serial_number_to_uid():
    assert (
        module_qc_database_tools.utils.chip_serial_number_to_uid("20UPGFC0087209")
        == "0x154a9"
    )


def test_uid_to_serial_number():
    assert (
        module_qc_database_tools.utils.chip_uid_to_serial_number("0x154a9")
        == "20UPGFC0087209"
    )
