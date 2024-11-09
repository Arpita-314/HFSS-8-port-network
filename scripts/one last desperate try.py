# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 22:28:00 2024

@author: go29lap
"""

import ansys.aedt.core
with ansys.aedt.core.Desktop(specified_version="2023.2", non_graphical=True, new_desktop_session=True, close_on_exit=True,
             student_version=False):
    circuit = ansys.aedt.core.Circuit()
    ...
    # Any error here is caught by AEDT.
    ...
# AEDT is automatically closed here.