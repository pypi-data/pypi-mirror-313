import os

from sphinx.application import Sphinx
from sphinx.util.fileutil import copy_asset_file

try:
    from sphinx_tudelft_theme._version import version as __version__
except ImportError:
    __version__ = "1.0.0"

def copy_stylesheet(app: Sphinx, exc: None) -> None:
    base_dir = os.path.dirname(__file__)
    style = os.path.join(base_dir, 'static', 'tudelft_style.css')
    fonts_src_dir = os.path.join(base_dir, 'static', 'fonts', 'RobotoSlab-Regular.ttf')
    
    if app.builder.format == 'html' and not exc:
        static_dir = os.path.join(app.builder.outdir, '_static')
        fonts_dest_dir = os.path.join(static_dir, 'fonts')

        copy_asset_file(style, static_dir)
        copy_asset_file(fonts_src_dir, fonts_dest_dir)


def setup(app: Sphinx):
    app.add_css_file('tudelft_style.css')
    app.connect('build-finished', copy_stylesheet)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }