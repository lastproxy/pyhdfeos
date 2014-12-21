import os
import pkg_resources as pkg
import tempfile
import unittest

import numpy as np

from pyhdfeos.lib import he4
from pyhdfeos import SwathFile

from . import fixtures

class TestMetadata4(unittest.TestCase):
    """
    """
    @classmethod
    def setUpClass(cls):
        file = pkg.resource_filename(__name__, os.path.join('data', 'Swath219.hdf'))
        cls.test_driver_swathfile4 = file

    def test_inqswaths4(self):
        swf = SwathFile(self.test_driver_swathfile4)
        self.assertEqual(list(swf.swaths.keys()), ['Swath1'])

    def test_inqgeofields4(self):
        swf = SwathFile(self.test_driver_swathfile4)
        self.assertEqual(list(swf.swaths['Swath1'].geofields.keys()),
                         ['Time', 'Longitude', 'Latitude'])

    def test_inqdatafields4(self):
        swf = SwathFile(self.test_driver_swathfile4)
        self.assertEqual(list(swf.swaths['Swath1'].datafields.keys()),
                         ['Density', 'Temperature', 'Temperature_3D',
                          'Pressure', 'Spectra', 'Count'])

    def test_inqdims(self):
        swf = SwathFile(self.test_driver_swathfile4)
        self.assertEqual(swf.swaths['Swath1'].dims,
                         {'GeoTrack': 20,
                          'GeoXtrack': 10,
                          'Res2tr': 40,
                          'Res2xtr': 20, 
                          'Bands': 15,
                          'IndxTrack': 12,
                          'Unlim': 0})


class TestMetadata5(unittest.TestCase):
    """
    """
    @classmethod
    def setUpClass(cls):
        file = pkg.resource_filename(__name__, os.path.join('data',
                                                            'SimpleSwath.h5'))
        cls.swathfile = file

    def test_inqgeofields(self):
        swf = SwathFile(self.swathfile)
        self.assertEqual(list(swf.swaths['INDEX'].geofields.keys()),
                         ['Latitude', 'Longi'])
        self.assertEqual(list(swf.swaths['SIMPLE'].geofields.keys()),
                         ['Time', 'Latitude', 'Longitude'])

    def test_inqdatafields(self):
        swf = SwathFile(self.swathfile)
        self.assertEqual(list(swf.swaths['INDEX'].datafields.keys()),
                         ['Indexed_Data'])
        self.assertEqual(list(swf.swaths['SIMPLE'].datafields.keys()),
                         ['Temperature', 'Count', 'Conduction'])

    def test_inqswaths(self):
        swf = SwathFile(self.swathfile)
        self.assertEqual(list(swf.swaths.keys()), ['INDEX', 'SIMPLE'])

    def test_inqdims(self):
        swf = SwathFile(self.swathfile)
        self.assertEqual(swf.swaths['INDEX'].dims,
                         {'TrackDim': 8,
                          'XtrackDim': 8,
                          'GeoDim': 6,
                          'GeoXDim': 6})
        self.assertEqual(swf.swaths['SIMPLE'].dims['DataTrack'], 10)
        self.assertEqual(swf.swaths['SIMPLE'].dims['DataXtrack'], 4)
        self.assertEqual(swf.swaths['SIMPLE'].dims['GeoTrack'], 5)
        self.assertEqual(swf.swaths['SIMPLE'].dims['GeoXtrack'], 4)
        self.assertTrue('Unlim' in swf.swaths['SIMPLE'].dims)

