"""
Setif's people is a small application that allows to communicate with a data base
built with pandas,PyQt5 and matplotlib
"""

__version__ = '0.1'
__author__ = 'khaled bouabdallah'


import sys
import json
from text_strings import arabic
import pandas as pd
import datetime
import metadata
from functools import partial
from PyQt5.QtCore import QAbstractTableModel,Qt


# get access to the  resources
import qrc_resources

from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QKeySequence

# import GUI components
from PyQt5.QtWidgets import (
    QToolBar,
    QAction,
    QTabWidget,
    QApplication,
    QMainWindow,
    QMenu,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QFormLayout,
    QComboBox,
    QPushButton,
    QTableView,
    QStatusBar,
    QDialog,
    QFileDialog
)

class Window(QMainWindow):

    def __init__(self,parent=None,text =arabic):
        self.texts = text
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
        pass


    #todo
    def _createContextMenu(self):
        # Setting contextMenuPolicy

        self._centralWididget.setContextMenuPolicy(Qt.ActionsContextMenu)
        # Populating the widget with actions
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
            self.people_options['gender'].currentText()
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
        # building a table view
        self.people_table_view = QTableView()
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

    #todo
    def set_families_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = layout.addWidget(QLabel('<h1>families</h1>'))
        widget.setLayout(layout)
        return widget

    #todo
    def set_regions_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = layout.addWidget(QLabel('<h1>regions</h1>'))
        widget.setLayout(layout)
        return widget

    #todo
    def set_general_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = layout.addWidget(QLabel('<h1>general</h1>'))
        widget.setLayout(layout)
        return widget

class Model(object):

    def __init__(self,path):
        df = pd.read_excel(path)
        df["الجنس"] = pd.Categorical(df["الجنس"])
        self.df = df
        self.path = path

    def get_dataframe(self):
        return self.df

    def get_path(self):
        return self.path


    def set_dataframe(self,path):
        self.df = pd.read_excel(path)

class Controller(object):

    def __init__(self,view,model):
        dataframe = model.get_dataframe()
        self.view = view
        self.model = model
        self.pandas_model = PandasModel(dataframe)
        self.load_people()
        self._connect()

    # build people table view
    def load_people(self):
        self.view.people_table_view.setModel(self.pandas_model)

    # search for people and build the new table view
    def search_people(self):
        #setting up the information
        df = self.model.get_dataframe()
        fname = self.view.people_options['fname'].text().strip()
        lname = self.view.people_options['lname'].text().strip()
        region = self.view.people_options['region'].text().strip()
        year = self.view.people_options['year'].text().strip()
        month = self.view.people_options['month'].text().strip()
        day = self.view.people_options['day'].text().strip()
        gender = self.view.people_options['gender'].currentText().strip()
        sort = self.view.people_options['sort'].currentText().strip()


        if fname:
            df = df[df['الاسم']==fname]
        elif lname:
            df = df[df['اللقب'] == lname]
        elif region:
            df = df[df['المنطقة'] == region]
        elif year:
            pass
        elif month:
            pass
        elif day:
            pass

        pandas_model = PandasModel(df)
        self.view.people_table_view.setModel(pandas_model)

    def change_file_action(self):

        def showdialog():

            def func(decision):

                global app

                if decision :
                    print("1")
                    d.close()
                    app.exit(0)

                else:
                    print("0")
                    d.close()

            d = QDialog()
            layout = QVBoxLayout()
            d.setLayout(layout)
            layout.addWidget(QLabel(self.view.texts['exit_message']))
            layout2 = QHBoxLayout()
            btn1 = QPushButton(self.view.texts['yes'])
            btn2 = QPushButton(self.view.texts['no'])
            layout2.addWidget(btn1)
            layout2.addWidget(btn2)
            layout.addLayout(layout2)
            btn1.clicked.connect(partial(func,True))
            btn2.clicked.connect(partial(func,False))
            d.setWindowTitle("Dialog")
            d.setWindowModality(Qt.ApplicationModal)
            d.exec_()




        fname = QFileDialog.getOpenFileName(self.view, 'Open file',
                                            'c:\\', "Image files (*.xlsx)")
        settings = load_settings()
        print('fname')
        print(fname[0])
        print('settings')
        print(settings[1])
        if fname[0]:
            a_file = open("config.json", "r")
            json_object = json.load(a_file)
            a_file.close()
            json_object['file'] = fname[0]
            a_file = open("config.json", "w")
            json.dump(json_object, a_file)
            a_file.close()
            showdialog()




    # connect widgets with methodes using singnals
    def _connect(self):
        self.view.people_options['search'].clicked.connect(self.search_people)
        self.view.change_dataframe_action.triggered.connect(self.change_file_action)
        pass

class PandasModel(QAbstractTableModel):

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

def main():
    # get setiings from config.json
    settings = load_settings()
    # set the application
    global app
    app = QApplication(sys.argv)
    # set view - model - controller
    view = Window(text=settings[0])
    model = Model(settings[1])
    controller = Controller(view,model)
    # show the view
    view.show()
    # exit when app closed
    sys.exit(app.exec())

def get_current_time():
    x = datetime.datetime.now()
    return x.strftime('%H : %M')

def load_settings():
    with open('config.json') as json_file:
        data = json.load(json_file)
    if data['language']=='arabic':
        text = arabic
    elif data['language']=='english':
        pass
    elif data['language']=='frensh':
        pass

    file = data['file']

    return text,file


if __name__ == '__main__':
    main()