from ..fcs.get_fcs_info import get_file_info, get_metafile_from_file
from .analysis_settings import FFSmetadata

def load_ffs_metadata(fname):
    """
    Load FFS metadata. Function assumes that metadata is stored in 
    'ffs_info.txt' with ffs the raw file name  (i.e. "fname" without .bin), e.g.
    'myFCSmeasurement.bin' is the raw data file, and
    'myFCSmeasurement_info.txt' is the metadata file
    OR
    metadata is stored in same .h5 file as the actual data
    ===========================================================================
    Input       Meaning
    ---------------------------------------------------------------------------
    ffs         File name of raw data file (not metadata file).
    ===========================================================================
    Output      Meaning
    ---------------------------------------------------------------------------
    metadata    analysis_settings metadata object with all fields filled in
                returns None if the file is not found
    ===========================================================================
    """
    
    # metadata
    fname = get_metafile_from_file(fname)
    md = get_file_info(fname)
    if md is not None:
        metadata = FFSmetadata()
        for attribute in list(metadata.__dict__.keys()):
            if hasattr(md, attribute) and getattr(md, attribute) is not None:
                setattr(metadata, attribute, getattr(md, attribute))
            else:
                setattr(metadata, attribute, 0)
        # get coordinates from file name
        # Cells_DEKegfp_4_LP70_75x75um_1500x1500px_y_52_x_1480.bin
        # returns [52, 1480]
        idx = fname.rfind("y_") + 2
        idx2 = fname.rfind("_x_")
        if fname[idx2+3:].rfind("_"):
            idx3 = fname.rfind("_")
        else:
            idx3 = fname.rfind(".")
        try:
            y = int(fname[idx:idx2])
        except:
            y = 0
        try:
            x = int(fname[idx2+3:idx3])
        except:
            x = 0
        metadata.coords = [y, x]
    else:
        metadata = None
    return metadata
