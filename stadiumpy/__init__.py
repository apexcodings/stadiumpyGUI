# -*- coding: utf-8 -*-
"""
Initialize the library.
:copyright: 2020 STADIUMPy
:license: MIT
"""
# from stadiumpy.stadiumpy.startpage import StartPage
# from stadiumpy.prf_page import prfview
# from stadiumpy.srf_page import srfview
# from stadiumpy.dataenquirypage import dataenquiry
# from stadiumpy.sks_page import sksview
# from stadiumpy.page_control import PageControl
# from stadiumpy.plot_map_gui import plotMap

print("Hello from ", __name__)

__version__ = "unknown"
try:
    from ._version import __version__
except ImportError:
    pass