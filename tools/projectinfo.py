#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, 2014, 2018 Emilio Coppola, Johnny Stene
#
# This file is part of Astral.
#
# Astral is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Astral is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Astral.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5 import *
import os, sys
from PyQt5.QtGui import QFont
#from PyQt5.QtWebKitWidgets import QWebEngineView , QWebEnginePage
#from PyQt5.QtWebKit import QWebEngineSettings

if sys.version_info.major == 2:
    str = unicode    

class ProjectInfo(QtWidgets.QWidget):
    def __init__(self, main):
        super(ProjectInfo, self).__init__(main)
        self.main = main

        self.ContainerGrid = QtWidgets.QGridLayout(self)
        self.ContainerGrid.setContentsMargins(0, 0, 0, 0)
        self.ContainerGrid.setSpacing(0)

        self.webkit = QtWebKit.QWebEngineView()
        self.webkit.setHtml("""
            <h1>Example</h1>
            <p>whoa!</p>
            """)
        
        self.ContainerGrid.addWidget(self.webkit)
        self.setLayout(self.ContainerGrid)
