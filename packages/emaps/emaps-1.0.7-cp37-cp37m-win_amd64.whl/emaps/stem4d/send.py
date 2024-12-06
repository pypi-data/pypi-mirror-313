"""
.. This file is part of pyEMAPS backend and its binary dependents.

.. ----

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


getBDF = _stem4d.getBDF
getMaskedImage = _stem4d.getMaskedImage
