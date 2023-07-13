from Ferramentas_Producao.widgets.widget import Widget
from Ferramentas_Producao.interfaces.IActivityDataWidget import IActivityDataWidget

import os
from PyQt5 import QtWidgets, QtGui, QtCore, uic

class ActivityData(Widget, IActivityDataWidget):

    def __init__(self, controller=None):
        super(ActivityData, self).__init__(controller)
        uic.loadUi(self.getUiPath(), self)
        self.loadReviewToolBtn.setVisible(False)

    def getUiPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '..',
            'uis',
            'activityData.ui'
        )

    @QtCore.pyqtSlot(bool)
    def on_loadLayersBtn_clicked(self):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        try:
            self.getController().loadActivityLayers()
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    @QtCore.pyqtSlot(bool)
    def on_summaryBtn_clicked(self):
        self.getController().showActivityDataSummary()

    @QtCore.pyqtSlot(bool)
    def on_loadMenuBtn_clicked(self):
        self.getController().loadMenu()
    
    @QtCore.pyqtSlot(bool)
    def on_loadReviewToolBtn_clicked(self):
        self.getController().loadReviewTool()

    def setVisibleWidgetsLayout(self, layout, visible):
        for idx in range(layout.count()):
            item = layout.itemAt(idx)
            widget = item.widget()
            if widget is None:
                continue
            widget.setVisible( visible )

    def enabledMenuButton(self, enable):
        self.loadMenuBtn.setEnabled( enable )