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

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# root directory for all emaps modules
try:
    from .emaps_sims import dif
except Exception as e:
    print(f'Error loading diffraction simulation modules: {e}')
    raise e

#check other modules existence
try:
    from .emaps_sims import dpgen, csf, powder, bloch, stereo, mxtal

except ImportError as e:
    print(f'Warning: no other simulation modules found in emaps')
    raise e
    