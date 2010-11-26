# -*- coding: utf-8 -*-
#
# Copyright © 2009-2010 CEA
# Pierre Raybaut
# Licensed under the terms of the CECILL License
# (see guiqwt/__init__.py for details)

"""Simple filter testing application based on PyQt and guiqwt"""

SHOW = True # Show test in GUI-based test launcher

from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt4.QtCore import SIGNAL

#---Import plot widget base class
from guiqwt.plot import CurvePlotWidget
from guiqwt.builder import make
from guidata.configtools import get_icon
#---

class FilterTestWidget(QWidget):
    """
    Filter testing widget
    parent: parent widget (QWidget)
    x, y: NumPy arrays
    func: function object (the signal filter to be tested)
    """
    def __init__(self, parent, x, y, func):
        QWidget.__init__(self, parent)
        self.setMinimumSize(320, 200)
        self.x = x
        self.y = y
        self.func = func
        #---guiqwt curve item attribute:
        self.curve_item = None
        #---
        
    def setup_widget(self, title):
        #---Create the plot widget:
        plotwidget = CurvePlotWidget(self)
        plotwidget.register_tools()
        self.curve_item = make.curve([], [], color='b')
        plotwidget.plot.add_item(self.curve_item)
        plotwidget.plot.set_antialiasing(True)
        #---
        
        button = QPushButton(u"Test filter: %s" % title)
        self.connect(button, SIGNAL('clicked()'), self.process_data)
        vlayout = QVBoxLayout()
        vlayout.addWidget(plotwidget)
        vlayout.addWidget(button)
        self.setLayout(vlayout)
        
        self.update_curve()
        
    def process_data(self):
        self.y = self.func(self.y)
        self.update_curve()
        
    def update_curve(self):
        #---Update curve
        self.curve_item.set_data(self.x, self.y)
        self.curve_item.plot().replot()
        #---
    
    
class TestWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Signal filtering (guiqwt)")
        self.setWindowIcon(get_icon('guiqwt.png'))
        hlayout = QHBoxLayout()
        self.setLayout(hlayout)
        
    def add_plot(self, x, y, func, title):
        widget = FilterTestWidget(self, x, y, func)
        widget.setup_widget(title)
        self.layout().addWidget(widget)
        

def test():
    """Testing this simple Qt/guiqwt example"""
    from PyQt4.QtGui import QApplication
    import numpy as np
    import scipy.signal as sps, scipy.ndimage as spi
    
    app = QApplication([])
    win = TestWindow()
    
    x = np.linspace(-10, 10, 500)
    y = np.random.rand(len(x))+5*np.sin(2*x**2)/x
    win.add_plot(x, y, lambda x: spi.gaussian_filter1d(x, 1.), "Gaussian")
    win.add_plot(x, y, sps.wiener, "Wiener")
    
    win.show()
    app.exec_()
        
        
if __name__ == '__main__':
    test()
    