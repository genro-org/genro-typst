# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Python values to Typst code fragments."""

from __future__ import annotations

import pytest

from genro_typst.typst_values import (
    typst_align,
    typst_color,
    typst_length,
    typst_string,
    typst_width,
)


def test_string_escapes():
    assert typst_string('a"b\\c\nd') == '"a\\"b\\\\c\\nd"'
    assert typst_string("#*_$@<") == '"#*_$@<"'


@pytest.mark.parametrize("value", ["25mm", "2.5cm", "10pt", "30%", "2fr", "auto", "1em"])
def test_length_accepted(value):
    assert typst_length(value) == value


@pytest.mark.parametrize("value", ["25", "25 mm", "mm", "1px"])
def test_length_rejected(value):
    with pytest.raises(ValueError):
        typst_length(value)


def test_length_must_be_a_string():
    with pytest.raises(TypeError):
        typst_length(25)


def test_width_numbers_are_fractions():
    assert typst_width(0) == "1fr"
    assert typst_width(2) == "2fr"
    assert typst_width("30mm") == "30mm"
    with pytest.raises(ValueError):
        typst_width(-1)
    with pytest.raises(TypeError):
        typst_width(True)


def test_color():
    assert typst_color("#eeeeee") == 'rgb("#eeeeee")'
    assert typst_color("red") == "red"
    with pytest.raises(ValueError):
        typst_color("lightred")


def test_align():
    assert typst_align("right", "middle") == "right + horizon"
    assert typst_align(None, None) is None
    with pytest.raises(ValueError):
        typst_align("justify", None)
