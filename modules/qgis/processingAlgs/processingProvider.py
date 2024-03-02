# -*- coding: utf-8 -*-
from PyQt5.QtCore import QCoreApplication
from processing.core.ProcessingConfig import ProcessingConfig, Setting
from qgis.core import QgsApplication, QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from SAP_Operador.modules.qgis.processingAlgs.uuidCheckerAlg import UuidCheckerAlg
from SAP_Operador.modules.qgis.processingAlgs.spellCheckerAlg import SpellCheckerAlg
from SAP_Operador.modules.qgis.processingAlgs.loadShapefilesAlg import LoadShapefilesAlg

class ProcessingProvider(QgsProcessingProvider):

    def __init__(self):
        super(ProcessingProvider, self).__init__()
        self.iconPath = ''

    def getAlgList(self):
        return [
            UuidCheckerAlg(),
            SpellCheckerAlg(),
            LoadShapefilesAlg()
        ]

    def load(self):
        ProcessingConfig.settingIcons[self.name()] = self.icon()
        ProcessingConfig.addSetting(Setting(self.name(), 'ACTIVATE_SAP_Operador',
                                            'Activate', True))
        ProcessingConfig.readSettings()
        self.refreshAlgorithms()
        return True

    def unload(self):
        ProcessingConfig.removeSetting('ACTIVATE_SAP_Operador')

    def isActive(self):
        return ProcessingConfig.getSetting('ACTIVATE_SAP_Operador')

    def setActive(self, active):
        ProcessingConfig.setSettingValue('ACTIVATE_SAP_Operador', active)

    def id(self):
        return 'SAP Operador'

    def name(self):
        return 'SAP Operador'

    def setIconPath(self, iconPath):
        self.iconPath = iconPath

    def getIconPath(self):
        return self.iconPath

    def icon(self):
        return QIcon(self.getIconPath())

    def loadAlgorithms(self):
        for alg in self.getAlgList():
            self.addAlgorithm(alg)
