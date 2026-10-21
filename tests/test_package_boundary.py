"""The library works without application or optional compiler imports."""

import subprocess
import sys

import pytest

from genro_typst import TypstBuilder
from genro_typst.compiler import TypstEngine


def test_source_generation_does_not_import_app_or_compiler():
    code = '''
import sys
from importlib.abc import MetaPathFinder
class RejectApplications(MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'genro_pdf_builder', 'kajenn', 'gramlot', 'weasyprint', 'typst'}:
            raise AssertionError(f'Unexpected dependency: {fullname}')
sys.meta_path.insert(0, RejectApplications())
from genro_typst import TypstBuilder
builder = TypstBuilder()
builder.source.document().paragraph(content='Independent library')
assert 'Independent library' in builder.render()
'''
    subprocess.run([sys.executable, '-c', code], check=True, capture_output=True, text=True)


def test_typst_compiler_produces_pdf_and_svg():
    result = TypstEngine().compile('= Standalone library', preview=True)
    assert result.pdf.startswith(b'%PDF')
    assert result.pages == 1
    assert b'<svg' in result.svg_pages[0]


def test_pdf_builder_keeps_typst_engine_and_supports_stream():
    import io

    builder = TypstBuilder()
    builder.source.document().paragraph(content='PDF stream')
    with pytest.raises(ValueError, match='requires the typst engine'):
        builder.render(mode='pdf', engine='weasyprint')
    stream = io.BytesIO()
    builder.render(mode='pdf', target=stream)
    assert stream.getvalue().startswith(b'%PDF')
