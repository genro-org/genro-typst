# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Example component library: ordinary Python functions, no plugin registry."""

from .chrome import branded_document
from .sections import contact_card, item_table, notice, signature
from .theme import Theme

__all__ = ["Theme", "branded_document", "contact_card", "item_table", "notice", "signature"]
