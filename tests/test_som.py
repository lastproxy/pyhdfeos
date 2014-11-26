import unittest

import numpy as np

from pyhdfeos import som
from pyhdfeos.lib import he4

from . import fixtures

class TestSuite(unittest.TestCase):

    def test_som(self):
        nline = 128
        nsample = 512
        file = 'MISR_AM1_GRP_ELLIPSOID_GM_P117_O058421_BA_F03_0024.hdf'
        file = fixtures.test_file_path(file)
        gdfid = he4.gdopen(file)
        gridid = he4.gdattach(gdfid, 'BlueBand')
        actual = he4.gdblksomoffset(gridid)
        shape, upleft, lowright = he4.gdgridinfo(gridid)
        projcode, zonecode, spherecode, projparms = he4.gdprojinfo(gridid)
        offset = he4.gdblksomoffset(gridid)
        he4.gddetach(gridid)
        he4.gdclose(gdfid)
        misr.init(shape[1], shape[0], offset, upleft, lowright)
        som.inv_init(projcode, projparms, spherecode)
        lat = np.zeros((nline,nsample, len(offset)+1))
        lon = np.zeros((nline,nsample, len(offset)+1))
        for b in range(len(offset) + 1):
            for j in range(nline):
                for k in range(nsample):
                    l = j
                    s = k
                    somx, somy = misr.inv(b+1, l, s)
                    lon_r, lat_r = som.inv(somx, somy)
                    lon[j,k,b] = lon_r
                    lat[j,k,b] = lat_r


