# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    company: str = "Northwind Engineering"
    accent: str = "#245b63"
    pale: str = "#edf4f3"
    font: str = "Libertinus Serif"


DEFAULT_THEME = Theme()
