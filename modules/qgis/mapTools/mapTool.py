from Ferramentas_Producao.modules.qgis.factories.mapFunctionsFactory import MapFunctionsFactory
from Ferramentas_Producao.modules.utils.factories.utilsFactory import UtilsFactory
from qgis.utils import iface
from qgis import gui, core

class MapTool:
    
    def __init__(self,
            mapFunctionsFactory=None,
            messageFactory=None,
        ):
        super(MapTool, self).__init__()
        self.mapFunctionsFactory = MapFunctionsFactory() if mapFunctionsFactory is None else mapFunctionsFactory
        self.messageFactory = UtilsFactory().createMessageFactory() if messageFactory is None else messageFactory

    def removeAllSelection(self):
        for a in iface.attributesToolBar().actions(): 
            if a.objectName() == 'mActionDeselectAll':
                a.trigger()
                break

    def showErrorMessageBox(self, parent, title, message):
        messageDlg = self.messageFactory.createMessage('ErrorMessageBox')
        messageDlg.show(parent, title, message)
