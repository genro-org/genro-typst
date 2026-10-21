"""Every catalog entry: real PDF/SVG, independent reference, TYTX and errors."""

from xml.etree import ElementTree

import pytest
import typst
from genro_builders import SourceBag

from genro_typst import TypstBuilder
from genro_typst.compiler import TypstEngine
from genro_typst.native_catalog import NATIVE
from native_cases import CASES, build_case, example_python, write_assets


def test_examples_cover_exactly_the_catalog():
    assert set(CASES) == set(NATIVE)


def restore(builder):
    result = TypstBuilder()
    source = SourceBag.from_tytx(builder.source.to_tytx())
    source._builder = result
    for node in source.traverse():
        if isinstance(node.value, SourceBag):
            node.value._builder = result
    source.set_backref()
    result.source = source
    return result


@pytest.mark.parametrize("tag", CASES)
def test_catalog_pdf_svg_reference_and_roundtrip(tag, tmp_path):
    write_assets(tmp_path)
    builder, _node, reference = build_case(CASES[tag])
    assert builder.validate_source() == []
    source = builder.render()
    namespace = {}
    exec(example_python(builder), namespace)  # noqa: S102 - owned, explicit test fixtures
    assert namespace["source"] == source
    restored = restore(builder)
    assert restored.validate_source() == []
    assert restored.render() == source
    (tmp_path / "generated.typ").write_text(source)
    (tmp_path / "reference.typ").write_text(reference)
    compiled = TypstEngine().compile(source, root=tmp_path, preview=True)
    assert compiled.pdf.startswith(b"%PDF")
    assert compiled.pages == len(compiled.svg_pages)
    assert compiled.pages == {"page": 3, "pagebreak": 2}.get(tag, 1)
    for page in compiled.svg_pages:
        svg = ElementTree.fromstring(page)
        assert svg.tag == "{http://www.w3.org/2000/svg}svg"
        assert float(svg.attrib["width"].removesuffix("pt")) > 0
        assert float(svg.attrib["height"].removesuffix("pt")) > 0
    expected = typst.compile(reference.encode(), root=str(tmp_path), format="svg")
    if isinstance(expected, bytes):
        expected = [expected]
    if compiled.svg_pages != tuple(expected):
        for index, page in enumerate(compiled.svg_pages, 1):
            (tmp_path / f"actual-{index}.svg").write_bytes(page)
        for index, page in enumerate(expected, 1):
            (tmp_path / f"expected-{index}.svg").write_bytes(page)
    assert compiled.svg_pages == tuple(expected), source + "\nREFERENCE:\n" + reference


@pytest.mark.parametrize("tag", CASES)
def test_catalog_rejects_unknown_parameter(tag, tmp_path):
    write_assets(tmp_path)
    builder, node, _reference = build_case(CASES[tag])
    node.attr["nonexistent_native_parameter"] = True
    with pytest.raises(typst.TypstError, match="unexpected argument"):
        TypstEngine().compile(builder.render(), root=tmp_path)
