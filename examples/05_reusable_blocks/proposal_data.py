# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Demonstration data; an application could supply these records from a Bag or DB."""

CUSTOMER = {"name": "Riverbank Foods", "details": "Packaging line B · Bristol"}
SECTIONS = [
    {"title": "Control cabinet", "items": [
        {"description": "Cabinet and power supply", "quantity": 1, "unit": "set", "price": "1850.00"},
        {"description": "I/O expansion module", "quantity": 4, "unit": "pc", "price": "215.50"},
        {"description": "Wiring and assembly", "quantity": 16, "unit": "h", "price": "65.00"},
    ], "note": "Factory-tested before delivery. Circuit diagrams supplied as an appendix."},
    {"title": "Installation and commissioning", "items": [
        {"description": "On-site installation", "quantity": 24, "unit": "h", "price": "75.00"},
        {"description": "Operator training", "quantity": 4, "unit": "h", "price": "90.00"},
        {"description": "Acceptance test", "quantity": 1, "unit": "day", "price": "650.00"},
    ], "note": "The customer provides safe access to the line during the agreed shutdown."},
]
