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

def copy_logos(app: Sphinx, exc: None) -> None:
    base_dir = os.path.dirname(__file__)
    light = os.path.join(base_dir, 'static', 'TUDelft_logo_descriptor_rgb.png')
    dark = os.path.join(base_dir, 'static', 'TUDelft_logo_descriptor_white.png')
    
    if app.builder.format == 'html' and not exc:
        static_dir = os.path.join(app.builder.outdir, '_static')

        copy_asset_file(light, static_dir)
        copy_asset_file(dark, static_dir)

def set_logo(app,conf) -> None:
    if conf.tud_change_logo:
        print('Changing logo to TU Delft logo')
        old =  app.config.html_theme_options
        old['logo'] = {'image_light':'TUDelft_logo_descriptor_rgb.png','image_dark': 'TUDelft_logo_descriptor_white.png'}
        app.config.html_theme_options = old
    else:
        print('Using user-defined logo')


def setup(app: Sphinx):
    app.add_config_value('tud_change_logo', True, 'env')
    app.add_css_file('tudelft_style.css')
    app.connect('build-finished', copy_stylesheet)
    app.connect('build-finished', copy_logos)
    app.connect('config-inited',set_logo)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }