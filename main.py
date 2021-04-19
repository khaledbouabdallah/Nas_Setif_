"""
Setif's people is a small application that allows to communicate with a data base
built with pandas,PyQt5 and matplotlib
"""

__version__ = '0.2beta'
__author__ = 'khaled bouabdallah'

import math
import sys
import time
import json

from PyQt5.uic.properties import QtCore, QtWidgets
from dateutil.relativedelta import relativedelta

from text_strings import arabic
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QPropertyAnimation, QRegExp
import pandas as pd
import datetime
from functools import partial
from PyQt5.QtCore import QAbstractTableModel, Qt


# get access to the  resources
import qrc_resources

from PyQt5.QtGui import QIcon, QPainter, QPixmap, QMovie, QRegExpValidator
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

    def __init__(self,parent=None,text= arabic):
        self.texts = text
        super().__init__(parent)
        self.init_Ui()


    def loading(self):
        self.wait = QLabel('ffs')
        self.statusbar.addWidget(self.wait)

    def unloading(self):
        self.wait.close()

    def init_Ui(self):
        self.setWindowTitle(self.texts['title'])
        self.resize(800, 400)
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
        self.statusbar.setLayoutDirection(0)
        self.setStatusBar(self.statusbar)
        #self.statusbar.showMessage("Ready", 3000)
        self.rows_count = QLabel('0')
        self.statusbar.addPermanentWidget(self.rows_count)

    #todo
    def waiting(self):
        pass

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

    #todo make imporvemnts
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
            formlayout.addRow(self.texts['firstname'],self.people_options['fname'])
            # adding last name option
            self.people_options['lname'] = QLineEdit()
            formlayout.addRow(self.texts["lastname"], self.people_options['lname'])
            # adding last name option
            self.people_options['tribe'] = QLineEdit()
            formlayout.addRow(self.texts["tribe"], self.people_options['tribe'])
            # adding date options
            formlayout.addWidget(QLabel('<hr>'))
            formlayout.addWidget(QLabel(self.texts['birth_date']))
            # making a numbers validator
            grammar = QRegExp("[0-9]*")
            validator = QRegExpValidator(grammar)
            # adding year option
            self.people_options['year'] = QLineEdit()
            self.people_options['year'].setValidator(validator)
            formlayout.addRow(self.texts['year'], self.people_options['year'])
            # adding month option
            self.people_options['month'] = QLineEdit()
            self.people_options['month'].setValidator(validator)
            formlayout.addRow(self.texts['month'], self.people_options['month'])
            # adding year option
            self.people_options['day'] = QLineEdit()
            self.people_options['day'].setValidator(validator)
            formlayout.addRow(self.texts['day'], self.people_options['day'])
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
        self.people_table_view.setFixedWidth(640)
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

        def build_options_widget(self):
            # to store options widgets
            self.tribe_options = {}
            # create option widget
            options_widget = QWidget()
            # craete form layout and set it up
            vlayout = QVBoxLayout()
            formlayout = QFormLayout()
            options_widget.setLayout(vlayout)
            # building the form

            # adding last name option
            self.tribe_options['tribe'] = QLineEdit()
            formlayout.addRow(self.texts["tribe"], self.tribe_options['tribe'])

            # adding sorting option
            formlayout.addWidget(QLabel('<hr>'))
            self.tribe_options['sort'] = QComboBox()
            self.tribe_options['sort'].addItem('لا')
            self.tribe_options['sort'].addItem('ابجدي')
            self.tribe_options['sort'].addItem('العمر')
            formlayout.addRow('رتب حسب:', self.tribe_options['sort'])
            # add label title
            vlayout.addWidget(QLabel('<h3>خصائص </h3>'))
            # adding the form
            vlayout.addLayout(formlayout)
            # adding search option
            vlayout.addWidget(QLabel('<hr>'))
            self.tribe_options['search'] = QPushButton('بحث')
            vlayout.addWidget(self.tribe_options['search'])
            return options_widget

        # building a table view
        self.tribes_table_view = QTableView()
        self.tribes_table_view.setFixedWidth(640)
        # setting up the widget and the lyout
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)
        # adding the table widget
        layout.addWidget(self.tribes_table_view)
        # adding the options widget
        layout.addWidget(build_options_widget(self))
        return widget

    #todo
    def set_general_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = layout.addWidget(QLabel('<h1>general</h1>'))
        widget.setLayout(layout)
        return widget

    #todo
    def change_to_english(self):
        self.setLayoutDirection(0)
    #todo
    def change_to_arabic(self):
        self.setLayoutDirection(1)
    #todo
    def change_to_frensh(self):
        self.setLayoutDirection(0)

    def loqding(self):
        self.movie = QMovie(r'resources\loading.gif')
        self.lab = QLabel('lmao')
        self.lab.setMovie(self.movie)

class Controller(object):

    def __init__(self,view,path):

        self.init_dataframe(path)
        self.init_tribes_df()
        self.view = view
        self.load_people()
        self.load_tribes()
        self._connect()

    def init_dataframe(self,path):

        def fix_gender(gender):
            gender = gender.strip()
            if gender in ['ذ','د']:
                return 'ذكر'
            elif gender in ['أ','ا']:
                return 'انثى'
            else:
                return 'غير محدد'

        # initiliasing the data base file path
        self.path = path
        # creating a data frame for the file
        df = pd.read_excel(path)
        # preparing the dataframe
        # fixing the 'Sexe' values
        df["Sexe"] = df["Sexe"].apply(fix_gender)
        df["Sexe"] = pd.Categorical(df["Sexe"])
        df["Date de naissanace"] = pd.to_datetime(df["Date de naissanace"])
        # setting the preparted dataframe for later
        self.dataframe = df
        # creatig the tribes dataframe

    def init_tribes_df(self):

        def fix_count(x):
            if math.isnan(x):
                return 0
            else:
                return x

        def yearsago(years, from_date=None):
            if from_date is None:
                from_date = datetime.datetime.now()
            return from_date - relativedelta(years=years)

        df = self.dataframe.copy()
        df['Age'] = [yearsago(x).year for x in df['Date de naissanace'].dt.year]
        tribes_groups = df.groupby(['Tribue'])
        # number of people in each tribe
        tribe_count = df['Tribue'].value_counts()
        tribe_count = tribe_count.rename('عدد الافراد')
        #
        age = df[df['Age'] < 20]
        age_count = age.groupby(['Tribue'])["Nom"].count()
        age_count00 = age_count.rename('اقل من 20 سنة')
        #
        age = df[(df['Age'] < 40) & (df['Age'] >= 20)]
        age_count = age.groupby(['Tribue'])["Nom"].count()
        age_count20 = age_count.rename('من 20 الى 40 سنة')
        #
        age = df[(df['Age'] < 60) & (df['Age'] >= 40)]
        age_count = age.groupby(['Tribue'])["Nom"].count()
        age_count40 = age_count.rename('من 40 الى 60 سنة')
        #
        age = df[(df['Age'] < 80) & (df['Age'] >= 60)]
        age_count = age.groupby(['Tribue'])["Nom"].count()
        age_count60 = age_count.rename('من 60 الى 80 سنة')
        #
        age = df[80 <= df['Age']]
        age_count = age.groupby(['Tribue'])["Nom"].count()
        age_count80 = age_count.rename('اكبر من 80 سنة')
        #
        sexe_count = df.groupby(['Tribue', 'Sexe'], as_index=False, sort=False)['Nom'].count()
        sexe_count = sexe_count.pivot_table('Nom', ['Tribue'], 'Sexe')
        #
        df_tribe = pd.concat([tribe_count, sexe_count], axis='columns', sort=False)
        #
        df_tribe['نسبة الذكور'] = df_tribe['ذكر'] / df_tribe['عدد الافراد']
        df_tribe['نسبة الاناث'] = df_tribe['انثى'] / df_tribe['عدد الافراد']
        df_tribe['نسبة الذكور'] = [round(x, 2) for x in df_tribe['نسبة الذكور']]
        df_tribe['نسبة الاناث'] = [round(x, 2) for x in df_tribe['نسبة الاناث']]
        #
        df_tribe = pd.concat([df_tribe, age_count00, age_count20, age_count40, age_count60, age_count80],
                             axis='columns', sort=False)
        #
        df_tribe['اقل من 20 سنة'] = df_tribe['اقل من 20 سنة'].apply(fix_count)
        df_tribe['من 20 الى 40 سنة'] = df_tribe['من 20 الى 40 سنة'].apply(fix_count)
        df_tribe['من 40 الى 60 سنة'] = df_tribe['من 40 الى 60 سنة'].apply(fix_count)
        df_tribe['من 60 الى 80 سنة'] = df_tribe['من 60 الى 80 سنة'].apply(fix_count)
        df_tribe['اكبر من 80 سنة'] = df_tribe['اكبر من 80 سنة'].apply(fix_count)
        self.tribe_dataframe = df_tribe

    # build people table view
    def load_people(self):
        renamed = self.rename_dataframe_columns(self.dataframe,self.view.texts['columns_names'])
        pdmodel = PandasModelPeople(renamed)
        self.update_rows_count(pdmodel.rowCount())
        self.view.people_table_view.setModel(pdmodel)

    def load_tribes(self):
        pdmodel = PandasModelPeople(self.tribe_dataframe)
        self.view.tribes_table_view.setModel(pdmodel)

    # search for people and build the new table view
    # todo : finish all options
    def search_people(self):

        #gettings instance of the data frame
        df = self.dataframe
        # getting values from the user
        fname = self.view.people_options['fname'].text().strip()
        lname = self.view.people_options['lname'].text().strip()
        tribe = self.view.people_options['tribe'].text().strip()
        year = self.view.people_options['year'].text().strip()
        month = self.view.people_options['month'].text().strip()
        day = self.view.people_options['day'].text().strip()
        gender = self.view.people_options['gender']
        sort = self.view.people_options['sort']
        # filtring the dataframe
        if fname:
            df = df[df['Prénom']==fname]
        if lname:
            df = df[df['Nom'] == lname]
        if tribe:
            df = df[df['Tribue'] == tribe]
        if year:
            df = df[df['Date de naissanace'].dt.year == int(year)]
        if month:
            df = df[df['Date de naissanace'].dt.month== int(month)]
        if day:
            df = df[df['Date de naissanace'].dt.day== int(day)]
        if gender.currentIndex() == 1:
            df = df[df['Sexe'] == 'ذكر']
        elif gender.currentIndex() == 2:
            df = df[df['Sexe'] == 'انثى']
        #todo implement sorted feature
        if sort.currentIndex() == 1:
            df = df.sort_values(by='Nom')
        elif sort.currentIndex() == 2:
            df = df.sort_values(by='Date de naissanace')
        # updating the statu bar
        self.update_rows_count(df.shape[0])
        # gettign a renamed version
        renamed = self.rename_dataframe_columns(df, self.view.texts['columns_names'])
        pandas_model = PandasModelPeople(renamed)
        # updating the GUI
        self.view.people_table_view.setModel(pandas_model)

    def edit_trabes(self):
        pass

     # return a renamed columns version of a dataframe
    def rename_dataframe_columns(self,df,args):
        columns = df.columns
        renamed = df.rename(columns={columns[0]: args[0], columns[1]: args[1],columns[2]: args[2],columns[3]: args[3],columns[4]: args[4],columns[5]: args[5],})
        return renamed

    def change_file_action(self):

        #takes 1 or 0 and shows the right dialog
        def showdialogs(n):
            self.view.unloading()
            if n:
                showdialog1()
            else:
                showdialog2()


        # show a dialog if the file changed
        def showdialog1():

            def func(decision):

                global app

                if decision :

                    d.close()
                    app.exit(0)

                else:
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

        # show a dialog if file didnt change
        def showdialog2():
            d = QDialog()
            layout = QVBoxLayout()
            layout.addWidget(QLabel('قاعدة البيانات التي اخترتها ليست مناسبة'))
            d.setLayout(layout)
            d.setWindowTitle("Dialog")
            d.setWindowModality(Qt.ApplicationModal)
            d.exec_()
            pass

        # show the file navigation interface and saving the path file chosen as str in 'fname'
        fname = QFileDialog.getOpenFileName(self.view, 'اختر ملف',
                                            'c:\\', "قاعدة البيانات (*.xlsx)")
        # check if user chose a file
        if fname[0]:
            # setting a worker and a thread for processing the file chosen
            self.thread = QThread()
            self.worker = Worker(fname[0])
            # moving the worker to the therad and connecting them
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            # making sure to close the thread and the worker after they finish
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            # when the worker finish processing the file show the result dialog
            self.worker.progress.connect(showdialogs)
            # start the worker thread
            self.thread.start()
            # start the loading animation #todo
            self.view.loading()

    # updating the rows count in statu bar
    def update_rows_count(self,rows):
        string = self.view.texts['found_message']+' ' + str(rows) + ' نتائج '
        self.view.rows_count.setText(string)

    # connect widgets with methodes using singnals
    def _connect(self):
        # connect search people action
        self.view.people_options['search'].clicked.connect(self.search_people)
        # connect change file action
        self.view.change_dataframe_action.triggered.connect(self.change_file_action)
        # connect the change lanugage actions
        self.view.change_lanugage_english_action.triggered.connect(self.view.change_to_english)
        self.view.change_lanugage_frensh_action.triggered.connect(self.view.change_to_frensh)
        self.view.change_lanugage_arabic_action.triggered.connect(self.view.change_to_arabic)
        #todo connect the rest
        pass

class PandasModelPeople(QAbstractTableModel):

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
                if type(self._data.iloc[index.row(), index.column()]) == pd._libs.tslibs.timestamps.Timestamp:
                    temp = self._data.iloc[index.row(), index.column()]
                    temp = temp.strftime("%d/%m/%Y")
                    return str(temp)
                else:
                    return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None



class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    def __init__(self,path):
        super().__init__()
        self.path = path
    def run(self):
        # load data bse
        df = pd.read_excel(self.path)

        # check if user chose a compateble file
        if df.columns[0] == 'Nom':
            df["Sexe"] = pd.Categorical(df["Nom"])
            # updating the config.json
            a_file = open("config.json", "r")
            json_object = json.load(a_file)
            a_file.close()
            json_object['file'] = self.path
            a_file = open("config.json", "w")
            json.dump(json_object, a_file)
            a_file.close()
            # show confirmation dialog
            self.progress.emit(1)

        else:
            # show file unsupported dialog
            self.progress.emit(0)
        self.finished.emit()

def main():
    # get setiings from config.json
    settings = load_settings()
    # set the application
    global app
    app = QApplication(sys.argv)
    # set view and  controller
    view = Window(text=settings[0])
    controller = Controller(view,settings[1])
    # show the view
    view.show()
    # exit when app closed
    sys.exit(app.exec())

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