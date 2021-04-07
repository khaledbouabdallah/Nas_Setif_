"""
Setif's people is a small application that allows to communicate with a data base
built with pandas,PyQt5 and matplotlib
"""
__version__ = '0.1'
__author__ = 'khaled bouabdallah'


import sys
from text_strings import arabic
import pandas as pd
import datetime
from functools import partial
from PyQt5.QtCore import QAbstractTableModel,Qt


# get access to the  resources
import qrc_resources
# import GUI components
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QSpinBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QFormLayout,
    QComboBox,
    QPushButton
)







class EditWindow(QMainWindow):

    def __init__(self,parent=None):
        self.texts = arabic
        super().__init__(parent)
        self.setWindowTitle(self.texts['title'])
        self.resize(800,400)
        self.setWindowIcon(QIcon(':icon.png'))
        # right to left for arabic
        self.setLayoutDirection(1)
        self.set_centralWidget()
        self.set_actions()
        self.set_Menu()
        self.set_toolbar()
        self._createContextMenu()
        self.connect_actions()
        self.set_statuBar()

    def set_Menu(self):
        # getting the menubar object (already created by default empty)
        menuBar = self.menuBar()
        # add tools menu
        self.tools_menu = QMenu(self.texts['tools'],self)
        menuBar.addMenu(self.tools_menu)
        # add actions to the tools menu
        self.tools_menu.addAction(self.pdf_action)
        self.tools_menu.addAction(self.favorite_action)

        # add settings menu
        self.settings_menu = menuBar.addMenu(self.texts['settings'])
        # add actions to the settings menu
        self.settings_menu.addAction(self.change_dataframe_action)
        self.settings_menu.addSeparator()
        # add a submenu language to the settings menu
        self.languageMenu = self.settings_menu.addMenu(self.texts['language'])
        # add actions to the submenu language
        self.languageMenu.addAction(self.change_lanugage_arabic_action)
        self.languageMenu.addAction(self.change_lanugage_english_action)
        self.languageMenu.addAction(self.change_lanugage_frensh_action)

        # add information menu
        self.helpMenu = menuBar.addMenu(QIcon(":help-content.svg"), self.texts['information'])
        self.helpMenu.addAction(self.help_action)
        self.helpMenu.addAction(self.about_action)
        # add actions to the information menu

    #todo
    def set_statuBar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready", 3000)
        time_text = QLabel(get_current_time())
        self.statusbar.addPermanentWidget(time_text)

    def set_toolbar(self):

        # add the tools toolbar
        self.tools_toolbar = QToolBar()
        self.tools_toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea,self.tools_toolbar)
        # add actions to the tools toolbar
        self.tools_toolbar.addAction(self.pdf_action)
        self.tools_toolbar.addAction(self.favorite_action)
        # add the options tool bar
        self.options_toolbar = QToolBar()
        self.options_toolbar.setMovable(False)
        self.addToolBar(Qt.LeftToolBarArea, self.options_toolbar)


    #todo
    def set_centralWidget(self):
        self.tabs = QTabWidget()
        self._centralWididget = self.tabs
        self.setCentralWidget(self._centralWididget)
        self.tabs.addTab(self.set_people_widget(),self.texts['people'])
        self.tabs.addTab(self.set_families_widget(),self.texts['families'])
        self.tabs.addTab(self.set_regions_widget(),self.texts['regions'])
        self.tabs.addTab(self.set_general_widget(),self.texts['general'])


    def set_actions(self):
        #setting language actions
        self.change_lanugage_arabic_action = QAction(QIcon(':saudi-arabia.png'), self.texts['arabic'], self)
        self.change_lanugage_english_action = QAction(QIcon(':united-kingdom.png'), self.texts['english'], self)
        self.change_lanugage_frensh_action = QAction(QIcon(':france.png'), self.texts['frensh'], self)
        # setting changing dataframe action
        self.change_dataframe_action = QAction(self.texts['file'], self)
        # setting help/about actions
        self.help_action = QAction(self.texts['help'], self)
        self.about_action = QAction(self.texts['about'], self)
        # setting navigation actions
        self.people_action = QAction(self.texts['people'],self)
        self.familiy_action = QAction(self.texts['families'], self)
        self.region_action = QAction(self.texts['regions'], self)
        self.global_action = QAction(self.texts['general'], self)
        # settings tools actions
        self.pdf_action = QAction(self.texts['expo_pdf'], self)
        self.favorite_action = QAction(self.texts['favorite'], self)
        # Using string-based key sequences todo

    #todo
    def _createContextMenu(self):
        # Setting contextMenuPolicy

        self._centralWididget.setContextMenuPolicy(Qt.ActionsContextMenu)
        # Populating the widget with actions
        pass

    #todo
    def connect_actions(self):
        pass

    def set_people_widget(self):


        def build_options_widget(self):
            # to store options widgets
            self.people_options = {}
            # create option widget
            options_widget = QWidget()
            # craete form layout and set it up
            vlayout = QVBoxLayout()
            formlayout = QFormLayout()
            options_widget.setLayout(vlayout)

            # building the form
            #adding first name option
            self.people_options['fname']=QLineEdit()
            formlayout.addRow('الاسم:',self.people_options['fname'])
            # adding last name option
            self.people_options['lname'] = QLineEdit()
            formlayout.addRow('اللقب:', self.people_options['lname'])
            # adding last name option
            self.people_options['region'] = QLineEdit()
            formlayout.addRow('المنطقة:', self.people_options['region'])
            # adding date options
            formlayout.addWidget(QLabel('<hr>'))
            formlayout.addWidget(QLabel('تاريخ الميلاد'))
            # adding year option
            self.people_options['year'] = QLineEdit()
            formlayout.addRow('السنة:', self.people_options['year'])
            # adding month option
            self.people_options['month'] = QLineEdit()
            formlayout.addRow('الشهر:', self.people_options['month'])
            # adding year option
            self.people_options['day'] = QLineEdit()
            formlayout.addRow('اليوم:', self.people_options['day'])
            # adding gender option
            formlayout.addWidget(QLabel('<hr>'))
            self.people_options['gender'] = QComboBox()
            self.people_options['gender'].addItem('غير محدد')
            self.people_options['gender'].addItem('ذكر')
            self.people_options['gender'].addItem('انثي')
            formlayout.addRow('الجنس:', self.people_options['gender'])
            # adding sorting option
            formlayout.addWidget(QLabel('<hr>'))
            self.people_options['sort'] = QComboBox()
            self.people_options['sort'].addItem('لا')
            self.people_options['sort'].addItem('ابجدي')
            self.people_options['sort'].addItem('العمر')
            formlayout.addRow('رتب حسب:', self.people_options['sort'])


            # add label title
            vlayout.addWidget(QLabel('<h3>خصائص </h3>'))
            # adding the form
            vlayout.addLayout(formlayout)
            # adding search option
            vlayout.addWidget(QLabel('<hr>'))
            self.people_options['search'] = QPushButton('بحث')
            vlayout.addWidget(self.people_options['search'])

            return options_widget

        # loading data from excel file
        df = pd.read_excel(r'resources\data_frame\example_dataframe.xlsx')
        # modeling the data
        model = pandasModel(df)
        # building a table view for the data
        self.people_table_view = QTableView()
        self.people_table_view.setModel(model)
        self.people_table_view.setFixedWidth(710)
        # setting up the widget and the lyout
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)
        # adding the table widget
        layout.addWidget(self.people_table_view)
        # adding the options widget
        layout.addWidget(build_options_widget(self))
        return widget





    def set_families_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = layout.addWidget(QLabel('<h1>families</h1>'))
        widget.setLayout(layout)
        return widget

    def set_regions_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = layout.addWidget(QLabel('<h1>regions</h1>'))
        widget.setLayout(layout)
        return widget

    def set_general_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = layout.addWidget(QLabel('<h1>general</h1>'))
        widget.setLayout(layout)
        return widget





    #todo implemnting actions methodes


def main():
    app = QApplication(sys.argv)
    view = EditWindow()
    view.show()
    sys.exit(app.exec())

def get_current_time():
    x = datetime.datetime.now()
    return x.strftime('%H : %M')

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

if __name__ == '__main__':
    main()