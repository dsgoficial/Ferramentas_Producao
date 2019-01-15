# -*- coding: utf-8 -*-
import os, sys, copy
from PyQt5 import QtCore, uic, QtWidgets, QtGui
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
from utils import msgBox, cursorWait

class MenuDock(QtWidgets.QDockWidget):

    dialog_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 
        'menuDock.ui'
    )

    start_button = QtCore.pyqtSignal(dict)

    def __init__(self, iface):
        super(MenuDock, self).__init__()
        self.iface = iface
        uic.loadUi(self.dialog_path, self)
        self.db_data = {}
        self.menu_area_buttons.setTabPosition(QtWidgets.QTabWidget.West)
        self.menu_area_buttons.setElideMode(QtCore.Qt.ElideNone)
        self.menu_area_buttons.setStyleSheet(
            "QTabBar::tab::disabled {width: 0; heigth: 0; margin: 0; padding: 0; border: none;}"
        )
        self.menu_search.mousePressEvent = lambda _ : self.menu_search.selectAll()
        self.menu_search.textEdited.connect(self.filter_button)

    def filter_button(self, text):
        buttons = self.get_all_buttons_tab(u'**Pesquisa**')
        if text:
            self.show_tab_search()
            for button_name in  buttons:
                button_widget = buttons[button_name]
                button_widget.hide()
                geom_btn = button_widget.button_data['formValues'][u'*Selecione camada:'][-1:]
                lyr = self.iface.activeLayer()
                geom_lyr = lyr.name()[-1:] if lyr else '' 
                word_list = [
                    w.lower() for w in 
                    button_widget.button_data['formValues'][u'Definir palavras chaves(separar com ";"):'].split(';')
                ]
                validate_with_geom = (
                    (geom_lyr.lower() in geom_btn.lower()) and 
                    (
                        text.lower() in button_name.lower() 
                        or
                        text.lower() in word_list
                    )
                )
                validate_without_geom = (
                    text.lower() in button_name.lower() 
                    or
                    text.lower() in word_list
                )
                validate_button = validate_with_geom if geom_lyr else validate_without_geom
                if validate_button:
                    button_widget.show()
        else:
            self.hide_tab_search()
    
    def show_tab_search(self):
        self.menu_area_buttons.setTabEnabled(0, True)
        self.menu_area_buttons.setCurrentIndex(0)

    def hide_tab_search(self):
        self.menu_area_buttons.setTabEnabled(0, False)
        self.menu_area_buttons.setCurrentIndex(1)

    def show_menu(self):
        db_data = self.db_data
        profiles_name = [u"..."] + [db_data['db_menu'][idx]['nome_do_perfil'] for idx in db_data['db_menu']] if db_data else [u"..."]
        self.menu_profiles.addItems(profiles_name)
        self.iface.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self)

    @QtCore.pyqtSlot(int)
    def on_menu_profiles_currentIndexChanged(self, idx):
        profile_selected = self.menu_profiles.currentText() if idx != 0 else ''
        if profile_selected:
            db_data = self.db_data
            for idx in db_data['db_menu']:
                if db_data['db_menu'][idx]['nome_do_perfil'] == profile_selected:
                    profile_data = db_data['db_menu'][idx]
                    self.load_menu_profile(profile_data)
                    return
        else:
            self.clean_menu()

    def load_menu_profile(self, profile_data):
        self.clean_menu()
        for tab_name in reversed(profile_data['orderMenu']['orderTab']):
            self.add_tab(tab_name)
            for button_name in reversed(profile_data['orderMenu']['orderButton'][tab_name]):
                button_data = profile_data['perfil'][tab_name][button_name]
                self.add_button(button_data)
        self.add_tab_search(profile_data)

    def add_tab_search(self, profile_data):
        self.add_tab(u'**Pesquisa**')
        for tab_name in reversed(profile_data['orderMenu']['orderTab']):
            for button_name in reversed(profile_data['orderMenu']['orderButton'][tab_name]):
                button_data = copy.deepcopy(
                    profile_data['perfil'][tab_name][button_name]
                ) 
                button_data['formValues'][u'*Selecione aba:'] = u'**Pesquisa**'
                self.add_button(button_data)

    def add_tab(self, tab_name):
        tab = QtWidgets.QWidget()
        layout_tab = QtWidgets.QVBoxLayout(tab)
        layout_tab.setObjectName(u'area')
        scroll = QtWidgets.QScrollArea(tab)
        scroll.setWidgetResizable(True)
        scroll_widget = QtWidgets.QWidget()
        scroll_widget.setGeometry(QtCore.QRect(0, 0, 328, 386))
        scroll_widget.setObjectName(u'scroll')
        layout_button = QtWidgets.QVBoxLayout(scroll_widget)
        layout_button.setObjectName(u'layout')
        scroll.setWidget(scroll_widget)
        layout_tab.addWidget(scroll)
        if tab_name == u'**Pesquisa**':
            if u'**Pesquisa**' in self.get_all_tabs_map():
                self.remove_tab(u'**Pesquisa**')
            else:
                self.menu_area_buttons.insertTab(0, tab, tab_name)
                self.menu_area_buttons.setTabEnabled(0, False)
        else:
            self.menu_area_buttons.insertTab(1, tab, tab_name)
        self.menu_area_buttons.setCurrentIndex(1)

    def get_all_tabs_map(self):
        tabs = {}
        for idx in range(self.menu_area_buttons.count()):
            tabs[self.menu_area_buttons.tabText(idx)] = idx
        return tabs
            
    def remove_tab(self, tab_name):
        tabs_map = self.get_all_tabs_map()
        self.menu_area_buttons.removeTab(tabs_map[tab_name])
    
    def get_tab_widgets(self, tab_name):
        tabs_map = self.get_all_tabs_map()
        tab_scroll = self.menu_area_buttons.widget(
            tabs_map[tab_name]
        ).findChildren(QtWidgets.QScrollArea)[0].children()[0].children()[0]
        tab_layout = tab_scroll.children()[0]
        return {
            'scroll' : tab_scroll,
            'layout' : tab_layout,
        }
             
    def get_all_buttons_tab(self, tab_name):
        buttons = {}
        tab_widgets = self.get_tab_widgets(tab_name)
        for idx in range(tab_widgets['layout'].count()):
            button_name = tab_widgets['layout'].itemAt(idx).widget().objectName()
            button_widget = tab_widgets['layout'].itemAt(idx).widget()
            buttons[button_name] = button_widget
        return buttons

    def add_button(self, button_data):
        button_name = button_data[u'formValues'][u'*Nome do botão:']
        tab_name = button_data[u'formValues'][u'*Selecione aba:']
        layer_name = button_data[u'formValues'][u'*Selecione camada:']
        tab_data = self.get_tab_widgets(tab_name)
        tab_scroll = tab_data['scroll']
        tab_layout = tab_data['layout']
        count = tab_layout.count()
        button = QtWidgets.QPushButton(tab_scroll)
        button.setStyleSheet(
            self.get_button_style(layer_name)
        )
        button.button_data = button_data
        tab_layout.addWidget(button)
        if count >=0 and count <= 8:
            button.setText("{0}_[{1}]".format(button_name, count+1))
            button.setShortcut(
                self.get_button_shortcut(count)
            )
        else:
            button.setText(button_name)
        button.setObjectName(button_name)
        button.clicked.connect(self.run_button)

    def run_button(self):
        cursorWait.start()
        button = self.sender()
        self.reload_button_style()
        layer_name = button.button_data[u'formValues'][u'*Selecione camada:']
        button.setStyleSheet(
            self.get_button_style(layer_name, default=False)
        )
        self.start_button.emit({
            "button_data" : button.button_data,
            "reclassify" : self.menu_reclassify.isChecked()
        })
        cursorWait.stop()

    def reload_button_style(self):
        for tab_name in self.get_all_tabs_map():
            buttons = self.get_all_buttons_tab(tab_name)
            for button_name in buttons:
                button = buttons[button_name]
                layer_name = button.button_data[u'formValues'][u'*Selecione camada:']
                button.setStyleSheet(
                    self.get_button_style(layer_name)
                )
    
    def clean_menu(self):
        for tab_name in self.get_all_tabs_map():
            self.remove_tab(tab_name)

    def get_button_shortcut(self, no):
        shortcuts = {
            0 : QtCore.Qt.Key_1,
            1 : QtCore.Qt.Key_2,
            2 : QtCore.Qt.Key_3,
            3 : QtCore.Qt.Key_4,
            4 : QtCore.Qt.Key_5,
            5 : QtCore.Qt.Key_6,
            6 : QtCore.Qt.Key_7,
            7 : QtCore.Qt.Key_8,
            8 : QtCore.Qt.Key_9
        }
        return shortcuts[no]

    def get_button_style(self, layer_name, default=True):
        click_styles = {
            'a' : '''color: rgb(255, 255, 255);
                   background-color: rgb(255, 128, 0);''', 
            'c' : '''background-color: rgb(255, 128, 0);''',
            'p' : '''color: rgb(255, 255, 255);
                   background-color: rgb(255, 128, 0);''', 
            'd' : '''background-color: rgb(255, 128, 0);''',
            'l' : '''background-color: rgb(21, 7, 7);
                   color: rgb(255, 128, 0);''',
        }
        default_styles = {
            'a' : "color: rgb(255, 255, 255); \
                  background-color: rgb(246, 13, 13);", 
            'c' : "background-color: rgb(85, 255, 0);",
            'p' : "color: rgb(255, 255, 255); \
                  background-color: rgb(0, 0, 255);", 
            'd' : "background-color: rgb(255, 255, 0);",
            'l' : "background-color: rgb(21, 7, 7); \
                  color: rgb(255, 255, 255);",
        }
        if default:
            return default_styles[layer_name.split('_')[-1]]
        return click_styles[layer_name.split('_')[-1]]

    ###sem uso
    def remove_all_buttons(self, tab_name):
        buttons = self.get_all_buttons_tab(tab_name)
        for button_name in buttons:
            buttons[button_name].deleteLater()

    ####sem uso
    def get_order_menu(self):
        orderMenu = {
            "orderTab" : [],
            "orderButton" : {},
        }
        for tab_name in self.get_all_tabs_map():
            if not(tab_name in [u'**Pesquisa**']):
                orderMenu["orderTab"].append(tab_name)
                orderMenu["orderButton"][tab_name] = []
                tab_widgets = self.get_tab_widgets(tab_name)
                for idx in range(tab_widgets['layout'].count()):
                    button_name = tab_widgets['layout'].itemAt(idx).widget().objectName()
                    orderMenu["orderButton"][tab_name].append(button_name)
        return orderMenu             

    