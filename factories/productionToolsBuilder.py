from PyQt5 import QtCore

from SAP_Operador.interfaces.IProductionToolsBuilder import IProductionToolsBuilder

from SAP_Operador.widgets.productionToolsDock import ProductionToolsDock

class ProductionToolsBuilder(IProductionToolsBuilder):

    def __init__(self):
        super(ProductionToolsBuilder, self).__init__()
        self.reset()

    def reset(self):
        self.obj = ProductionToolsDock()

    def setObject(self, obj):
        self.obj = obj

    def setController(self, controller):
        self.obj.setController(controller)

    def addActivityWidget(self, name, widget):
        self.obj.addActivityWidget(name, widget)

    def addLine(self):
        self.obj.addLine()
    
    def addLineageLabel(self, lineage):
        self.obj.addLineageLabel(lineage)

    def addPomodoro(self, pomodoro):
        self.obj.addPomodoro(pomodoro)

    def setShortcutDescription(self, description):
        self.obj.setShortcutDescription(description)

    def removeTab(self, index):
        self.obj.removeTab(index)

    def getResult(self):
        obj = self.obj
        self.reset()
        return obj