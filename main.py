"""
Setif's people is a small application that allows to communicate with a data base
built with pandas,PyQt5 and matplotlib
"""

__version__ = '0.2beta'
__author__ = 'khaled bouabdallah'

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
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

    def __init__(self, parent=None, text=arabic):
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
        self.setBaseSize(1280, 800)
        self.setFixedWidth(1280)
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
        self.tools_menu = QMenu(self.texts['tools'], self)
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

    # todo
    def set_statuBar(self):
        self.statusbar = QStatusBar()
        self.statusbar.setLayoutDirection(0)
        self.setStatusBar(self.statusbar)
        # self.statusbar.showMessage("Ready", 3000)
        self.rows_count = QLabel('0')
        self.statusbar.addPermanentWidget(self.rows_count)

    # todo
    def waiting(self):
        pass

    def set_toolbar(self):
        # add the tools toolbar
        self.tools_toolbar = QToolBar()
        self.tools_toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, self.tools_toolbar)
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
        self.tabs.addTab(self.set_people_widget(), self.texts['people'])

        self.tabs.addTab(self.set_families_widget(), self.texts['families'])
        self.tabs.addTab(self.set_regions_widget(), self.texts['regions'])
        self.tabs.addTab(self.set_general_widget(), self.texts['general'])

    def set_actions(self):
        # setting language actions
        self.change_lanugage_arabic_action = QAction(QIcon(':saudi-arabia.png'), self.texts['arabic'], self)
        self.change_lanugage_english_action = QAction(QIcon(':united-kingdom.png'), self.texts['english'], self)
        self.change_lanugage_frensh_action = QAction(QIcon(':france.png'), self.texts['frensh'], self)
        # setting changing dataframe action
        self.change_dataframe_action = QAction(self.texts['file'], self)
        # setting help/about actions
        self.help_action = QAction(self.texts['help'], self)
        self.about_action = QAction(self.texts['about'], self)
        # setting navigation actions
        self.people_action = QAction(self.texts['people'], self)
        self.familiy_action = QAction(self.texts['families'], self)
        self.region_action = QAction(self.texts['regions'], self)
        self.global_action = QAction(self.texts['general'], self)
        # settings tools actions
        self.pdf_action = QAction(self.texts['expo_pdf'], self)
        self.favorite_action = QAction(self.texts['favorite'], self)
        # Using string-based key sequences todo
        pass

    # todo
    def _createContextMenu(self):
        # Setting contextMenuPolicy

        self._centralWididget.setContextMenuPolicy(Qt.ActionsContextMenu)
        # Populating the widget with actions
        pass

    # todo make imporvemnts
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

            self.people_options['fname'] = QLineEdit()
            formlayout.addRow(self.texts['firstname'], self.people_options['fname'])
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
        # layout.setSpacing(100)
        widget.setLayout(layout)
        # adding the table widget
        layout.addWidget(self.people_table_view)
        # adding the options widget
        option_widget = build_options_widget(self)
        # option_widget.setFixedWidth(200)
        layout.addWidget(option_widget)
        # layout.addSpacing(300)
        return widget

    # todo
    def set_families_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = layout.addWidget(QLabel('<h1>families</h1>'))
        widget.setLayout(layout)
        return widget

    # todo
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
                                                  'ن +80 سنة', ]
            self.tribe_option_widget.comboBox_sort_by.addItems(self.tribe_option_widget.sort_list)
            self.tribe_option_widget.spinBox_view_few.setValue(5)
            return w

        # building a table view
        self.tribes_table_view = QTableView()
        self.tribes_table_view.setFixedWidth(900)
        self.tribes_table_view.setFixedHeight(200)

        # stetching the table columns
        # header = self.tribes_table_view.horizontalHeader()
        # header.setSectionResizeMode(QHeaderView.Stretch)
        # building matplotlib canvas
        self.tribe_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar(self.tribe_canvas, self)

        # setting up the widget and the lyout
        widget = QWidget()
        layout = QHBoxLayout()
        self.vlayout = QVBoxLayout()
        widget.setLayout(layout)
        # adding the table widget
        layout.addLayout(self.vlayout)
        layout.addWidget(QVSeperationLine())

        self.vlayout.addWidget(self.tribes_table_view)
        # adding the canvas widget and its tool bar
        self.vlayout.addWidget(self.tribe_canvas)
        self.vlayout.addWidget(self.toolbar)

        # adding the options widget
        layout.addWidget(build_options_widget(self))
        return widget

    # todo
    def set_general_widget(self):
        w = QWidget()
        return w

    # todo
    def change_to_english(self):
        self.setLayoutDirection(0)

    # todo
    def change_to_arabic(self):
        self.setLayoutDirection(1)

    # todo
    def change_to_frensh(self):
        self.setLayoutDirection(0)

    def loqding(self):
        self.movie = QMovie(r'resources\loading.gif')
        self.lab = QLabel('lmao')
        self.lab.setMovie(self.movie)


class Controller(object):

    def __init__(self, view, path):

        self.init_dataframe(path)
        self.init_tribes_df()
        self.view = view
        self.load_people()
        self.load_tribes()
        self.init_tribe_ui()
        self.load_matplotlib_tribe_fig()
        self._connect()

    def init_tribe_ui(self):
        columns = list(self.tribe_dataframe.columns)
        columns = [str(x) for x in columns]
        tribues = self.dataframe['Tribue'].unique()
        charts_types = ['رسم بياني شريطي', 'رسم بياني عمودي', 'رسم بياني خطي', 'رسم بياني دائري']

        self.view.tribe_option_widget.comboBox.addItems(columns)
        self.view.tribe_option_widget.comboBox_2.addItems(columns)
        self.view.tribe_option_widget.comboBox_2.setCurrentText(columns[1])
        self.view.tribe_option_widget.checkBox.setChecked(True)
        self.view.tribe_option_widget.spinBox.setEnabled(True)
        self.view.tribe_option_widget.spinBox.setValue(5)
        self.view.tribe_option_widget.comboBox_chart.addItems(charts_types)
        self.view.tribe_option_widget.comboBox_find_tribe.addItems(tribues)

    def init_dataframe(self, path):

        def fix_gender(gender):
            gender = gender.strip()
            if gender in ['ذ', 'د']:
                return 'ذكر'
            elif gender in ['أ', 'ا']:
                return 'انثى'
            else:
                return 'غير محدد'

        def fix_time(time):
            time = str(time)
            time = time.strip()
            if len(time) == 4:
                return '01/01/' + time
            else:
                return time

        # initiliasing the data base file path
        self.path = path
        # creating a data frame for the file
        df = pd.read_excel(path)
        # preparing the dataframe
        # fixing the 'Sexe' values
        df["Sexe"] = df["Sexe"].apply(fix_gender)
        df["Sexe"] = pd.Categorical(df["Sexe"])
        # changing bithdate to datetime type
        df["Date de naissanace"] = df["Date de naissanace"].apply(fix_time)
        df["Date de naissanace"] = pd.to_datetime(df["Date de naissanace"])
        # removing incorent data
        df.drop(df[df['Date de naissanace'] > '2020'].index, inplace=True)
        # striping the strings 'nom' and 'prenom'
        df['Nom'] = [x.strip() for x in df["Nom"]]
        df['Prénom'] = [x.strip() for x in df["Prénom"]]
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

        ## median age
        median_age = df.groupby('Tribue')['Age'].median()
        median_age.rename('متوسط العمر', inplace=True)

        ## count females and males (another way)

        sexe_count = df.groupby(['Tribue', 'Sexe'], as_index=False, sort=False)['Nom'].count()
        sexe_count = sexe_count.pivot_table('Nom', ['Tribue'], 'Sexe')
        sexe_count.rename(columns={'ذكر': 'ع الذكور', 'انثى': 'ع الاناث'}, inplace=True)

        ## Concatinating the series

        df_tribe = pd.concat(
            [tribe_count, tribe_family_count, sexe_count, age_count00, age_count20, age_count40, age_count60,
             age_count80, median_age], axis='columns', sort=False)

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
               'ن +80 سنة',
               'متوسط العمر',
               ]

        df_tribe = df_tribe[col]

        self.tribe_dataframe = df_tribe

    # build people table view
    def load_people(self):
        renamed = self.rename_dataframe_columns(self.dataframe, self.view.texts['columns_names'])
        pdmodel = PandasModelPeople(renamed)
        self.update_rows_count(pdmodel.rowCount())
        self.view.people_table_view.setModel(pdmodel)

    def load_tribes(self):
        # getting ressources ready
        df = self.tribe_dataframe.copy()
        sort_value = self.view.tribe_option_widget.comboBox_sort_by.currentText()
        if sort_value == 'ابجدي':
            sort_value = 'القبيلة'
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
        cb17 = self.view.tribe_option_widget.cb17.isChecked()

        # sorting the df
        df = df.sort_values(by=sort_value, ascending=sort_settings)

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
        if cb17:
            self.view.tribes_table_view.setColumnHidden(17, False)
        else:
            self.view.tribes_table_view.setColumnHidden(17, True)

    # search for people and build the new table view
    def search_people(self):

        # gettings instance of the data frame
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
            df = df[df['Prénom'] == fname]
        if lname:
            df = df[df['Nom'] == lname]
        if tribe:
            df = df[df['Tribue'] == tribe]
        if year:
            df = df[df['Date de naissanace'].dt.year == int(year)]
        if month:
            df = df[df['Date de naissanace'].dt.month == int(month)]
        if day:
            df = df[df['Date de naissanace'].dt.day == int(day)]
        if gender.currentIndex() == 1:
            df = df[df['Sexe'] == 'ذكر']
        elif gender.currentIndex() == 2:
            df = df[df['Sexe'] == 'انثى']
        # todo implement sorted feature
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
        def barh():
            fig.barh(axe_x, axe_y)

        def bar():
            fig.bar(axe_x, axe_y, )

        def plot():
            fig.plot(axe_x, axe_y)

        def pie():

            df = self.tribe_dataframe
            # if few option is yes
            if select_few:
                df = df.sort_values(by=select_x, ascending=False)
                big = df.head(how_many)
                big = big[select_x]
                small = df[~df.index.isin(big.index)]
                small_sums = pd.Series([small[select_x].sum()], index=["اخرى"])
                big = big.append(small_sums)
                ax_tribe = big.index
                ax_tribe = list([get_display(arabic_reshaper.reshape(x)) for x in ax_tribe])
                fig.pie(big, labels=ax_tribe, autopct='%1.1f%%')
            else:
                axe_x = df[select_x]
                ax_tribe = df.index
                ax_tribe = list([get_display(arabic_reshaper.reshape(x)) for x in ax_tribe])
                fig.pie(axe_x, labels=ax_tribe, autopct='%1.1f%%')

        # removing old figure
        fig = self.view.tribe_canvas.axes
        fig.set_aspect('auto')
        fig.clear()
        fig.cla()
        plt.setp(fig.xaxis.get_majorticklabels(), rotation=45)
        # getting dataframe copy
        df = self.tribe_dataframe.copy()
        # getting user inputs
        select_x = self.view.tribe_option_widget.comboBox.currentText()
        select_chart = self.view.tribe_option_widget.comboBox_chart.currentText()
        select_few = bool(self.view.tribe_option_widget.checkBox.isChecked())
        how_many = self.view.tribe_option_widget.spinBox.value()
        select_y = self.view.tribe_option_widget.comboBox_2.currentText()
        if select_chart != 'رسم بياني دائري':
            # if few option is yes
            if select_few:
                df = df.sort_values(by=[select_y], ascending=False).head(how_many)

        # preparing axis and there lists
        axe_x = df[select_x]
        if select_x == 'القبيلة':
            axe_x = list([get_display(arabic_reshaper.reshape(x)) for x in axe_x])
        axe_y = df[select_y]
        if select_y == 'القبيلة':
            axe_y = list([get_display(arabic_reshaper.reshape(x)) for x in axe_y])

        title = get_display(arabic_reshaper.reshape(select_chart))
        xlbl = get_display(arabic_reshaper.reshape(select_x))
        ylbl = get_display(arabic_reshaper.reshape(select_y))
        fig.set_title(title)

        # drawing the figure
        if select_chart == 'رسم بياني شريطي':
            fig.set_xlabel(ylbl)
            fig.set_ylabel(xlbl)
            barh()
        elif select_chart == 'رسم بياني دائري':
            fig.set_xlabel(xlbl)
            pie()
        elif select_chart == 'رسم بياني عمودي':
            fig.set_xlabel(xlbl)
            fig.set_ylabel(ylbl)
            bar()
        elif select_chart == 'رسم بياني خطي':
            fig.set_xlabel(xlbl)
            fig.set_ylabel(ylbl)
            plot()

        self.view.tribe_canvas.fig.tight_layout()
        self.view.tribe_canvas.draw()

    # return a renamed columns version of a dataframe
    def rename_dataframe_columns(self, df, args):
        columns = df.columns
        renamed = df.rename(columns={columns[0]: args[0], columns[1]: args[1], columns[2]: args[2], columns[3]: args[3],
                                     columns[4]: args[4], columns[5]: args[5], })
        return renamed

    def change_file_action(self):

        # takes 1 or 0 and shows the right dialog
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

                if decision:

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
            btn1.clicked.connect(partial(func, True))
            btn2.clicked.connect(partial(func, False))
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
    def update_rows_count(self, rows):
        string = self.view.texts['found_message'] + ' ' + str(rows) + ' نتائج '
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
        self.view.tribe_option_widget.comboBox_chart.activated.connect(self.change_chart_state)
        self.view.tribe_option_widget.pushButton_find_tribe.clicked.connect(self.show_region_widget)
        pass

    # tribe table many checkbox activated
    def change_button_state(self):
        if self.view.tribe_option_widget.cb_view_few.isChecked():
            self.view.tribe_option_widget.spinBox_view_few.setEnabled(True)
        else:
            self.view.tribe_option_widget.spinBox_view_few.setEnabled(False)

    # tribe chart many checkbox activeted
    def change_button_state2(self):
        if self.view.tribe_option_widget.checkBox.isChecked():
            self.view.tribe_option_widget.spinBox.setEnabled(True)
        else:
            self.view.tribe_option_widget.spinBox.setEnabled(False)

    # tribe chart combobox activated
    def change_chart_state(self):
        columns = list(self.tribe_dataframe.columns)

        self.view.tribe_option_widget.comboBox.clear()
        value = self.view.tribe_option_widget.comboBox_chart.currentText()
        if value == 'رسم بياني دائري':
            columns.remove('القبيلة')
            columns.remove('ن 00-20 سنة')
            columns.remove('ن 20-40 سنة')
            columns.remove('ن 40-60 سنة')
            columns.remove('ن 60-80 سنة')
            columns.remove('ن +80 سنة')
            self.view.tribe_option_widget.comboBox.addItems(columns)
            self.view.tribe_option_widget.comboBox_2.setEnabled(False)
        else:
            self.view.tribe_option_widget.comboBox.addItems(columns)
            self.view.tribe_option_widget.comboBox_2.setEnabled(True)

    def show_region_widget(self):
        region_selected = self.view.tribe_option_widget.comboBox_find_tribe.currentText()
        tribues = self.dataframe['Tribue'].unique()
        if region_selected in tribues:
            self.window = specific_region_widget(region=region_selected, dataframe=self.dataframe,
                                                 region_dataframe=self.tribe_dataframe)
            self.window.show()
        else:
            print("selected region not found")


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

    def __init__(self, path):
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
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        with sns.axes_style("whitegrid"):
            self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


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
    controller = Controller(view, settings[1])
    # show the view
    view.show()
    # exit when app closed
    sys.exit(app.exec())


def load_settings():
    with open('config.json') as json_file:
        data = json.load(json_file)
    if data['language'] == 'arabic':
        text = arabic
    elif data['language'] == 'english':
        pass
    elif data['language'] == 'frensh':
        pass

    file = data['file']

    return text, file


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
        self.cb17 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb17.setObjectName("cb17")
        self.gridLayout.addWidget(self.cb17, 10, 0, 1, 1)
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
        self.comboBox_2 = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setObjectName("comboBox_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_2)
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

        self.comboBox_find_tribe = ExtendedComboBox(Form)
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
        self.cb17.setText(_translate("Form", "متوسط العمر"))
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


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(908, 854)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        Form.setPalette(palette)
        Form.setLayoutDirection(QtCore.Qt.RightToLeft)
        Form.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tableView = QtWidgets.QTableView(Form)
        self.tableView.setMaximumSize(QtCore.QSize(16777215, 150))
        self.tableView.setObjectName("tableView")
        self.verticalLayout_3.addWidget(self.tableView)
        # todo
        self.widget = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar(self.widget, Form)
        self.widget.setObjectName("widget")
        self.verticalLayout_3.addWidget(self.widget)
        self.verticalLayout_3.addWidget(self.toolbar)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_7.addWidget(self.label_3)
        self.toolButton = QtWidgets.QToolButton(Form)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_7.addWidget(self.toolButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 80))
        self.scrollArea.setMaximumSize(QtCore.QSize(16777215, 80))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 415, 196))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.cb6 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb6.setChecked(True)
        self.cb6.setObjectName("cb6")
        self.gridLayout_2.addWidget(self.cb6, 2, 1, 1, 1)
        self.cb4 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb4.setChecked(True)
        self.cb4.setObjectName("cb4")
        self.gridLayout_2.addWidget(self.cb4, 1, 1, 1, 1)
        self.cb10 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb10.setObjectName("cb10")
        self.gridLayout_2.addWidget(self.cb10, 4, 1, 1, 1)
        self.cb9 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb9.setObjectName("cb9")
        self.gridLayout_2.addWidget(self.cb9, 4, 0, 1, 1)
        self.cb2 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(194, 200, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(194, 200, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.cb2.setPalette(palette)
        self.cb2.setChecked(True)
        self.cb2.setObjectName("cb2")
        self.gridLayout_2.addWidget(self.cb2, 0, 1, 1, 1)
        self.cb1 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb1.setChecked(True)
        self.cb1.setObjectName("cb1")
        self.gridLayout_2.addWidget(self.cb1, 0, 0, 1, 1)
        self.cb14 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb14.setObjectName("cb14")
        self.gridLayout_2.addWidget(self.cb14, 6, 1, 1, 1)
        self.cb3 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb3.setChecked(True)
        self.cb3.setObjectName("cb3")
        self.gridLayout_2.addWidget(self.cb3, 1, 0, 1, 1)
        self.cb11 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb11.setChecked(False)
        self.cb11.setObjectName("cb11")
        self.gridLayout_2.addWidget(self.cb11, 5, 0, 1, 1)
        self.cb12 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb12.setObjectName("cb12")
        self.gridLayout_2.addWidget(self.cb12, 5, 1, 1, 1)
        self.cb5 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb5.setChecked(True)
        self.cb5.setObjectName("cb5")
        self.gridLayout_2.addWidget(self.cb5, 2, 0, 1, 1)
        self.cb7 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb7.setObjectName("cb7")
        self.gridLayout_2.addWidget(self.cb7, 3, 0, 1, 1)
        self.cb8 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb8.setObjectName("cb8")
        self.gridLayout_2.addWidget(self.cb8, 3, 1, 1, 1)
        self.cb13 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb13.setObjectName("cb13")
        self.gridLayout_2.addWidget(self.cb13, 6, 0, 1, 1)
        self.cb16 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb16.setObjectName("cb16")
        self.gridLayout_2.addWidget(self.cb16, 7, 1, 1, 1)
        self.cb15 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cb15.setObjectName("cb15")
        self.gridLayout_2.addWidget(self.cb15, 7, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.checkBox_17 = QtWidgets.QCheckBox(Form)
        self.checkBox_17.setObjectName("checkBox_17")
        self.horizontalLayout_9.addWidget(self.checkBox_17)
        self.spinBox = QtWidgets.QSpinBox(Form)
        self.spinBox.setEnabled(False)
        self.spinBox.setProperty("value", 5)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_9.addWidget(self.spinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_25 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_10.addWidget(self.label_25)
        self.comboBox = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_10.addWidget(self.comboBox)
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setChecked(True)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_10.addWidget(self.radioButton_2)
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_10.addWidget(self.radioButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.line_4 = QtWidgets.QFrame(Form)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_2.addWidget(self.line_4)
        self.label_26 = QtWidgets.QLabel(Form)
        self.label_26.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_26.setObjectName("label_26")
        self.verticalLayout_2.addWidget(self.label_26)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_27 = QtWidgets.QLabel(Form)
        self.label_27.setObjectName("label_27")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_27)
        self.label_28 = QtWidgets.QLabel(Form)
        self.label_28.setObjectName("label_28")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_28)
        self.label_29 = QtWidgets.QLabel(Form)
        self.label_29.setObjectName("label_29")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_29)
        self.comboBox_2 = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setObjectName("comboBox_2")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_2)
        self.comboBox_3 = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_3.sizePolicy().hasHeightForWidth())
        self.comboBox_3.setSizePolicy(sizePolicy)
        self.comboBox_3.setObjectName("comboBox_3")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_3)
        self.comboBox_4 = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_4.sizePolicy().hasHeightForWidth())
        self.comboBox_4.setSizePolicy(sizePolicy)
        self.comboBox_4.setObjectName("comboBox_4")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_4)
        self.verticalLayout_2.addLayout(self.formLayout_3)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.checkBox_18 = QtWidgets.QCheckBox(Form)
        self.checkBox_18.setObjectName("checkBox_18")
        self.horizontalLayout_11.addWidget(self.checkBox_18)
        self.spinBox_2 = QtWidgets.QSpinBox(Form)
        self.spinBox_2.setEnabled(False)
        self.spinBox_2.setProperty("value", 5)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_11.addWidget(self.spinBox_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_11)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label_2 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.label_5 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.label_8 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.label_7 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(-1, 30, -1, -1)
        self.formLayout.setVerticalSpacing(50)
        self.formLayout.setObjectName("formLayout")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setObjectName("label_11")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.label_13 = QtWidgets.QLabel(Form)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_13)
        self.label_18 = QtWidgets.QLabel(Form)
        self.label_18.setObjectName("label_18")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_18)
        self.label_17 = QtWidgets.QLabel(Form)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_17)
        self.horizontalLayout_6.addLayout(self.formLayout)
        self.sexe_widget = MplCanvas(self, width=5, height=4, dpi=100)
        self.sexe_widget.setMinimumSize(QtCore.QSize(180, 180))
        self.sexe_widget.setMaximumSize(QtCore.QSize(180, 180))
        self.sexe_widget.setObjectName("sexe_widget")
        self.horizontalLayout_6.addWidget(self.sexe_widget)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_4.addWidget(self.line_3)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setVerticalSpacing(18)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setObjectName("label_12")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.label_14 = QtWidgets.QLabel(Form)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_14)
        self.label_15 = QtWidgets.QLabel(Form)
        self.label_15.setObjectName("label_15")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.label_16 = QtWidgets.QLabel(Form)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_16)
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setObjectName("label_9")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setObjectName("label_10")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.label_19 = QtWidgets.QLabel(Form)
        self.label_19.setObjectName("label_19")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_19)
        self.label_20 = QtWidgets.QLabel(Form)
        self.label_20.setObjectName("label_20")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_20)
        self.label_21 = QtWidgets.QLabel(Form)
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_21)
        self.label_22 = QtWidgets.QLabel(Form)
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName("label_22")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_22)
        self.label_23 = QtWidgets.QLabel(Form)
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.label_23)
        self.label_24 = QtWidgets.QLabel(Form)
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.label_24.setObjectName("label_24")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.label_24)
        self.horizontalLayout_4.addLayout(self.formLayout_2)
        # style = "style_{}.mpstyle".format('fivethirtyeight')
        # with plt.style.context(self.style):
        self.age_widget = MplCanvas(self, width=5, height=4, dpi=100)
        self.age_widget.setMinimumSize(QtCore.QSize(180, 180))
        self.age_widget.setMaximumSize(QtCore.QSize(180, 180))
        self.age_widget.setObjectName("age_widget")
        self.horizontalLayout_4.addWidget(self.age_widget)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form",
                                      "<html><head/><body><p><span style=\" font-size:22pt; font-weight:600;\">سطيف</span></p></body></html>"))
        self.label_4.setText(_translate("Form",
                                        "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">اعدادات الجدول</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "اعمدة الجدول:"))
        self.toolButton.setText(_translate("Form", "?"))
        self.cb6.setText(_translate("Form", "ن الاناث"))
        self.cb4.setText(_translate("Form", "ع الاناث"))
        self.cb10.setText(_translate("Form", "ن 20-40 سنة"))
        self.cb9.setText(_translate("Form", "ع 20-40 سنة"))
        self.cb2.setText(_translate("Form", "متوسط العمر"))
        self.cb1.setText(_translate("Form", "ع الافراد"))
        self.cb14.setText(_translate("Form", "ن 60-80 سنة"))
        self.cb3.setText(_translate("Form", "ع الذكور"))
        self.cb11.setText(_translate("Form", "ع 40-60 سنة"))
        self.cb12.setText(_translate("Form", "ن 40-60 سنة"))
        self.cb5.setText(_translate("Form", "ن الذكور"))
        self.cb7.setText(_translate("Form", "ع 00-20 سنة"))
        self.cb8.setText(_translate("Form", "ن 00-20 سنة"))
        self.cb13.setText(_translate("Form", "ع 60-80 سنة"))
        self.cb16.setText(_translate("Form", "ن +80 سنة"))
        self.cb15.setText(_translate("Form", "ع +80 سنة"))
        self.checkBox_17.setText(_translate("Form", "اظهر فقط اول النتائح"))
        self.label_25.setText(_translate("Form", "رتب حسب:"))
        self.radioButton_2.setText(_translate("Form", "تصاعدي"))
        self.radioButton.setText(_translate("Form", "تنازلي"))
        self.pushButton.setText(_translate("Form", "تحديث"))
        self.label_26.setText(_translate("Form",
                                         "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">اعددات الرسم البياني</span></p></body></html>"))
        self.label_27.setText(_translate("Form", "النوع:"))
        self.label_28.setText(_translate("Form", "الفواصل:"))
        self.label_29.setText(_translate("Form", "التراتيب:"))
        self.checkBox_18.setText(_translate("Form", "اظهر فقط اول النتائح"))
        self.pushButton_2.setText(_translate("Form", "تحديث"))
        self.label_2.setText(_translate("Form", "معلومات عامة:"))
        self.label_6.setText(_translate("Form", "عدد الافراد:"))
        self.label_5.setText(_translate("Form", "TextLabel"))
        self.label_8.setText(_translate("Form", "عدد الالقاب:"))
        self.label_7.setText(_translate("Form", "TextLabel"))
        self.label_11.setText(_translate("Form", "عدد الذكور:"))
        self.label_13.setText(_translate("Form", "TextLabel"))
        self.label_18.setText(_translate("Form", "عدد الاناث:"))
        self.label_17.setText(_translate("Form", "TextLabel"))
        self.label_12.setText(_translate("Form", "من 00 الى 20 سنة:"))
        self.label_14.setText(_translate("Form", "TextLabel"))
        self.label_15.setText(_translate("Form", "من 20 الى 40 سنة:"))
        self.label_16.setText(_translate("Form", "TextLabel"))
        self.label_9.setText(_translate("Form", "من 40 الى 60 سنة:"))
        self.label_10.setText(_translate("Form", "من 60 الى 80 سنة:"))
        self.label_19.setText(_translate("Form", "اكبر من 80 سنة:"))
        self.label_20.setText(_translate("Form", "متوسط العمر:"))
        self.label_21.setText(_translate("Form", "TextLabel"))
        self.label_22.setText(_translate("Form", "TextLabel"))
        self.label_23.setText(_translate("Form", "TextLabel"))
        self.label_24.setText(_translate("Form", "TextLabel"))


class specific_region_widget(QWidget):

    def __init__(self, parent=None, region=None, dataframe=None, region_dataframe=None):
        super().__init__(parent=parent)
        # getting region name
        self.region_name = region
        # getting the specific region df
        region_groupby = dataframe.groupby(['Tribue'])
        self.dataframe = region_groupby.get_group(self.region_name)
        # getting region general info
        self.info = region_dataframe[region_dataframe['القبيلة'] == self.region_name]
        # getting the families dataframe
        self.init_df()
        # updating the gui
        self.init_ui()
        # connecting signals
        self.connect()
        self.load_families()
        self.load_matplotlib_fig()

    def init_df(self):
        x = self.dataframe.copy()
        ### people count
        people_count = x['Nom'].value_counts()
        people_count.rename('ع الافراد', inplace=True)
        ### Families sexe count
        sexe_count = x.groupby(['Nom', 'Sexe'], as_index=False, sort=False)['Prénom'].count()
        sexe_count = pd.pivot_table(sexe_count, index=['Nom'],
                                    columns=['Sexe'], aggfunc=np.sum)
        sexe_count.rename(columns={'ذكر': 'ع الذكور', 'انثى': 'ع الاناث'}, inplace=True)
        sexe_count.columns = sexe_count.columns.droplevel()

        ## adding age
        def yearsago(years, from_date=None):
            if from_date is None:
                from_date = datetime.datetime.now()
            return from_date - relativedelta(years=years)

        df = self.dataframe.copy()
        df['Age'] = [yearsago(x).year for x in df['Date de naissanace'].dt.year]
        ## number of people 0-20 years old in each group
        age = df[df['Age'] < 20]
        age_count = age.groupby(['Nom'])["Nom"].count()
        age_count00 = age_count.rename('ع 00-20 سنة')
        ## number of people 20-40 years old in each group
        age = df[(df['Age'] < 40) & (df['Age'] >= 20)]
        age_count = age.groupby(['Nom'])["Prénom"].count()
        age_count20 = age_count.rename('ع 20-40 سنة')
        ## number of people 40-60 years old in each group
        age = df[(df['Age'] < 60) & (df['Age'] >= 40)]
        age_count = age.groupby(['Nom'])["Prénom"].count()
        age_count40 = age_count.rename('ع 40-60 سنة')
        ## number of people 60-80 years old in each group
        age = df[(df['Age'] < 80) & (df['Age'] >= 60)]
        age_count = age.groupby(['Nom'])["Prénom"].count()
        age_count60 = age_count.rename('ع 60-80 سنة')
        ## number of people +80 years old in each group
        age = df[80 <= df['Age']]
        age_count = age.groupby(['Nom'])["Prénom"].count()
        age_count80 = age_count.rename('ع +80 سنة')
        ## median age
        median_age = df.groupby('Nom')['Age'].median()
        median_age.rename('متوسط العمر', inplace=True)
        ##Concatinating
        family_df = pd.concat([people_count, sexe_count, age_count00, age_count20,
                               age_count40, age_count60, age_count80, median_age], axis='columns', sort=False)
        ## sexe percentage
        family_df['ن الذكور'] = family_df['ع الذكور'] / family_df['ع الافراد']
        family_df['ن الاناث'] = family_df['ع الاناث'] / family_df['ع الافراد']
        family_df['ن الذكور'] = [round(x, 2) for x in family_df['ن الذكور']]
        family_df['ن الاناث'] = [round(x, 2) for x in family_df['ن الاناث']]

        ## fix age counts
        def fix_count(x):
            if math.isnan(x):
                return 0
            else:
                return x

        family_df['ع 00-20 سنة'] = family_df['ع 00-20 سنة'].apply(fix_count)
        family_df['ع 20-40 سنة'] = family_df['ع 20-40 سنة'].apply(fix_count)
        family_df['ع 40-60 سنة'] = family_df['ع 40-60 سنة'].apply(fix_count)
        family_df['ع 60-80 سنة'] = family_df['ع 60-80 سنة'].apply(fix_count)
        family_df['ع +80 سنة'] = family_df['ع +80 سنة'].apply(fix_count)
        ## age percentages
        family_df['ن 00-20 سنة'] = family_df['ع 00-20 سنة'] / family_df['ع الافراد']
        family_df['ن 20-40 سنة'] = family_df['ع 20-40 سنة'] / family_df['ع الافراد']
        family_df['ن 40-60 سنة'] = family_df['ع 40-60 سنة'] / family_df['ع الافراد']
        family_df['ن 60-80 سنة'] = family_df['ع 60-80 سنة'] / family_df['ع الافراد']
        family_df['ن +80 سنة'] = family_df['ع +80 سنة'] / family_df['ع الافراد']
        family_df['ن 00-20 سنة'] = [round(x, 2) for x in family_df['ن 00-20 سنة']]
        family_df['ن 20-40 سنة'] = [round(x, 2) for x in family_df['ن 20-40 سنة']]
        family_df['ن 40-60 سنة'] = [round(x, 2) for x in family_df['ن 40-60 سنة']]
        family_df['ن 60-80 سنة'] = [round(x, 2) for x in family_df['ن 60-80 سنة']]
        family_df['ن +80 سنة'] = [round(x, 2) for x in family_df['ن +80 سنة']]
        ### adding index as a column
        family_df['اللقب'] = family_df.index
        ### fixing columns order
        col = ['اللقب',
               'ع الافراد',
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
               'ن +80 سنة',
               'متوسط العمر', ]
        self.family_df = family_df[col]

    def connect(self):
        # self.view.tribe_option_widget.cb_view_few.stateChanged.connect(self.change_button_state)
        self.ui.pushButton.clicked.connect(self.load_families)
        self.ui.checkBox_17.stateChanged.connect(
            partial(self.many_checkboxTriggred, self.ui.checkBox_17, self.ui.spinBox))
        self.ui.checkBox_18.stateChanged.connect(
            partial(self.many_checkboxTriggred, self.ui.checkBox_18, self.ui.spinBox_2))
        self.ui.comboBox_2.activated.connect(self.change_chart_state)
        self.ui.pushButton_2.clicked.connect(self.load_matplotlib_fig)

    def load_matplotlib_fig(self):
        def barh():
            fig.barh(axe_x, axe_y)

        def scatter():
            fig.scatter(axe_x, axe_y, )

        def bar():
            fig.bar(axe_x, axe_y, )

        def plot():
            fig.plot(axe_x, axe_y)

        def pie():

            df = self.family_df
            # if few option is yes
            if select_few:
                df = df.sort_values(by=select_x, ascending=False)
                big = df.head(how_many)
                big = big[select_x]
                small = df[~df.index.isin(big.index)]
                small_sums = pd.Series([small[select_x].sum()], index=["اخرى"])
                big = big.append(small_sums)
                ax_tribe = big.index
                ax_tribe = list([get_display(arabic_reshaper.reshape(x)) for x in ax_tribe])
                fig.pie(big, labels=ax_tribe, autopct='%1.1f%%')
            else:
                axe_x = df[select_x]
                ax_tribe = df.index
                ax_tribe = list([get_display(arabic_reshaper.reshape(x)) for x in ax_tribe])
                fig.pie(axe_x, labels=ax_tribe, autopct='%1.1f%%')

        # removing old figure

        fig = self.ui.widget.axes
        fig.set_aspect('auto')
        fig.clear()
        fig.cla()
        plt.setp(fig.xaxis.get_majorticklabels(), rotation=45)
        # getting dataframe copy
        df = self.family_df.copy()
        # getting user inputs
        select_x = self.ui.comboBox_3.currentText()
        select_chart = self.ui.comboBox_2.currentText()
        select_few = bool(self.ui.checkBox_18.isChecked())
        how_many = self.ui.spinBox_2.value()
        select_y = self.ui.comboBox_4.currentText()
        if select_chart != 'رسم بياني دائري':
            # if few option is yes
            if select_few:
                df = df.sort_values(by=[select_y], ascending=False).head(how_many)

        # preparing axis and there lists
        axe_x = df[select_x]
        if select_x == 'اللقب':
            axe_x = list([get_display(arabic_reshaper.reshape(x)) for x in axe_x])
        axe_y = df[select_y]
        if select_y == 'اللقب':
            axe_y = list([get_display(arabic_reshaper.reshape(x)) for x in axe_y])

        title = get_display(arabic_reshaper.reshape(select_chart))
        xlbl = get_display(arabic_reshaper.reshape(select_x))
        ylbl = get_display(arabic_reshaper.reshape(select_y))
        fig.set_title(title)
        # drawing the figure
        if select_chart == 'رسم بياني شريطي':
            fig.set_xlabel(ylbl)
            fig.set_ylabel(xlbl)
            barh()
        elif select_chart == 'رسم بياني دائري':
            fig.set_xlabel(xlbl)
            pie()
        elif select_chart == 'رسم بياني عمودي':
            fig.set_xlabel(xlbl)
            fig.set_ylabel(ylbl)
            bar()
        elif select_chart == 'رسم بياني خطي':
            fig.set_xlabel(xlbl)
            fig.set_ylabel(ylbl)
            plot()
        elif select_chart == 'رسم بياني لنقاط المبعثرة':
            fig.set_xlabel(xlbl)
            fig.set_ylabel(ylbl)
            scatter()

        self.ui.widget.fig.tight_layout()
        self.ui.widget.draw()

    def load_families(self):
        # getting ressources ready
        df = self.family_df.copy()
        sort_value = self.ui.comboBox.currentText()
        if sort_value == 'ابجدي':
            sort_value = 'اللقب'
        sort_settings = bool(self.ui.radioButton_2.isChecked())
        first_only = bool(self.ui.checkBox_17.isChecked())
        how_mutch = self.ui.spinBox.value()
        cb1 = self.ui.cb1.isChecked()
        cb2 = self.ui.cb2.isChecked()
        cb3 = self.ui.cb3.isChecked()
        cb4 = self.ui.cb4.isChecked()
        cb5 = self.ui.cb5.isChecked()
        cb6 = self.ui.cb6.isChecked()
        cb7 = self.ui.cb7.isChecked()
        cb8 = self.ui.cb8.isChecked()
        cb9 = self.ui.cb9.isChecked()
        cb10 = self.ui.cb10.isChecked()
        cb11 = self.ui.cb11.isChecked()
        cb12 = self.ui.cb12.isChecked()
        cb13 = self.ui.cb13.isChecked()
        cb14 = self.ui.cb14.isChecked()
        cb15 = self.ui.cb15.isChecked()
        cb16 = self.ui.cb16.isChecked()
        # sorting the df
        df = df.sort_values(by=sort_value, ascending=sort_settings)
        # getting only first results
        if first_only:
            df = df.head(how_mutch)
        # buildig the table model
        pdmodel = PandasModelTribes(df)
        # drawing the tribes table
        self.ui.tableView.setModel(pdmodel)
        # showing only columns that we want
        if cb1:
            self.ui.tableView.setColumnHidden(1, False)
        else:
            self.ui.tableView.setColumnHidden(1, True)
        if cb2:
            self.ui.tableView.setColumnHidden(16, False)
        else:
            self.ui.tableView.setColumnHidden(16, True)
        if cb3:
            self.ui.tableView.setColumnHidden(2, False)
        else:
            self.ui.tableView.setColumnHidden(2, True)
        if cb4:
            self.ui.tableView.setColumnHidden(3, False)
        else:
            self.ui.tableView.setColumnHidden(3, True)
        if cb5:
            self.ui.tableView.setColumnHidden(4, False)
        else:
            self.ui.tableView.setColumnHidden(4, True)
        if cb6:
            self.ui.tableView.setColumnHidden(5, False)
        else:
            self.ui.tableView.setColumnHidden(5, True)
        if cb7:
            self.ui.tableView.setColumnHidden(6, False)
        else:
            self.ui.tableView.setColumnHidden(6, True)
        if cb8:
            self.ui.tableView.setColumnHidden(7, False)
        else:
            self.ui.tableView.setColumnHidden(7, True)
        if cb9:
            self.ui.tableView.setColumnHidden(8, False)
        else:
            self.ui.tableView.setColumnHidden(8, True)
        if cb10:
            self.ui.tableView.setColumnHidden(9, False)
        else:
            self.ui.tableView.setColumnHidden(9, True)
        if cb11:
            self.ui.tableView.setColumnHidden(10, False)
        else:
            self.ui.tableView.setColumnHidden(10, True)
        if cb12:
            self.ui.tableView.setColumnHidden(11, False)
        else:
            self.ui.tableView.setColumnHidden(11, True)
        if cb13:
            self.ui.tableView.setColumnHidden(12, False)
        else:
            self.ui.tableView.setColumnHidden(12, True)
        if cb14:
            self.ui.tableView.setColumnHidden(13, False)
        else:
            self.ui.tableView.setColumnHidden(13, True)
        if cb15:
            self.ui.tableView.setColumnHidden(14, False)
        else:
            self.ui.tableView.setColumnHidden(14, True)
        if cb16:
            self.ui.tableView.setColumnHidden(15, False)
        else:
            self.ui.tableView.setColumnHidden(15, True)

    def many_checkboxTriggred(self, checkBox, spinBox):
        if checkBox.isChecked():
            spinBox.setEnabled(True)
        else:
            spinBox.setEnabled(False)

    def change_chart_state(self):
        print(0)
        columns = list(self.family_df)
        self.ui.comboBox_3.clear()
        value = self.ui.comboBox_2.currentText()
        if value == 'رسم بياني دائري':
            print(2)
            columns.remove('اللقب')
            columns.remove('ن 00-20 سنة')
            columns.remove('ن 20-40 سنة')
            columns.remove('ن 40-60 سنة')
            columns.remove('ن 60-80 سنة')
            columns.remove('ن +80 سنة')
            self.ui.comboBox_3.addItems(columns)
            self.ui.comboBox_4.setEnabled(False)
        else:
            self.ui.comboBox_3.addItems(columns)
            self.ui.comboBox_4.setEnabled(True)

    def init_ui(self):
        columns = self.family_df.columns
        charts_types = ['رسم بياني شريطي', 'رسم بياني عمودي', 'رسم بياني خطي', 'رسم بياني دائري']

        # initlisazing the ui
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # updating
        self.setWindowTitle(self.region_name)
        self.ui.tableView.setMinimumHeight(200)
        # setting the region info
        self.ui.label.setText('<h1>' + self.region_name + '<\\h1>')
        self.ui.label_13.setText(str(self.info['ع الذكور'][0]))
        self.ui.label_17.setText(str(self.info['ع الاناث'][0]))
        self.ui.label_5.setText(str(self.info['ع الافراد'][0]))
        self.ui.label_7.setText(str(self.info['ع الالقاب'][0]))
        self.ui.label_14.setText(str(int(self.info['ع 00-20 سنة'][0])))
        self.ui.label_16.setText(str(int(self.info['ع 20-40 سنة'][0])))
        self.ui.label_21.setText(str(int(self.info['ع 40-60 سنة'][0])))
        self.ui.label_22.setText(str(int(self.info['ع 60-80 سنة'][0])))
        self.ui.label_23.setText(str(int(self.info['ع +80 سنة'][0])))
        self.ui.label_24.setText(str(int(self.info['متوسط العمر'][0])))
        # initlizaing the widgets
        self.ui.comboBox.addItems(columns)
        self.ui.comboBox_3.addItems(columns)
        self.ui.comboBox_4.addItems(columns)
        self.ui.comboBox_2.addItems(charts_types)
        self.ui.comboBox_4.setCurrentText(columns[1])
        self.ui.checkBox_18.setChecked(True)
        self.ui.spinBox_2.setEnabled(True)
        self.ui.spinBox_2.setValue(5)
        # setting the pies
        self.build_pies()

    def build_pies(self):
        sexe_list = [self.info['ع الذكور'][0], self.info['ع الاناث'][0]]
        sexe_labels = [get_display(arabic_reshaper.reshape('ذكور')),
                  get_display(arabic_reshaper.reshape('اناث'))]

        df_1 = pd.DataFrame(list(zip(sexe_labels, sexe_list)),
                          columns=['name', 'val'])
        df_1 = df_1[df_1['val'] != 0]

        self.ui.sexe_widget.axes.pie(df_1['val'], labels=df_1['name'], autopct='%1.1f%%')



        age_list = [self.info['ع 00-20 سنة'][0],
                    self.info['ع 20-40 سنة'][0],
                    self.info['ع 40-60 سنة'][0],
                    self.info['ع 60-80 سنة'][0],
                    self.info['ع +80 سنة'][0]
                    ]
        age_labels = [get_display(arabic_reshaper.reshape('20-00')),
                      get_display(arabic_reshaper.reshape('40-20')),
                      get_display(arabic_reshaper.reshape('60-40')),
                      get_display(arabic_reshaper.reshape('80-60')),
                      get_display(arabic_reshaper.reshape('80+')),
                      ]
        df = pd.DataFrame(list(zip(age_labels, age_list)),
                          columns=['name', 'val'])
        df = df[df['val'] != 0]
        self.ui.age_widget.axes.pie(df['val'], labels=df['name'], autopct='%1.1f%%')


if __name__ == '__main__':
    main()
