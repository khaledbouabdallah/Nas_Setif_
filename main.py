"""
Setif's people is a small application that allows to communicate with a data base
built with pandas,PyQt5 and matplotlib
"""

__version__ = '0.2beta'
__author__ = 'khaled bouabdallah'


import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets
import math
import sys
import json
from dateutil.relativedelta import relativedelta
from text_strings import arabic
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QPropertyAnimation, QRegExp, QSortFilterProxyModel
import pandas as pd
import datetime
from functools import partial
from PyQt5.QtCore import QAbstractTableModel, Qt
import arabic_reshaper
from bidi.algorithm import get_display

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
    QFileDialog, QCompleter, QHeaderView
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
        self.setFixedSize(1280,800)
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
            vlayout.setSpacing(20)
            return options_widget
        # building a table view
        self.people_table_view = QTableView()
        self.people_table_view.setFixedWidth(900)
        header = self.people_table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        # setting up the widget and the lyout
        widget = QWidget()
        layout = QHBoxLayout()
        #layout.setSpacing(100)
        widget.setLayout(layout)
        # adding the table widget
        layout.addWidget(self.people_table_view)
        # adding the options widget
        option_widget = build_options_widget(self)
        #option_widget.setFixedWidth(200)
        layout.addWidget(option_widget)
        #layout.addSpacing(300)
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

            self.tribe_option_widget = Tribe_tools_widget_Form()
            w = QWidget()
            self.tribe_option_widget.setupUi(w)
            self.tribe_option_widget.sort_list = ['ابجدي',
                                                  'ع الافراد',
                                                  'ع الالقاب',
                                                  'ع الذكور',
                                                  'ع الاناث',
                                                  'ن الذكور',
                                                  'ن الاناث',
                                                  'ع 00-20 سنة',
                                                  'ع 20-40 سنة',
                                                  'ع 40-60 سنة',
                                                  'ع 60-80 سنة',
                                                  'ع +80 سنة',
                                                  'ن 00-20 سنة',
                                                  'ن 20-40 سنة',
                                                  'ن 40-60 سنة',
                                                  'ن 60-80 سنة',
                                                  'ن +80 سنة',]
            self.tribe_option_widget.comboBox_sort_by.addItems(self.tribe_option_widget.sort_list)
            self.tribe_option_widget.spinBox_view_few.setValue(5)
            return w

        # building a table view
        self.tribes_table_view = QTableView()
        self.tribes_table_view.setFixedWidth(900)
        # stetching the table columns
        #header = self.tribes_table_view.horizontalHeader()
        #header.setSectionResizeMode(QHeaderView.Stretch)
        # building matplotlib canvas
        self.tribe_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar(self.tribe_canvas, self)


        # setting up the widget and the lyout
        widget = QWidget()
        layout = QHBoxLayout()
        vlayout = QVBoxLayout()
        widget.setLayout(layout)
        # adding the table widget
        layout.addLayout(vlayout)
        layout.addWidget(QVSeperationLine())

        vlayout.addWidget(self.tribes_table_view)
        # adding the canvas widget and its tool bar
        vlayout.addWidget(self.tribe_canvas)
        vlayout.addWidget(toolbar)

        # adding the options widget
        layout.addWidget(build_options_widget(self))
        return widget

    #todo
    def set_general_widget(self):
        w = QWidget()
        return w

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
        self.load_matplotlib_tribe_fig()
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

        ## number of  people in each tribe

        tribe_count = df['Tribue'].value_counts()
        tribe_count = tribe_count.rename('ع الافراد')

        ### number of families in each tribe

        tribe_family_count = tribes_groups['Nom'].nunique()
        tribe_family_count = tribe_family_count.rename('ع الالقاب')

        ## number of people 0-20 years old in each group

        age = df[df['Age'] < 20]
        age_count = age.groupby(['Tribue'])["Nom"].count()
        age_count00 = age_count.rename('ع 00-20 سنة')

        ## number of people 20-40 years old in each group

        age = df[(df['Age'] < 40) & (df['Age'] >= 20)]
        age_count = age.groupby(['Tribue'])["Nom"].count()
        age_count20 = age_count.rename('ع 20-40 سنة')

        ## number of people 40-60 years old in each group

        age = df[(df['Age'] < 60) & (df['Age'] >= 40)]
        age_count = age.groupby(['Tribue'])["Nom"].count()
        age_count40 = age_count.rename('ع 40-60 سنة')

        ## number of people 60-80 years old in each group

        age = df[(df['Age'] < 80) & (df['Age'] >= 60)]
        age_count = age.groupby(['Tribue'])["Nom"].count()
        age_count60 = age_count.rename('ع 60-80 سنة')

        ## number of people +80 years old in each group

        age = df[80 <= df['Age']]
        age_count = age.groupby(['Tribue'])["Nom"].count()
        age_count80 = age_count.rename('ع +80 سنة')

        ## count females and males (another way)

        sexe_count = df.groupby(['Tribue', 'Sexe'], as_index=False, sort=False)['Nom'].count()
        sexe_count = sexe_count.pivot_table('Nom', ['Tribue'], 'Sexe')
        sexe_count.rename(columns={'ذكر': 'ع الذكور', 'انثى': 'ع الاناث'}, inplace=True)

        ## Concatinating the series

        df_tribe = pd.concat(
            [tribe_count, tribe_family_count, sexe_count, age_count00, age_count20, age_count40, age_count60,
             age_count80], axis='columns', sort=False)

        ## Sexe percentege by each group

        df_tribe['ن الذكور'] = df_tribe['ع الذكور'] / df_tribe['ع الافراد']
        df_tribe['ن الاناث'] = df_tribe['ع الاناث'] / df_tribe['ع الافراد']
        df_tribe['ن الذكور'] = [round(x, 2) for x in df_tribe['ن الذكور']]
        df_tribe['ن الاناث'] = [round(x, 2) for x in df_tribe['ن الاناث']]

        ## adding age columns

        ## cleaning age columns

        df_tribe['ع 00-20 سنة'] = df_tribe['ع 00-20 سنة'].apply(fix_count)
        df_tribe['ع 20-40 سنة'] = df_tribe['ع 20-40 سنة'].apply(fix_count)
        df_tribe['ع 40-60 سنة'] = df_tribe['ع 40-60 سنة'].apply(fix_count)
        df_tribe['ع 60-80 سنة'] = df_tribe['ع 60-80 سنة'].apply(fix_count)
        df_tribe['ع +80 سنة'] = df_tribe['ع +80 سنة'].apply(fix_count)

        ### adding percentage age columns

        df_tribe['ن 00-20 سنة'] = df_tribe['ع 00-20 سنة'] / df_tribe['ع الافراد']
        df_tribe['ن 20-40 سنة'] = df_tribe['ع 20-40 سنة'] / df_tribe['ع الافراد']
        df_tribe['ن 40-60 سنة'] = df_tribe['ع 40-60 سنة'] / df_tribe['ع الافراد']
        df_tribe['ن 60-80 سنة'] = df_tribe['ع 60-80 سنة'] / df_tribe['ع الافراد']
        df_tribe['ن +80 سنة'] = df_tribe['ع +80 سنة'] / df_tribe['ع الافراد']

        df_tribe['ن 00-20 سنة'] = [round(x, 2) for x in df_tribe['ن 00-20 سنة']]
        df_tribe['ن 20-40 سنة'] = [round(x, 2) for x in df_tribe['ن 20-40 سنة']]
        df_tribe['ن 40-60 سنة'] = [round(x, 2) for x in df_tribe['ن 40-60 سنة']]
        df_tribe['ن 60-80 سنة'] = [round(x, 2) for x in df_tribe['ن 60-80 سنة']]
        df_tribe['ن +80 سنة'] = [round(x, 2) for x in df_tribe['ن +80 سنة']]

        ### adding index as a column

        df_tribe['القبيلة'] = df_tribe.index

        ### fixing columns order

        col = ['القبيلة',
               'ع الافراد',
               'ع الالقاب',
               'ع الذكور',
               'ع الاناث',
               'ن الذكور',
               'ن الاناث',
               'ع 00-20 سنة',
               'ع 20-40 سنة',
               'ع 40-60 سنة',
               'ع 60-80 سنة',
               'ع +80 سنة',
               'ن 00-20 سنة',
               'ن 20-40 سنة',
               'ن 40-60 سنة',
               'ن 60-80 سنة',
               'ن +80 سنة', ]

        df_tribe = df_tribe[col]

        self.tribe_dataframe = df_tribe

    # build people table view
    def load_people(self):
        renamed = self.rename_dataframe_columns(self.dataframe,self.view.texts['columns_names'])
        pdmodel = PandasModelPeople(renamed)
        self.update_rows_count(pdmodel.rowCount())
        self.view.people_table_view.setModel(pdmodel)

    def load_tribes(self):
        # getting ressources ready
        df = self.tribe_dataframe.copy()
        sort_value = self.view.tribe_option_widget.comboBox_sort_by.currentText()
        if sort_value == 'ابجدي':
            sort_value='القبيلة'
        sort_settings = bool(self.view.tribe_option_widget.radioButton_up.isChecked())
        first_only = bool(self.view.tribe_option_widget.cb_view_few.isChecked())
        how_mutch = self.view.tribe_option_widget.spinBox_view_few.value()
        cb1 = self.view.tribe_option_widget.cb1.isChecked()
        cb2 = self.view.tribe_option_widget.cb2.isChecked()
        cb3 = self.view.tribe_option_widget.cb3.isChecked()
        cb4 = self.view.tribe_option_widget.cb4.isChecked()
        cb5 = self.view.tribe_option_widget.cb5.isChecked()
        cb6 = self.view.tribe_option_widget.cb6.isChecked()
        cb7 = self.view.tribe_option_widget.cb7.isChecked()
        cb8 = self.view.tribe_option_widget.cb8.isChecked()
        cb9 = self.view.tribe_option_widget.cb9.isChecked()
        cb10 = self.view.tribe_option_widget.cb10.isChecked()
        cb11 = self.view.tribe_option_widget.cb11.isChecked()
        cb12 = self.view.tribe_option_widget.cb12.isChecked()
        cb13 = self.view.tribe_option_widget.cb13.isChecked()
        cb14 = self.view.tribe_option_widget.cb14.isChecked()
        cb15 = self.view.tribe_option_widget.cb15.isChecked()
        cb16 = self.view.tribe_option_widget.cb16.isChecked()

        # sorting the df
        df = df.sort_values(by=sort_value,ascending=sort_settings)

        # getting only first results
        if first_only:
            df = df.head(how_mutch)


        pdmodel = PandasModelTribes(df)

        # drawing the tribes table
        self.view.tribes_table_view.setModel(pdmodel)
        # showing only columns that we want
        if cb1:
            self.view.tribes_table_view.setColumnHidden(1, False)
        else:
            self.view.tribes_table_view.setColumnHidden(1, True)
        if cb2:
            self.view.tribes_table_view.setColumnHidden(2, False)
        else:
            self.view.tribes_table_view.setColumnHidden(2, True)
        if cb3:
            self.view.tribes_table_view.setColumnHidden(3, False)
        else:
            self.view.tribes_table_view.setColumnHidden(3, True)
        if cb4:
            self.view.tribes_table_view.setColumnHidden(4, False)
        else:
            self.view.tribes_table_view.setColumnHidden(4, True)
        if cb5:
            self.view.tribes_table_view.setColumnHidden(5, False)
        else:
            self.view.tribes_table_view.setColumnHidden(5, True)
        if cb6:
            self.view.tribes_table_view.setColumnHidden(6, False)
        else:
            self.view.tribes_table_view.setColumnHidden(6, True)
        if cb7:
            self.view.tribes_table_view.setColumnHidden(7, False)
        else:
            self.view.tribes_table_view.setColumnHidden(7, True)
        if cb8:
            self.view.tribes_table_view.setColumnHidden(12, False)
        else:
            self.view.tribes_table_view.setColumnHidden(12, True)
        if cb9:
            self.view.tribes_table_view.setColumnHidden(8, False)
        else:
            self.view.tribes_table_view.setColumnHidden(8, True)
        if cb10:
            self.view.tribes_table_view.setColumnHidden(13, False)
        else:
            self.view.tribes_table_view.setColumnHidden(13, True)
        if cb11:
            self.view.tribes_table_view.setColumnHidden(9, False)
        else:
            self.view.tribes_table_view.setColumnHidden(9, True)
        if cb12:
            self.view.tribes_table_view.setColumnHidden(14, False)
        else:
            self.view.tribes_table_view.setColumnHidden(14, True)
        if cb13:
            self.view.tribes_table_view.setColumnHidden(10, False)
        else:
            self.view.tribes_table_view.setColumnHidden(10, True)
        if cb14:
            self.view.tribes_table_view.setColumnHidden(15, False)
        else:
            self.view.tribes_table_view.setColumnHidden(15, True)
        if cb15:
            self.view.tribes_table_view.setColumnHidden(11, False)
        else:
            self.view.tribes_table_view.setColumnHidden(11, True)
        if cb16:
            self.view.tribes_table_view.setColumnHidden(16, False)
        else:
            self.view.tribes_table_view.setColumnHidden(16, True)

    # search for people and build the new table view
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


    def load_matplotlib_tribe_fig(self):
         fig = self.view.tribe_canvas.axes
         #fig.clear()
         # getting data ready

         df = self.tribe_dataframe.copy()
         columns = list(df.columns)
         columns = [str(x) for x in columns]
         charts_types = ['رسم بياني شريطي','رسم بياني عمودي','رسم بياني خطي','رسم بياني مساحي','رسم بياني دائري','رسم بياني لنقاط المبعثرة']

         self.view.tribe_option_widget.comboBox.addItems(columns)
         select_x = self.view.tribe_option_widget.comboBox.currentText()

         self.view.tribe_option_widget.comboBox_chart.addItems(charts_types)
         select_chart = self.view.tribe_option_widget.comboBox_chart.currentText()

         select_few = bool(self.view.tribe_option_widget.checkBox.isChecked())
         how_many = self.view.tribe_option_widget.spinBox.value()
         print(select_x)
         print(select_chart)

         #axe_x = df[select_x]
         #axe_y = df['ع الافراد']
         #axe_x = list([get_display(arabic_reshaper.reshape(x)) for x in axe_x])



         #fig.barh(axe_x,axe_y)

         fig.barh(df[select_x],df['ن الاناث'])



         fig.set_title('fking working')

         xlbl = get_display(arabic_reshaper.reshape(select_x))
         ylbl = get_display(arabic_reshaper.reshape('الترتيبات'))

         fig.set_xlabel(xlbl)

         #fig.pie(axe_y,labels = axe_x,autopct='%1.1f%%')
         #fig.set_ylabel(ylbl)



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
        # connect cb_view_few with its function
        self.view.tribe_option_widget.cb_view_few.stateChanged.connect(self.change_button_state)
        self.view.tribe_option_widget.pushButton_refresh.clicked.connect(self.load_tribes)
        self.view.tribe_option_widget.checkBox.stateChanged.connect(self.change_button_state2)
        self.view.tribe_option_widget.pushButton_chart.clicked.connect(self.load_matplotlib_tribe_fig)

        pass

    def change_button_state(self):
        if self.view.tribe_option_widget.cb_view_few.isChecked():
            self.view.tribe_option_widget.spinBox_view_few.setEnabled(True)
        else:
            self.view.tribe_option_widget.spinBox_view_few.setEnabled(False)

    def change_button_state2(self):
        if self.view.tribe_option_widget.checkBox.isChecked():
            self.view.tribe_option_widget.spinBox.setEnabled(True)
        else:
            self.view.tribe_option_widget.spinBox.setEnabled(False)


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

class PandasModelTribes(QAbstractTableModel):

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

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)


    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))


    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)


class QVSeperationLine(QtWidgets.QFrame):
  '''
  a vertical seperation line\n
  '''
  def __init__(self):
    super().__init__()
    self.setFixedWidth(20)
    self.setMinimumHeight(1)
    self.setFrameShape(QtWidgets.QFrame.VLine)
    self.setFrameShadow(QtWidgets.QFrame.Sunken)
    self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
    return

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




class Tribe_tools_widget_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(388, 859)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(0, 100))
        Form.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(20, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.toolButton = QtWidgets.QToolButton(Form)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_4.addWidget(self.toolButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.scrollArea = QtWidgets.QScrollArea(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 80))
        self.scrollArea.setMaximumSize(QtCore.QSize(16777215, 80))
        self.scrollArea.setBaseSize(QtCore.QSize(0, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 340, 196))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.cb16 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb16.setObjectName("cb16")
        self.gridLayout.addWidget(self.cb16, 9, 1, 1, 1)
        self.cb11 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb11.setObjectName("cb11")
        self.gridLayout.addWidget(self.cb11, 7, 0, 1, 1)
        self.cb13 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb13.setObjectName("cb13")
        self.gridLayout.addWidget(self.cb13, 8, 0, 1, 1)
        self.cb3 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb3.setChecked(True)
        self.cb3.setObjectName("cb3")
        self.gridLayout.addWidget(self.cb3, 2, 0, 1, 1)
        self.cb14 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb14.setObjectName("cb14")
        self.gridLayout.addWidget(self.cb14, 8, 1, 1, 1)
        self.cb15 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb15.setObjectName("cb15")
        self.gridLayout.addWidget(self.cb15, 9, 0, 1, 1)
        self.cb12 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb12.setObjectName("cb12")
        self.gridLayout.addWidget(self.cb12, 7, 1, 1, 1)
        self.cb7 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb7.setObjectName("cb7")
        self.gridLayout.addWidget(self.cb7, 4, 0, 1, 1)
        self.cb6 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb6.setChecked(True)
        self.cb6.setObjectName("cb6")
        self.gridLayout.addWidget(self.cb6, 3, 1, 1, 1)
        self.cb4 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb4.setChecked(True)
        self.cb4.setObjectName("cb4")
        self.gridLayout.addWidget(self.cb4, 2, 1, 1, 1)
        self.cb8 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb8.setObjectName("cb8")
        self.gridLayout.addWidget(self.cb8, 4, 1, 1, 1)
        self.cb5 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb5.setChecked(True)
        self.cb5.setObjectName("cb5")
        self.gridLayout.addWidget(self.cb5, 3, 0, 1, 1)
        self.cb9 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb9.setObjectName("cb9")
        self.gridLayout.addWidget(self.cb9, 5, 0, 1, 1)
        self.cb10 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb10.setObjectName("cb10")
        self.gridLayout.addWidget(self.cb10, 5, 1, 1, 1)
        self.cb1 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb1.setCheckable(True)
        self.cb1.setChecked(True)
        self.cb1.setTristate(False)
        self.cb1.setObjectName("cb1")
        self.gridLayout.addWidget(self.cb1, 1, 0, 1, 1)
        self.cb2 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb2.setChecked(True)
        self.cb2.setObjectName("cb2")
        self.gridLayout.addWidget(self.cb2, 1, 1, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        spacerItem3 = QtWidgets.QSpacerItem(40, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cb_view_few = QtWidgets.QCheckBox(Form)
        self.cb_view_few.setObjectName("cb_view_few")
        self.horizontalLayout.addWidget(self.cb_view_few)
        self.spinBox_view_few = QtWidgets.QSpinBox(Form)
        self.spinBox_view_few.setEnabled(False)
        self.spinBox_view_few.setObjectName("spinBox_view_few")
        self.horizontalLayout.addWidget(self.spinBox_view_few)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem4 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.comboBox_sort_by = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_sort_by.sizePolicy().hasHeightForWidth())
        self.comboBox_sort_by.setSizePolicy(sizePolicy)
        self.comboBox_sort_by.setObjectName("comboBox_sort_by")
        self.horizontalLayout_2.addWidget(self.comboBox_sort_by)
        self.radioButton_up = QtWidgets.QRadioButton(Form)
        self.radioButton_up.setChecked(True)
        self.radioButton_up.setObjectName("radioButton_up")
        self.horizontalLayout_2.addWidget(self.radioButton_up)
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_2.addWidget(self.radioButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.pushButton_refresh = QtWidgets.QPushButton(Form)
        self.pushButton_refresh.setObjectName("pushButton_refresh")
        self.verticalLayout.addWidget(self.pushButton_refresh)
        spacerItem5 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem5)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        spacerItem6 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem6)
        self.label_7 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.comboBox_chart = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_chart.sizePolicy().hasHeightForWidth())
        self.comboBox_chart.setSizePolicy(sizePolicy)
        self.comboBox_chart.setObjectName("comboBox_chart")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_chart)
        self.label_9 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.comboBox = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_7.addWidget(self.checkBox)
        self.spinBox = QtWidgets.QSpinBox(Form)
        self.spinBox.setEnabled(False)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_7.addWidget(self.spinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.pushButton_chart = QtWidgets.QPushButton(Form)
        self.pushButton_chart.setObjectName("pushButton_chart")
        self.verticalLayout.addWidget(self.pushButton_chart)
        spacerItem7 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem7)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        spacerItem8 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem8)
        self.label_4 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        spacerItem9 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem9)
        self.label_6 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        spacerItem10 = QtWidgets.QSpacerItem(20, 8, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem10)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.comboBox_find_tribe = QtWidgets.QComboBox(Form)
        self.comboBox_find_tribe.setObjectName("comboBox_find_tribe")
        self.horizontalLayout_3.addWidget(self.comboBox_find_tribe)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.pushButton_find_tribe = QtWidgets.QPushButton(Form)
        self.pushButton_find_tribe.setObjectName("pushButton_find_tribe")
        self.verticalLayout.addWidget(self.pushButton_find_tribe)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem11)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<h3>اعددات الجدول</h3>"))
        self.label_2.setText(_translate("Form", "اعمدة الجدول:"))
        self.toolButton.setText(_translate("Form", "?"))
        self.cb16.setText(_translate("Form", "ن +80 سنة"))
        self.cb11.setText(_translate("Form", "ع 40-60 سنة"))
        self.cb13.setText(_translate("Form", "ع 60-80 سنة"))
        self.cb3.setText(_translate("Form", "ع الذكور"))
        self.cb14.setText(_translate("Form", "ن 60-80 سنة"))
        self.cb15.setText(_translate("Form", "ع +80 سنة"))
        self.cb12.setText(_translate("Form", "ن 40-60 سنة"))
        self.cb7.setText(_translate("Form", "ع 00-20 سنة"))
        self.cb6.setText(_translate("Form", "    ن الاناث"))
        self.cb4.setText(_translate("Form", "ع الاناث"))
        self.cb8.setText(_translate("Form", "ن 00-20 سنة"))
        self.cb5.setText(_translate("Form", "    ن الذكور"))
        self.cb9.setText(_translate("Form", "ع 20-40 سنة"))
        self.cb10.setText(_translate("Form", "ن 20-40 سنة"))
        self.cb1.setText(_translate("Form", "ع  الافراد"))
        self.cb2.setText(_translate("Form", "ع  الالقاب"))
        self.cb_view_few.setText(_translate("Form", "اظهر فقط اول النتائح"))
        self.label_3.setText(_translate("Form", "رتب حسب:"))
        self.radioButton_up.setText(_translate("Form", "تصاعدي"))
        self.radioButton_2.setText(_translate("Form", "تنازلي"))
        self.pushButton_refresh.setText(_translate("Form", "تحديث"))
        self.label_7.setText(_translate("Form", "<h3>اعدادت الرسم البياني<h3>"))
        self.label_8.setText(_translate("Form", "النوع:"))
        self.label_9.setText(_translate("Form", "الفواصل:"))
        self.label_10.setText(_translate("Form", "التراتيب:"))
        self.checkBox.setText(_translate("Form", "اظهر فقط اول النتائح"))
        self.pushButton_chart.setText(_translate("Form", "تحديث"))
        self.label_4.setText(_translate("Form", "<h3>بحث </h3>"))
        self.label_6.setText(_translate("Form", "اختر منطقة لرؤية معلومات حولها اكثر "))
        self.label_5.setText(_translate("Form", "المنطقة:"))
        self.pushButton_find_tribe.setText(_translate("Form", "بحث"))



if __name__ == '__main__':
    main()