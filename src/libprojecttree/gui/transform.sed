#!/bin/sed -f
s/PyQt5/PySide2/g
s/^import icons_rc/from . &/
