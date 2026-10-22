Declared grammar signatures
===========================

Generated from the Python grammar declarations. Do not edit by hand.
Call these methods on source nodes; they are not module-level functions.
Language constructs use keyword arguments. For ``label``, use the
``typst_label`` alias to avoid the SourceBag property with that name.
See :doc:`typst-guide` for usage and :doc:`native-reference` for native calls.

Legacy document elements
------------------------

.. py:function:: document(paper='a4', flipped=False, margin='15mm', page_options=None, metadata=None)

   Document root: page format, orientation and margins.

   :param paper: Paper name (``a4``, ``a5``, ``us-letter``...).
   :param flipped: Landscape orientation.
   :param margin: Page margin on every side.

.. py:function:: layout(border_width=None, border_color='black', row_border=True, cell_border=True, inset='1mm')

   Layout container: a vertical sequence of rows.

   :param border_width: Width of the outer border and of the lines between rows and cells. ``None`` draws no line.
   :param border_color: Color of every line of the layout.
   :param row_border: Default for the line below each row.
   :param cell_border: Default for the line after each cell.
   :param inset: Padding inside every cell.

.. py:function:: row(height=None, row_border=None, cell_border=None)

   Row: a horizontal sequence of cells.

   :param height: Row height. ``None`` takes the height of the content.
   :param row_border: Line below this row (``None`` inherits from layout).
   :param cell_border: Default for the cells of this row (``None`` inherits from layout).

.. py:function:: cell(content=None, width=0, lbl=None, cell_border=None, align=None, valign=None, background=None)

   Cell: text content, nested layout or content elements.

   :param content: Text of the cell, shown after the label.
   :param width: Number (fraction, ``0`` = ``1fr``) or length string.
   :param lbl: Label shown above the content.
   :param cell_border: Line after this cell (``None`` inherits from row).
   :param align: ``left``, ``center``, ``right``.
   :param valign: ``top``, ``middle``, ``bottom``.
   :param background: Fill color (``'#rrggbb'`` or a Typst color name).

.. py:function:: table(data='', headerRepeat=True, totalize_footer=False, border_width='0.5pt', border_color='black', inset='1mm')

   Data table: one row per child of the ``data`` Bag.

   The columns come from the ``column`` children (GenroPy grid struct).

   :param data: Pointer to a Bag whose children are the rows (each a Bag of fields).
   :param headerRepeat: Repeat the header on every page.
   :param totalize_footer: Total row after the last row. A string is the caption, shown across the columns before the first total (GenroPy ``totalize_footer``). ``True`` shows no caption.
   :param border_width: Width of the table lines.
   :param border_color: Color of the table lines.
   :param inset: Padding inside every cell.

.. py:function:: column(field='', name='', width=0, align=None, totalize=False)

   Column of a data table.

   :param field: Field of the row Bag shown in the column.
   :param name: Header text.
   :param width: Number (fraction, ``0`` = ``1fr``) or length string.
   :param align: ``left``, ``center``, ``right``.
   :param totalize: Sum the column in the total row.

.. py:function:: paragraph(content='')

   Paragraph of plain text.

.. py:function:: pageNumber(template='{page} / {total}')

   Page number. ``{page}`` is the current page, ``{total}`` the last.

Language constructs
-------------------

.. py:function:: call(function, content=None, args=None, options=None, mode='body', **attrs)

   Call a native or imported Typst function; mode is body, items, args or value.

.. py:function:: set_rule(target, options=None, **attrs)

   Emit a set rule; applies to following siblings in the enclosing scope.

.. py:function:: show_rule(selector, transform=None, target=None, options=None, **attrs)

   Emit a transformational show or show-set rule.

.. py:function:: scope()

   Content scope: local set/show/let rules do not escape.

.. py:function:: context()

   Evaluate children in Typst's contextual evaluation scope.

.. py:function:: equation(formula, block=True, **options)

   Math-mode Typst source without the surrounding dollar signs.

.. py:function:: label(name)

   Attach a label to the preceding labellable element.

.. py:function:: let(name, value)

   Bind a literal or explicit expression for following siblings.

.. py:function:: import_module(path, names=None, alias=None)

   Import a local module or versioned Typst package.

.. py:function:: include(path)

   Include a local Typst file relative to the compiler root.

.. py:function:: typst_code(code)

   Insert trusted Typst code as one code block; definitions stay local.

.. py:function:: typst_markup(source)

   Insert trusted Typst markup in its own content scope.
