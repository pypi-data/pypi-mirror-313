
"""
.. This file is part of pyEMAPS backend and its binary dependents.

.. ----

.. emaps is only free when it is used with pyEMAPS. 
.. For license agreement, please refer to that in pyEMAPS package.

.. Contact supprort@emlabsoftware.com for any questions and comments.

.. ----

.. Author:     EMLab Solutions, Inc.
.. Date:       Oct 20, 2023    

"""


from . import __config__

# These definitions match those in pyEMAPS
TYPE_FREE = 1 # Free package includes basic diffraction simulations and crystallogrphic calculations
TYPE_FULL = 2 # Paid package with stem4d modules. license must be generated using python -m pyemaps -l trial|prod <license token>
TYPE_UIUC = 3 # Special package for exclusive usage in University if Illinois at Urbana Champaign

#--------------from diffraction extension module------------------------
try:
    from .diffract import dif
except ImportError:
    raise Exception('No diffraction module found')
else:
#--------------defaults from the backend for simulation control parameters
    # Default excitation from backend: DEF_EXCITATION (low, high)
    # Default gmax from backend: DEF_GMAX  
    # Default bmin from backend: DEF_BMIN  
    # Default intensity from backend: DEF_INTENSITY (low, high)
    # Default gctl from backend: DEF_GCTL  
    # Default zctl from backend: DEF_ZCTL
#------------------------------------------------------------------------
    PKG_TYPE = dif.get_pkgtype()
    (sgmn, 
     sgmx, 
     DEF_GMAX, 
     DEF_BMIN, 
     intc, 
     intz, 
     DEF_GCTL, 
     DEF_ZCTL, 
     DEF_MODE) = dif.get_sim_defs()

    DEF_EXCITATION= (sgmn, sgmx)
    DEF_INTENSITY = (intz, intc)
    XMAX = 75  # set in dif backend
    YMAX = 75  #set in dif backend

#-------------- defaults from backend for sample controls---------------
    # Default starting zone setting: DEF_ZONE
    # Default tilt: DEF_TILT (x, y)
    # Default xaxis: DEF_XAXIS
#------------------------------------------------------------------------
    zn0, zn1, zn2, tlt0, xax0 = dif.get_sam_defs()
    DEF_ZONE= (zn0, zn1, zn2)
    DEF_TILT =(tlt0, tlt0)
    DEF_XAXIS = (xax0, xax0, xax0)

#-------------- defaults from backend for microscope controls-----------
    # Default hight voltage setting: DEF_KV
    # Default camera length: DEF_CL (x, y)
    # Default deflection: DEF_DEFL
    # Default normal disk size: DEF_NORM_DSIZE
    # Default CBED disk size: DEF_CBED_DS
    # Default disk size: DEF_DS_LIMITS (min, max)
#------------------------------------------------------------------------

    DEF_DEFL = (tlt0, tlt0)
    (DEF_CL, 
     DEF_KV, 
     DEF_NORM_DSIZE, 
     DEF_CBED_DSIZE, 
     dmin, 
     dmax) = dif.get_mic_defs()

    DEF_DSIZE_LIMITS = (dmin, dmax)
    
#------------------------Pyemaps Helper Modules---------------------------------

from .spg import spgseek
from .scattering import sct

#------------------------Crystal Structure Factor Module------------------------
try:
    from .diffract import csf

except ImportError as e:
    pass


#------------------------Powder Diffraction Module------------------------------
try:
    from .diffract import powder

except ImportError as e:
    pass

#------------------------Dynamic Diffraction Module----------------------------
try:
    from .diffract import bloch
    
except ImportError as e:
    raise Exception('No diffraction module found')
else:

    TY_NORMAL = 0 # Normal Bloch Image type
    TY_LACBED = 1 # Large angle Bloch image type
    th_start, th_end, th_step = bloch.get_sam_defs()
    
    DEF_THICKNESS = (th_start, th_end, th_step)
  
    (DEF_SAMPLING, 
     DEF_PIXSIZE, 
     DEF_DETSIZE, 
     MAX_DEPTH, 
     DEF_OMEGA) = bloch.get_sim_defs()
    DEF_APERTURE = bloch.get_mic_defs()

#------------------------Stereodiagram Module--------------------------------
try:
    from .diffract import stereo
    
except ImportError as e:
    raise Exception('No stereo module found')
else:
    pass


#------------------Crystal Constructor Module--------------------------------
try:
    from .diffract import mxtal
    
except ImportError as e:
    raise Exception('No mxtal module found')
else:
    
    # TY_NORMAL = 0 # Normal Bloch Image type
    # TY_LACBED = 1 # Large angle Bloch image type

    ID_MATRIX = [[1,0,0], [0,1,0], [0,0,1]]
    MLEN = 10 
    DEF_TRSHIFT = [0,0,0]
    DEF_CELLBOX = [[0,0,0], [3,3,3]]
    DEF_XZ = [[1,0,0], [0,0,1]]
    DEF_ORSHIFT = [0, 0, 0] #Origin shift
    DEF_LOCASPACE = [0, 0, 0] #location in A Space


# #------------------Diffraction Database Generator - paid package only---------------------------
try:
    from .diffract import dpgen
    
except ImportError as e:
    # skip this in free package
    pass


# #------------------Diffraction Pattern Indexing - paid package only---------------------------
#  used only with dpgen module above
if PKG_TYPE != TYPE_FREE:
    try:
        from .stem4d import stem4d
    except ImportError as e:
        print(f'Failed to import 4d stem module: {e}')
        pass
    except stem4d.EmapsLicenseError as e:
        print(f'Failed to find license: {e}')
        pass
    except Exception as e:
        print(f'Failed to find license: {e}')
        pass
    else:
        E_INT = stem4d.E_INT 
        EM_INT = stem4d.EM_INT

        E_FLOAT = stem4d.E_FLOAT
        EM_FLOAT = stem4d.EM_FLOAT

        E_DOUBLE = stem4d.E_DOUBLE
        EM_DOUBLE = stem4d.EM_DOUBLE

        MAX_IMAGESIZE = stem4d.MAX_IMAGESIZE
        MIN_IMAGESIZE = stem4d.MIN_IMAGESIZE
        MAX_IMAGESTACK = stem4d.MAX_IMAGESTACK
        MIN_IMAGESTACK = 1
        DEF_FILTER_THRESHOLD = 0.2                       
        DEF_SEARCH_THRESHOLD = 0.825
        DEF_RMIN = 7
        DEF_BOXSIZE = 10
        DEF_CC = stem4d.cvar.edc.cc      #default value from backend
        DEF_SIGMA = stem4d.cvar.edc.sigma
        DEF_ICENTER = stem4d.cvar.edc.get_center()
        DEF_XSCALE = 1
        DEF_TSCALE = 2

        E_SH = 0
        E_RAW = 1
        E_NPY = 2

        # imageloading mode
        EL_ONE = 1  #STEM4D image loading one stack at one time
        EL_MORE = 2 #STEM4D image loading all stacks

