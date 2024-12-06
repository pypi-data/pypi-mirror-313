"""
.. This file is part of pyEMAPS backend and its binary dependents.

.. 
.. emaps is only free when it is used with pyEMAPS. 
.. For license agreement, please refer to that in pyEMAPS package.

.. Contact supprort@emlabsoftware.com for any questions and comments.

.. ----

.. Author:     EMLab Solutions, Inc.
.. Date:       June 11, 2024 
   
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _stem4d
else:
    import _stem4d

readDPDB = _stem4d.readDPDB
prepareSearch = _stem4d.prepareSearch
DPGetMask = _stem4d.DPGetMask
DPListMaskSelect = _stem4d.DPListMaskSelect
DPGetCurrentImage = _stem4d.DPGetCurrentImage
loadXTemplateMask = _stem4d.loadXTemplateMask
getXTemplateMask = _stem4d.getXTemplateMask
loadXMask = _stem4d.loadXMask
getXMask = _stem4d.getXMask
getFitMap = _stem4d.getFitMap
getFitImage = _stem4d.getFitImage
searchXPeaks = _stem4d.searchXPeaks
indexXPeaks = _stem4d.indexXPeaks
getExpImagePeaks = _stem4d.getExpImagePeaks
printIndexDetails = _stem4d.printIndexDetails
selectExSHImage = _stem4d.selectExSHImage
getDPListKDif = _stem4d.getDPListKDif
getXKDif = _stem4d.getXKDif

DPListPatternImage = _stem4d.DPListPatternImage
getCurrentXImage = _stem4d.getCurrentXImage
getCurrentXImage_new = _stem4d.getCurrentXImage_new