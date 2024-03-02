import os
from PyQt5 import QtWidgets, uic
from SAP_Operador.modules.utils.interfaces.IMessage  import IMessage

class ErrorMessageBox(IMessage):

    def __init__(self):
        super(ErrorMessageBox, self).__init__()

    def show(self, parent, title, text):
        QtWidgets.QMessageBox.critical(
            parent,
            title, 
            text
        )