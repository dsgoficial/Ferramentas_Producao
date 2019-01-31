# -*- coding: utf-8 -*-
import os, sys
from PyQt5 import QtCore, uic, QtWidgets
from .worksItem import WorksItem
from .worksCloseDialog import WorksCloseDialog
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
from utils import msgBox

class WorksFrame(QtWidgets.QFrame):

    dialog_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 
        'worksFrame.ui'
    )

    close_works = QtCore.pyqtSignal()

    def __init__(self):
        super(WorksFrame, self).__init__()
        uic.loadUi(self.dialog_path, self)
        self.spacer_item = None
        self.sap_data = {}

    def clean_works(self):
        layout = self.works_area.layout()
        for idx in range(layout.count()):
            if type(layout.itemAt(idx)) == QtWidgets.QtWidgetItem:
                layout.itemAt(idx).widget().deleteLater()
        layout.removeItem(self.spacer_item) if self.spacer_item else ''

    def load(self, sap_data):
        self.clean_works()
        self.sap_data = sap_data
        woks_data = self.sap_data['dados']['atividade']
        description = woks_data['nome']
        values_cbx = woks_data['requisitos'] if 'requisitos' in woks_data else []
        if len(values_cbx) > 0:
            self.close_works_btn.setEnabled(False)
        self.works_item = WorksItem(description, values_cbx, self)
        self.works_item.enable_btn.connect(lambda:self.close_works_btn.setEnabled(True))
        self.works_item.disable_btn.connect(lambda:self.close_works_btn.setEnabled(False))
        self.works_area.layout().addWidget(self.works_item)
        self.spacer_item = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.works_area.layout().addItem(self.spacer_item)

    @QtCore.pyqtSlot(bool)
    def on_close_works_btn_clicked(self, b):
        user_name = self.sap_data['user']
        worksCloseDialog  = WorksCloseDialog(user_name)
        worksCloseDialog.finish.connect(
            self.close_works.emit
        )
        worksCloseDialog.exec_()