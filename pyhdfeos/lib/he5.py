import os
import platform
import sys

from cffi import FFI
import numpy as np

from . import config

CDEF = """
    typedef unsigned uintn;
    typedef unsigned long long hsize_t;
    typedef int hid_t;
    typedef int herr_t;

    hid_t  HE5_GDattach(hid_t fid, char *gridname);
    long   HE5_GDattrinfo(hid_t gridID, const char *attrname,
                             hid_t *ntype, hsize_t *count);
    herr_t HE5_GDclose(hid_t fid);
    herr_t HE5_GDdetach(hid_t gridid);
    herr_t HE5_GDfieldinfo(hid_t gridID, const char *fieldname, int *rank,
                           hsize_t dims[], hid_t *ntype, char *dimlist,
                           char *maxdimlist);
    herr_t HE5_GDgridinfo(hid_t gridID, long *xdimsize, long *ydimsize,
                          double upleftpt[], double lowrightpt[]);
    herr_t HE5_GDij2ll(int projcode, int zonecode,
                       double projparm[], int spherecode, long xdimsize,
                       long ydimsize, double upleft[], double lowright[],
                       long npts, long row[], long col[],
                       double longititude[], double latitude[],
                       int pixcen, int pixcnr);
    long   HE5_GDinqattrs(hid_t gridID, char *attrnames, long *strbufsize);
    int    HE5_GDinqdims(hid_t gridid, char *dims, hsize_t *dims);
    int    HE5_GDinqfields(hid_t gridID, char *fieldlist, int rank[],
                           hid_t ntype[]);
    long   HE5_GDinqgrid(const char *filename, char *gridlist,
                         long *strbufsize);
    long   HE5_GDinqlocattrs(hid_t gridID, char *fieldname, char *attrnames,
                             long *strbufsize);
    long   HE5_GDlocattrinfo(hid_t gridID, char *fieldname, char *attrname,
                             hid_t *ntype, hsize_t *count);
    long   HE5_GDnentries(hid_t gridID, int entrycode, long *strbufsize);
    hid_t  HE5_GDopen(const char *filename, uintn access);
    herr_t HE5_GDorigininfo(hid_t gridID, int *origincode);
    herr_t HE5_GDpixreginfo(hid_t gridID, int *pixregcode);
    herr_t HE5_GDprojinfo(hid_t gridID, int *projcode, int *zonecode,
                          int *spherecode, double projparm[]);
    herr_t HE5_GDreadattr(hid_t gridID, const char* attrname, void *buffer);
    herr_t HE5_GDreadfield(hid_t gridid, const char* fieldname,
                           const hsize_t start[],
                           const hsize_t stride[],
                           const hsize_t edge[],
                           void *buffer);
    herr_t HE5_GDreadlocattr(hid_t gridID, const char *fieldname,
                             const char *attrname, void *databuf);
    /*int HE5_EHHEisHE5(char *filename);*/
"""

SOURCE = """
    #include "HE5_HdfEosDef.h"
"""

ffi = FFI()
ffi.cdef(CDEF)

libraries = config.hdfeos5_libs
library_dirs = config.library_config(libraries)

_lib = ffi.verify(SOURCE,
                  ext_package='pyhdfeos',
                  libraries=libraries,
                  include_dirs=config.include_dirs,
                  library_dirs=library_dirs,
                  modulename=config._create_modulename("_hdfeos5",
                                                       CDEF,
                                                       SOURCE,
                                                       sys.version))

H5F_ACC_RDONLY = 0x0000

HE5_HDFE_NENTDIM = 0
HE5_HDFE_NENTDFLD = 4

number_type_dict = {0: np.int32,
                    1: np.uint32,
                    2: np.int16,
                    3: np.uint16,
                    4: np.int8,
                    5: np.uint8,
                    8: np.int64,
                    9: np.uint64,
                    10: np.float32,
                    11: np.float64,
                    57: np.str
        }

    
cast_string_dict = {0: "int *",
                    1: "unsigned int *",
                    2: "short int *",
                    3: "unsigned short int *",
                    4: "signed char *",
                    5: "unsigned char *",
                    8: "long long int *",
                    9: "unsigned long long int *",
                    10: "float *",
                    11: "double *",
                    57: "char *"
        }

    
def _handle_error(status):
    if status < 0:
        raise IOError("Library routine failed.")

def gdattach(gdfid, gridname):
    """Attach to an existing grid within the file.

    This function wraps the HDF-EOS5 HE5_GDattach library function.

    Parameters
    ----------
    gdfid : int
        grid file id
    gridname : str
        name of grid to be attached

    Returns
    -------
    grid_id : int
        grid identifier
    """
    return _lib.HE5_GDattach(gdfid, gridname.encode())

def gdattrinfo(grid_id, attrname):
    """return information about a grid attribute

    Parameters
    ----------
    grid_id : int
        grid identifier
    attrname : str
        attribute name

    Returns
    -------
    ntype : int
        number type of attribute, see Appendix A in "HDF-EOS Interface Based
        on HDF5, Volume 2: Function Reference Guide"
    count : int
        number of attribute elements
    """
    ntypep = ffi.new("hid_t *")
    countp = ffi.new("hsize_t *")
    status = _lib.HE5_GDattrinfo(grid_id, attrname.encode(), ntypep, countp)
    _handle_error(status)

    return ntypep[0], countp[0]

def gdclose(fid):
    """Closes the HDF-EOS grid file.

    This function wraps the HDF-EOS5 HE5_GDclose library function.

    Parameters
    ----------
    fid : int
        grid file ID
    """
    status = _lib.HE5_GDclose(fid)
    _handle_error(status)

def gddetach(grid_id):
    """Detach from grid structure.

    This function wraps the HDF-EOS5 HE5_GDdetach library function.

    Parameters
    ----------
    grid_id : int
        Grid identifier.
    """
    status = _lib.HE5_GDdetach(grid_id)
    _handle_error(status)

def gdfieldinfo(grid_id, fieldname):
    """Return information about a geolocation field or data field in a grid.

    This function wraps the HDF-EOS5 HE5_GDfieldinfo library function.

    Parameters
    ----------
    grid_id : int
        Grid identifier.
    fieldname : str
        field name

    Returns
    -------
    shape : tuple
        size of the field
    ntype : type
        datatype of the field
    dimlist, maxdimlist : list
        list of dimensions
    """
    _, strbufsize = gdnentries(grid_id, HE5_HDFE_NENTDIM)
    dimlist_buffer = ffi.new("char[]", b'\0' * (strbufsize + 1))
    max_dimlist_buffer = ffi.new("char[]", b'\0' * (strbufsize + 1))

    rankp = ffi.new("int *")
    ntypep = ffi.new("hid_t *")

    # Assume that no field has more than 8 dimensions.  Seems like a safe bet.
    #dimsp = ffi.new("unsigned long long []", 8)
    dims = np.zeros(8, dtype=np.uint64)
    dimsp = ffi.cast("hsize_t *", dims.ctypes.data)

    status = _lib.HE5_GDfieldinfo(grid_id, fieldname.encode(), rankp, dimsp,
                                  ntypep, dimlist_buffer, max_dimlist_buffer)
    _handle_error(status)

    shape = []
    for j in range(rankp[0]):
        shape.append(dimsp[j])

    dimlist = ffi.string(dimlist_buffer).decode('ascii').split(',')
    maxdimlist = ffi.string(max_dimlist_buffer).decode('ascii').split(',')

    return tuple(shape), ntypep[0], dimlist, maxdimlist

def gdgridinfo(grid_id):
    """Return information about a grid structure.

    This function wraps the HDF-EOS5 HE5_GDgridinfo library function.

    Parameters
    ----------
    grid_id : int
        Grid identifier.

    Returns
    -------
    shape : tuple
        Number of rows, columns in grid.
    upleft, lowright : np.float64[2]
        Location in meters of upper left, lower right corners.
    """
    xdimsize = ffi.new("long *")
    ydimsize = ffi.new("long *")
    upleft_buffer = ffi.new("double[]", 2)
    lowright_buffer = ffi.new("double[]", 2)

    upleft = np.zeros(2, dtype=np.float64)
    upleftp = ffi.cast("double *", upleft.ctypes.data)
    lowright = np.zeros(2, dtype=np.float64)
    lowrightp = ffi.cast("double *", lowright.ctypes.data)

    status = _lib.HE5_GDgridinfo(grid_id, xdimsize, ydimsize, upleftp, lowrightp)
    _handle_error(status)

    return xdimsize[0], ydimsize[0], upleft, lowright

def gdij2ll(projcode, zonecode, projparm, spherecode, xdimsize, ydimsize,
            upleft, lowright, row, col, pixcen, pixcnr):
    """Convert coordinates (i, j) to (longitude, latitude).

    This function wraps the HDF-EOS5 HE5_GDij2ll library function.

    Parameters
    ----------
    projcode : int
        GCTP projection code
    zonecode : int
        GCTP zone code used by UTM projection
    projparm : ndarray
        Projection parameters.
    spherecode : int
        GCTP spherecode
    xdimsize, ydimsize : int
        Size of grid.
    upleft, lowright : ndarray
        Upper left, lower right corner of the grid in meter (all projections
        except Geographic) or DMS degree (Geographic).
    row, col : ndarray
        row, column numbers of the pixels (zero based)

    Returns
    -------
    longitude, latitude : ndarray
        Longitude and latitude in decimal degrees.
    """
    # This might be wrong on 32-bit machines.
    if sys.maxsize < 2**32 and platform.system().startswith('Linux'):
        row = row.astype(np.int32)
        col = col.astype(np.int32)
    else:
        row = row.astype(np.int64)
        col = col.astype(np.int64)

    longitude = np.zeros(col.shape, dtype=np.float64)
    latitude = np.zeros(col.shape, dtype=np.float64)
    upleftp = ffi.cast("double *", upleft.ctypes.data)
    lowrightp = ffi.cast("double *", lowright.ctypes.data)
    projparmp = ffi.cast("double *", projparm.ctypes.data)
    colp = ffi.cast("long *", col.ctypes.data)
    rowp = ffi.cast("long *", row.ctypes.data)
    longitudep = ffi.cast("double *", longitude.ctypes.data)
    latitudep = ffi.cast("double *", latitude.ctypes.data)
    status = _lib.HE5_GDij2ll(projcode, zonecode, projparmp, spherecode,
                              xdimsize, ydimsize, upleftp, lowrightp, col.size,
                              rowp, colp, longitudep, latitudep, pixcen, pixcnr)
    return longitude, latitude

def gdinqattrs(gridid):
    """Retrieve information about attributes for a specific grid.

    This function wraps the HDF-EOS5 HE5_GDinqattrs library function.

    Parameters
    ----------
    grid_id : int
        grid identifier

    Returns
    -------
    attrlist : list
        list of attributes defined for the grid
    """
    strbufsizep = ffi.new("long *")
    nattrs = _lib.HE5_GDinqattrs(gridid, ffi.NULL, strbufsizep)
    if nattrs == 0:
        return []
    strbufsize = strbufsizep[0]
    strbufsize = max(strbufsize, 1000)
    attr_buffer = ffi.new("char[]", b'\0' * (strbufsize + 1))
    nattrs = _lib.HE5_GDinqattrs(gridid, attr_buffer, strbufsizep)
    _handle_error(nattrs)
    if sys.hexversion < 0x03000000:
        attr_list = ffi.string(attr_buffer).split(',')
    else:
        attr_list = ffi.string(attr_buffer).decode('ascii').split(',')
    return attr_list

def gdinqdims(gridid):
    """Retrieve information about dimensions defined in a grid.

    This function wraps the HDF-EOS5 HE5_GDinqdims library function.

    Parameters
    ----------
    grid_id : int
        grid identifier

    Returns
    -------
    dimlist : list
        list of dimensions defined for the grid
    dimlens : ndarray
        corresponding length of each dimension
    """
    ndims, strbufsize = gdnentries(gridid, HE5_HDFE_NENTDIM)
    dim_buffer = ffi.new("char[]", b'\0' * (strbufsize + 1))
    dimlens = np.zeros(ndims, dtype=np.uint64)
    dimlensp = ffi.cast("unsigned long long *", dimlens.ctypes.data)
    status = _lib.HE5_GDinqdims(gridid, dim_buffer, dimlensp)
    _handle_error(status)
    dimlist = ffi.string(dim_buffer).decode('ascii').split(',')
    return dimlist, dimlens

def gdinqfields(gridid):
    """Retrieve information about the data fields defined in a grid.

    This function wraps the HDF-EOS5 HE5_GDinqfields library function.

    Parameters
    ----------
    grid_id : int
        grid identifier

    Returns
    -------
    fields : list
        List of fields in the grid.
    ranks : list
        List of ranks corresponding to the fields
    numbertypes : list
        List of numbertypes corresponding to the fields
    """
    nfields, strbufsize = gdnentries(gridid, HE5_HDFE_NENTDFLD)
    if nfields == 0:
        return [], None, None

    fieldlist_buffer = ffi.new("char[]", b'\0' * (strbufsize + 1))
    ranks = np.zeros(nfields, dtype=np.int32)
    rankp = ffi.cast("int *", ranks.ctypes.data)
    numbertypes = np.zeros(nfields, dtype=np.int32)
    numbertypep = ffi.cast("hid_t *", numbertypes.ctypes.data)
    nfields2 = _lib.HE5_GDinqfields(gridid, fieldlist_buffer,
                                    rankp, numbertypep)
    if sys.hexversion < 0x03000000:
        fieldlist = ffi.string(fieldlist_buffer).split(',')
    else:
        fieldlist = ffi.string(fieldlist_buffer).decode('ascii').split(',')

    return fieldlist, ranks, numbertypes

def gdinqgrid(filename):
    """Retrieve names of grids defined in HDF-EOS5 file.

    This function wraps the HDF-EOS5 HE5_GDinqgrid library function.

    Parameters
    ----------
    filename : str
        name of file

    Returns
    -------
    gridlist : list
        List of grids defined in HDF-EOS file.
    """
    strbufsizep = ffi.new("long *")
    ngrids = _lib.HE5_GDinqgrid(filename.encode(), ffi.NULL, strbufsizep)
    if ngrids == 0:
        return []
    gridbuffer = ffi.new("char[]", b'\0' * (strbufsizep[0] + 1))
    ngrids = _lib.HE5_GDinqgrid(filename.encode(), gridbuffer, ffi.NULL)
    _handle_error(ngrids)
    if sys.hexversion < 0x03000000:
        gridlist = ffi.string(gridbuffer).split(',')
    else:
        gridlist = ffi.string(gridbuffer).decode('ascii').split(',')
    return gridlist

def gdinqlocattrs(gridid, fieldname):
    """Retrieve information about grid field attributes.

    This function wraps the HDF-EOS5 HE5_GDinqlocattrs library function.

    Parameters
    ----------
    grid_id : int
        grid identifier
    fieldname : str
        retrieve attribute names for this field

    Returns
    -------
    attrlist : list
        list of attributes defined for the grid
    """
    strbufsize = ffi.new("long *")
    nattrs = _lib.HE5_GDinqlocattrs(gridid, fieldname.encode(), 
                                    ffi.NULL, strbufsize)
    if nattrs == 0:
        return []
    attr_buffer = ffi.new("char[]", b'\0' * (strbufsize[0] + 1))
    nattrs = _lib.HE5_GDinqlocattrs(gridid, fieldname.encode(),
                                    attr_buffer, strbufsize)
    _handle_error(nattrs)
    if sys.hexversion < 0x03000000:
        attr_list = ffi.string(attr_buffer).split(',')
    else:
        attr_list = ffi.string(attr_buffer).decode('ascii').split(',')
    return attr_list

def gdlocattrinfo(grid_id, fieldname, attrname):
    """return information about a grid field attribute

    Parameters
    ----------
    grid_id : int
        grid identifier
    fieldname : str
        attribute name
    attrname : str
        attribute name

    Returns
    -------
    numbertype : type
        numpy datatype of the attribute
    count : int
        number of attribute elements
    """
    ntypep = ffi.new("hid_t *")
    countp = ffi.new("hsize_t *")
    status = _lib.HE5_GDlocattrinfo(grid_id,
                                    fieldname.encode(), attrname.encode(),
                                    ntypep, countp)
    _handle_error(status)

    return ntypep[0], countp[0]

def gdnentries(gridid, entry_code):
    """Return number of specified objects in a grid.

    This function wraps the HDF-EOS5 HE5_GDnentries library function.

    Parameters
    ----------
    grid_id : int
        Grid identifier.
    entry_code : int
        Entry code, either HE5_HDFE_NENTDIM or HE5_HDFE_NENTDFLD

    Returns
    -------
    nentries, strbufsize : int
       Number of specified entries, number of bytes in descriptive strings. 
    """
    strbufsizep = ffi.new("long *")
    nentries = _lib.HE5_GDnentries(gridid, entry_code, strbufsizep)

    # Sometimes running this with HDFE_NENTDIM results in too small a value.
    # Since there's no real reason for a python user to be directly interested
    # in this value, we'll make it a minimum size of 100.
    if entry_code == HE5_HDFE_NENTDIM:
        strbufsize = max(100, strbufsizep[0])
    else:
        strbufsize = strbufsizep[0]
    #print(entry_code, nentries, strbufsize)
    return nentries, strbufsize

def gdopen(filename, access=H5F_ACC_RDONLY):
    """Opens or creates HDF file in order to create, read, or write a grid.
    
    This function wraps the HDF-EOS5 HE5_GDopen library function.

    Parameters
    ----------
    filename : str
        name of file
    access : int
        one of H5F_ACC_RDONLY, H5F_ACC_RDWR, or H5F_ACC_TRUNC

    Returns
    -------
    fid : int
        grid file ID handle
    """
    fid = _lib.HE5_GDopen(filename.encode(), access)
    _handle_error(fid)
    return fid

def gdorigininfo(grid_id):
    """Return grid pixel origin information.

    This function wraps the HDF-EOS5 HE5_GDorigininfo library function.

    Parameters
    ----------
    grid_id : int
        Grid identifier.

    Returns
    -------
    origincode : int
        Origin code.
    """
    origincode = ffi.new("int *")
    status = _lib.HE5_GDorigininfo(grid_id, origincode)
    _handle_error(status)
    return origincode[0]

def gdpixreginfo(grid_id):
    """Return pixel registration information.

    This function wraps the HDF-EOS5 HE5_GDpixreginfo library function.

    Parameters
    ----------
    grid_id : int
        Grid identifier.

    Returns
    -------
    pixregcode : int
        Pixel registration code.
    """
    pixregcode = ffi.new("int *")
    status = _lib.HE5_GDpixreginfo(grid_id, pixregcode)
    _handle_error(status)
    return pixregcode[0]

def gdprojinfo(grid_id):
    """Return projection information about grid.

    This function wraps the HDF-EOS5 HE5_GDprojinfo library function.

    Parameters
    ----------
    grid_id : int
        Grid identifier.

    Returns
    -------
    projode : int
        GCTP projection code.
    zonecode : int
        GCTP zone code used by UTM projection.
    spherecode : int
        GCTP spheroid code
    projparm : ndarray
        GCTP projection parameters
    """
    projcode = ffi.new("int *")
    zonecode = ffi.new("int *")
    spherecode = ffi.new("int *")
    projparm = np.zeros(13, dtype=np.float64)
    projparmp = ffi.cast("double *", projparm.ctypes.data)
    status = _lib.HE5_GDprojinfo(grid_id, projcode, zonecode, spherecode,
                                 projparmp)
    _handle_error(status)

    return projcode[0], zonecode[0], spherecode[0], projparm

def gdreadattr(gridid, attrname):
    """read grid attribute

    This function wraps the HDF-EOS5 HE5_GDreadattr library function.

    Parameters
    ----------
    grid_id : int
        grid identifier
    attrname : str
        attribute name

    Returns
    -------
    value : object
        grid field attribute value
    """
    [ntype, count] = gdattrinfo(gridid, attrname)
    if ntype == 57:
        #buffer = ffi.new("char[]", b'\0' * (count + 1))
        buffer = ffi.new("char[]", b'\0' * (1000 + 1))
        status = _lib.HE5_GDreadattr(gridid, attrname.encode(), buffer)
        _handle_error(status)
        return ffi.string(buffer).decode('ascii')

    buffer = np.zeros(count, dtype=number_type_dict[ntype])
    bufferp = ffi.cast(cast_string_dict[ntype], buffer.ctypes.data)

    status = _lib.HE5_GDreadattr(gridid, attrname.encode(), bufferp)
    _handle_error(status)

    if count == 1:
        # present as a scalar rather than an array.
        buffer = buffer[0]
    return buffer



def gdreadlocattr(gridid, fieldname, attrname):
    """read grid field attribute

    This function wraps the HDF-EOS5 library HE5_GDreadlocattr function.

    Parameters
    ----------
    grid_id : int
        grid identifier
    fieldname : str
        name of grid field
    attrname : str
        attribute name

    Returns
    -------
    value : object
        grid field attribute value
    """
    [ntype, count] = gdlocattrinfo(gridid, fieldname, attrname)
    #print(ntype, count, number_type_dict[ntype],  attrname, cast_string_dict[ntype])
    if ntype == 57:
        #buffer = ffi.new("char[]", b'\0' * (count + 1))
        buffer = ffi.new("char[]", b'\0' * (1000 + 1))
        status = _lib.HE5_GDreadlocattr(gridid,
                                        fieldname.encode(), attrname.encode(),
                                        buffer)
        _handle_error(status)
        return ffi.string(buffer).decode('ascii')

    buffer = np.zeros(count, dtype=number_type_dict[ntype])
    bufferp = ffi.cast(cast_string_dict[ntype], buffer.ctypes.data)

    status = _lib.HE5_GDreadlocattr(gridid,
                                    fieldname.encode(), attrname.encode(),
                                    bufferp)
    _handle_error(status)

    if count == 1:
        # present as a scalar rather than an array.
        buffer = buffer[0]
    return buffer


def gdreadfield(gridid, fieldname, start, stride, edge):
    """read data from grid field

    This function wraps the HDF-EOS5 library HE5_GDreadfield function.

    Parameters
    ----------
    grid_id : int
        grid identifier
    fieldname : str
        attribute name
    start : array-like
        specifies starting location within each dimension
    stride : array-like
        specifies number of values to skip along each dimension
    edge : array-like
        specifies number of values to read along each dimension

    Returns
    -------
    data : ndarray
        data read from field
    """
    _, ntype, _, _  = gdfieldinfo(gridid, fieldname)
    shape = tuple([int(x) for x in edge])
    buffer = np.zeros(shape, dtype=number_type_dict[ntype])
    pbuffer = ffi.cast(cast_string_dict[ntype], buffer.ctypes.data)

    startp = ffi.new("const hsize_t []", len(shape))
    stridep = ffi.new("const hsize_t []", len(shape))
    edgep = ffi.new("const hsize_t []", len(shape))

    for j in range(len(shape)):
        startp[j] = np.uint64(start[j])
        stridep[j] = np.uint64(stride[j])
        edgep[j] = np.uint64(edge[j])

    status = _lib.HE5_GDreadfield(gridid, fieldname.encode(), startp, stridep,
                                  edgep, pbuffer)
    _handle_error(status)
    return buffer

