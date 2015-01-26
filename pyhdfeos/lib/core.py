import os
import sys

from cffi import FFI

from . import config

def decode_comma_delimited_ffi_string(strbuf):
    if sys.hexversion < 0x03000000:
        lst = strbuf.split(',')
    else:
        lst = strbuf.decode('ascii').split(',')
    return lst

CDEF = """
    typedef float float32;
    typedef int int32;
    typedef int intn;
    typedef double float64;

    int   EHHEisHE2(char *filename);
    intn  EHidinfo(int32 fid, int32 *hdfid, int32 *sdid);
    int32 GDattach(int32 gdfid, char *grid);
    intn  GDattrinfo(int32 gdfid, char *attrname, int32 *nbyte, int32
                     *count);
    intn  GDblkSOMoffset(int32 fid, float32 [], int32 count, char *code);
    intn  GDdetach(int32 gid);
    intn  GDclose(int32 fid);
    intn  GDfieldinfo(int32 gridid, char *fieldname, int32 *rank,
                      int32 dims[], int32 *numbertype, char *dimlist);
    int32 GDij2ll(int32 projcode, int32 zonecode,
                  float64 projparm[], int32 spherecode, int32 xdimsize,
                  int32 ydimsize, float64 upleft[], float64 lowright[],
                  int32 npts, int32 row[], int32 col[], float64
                  longititude[], float64 latitude[], int32 pixcen,
                  int32 pixcnr);
    int32 GDinqattrs(int32 gridid, char *attrlist, int32 *strbufsize);
    int32 GDinqdims(int32 gridid, char *dimname, int32 *dims);
    int32 GDinqfields(int32 gridid, char *fieldlist, int32 rank[],
                      int32 numbertype[]);
    int32 GDinqgrid(char *filename, char *gridlist, int32 *strbufsize);
    int32 GDnentries(int32 gridid, int32 entrycode, int32 *strbufsize);
    intn  GDgridinfo(int32 gridid, int32 *xdimsize, int32 *ydimsize,
                     float64 upleft[2], float64 lowright[2]);
    int32 GDopen(char *name, intn access);
    intn  GDorigininfo(int32 gridid, int32 *origincode);
    intn  GDpixreginfo(int32 gridid, int32 *pixregcode);
    intn  GDprojinfo(int32 gridid, int32 *projcode, int32 *zonecode,
                     int32 *spherecode, float64 projparm[]);
    intn  GDreadattr(int32 gridid, char* attrname, void *buffer);
    intn  GDreadfield(int32 gridid, char* fieldname, int32 start[],
                      int32 stride[], int32 edge[], void *buffer);
    int32 SWattach(int32 swfid, char *swath);
    intn  SWattrinfo(int32 swathid, char *attrname, int32 *nbyte, int32
                     *count);
    intn  SWclose(int32 fid);
    intn  SWdetach(int32 swfid);
    intn  SWfieldinfo(int32 gridid, char *fieldname, int32 *rank,
                      int32 dims[], int32 *numbertype, char *dimlist);
    int32 SWidxmapinfo(int32, char *, char *, int32 []);
    int32 SWinqattrs(int32 swathid, char *attrlist, int32 *strbufsize);
    int32 SWinqdims(int32 swathid, char *dimname, int32 *dims);
    int32 SWinqdatafields(int32 swathid, char *fieldlist, int32 rank[],
                          int32 numbertype[]);
    int32 SWinqgeofields(int32 swathid, char *fieldlist, int32 rank[],
                         int32 numbertype[]);
    int32 SWinqidxmaps(int32, char *, int32 []);
    int32 SWinqmaps(int32, char *, int32 [], int32 []);
    int32 SWinqswath(char *filename, char *swathlist, int32 *strbufsize);
    int32 SWnentries(int32 swathid, int32 entrycode, int32 *strbufsize);
    intn  SWreadattr(int32 swathid, char* attrname, void *buffer);
    intn  SWreadfield(int32 gridid, char* fieldname, int32 start[],
                      int32 stride[], int32 edge[], void *buffer);
    int32 SWopen(char *name, intn access);


    typedef unsigned uintn;
    typedef unsigned long long hsize_t;
    typedef int hid_t;
    typedef int herr_t;

    int    HE5_EHHEisHE5(char *filename);
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
    hid_t  HE5_SWattach(hid_t fid, char *swathname);
    long   HE5_SWattrinfo(hid_t gridID, const char *attrname,
                             hid_t *ntype, hsize_t *count);
    herr_t HE5_SWdetach(hid_t swathid);
    herr_t HE5_SWfieldinfo(hid_t gridID, const char *fieldname, int *rank,
                           hsize_t dims[], hid_t *ntype, char *dimlist,
                           char *maxdimlist);
    long   HE5_SWgeogrpattrinfo(hid_t gridID, const char *attrname,
                                hid_t *ntype, hsize_t *count);
    long   HE5_SWgrpattrinfo(hid_t gridID, const char *attrname,
                             hid_t *ntype, hsize_t *count);
    hsize_t HE5_SWidxmapinfo(hid_t swathID, char *geodim, char *datadim,
                             long index []);
    long   HE5_SWinqattrs(hid_t gridID, char *attrnames, long *strbufsize);
    int    HE5_SWinqdims(hid_t swathid, char *dims, hsize_t *dims);
    int    HE5_SWinqdatafields(hid_t gridID, char *fieldlist, int rank[],
                               hid_t ntype[]);
    int    HE5_SWinqgeofields(hid_t gridID, char *fieldlist, int rank[],
                              hid_t ntype[]);
    long   HE5_SWinqgeogrpattrs(hid_t gridID, char *attrnames,
                                long *strbufsize);
    long   HE5_SWinqgrpattrs(hid_t gridID, char *attrnames, long *strbufsize);
    long   HE5_SWinqlocattrs(hid_t swathID, char *fieldname, char *attrnames,
                             long *strbufsize);
    long   HE5_SWinqidxmaps(hid_t, char *, hsize_t []);
    long   HE5_SWinqmaps(hid_t, char *, long [], long []);
    long   HE5_SWinqswath(const char *filename, char *swathlist,
                          long *strbufsize);
    long   HE5_SWlocattrinfo(hid_t swathID, char *fieldname, char *attrname,
                             hid_t *ntype, hsize_t *count);
    long   HE5_SWnentries(hid_t swathID, int entrycode, long *strbufsize);
    hid_t  HE5_SWopen(const char *filename, uintn access);
    herr_t HE5_SWreadattr(hid_t swathID, const char* attrname, void *buffer);
    herr_t HE5_SWreadgeogrpattr(hid_t swathID, const char* attrname,
                                void *buffer);
    herr_t HE5_SWreadgrpattr(hid_t swathID, const char* attrname,
                             void *buffer);
    herr_t HE5_SWreadfield(hid_t swathID, const char* fieldname,
                           const hsize_t start[],
                           const hsize_t stride[],
                           const hsize_t edge[],
                           void *buffer);
    herr_t HE5_SWreadlocattr(hid_t swathID, const char *fieldname,
                             const char *attrname, void *databuf);
    herr_t HE5_SWclose(hid_t fid);
    hid_t  HE5_ZAattach(hid_t fid, char *zaname);
    long   HE5_ZAattrinfo(hid_t zaid, const char *attrname,
                             hid_t *ntype, hsize_t *count);
    hid_t  HE5_ZAopen(const char *filename, uintn access);
    herr_t HE5_ZAclose(hid_t fid);
    herr_t HE5_ZAdetach(hid_t zaid);
    long   HE5_ZAgrpattrinfo(hid_t zaid, const char *attrname,
                             hid_t *ntype, hsize_t *count);
    herr_t HE5_ZAinfo(hid_t zaid, const char *fieldname, int *rank,
                      hsize_t dims[], hid_t *ntype, char *dimlist,
                      char *maxdimlist);
    long   HE5_ZAinqattrs(hid_t zaid, char *attrnames, long *strbufsize);
    long   HE5_ZAinqdims(hid_t zaid, char *dims, hsize_t *dims);
    long   HE5_ZAinqgrpattrs(hid_t zaid, char *attrnames, long *strbufsize);
    long   HE5_ZAinqlocattrs(hid_t zaid, char *fieldname, char *attrnames,
                             long *strbufsize);
    long   HE5_ZAinqza(const char *filename, char *zalist, long *strbufsize);
    long   HE5_ZAinquire(hid_t zaid, char *fieldlist, int rank[],
                         hid_t ntype[]);
    long   HE5_ZAlocattrinfo(hid_t zaid, char *fieldname, char *attrname,
                             hid_t *ntype, hsize_t *count);
    long   HE5_ZAnentries(hid_t zaid, int entrycode, long *strbufsize);
    herr_t HE5_ZAreadattr(hid_t zaid, const char* attrname, void *buffer);
    herr_t HE5_ZAreadgrpattr(hid_t zaid, const char* attrname,
                             void *buffer);
    herr_t HE5_ZAread(hid_t zaid, const char* fieldname,
                      const hsize_t start[],
                      const hsize_t stride[],
                      const hsize_t edge[],
                      void *buffer);
    herr_t HE5_ZAreadlocattr(hid_t zaid, const char *fieldname,
                             const char *attrname, void *databuf);
"""

SOURCE = """
    #include "mfhdf.h"
    #include "HdfEosDef.h"
    #include "HE5_HdfEosDef.h"
"""

ffi = FFI()
ffi.cdef(CDEF)

include_dirs = config.include_dirs
include_dirs.append("pyhdfeos/lib/source/hdfeos")
include_dirs.append("pyhdfeos/lib/source/hdfeos5")

hdfeos_srcs = ["EHapi.c", "GDapi.c", "PTapi.c", "SWapi.c"]
sources = [os.path.join('pyhdfeos', 'lib', 'source', 'hdfeos', file)
           for file in hdfeos_srcs]

he5_srcs = ["EHapi.c", "GDapi.c", "PTapi.c",
            "SWapi.c", "TSapi.c", "ZAapi.c"]
lst = [os.path.join('pyhdfeos', 'lib', 'source', 'hdfeos5', file)
       for file in he5_srcs]
sources.extend(lst)

lst = [os.path.join('pyhdfeos', 'lib', 'source', 'gctp', file)
       for file in config.gctp_srcs]
sources.extend(lst)

_lib = ffi.verify(SOURCE,
                  ext_package='pyhdfeos',
                  sources=sources,
                  libraries=config.libraries,
                  extra_compile_args=['-DH5_USE_16_API'],
                  include_dirs=include_dirs,
                  library_dirs=config.library_dirs,
                  extra_link_args=None,
                  modulename=config._create_modulename("_both_hdfeos",
                                                       CDEF,
                                                       SOURCE,
                                                       sys.version))

