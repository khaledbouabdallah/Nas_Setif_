"""
Setif's people is a small application that allows to communicate with a data base
built with pandas,PyQt5 and matplotlib
"""

__version__ = '0.3beta'
__author__ = 'khaled bouabdallah'

import matplotlib.pyplot as plt
from loading_widget import starting_screen
import numpy as np
import matplotlib
from ui import family_widget_ui,Ui_Form,QVSeperationLine,Tribe_tools_widget_ui,MplCanvas
matplotlib.use('Qt5Agg')
from family_tree import Family
from matplotlib.backends.backend_qt5agg import  NavigationToolbar2QT as NavigationToolbar

import math
import sys
import json
from dateutil.relativedelta import relativedelta
from text_strings import arabic
from PyQt5.QtCore import QObject, QThread, pyqtSignal,  QRegExp
import pandas as pd
import datetime
from functools import partial
from PyQt5.QtCore import QAbstractTableModel, Qt
import arabic_reshaper
from bidi.algorithm import get_display
import tempfile
# get access to the  resources
import qrc_resources

from PyQt5.QtGui import QIcon, QMovie, QRegExpValidator


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
    QFileDialog,  QHeaderView
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
        self.tabs.addTab(self.set_families_widget(), 'العائلات')
        self.tabs.addTab(self.set_names_widget(), 'الالقاب')
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

    def set_families_widget(self):
        w = QWidget()
        self.family_widget = family_widget_ui()
        self.family_widget.setupUi(w)
        return w

    # todo
    def set_names_widget(self):
        def build_options_widget(self):
            self.family_option_widget = Tribe_tools_widget_ui()
            w = QWidget()
            self.family_option_widget.setupUi(w)
            self.family_option_widget.sort_list = ['ابجدي',
                                                   'ع الافراد',
                                                   'ع المناطق',
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
            self.family_option_widget.comboBox_sort_by.addItems(self.family_option_widget.sort_list)
            self.family_option_widget.spinBox_view_few.setValue(5)
            return w

        # building a table view
        self.familes_table_view = QTableView()
        self.familes_table_view.setFixedWidth(900)
        self.familes_table_view.setFixedHeight(200)

        # building matplotlib canvas
        self.family_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar(self.family_canvas, self)

        # setting up the widget and the lyout
        widget = QWidget()
        layout = QHBoxLayout()
        self.vlayout_family = QVBoxLayout()
        widget.setLayout(layout)
        # adding the table widget
        layout.addLayout(self.vlayout_family)
        layout.addWidget(QVSeperationLine())

        self.vlayout_family.addWidget(self.familes_table_view)
        # adding the canvas widget and its tool bar
        self.vlayout_family.addWidget(self.family_canvas)
        self.vlayout_family.addWidget(self.toolbar)

        # adding the options widget
        layout.addWidget(build_options_widget(self))
        return widget

    # todo
    def set_regions_widget(self):
        def build_options_widget(self):
            self.tribe_option_widget = Tribe_tools_widget_ui()
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
        self.init_families_df()
        self.view = view
        self.load_people()
        self.load_tribes()
        self.load_familes()
        self.init_tribe_ui()
        self.init_family_ui()
        self.update_family_widget()
        self.search_family()
        self.load_matplotlib_tribe_fig()
        self.load_matplotlib_family_fig()
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

    def init_family_ui(self):
        columns = list(self.family_dataframe.columns)
        columns = [str(x) for x in columns]
        tribues = self.dataframe['Nom'].unique()
        charts_types = ['رسم بياني شريطي', 'رسم بياني عمودي', 'رسم بياني خطي', 'رسم بياني دائري']

        self.view.family_option_widget.comboBox.addItems(columns)
        self.view.family_option_widget.comboBox_2.addItems(columns)
        self.view.family_option_widget.comboBox_2.setCurrentText(columns[1])
        self.view.family_option_widget.checkBox.setChecked(True)
        self.view.family_option_widget.spinBox.setEnabled(True)
        self.view.family_option_widget.spinBox.setValue(5)
        self.view.family_option_widget.comboBox_chart.addItems(charts_types)
        self.view.family_option_widget.comboBox_find_tribe.addItems(tribues)
        self.view.family_option_widget.cb2.setText('ع المناطق')

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

        def yearsago(years, from_date=None):
            if from_date is None:
                from_date = datetime.datetime.now()
            return from_date - relativedelta(years=years)

        df['Age'] = [yearsago(x).year for x in df['Date de naissanace'].dt.year]
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

    def init_families_df(self):

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
        count_by = 'Prénom'
        group_by = 'Nom'
        familes_groups = df.groupby([group_by])

        ## number of  people in each tribe

        tribe_count = df[group_by].value_counts()
        tribe_count = tribe_count.rename('ع الافراد')

        ### number of regions in each family

        tribe_family_count = familes_groups['Tribue'].nunique()
        tribe_family_count = tribe_family_count.rename('ع المناطق')

        ## number of people 0-20 years old in each group

        age = df[df['Age'] < 20]
        age_count = age.groupby([group_by])[count_by].count()
        age_count00 = age_count.rename('ع 00-20 سنة')

        ## number of people 20-40 years old in each group

        age = df[(df['Age'] < 40) & (df['Age'] >= 20)]
        age_count = age.groupby([group_by])[count_by].count()
        age_count20 = age_count.rename('ع 20-40 سنة')

        ## number of people 40-60 years old in each group

        age = df[(df['Age'] < 60) & (df['Age'] >= 40)]
        age_count = age.groupby([group_by])[count_by].count()
        age_count40 = age_count.rename('ع 40-60 سنة')

        ## number of people 60-80 years old in each group

        age = df[(df['Age'] < 80) & (df['Age'] >= 60)]
        age_count = age.groupby([group_by])[count_by].count()
        age_count60 = age_count.rename('ع 60-80 سنة')

        ## number of people +80 years old in each group

        age = df[80 <= df['Age']]
        age_count = age.groupby([group_by])[count_by].count()
        age_count80 = age_count.rename('ع +80 سنة')

        ## median age
        median_age = df.groupby(group_by)['Age'].median()
        median_age.rename('متوسط العمر', inplace=True)

        ## count females and males (another way)

        sexe_count = df.groupby([group_by, 'Sexe'], as_index=False, sort=False)[count_by].count()
        sexe_count = sexe_count.pivot_table(count_by, [group_by], 'Sexe')
        sexe_count.rename(columns={'ذكر': 'ع الذكور', 'انثى': 'ع الاناث'}, inplace=True)

        ## Concatinating the series

        df_family = pd.concat(
            [tribe_count, tribe_family_count, sexe_count, age_count00, age_count20, age_count40, age_count60,
             age_count80, median_age], axis='columns', sort=False)

        ## Sexe percentege by each group

        df_family['ن الذكور'] = df_family['ع الذكور'] / df_family['ع الافراد']
        df_family['ن الاناث'] = df_family['ع الاناث'] / df_family['ع الافراد']
        df_family['ن الذكور'] = [round(x, 2) for x in df_family['ن الذكور']]
        df_family['ن الاناث'] = [round(x, 2) for x in df_family['ن الاناث']]

        ## adding age columns

        ## cleaning age columns

        df_family['ع 00-20 سنة'] = df_family['ع 00-20 سنة'].apply(fix_count)
        df_family['ع 20-40 سنة'] = df_family['ع 20-40 سنة'].apply(fix_count)
        df_family['ع 40-60 سنة'] = df_family['ع 40-60 سنة'].apply(fix_count)
        df_family['ع 60-80 سنة'] = df_family['ع 60-80 سنة'].apply(fix_count)
        df_family['ع +80 سنة'] = df_family['ع +80 سنة'].apply(fix_count)

        ### adding percentage age columns

        df_family['ن 00-20 سنة'] = df_family['ع 00-20 سنة'] / df_family['ع الافراد']
        df_family['ن 20-40 سنة'] = df_family['ع 20-40 سنة'] / df_family['ع الافراد']
        df_family['ن 40-60 سنة'] = df_family['ع 40-60 سنة'] / df_family['ع الافراد']
        df_family['ن 60-80 سنة'] = df_family['ع 60-80 سنة'] / df_family['ع الافراد']
        df_family['ن +80 سنة'] = df_family['ع +80 سنة'] / df_family['ع الافراد']

        df_family['ن 00-20 سنة'] = [round(x, 2) for x in df_family['ن 00-20 سنة']]
        df_family['ن 20-40 سنة'] = [round(x, 2) for x in df_family['ن 20-40 سنة']]
        df_family['ن 40-60 سنة'] = [round(x, 2) for x in df_family['ن 40-60 سنة']]
        df_family['ن 60-80 سنة'] = [round(x, 2) for x in df_family['ن 60-80 سنة']]
        df_family['ن +80 سنة'] = [round(x, 2) for x in df_family['ن +80 سنة']]

        ### adding index as a column

        df_family['اللقب'] = df_family.index

        ### fixing columns order

        col = ['اللقب',
               'ع الافراد',
               'ع المناطق',
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

        df_family = df_family[col]

        self.family_dataframe = df_family

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

    def load_familes(self):
        # getting ressources ready
        df = self.family_dataframe.copy()
        sort_value = self.view.family_option_widget.comboBox_sort_by.currentText()
        if sort_value == 'ابجدي':
            sort_value = 'اللقب'
        sort_settings = bool(self.view.family_option_widget.radioButton_up.isChecked())
        first_only = bool(self.view.family_option_widget.cb_view_few.isChecked())
        how_mutch = self.view.family_option_widget.spinBox_view_few.value()
        cb1 = self.view.family_option_widget.cb1.isChecked()
        cb2 = self.view.family_option_widget.cb2.isChecked()
        cb3 = self.view.family_option_widget.cb3.isChecked()
        cb4 = self.view.family_option_widget.cb4.isChecked()
        cb5 = self.view.family_option_widget.cb5.isChecked()
        cb6 = self.view.family_option_widget.cb6.isChecked()
        cb7 = self.view.family_option_widget.cb7.isChecked()
        cb8 = self.view.family_option_widget.cb8.isChecked()
        cb9 = self.view.family_option_widget.cb9.isChecked()
        cb10 = self.view.family_option_widget.cb10.isChecked()
        cb11 = self.view.family_option_widget.cb11.isChecked()
        cb12 = self.view.family_option_widget.cb12.isChecked()
        cb13 = self.view.family_option_widget.cb13.isChecked()
        cb14 = self.view.family_option_widget.cb14.isChecked()
        cb15 = self.view.family_option_widget.cb15.isChecked()
        cb16 = self.view.family_option_widget.cb16.isChecked()
        cb17 = self.view.family_option_widget.cb17.isChecked()

        # sorting the df
        df = df.sort_values(by=sort_value, ascending=sort_settings)

        # getting only first results
        if first_only:
            df = df.head(how_mutch)

        pdmodel = PandasModelTribes(df)

        # drawing the tribes table
        self.view.familes_table_view.setModel(pdmodel)
        # showing only columns that we want
        if cb1:
            self.view.familes_table_view.setColumnHidden(1, False)
        else:
            self.view.familes_table_view.setColumnHidden(1, True)
        if cb2:
            self.view.familes_table_view.setColumnHidden(2, False)
        else:
            self.view.familes_table_view.setColumnHidden(2, True)
        if cb3:
            self.view.familes_table_view.setColumnHidden(3, False)
        else:
            self.view.familes_table_view.setColumnHidden(3, True)
        if cb4:
            self.view.familes_table_view.setColumnHidden(4, False)
        else:
            self.view.familes_table_view.setColumnHidden(4, True)
        if cb5:
            self.view.familes_table_view.setColumnHidden(5, False)
        else:
            self.view.familes_table_view.setColumnHidden(5, True)
        if cb6:
            self.view.familes_table_view.setColumnHidden(6, False)
        else:
            self.view.familes_table_view.setColumnHidden(6, True)
        if cb7:
            self.view.familes_table_view.setColumnHidden(7, False)
        else:
            self.view.familes_table_view.setColumnHidden(7, True)
        if cb8:
            self.view.familes_table_view.setColumnHidden(12, False)
        else:
            self.view.familes_table_view.setColumnHidden(12, True)
        if cb9:
            self.view.familes_table_view.setColumnHidden(8, False)
        else:
            self.view.familes_table_view.setColumnHidden(8, True)
        if cb10:
            self.view.familes_table_view.setColumnHidden(13, False)
        else:
            self.view.familes_table_view.setColumnHidden(13, True)
        if cb11:
            self.view.familes_table_view.setColumnHidden(9, False)
        else:
            self.view.familes_table_view.setColumnHidden(9, True)
        if cb12:
            self.view.familes_table_view.setColumnHidden(14, False)
        else:
            self.view.familes_table_view.setColumnHidden(14, True)
        if cb13:
            self.view.familes_table_view.setColumnHidden(10, False)
        else:
            self.view.familes_table_view.setColumnHidden(10, True)
        if cb14:
            self.view.familes_table_view.setColumnHidden(15, False)
        else:
            self.view.familes_table_view.setColumnHidden(15, True)
        if cb15:
            self.view.familes_table_view.setColumnHidden(11, False)
        else:
            self.view.familes_table_view.setColumnHidden(11, True)
        if cb16:
            self.view.familes_table_view.setColumnHidden(16, False)
        else:
            self.view.familes_table_view.setColumnHidden(16, True)
        if cb17:
            self.view.familes_table_view.setColumnHidden(17, False)
        else:
            self.view.familes_table_view.setColumnHidden(17, True)

    def search_family(self):
        family_selected = self.view.family_widget.comboBox.currentText()
        region_selected = self.view.family_widget.comboBox_2.currentText()
        famlies = self.dataframe['Nom'].unique()
        df = self.dataframe[self.dataframe['Nom'] == family_selected]
        regions = df['Tribue'].unique()
        if family_selected not in famlies or region_selected not in regions:
            print('region or family wrong !')
        else:
            self.load_family(family_selected,region_selected)

    def update_family_widget(self):
        famlies = self.dataframe['Nom'].unique()
        famlies = list(famlies)
        famlies.sort()
        self.view.family_widget.comboBox.addItems(famlies)
        family = self.view.family_widget.comboBox.currentText()
        df = self.dataframe[self.dataframe['Nom'] == family]
        regions = df['Tribue'].unique()
        regions = list(regions)
        regions.sort()
        self.view.family_widget.comboBox_2.addItems(regions)
        header = self.view.family_widget.tableView.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

    def load_family(self,family,region):

        def make_pies(self,sexe_list,age_list):

            fig = self.view.family_widget.widget.axes
            fig.set_aspect('auto')
            fig.clear()
            fig.cla()

            fig1 = self.view.family_widget.widget_2.axes
            fig1.set_aspect('auto')
            fig1.clear()
            fig1.cla()


            sexe_labels = [get_display(arabic_reshaper.reshape('ذكور')),
                           get_display(arabic_reshaper.reshape('اناث'))]

            df_1 = pd.DataFrame(list(zip(sexe_labels, sexe_list)),
                                columns=['name', 'val'])
            df_1 = df_1[df_1['val'] != 0]

            self.view.family_widget.widget.axes.pie(df_1['val'], labels=df_1['name'], autopct='%1.1f%%')



            age_labels = [get_display(arabic_reshaper.reshape('20-00')),
                          get_display(arabic_reshaper.reshape('40-20')),
                          get_display(arabic_reshaper.reshape('60-40')),
                          get_display(arabic_reshaper.reshape('80-60')),
                          get_display(arabic_reshaper.reshape('80+')),
                          ]
            df = pd.DataFrame(list(zip(age_labels, age_list)),
                              columns=['name', 'val'])
            df = df[df['val'] != 0]
            self.view.family_widget.widget_2.axes.pie(df['val'], labels=df['name'], autopct='%1.1f%%')

            self.view.family_widget.widget.fig.tight_layout()
            self.view.family_widget.widget.draw()

            self.view.family_widget.widget_2.fig.tight_layout()
            self.view.family_widget.widget_2.draw()

        family_df = self.dataframe.copy()
        family_df = family_df[family_df['Nom']==family]
        family_df = family_df[family_df['Tribue']==region]
        self.view.family_widget.label_4.setText('<h2>'+family+'--'+region+'</h2>')

        people_count = family_df.shape[0]
        male_count = family_df[family_df['Sexe'] == 'ذكر'].shape[0]
        female_count = family_df[family_df['Sexe'] == 'انثى'].shape[0]
        age_median = family_df['Age'].median()
        age00 = family_df[(family_df['Age'] < 20) & (family_df['Age'] >= 0)].shape[0]
        age20 = family_df[(family_df['Age'] < 40) & (family_df['Age'] >= 20)].shape[0]
        age40 = family_df[(family_df['Age'] < 60) & (family_df['Age'] >= 40)].shape[0]
        age60 = family_df[(family_df['Age'] < 80) & (family_df['Age'] >= 60)].shape[0]
        age80 = family_df[family_df['Age'] >= 80].shape[0]

        self.view.family_widget.label_8.setText(str(people_count))
        self.view.family_widget.label_5.setText(str(age_median))
        self.view.family_widget.label_13.setText(str(male_count))
        self.view.family_widget.label_11.setText(str(female_count))
        self.view.family_widget.label_15.setText(str(age00))
        self.view.family_widget.label_17.setText(str(age20))
        self.view.family_widget.label_25.setText(str(age40))
        self.view.family_widget.label_18.setText(str(age60))
        self.view.family_widget.label_24.setText(str(age80))

        renamed = self.rename_dataframe_columns(family_df, self.view.texts['columns_names'])
        pdmodel = PandasModelPeople(renamed)
        self.view.family_widget.tableView.setModel(pdmodel)

        df_for_family = family_df.copy()
        df_for_family['Date de naissanace'] = df_for_family['Date de naissanace'].dt.year
        self.family_dicto =  df_for_family.to_dict(orient='index')

        make_pies(self,[male_count,female_count],[age00,age20,age40,age60,age80])

    def generate_tree(self):



        myfamily = Family()
        myfamily.members.clear()

        myfamily.populate(self.family_dicto.values())
        print(len(myfamily.members))
        myfamily.sort_family(True)

        for member in myfamily.members:
            myfamily.find_father(member)
        myfamily.sort_family(True)
        for member in myfamily.members:
            myfamily.find_father(member)
        print(len(myfamily.members))


        tree = myfamily.build_tree()
        tree.view(tempfile.mktemp('.gv'))

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

    def load_matplotlib_family_fig(self):
        def barh():
            fig.barh(axe_x, axe_y)

        def bar():
            fig.bar(axe_x, axe_y, )

        def plot():
            fig.plot(axe_x, axe_y)

        def pie():

            df = self.family_dataframe
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
        fig = self.view.family_canvas.axes
        fig.set_aspect('auto')
        fig.clear()
        fig.cla()
        plt.setp(fig.xaxis.get_majorticklabels(), rotation=45)
        # getting dataframe copy
        df = self.family_dataframe.copy()
        # getting user inputs
        select_x = self.view.family_option_widget.comboBox.currentText()
        select_chart = self.view.family_option_widget.comboBox_chart.currentText()
        select_few = bool(self.view.family_option_widget.checkBox.isChecked())
        how_many = self.view.family_option_widget.spinBox.value()
        select_y = self.view.family_option_widget.comboBox_2.currentText()
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

        self.view.family_canvas.fig.tight_layout()
        self.view.family_canvas.draw()

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
        # connect the region view widgets
        self.view.tribe_option_widget.cb_view_few.stateChanged.connect(self.change_button_state)
        self.view.tribe_option_widget.pushButton_refresh.clicked.connect(self.load_tribes)
        self.view.tribe_option_widget.checkBox.stateChanged.connect(self.change_button_state2)
        self.view.tribe_option_widget.pushButton_chart.clicked.connect(self.load_matplotlib_tribe_fig)
        self.view.tribe_option_widget.comboBox_chart.activated.connect(self.change_chart_state)
        self.view.tribe_option_widget.pushButton_find_tribe.clicked.connect(self.show_region_widget)
        # connect the family view widgets
        self.view.family_option_widget.cb_view_few.stateChanged.connect(self.change_button_state_family)
        self.view.family_option_widget.pushButton_refresh.clicked.connect(self.load_familes)
        self.view.family_option_widget.checkBox.stateChanged.connect(self.change_button_state2_family)
        self.view.family_option_widget.pushButton_chart.clicked.connect( self.load_matplotlib_family_fig)
        self.view.family_option_widget.comboBox_chart.activated.connect(self.change_chart_state_family)
        self.view.family_option_widget.pushButton_find_tribe.clicked.connect(self.show_family_widget)

        self.view.family_widget.comboBox.currentIndexChanged.connect(self.change_family_combobox)
        self.view.family_widget.pushButton.clicked.connect(self.search_family)
        self.view.family_widget.pushButton_2.clicked.connect(self.generate_tree)
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
            
    def show_family_widget(self):
        family_selected = self.view.family_option_widget.comboBox_find_tribe.currentText()
        families = self.dataframe['Nom'].unique()
        if family_selected in families:
            self.window = specific_family_widget(family=family_selected, dataframe=self.dataframe,
                                                 family_dataframe=self.family_dataframe)
            self.window.show()
        else:
            print("selected family not found")

    # family table many checkbox activated
    def change_button_state_family(self):
                if self.view.family_option_widget.cb_view_few.isChecked():
                    self.view.family_option_widget.spinBox_view_few.setEnabled(True)
                else:
                    self.view.family_option_widget.spinBox_view_few.setEnabled(False)

    # family chart many checkbox activeted
    def change_button_state2_family(self):
                if self.view.family_option_widget.checkBox.isChecked():
                    self.view.family_option_widget.spinBox.setEnabled(True)
                else:
                    self.view.family_option_widget.spinBox.setEnabled(False)

    # family chart combobox activated

    def change_chart_state_family(self):
                columns = list(self.family_dataframe.columns)

                self.view.family_option_widget.comboBox.clear()
                value = self.view.family_option_widget.comboBox_chart.currentText()
                if value == 'رسم بياني دائري':
                    columns.remove('اللقب')
                    columns.remove('ن 00-20 سنة')
                    columns.remove('ن 20-40 سنة')
                    columns.remove('ن 40-60 سنة')
                    columns.remove('ن 60-80 سنة')
                    columns.remove('ن +80 سنة')
                    self.view.family_option_widget.comboBox.addItems(columns)
                    self.view.family_option_widget.comboBox_2.setEnabled(False)
                else:
                    self.view.family_option_widget.comboBox.addItems(columns)
                    self.view.family_option_widget.comboBox_2.setEnabled(True)

    def change_family_combobox(self):
        familys = self.dataframe['Nom'].unique()
        family = self.view.family_widget.comboBox.currentText()
        self.view.family_widget.comboBox_2.clear()
        if family in familys:
            self.view.family_widget.comboBox_2.setEnabled(True)
            df = self.dataframe[self.dataframe['Nom'] == family]
            regions = df['Tribue'].unique()
            regions = list(regions)
            regions.sort()
            self.view.family_widget.comboBox_2.addItems(regions)
        else:
            self.view.family_widget.comboBox_2.setEnabled(False)

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

def main():
    # get setiings from config.json
    settings = load_settings()
    # set the application
    global app
    app = QApplication(sys.argv)
    # set view and  controller
    view = Window(text=settings[0])
    controller = Controller(view, settings[1])
    welcome = starting_screen()
    welcome.show()
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
        
class specific_family_widget(QWidget):

    def __init__(self, parent=None, family=None, dataframe=None, family_dataframe=None):

        super().__init__(parent=parent)
        # getting region name
        self.family_name = family
        # getting the specific region df
        family_groupby = dataframe.groupby(['Nom'])
        self.dataframe = family_groupby.get_group(self.family_name)
        # getting region general info
        self.info = family_dataframe[family_dataframe['اللقب'] == self.family_name]
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
        people_count = x['Tribue'].value_counts()
        people_count.rename('ع الافراد', inplace=True)
        ### Families sexe count
        sexe_count = x.groupby(['Tribue', 'Sexe'], as_index=False, sort=False)['Prénom'].count()
        sexe_count = pd.pivot_table(sexe_count, index=['Tribue'],
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
        age_count = age.groupby(['Tribue'])["Prénom"].count()
        age_count00 = age_count.rename('ع 00-20 سنة')
        ## number of people 20-40 years old in each group
        age = df[(df['Age'] < 40) & (df['Age'] >= 20)]
        age_count = age.groupby(['Tribue'])["Prénom"].count()
        age_count20 = age_count.rename('ع 20-40 سنة')
        ## number of people 40-60 years old in each group
        age = df[(df['Age'] < 60) & (df['Age'] >= 40)]
        age_count = age.groupby(['Tribue'])["Prénom"].count()
        age_count40 = age_count.rename('ع 40-60 سنة')
        ## number of people 60-80 years old in each group
        age = df[(df['Age'] < 80) & (df['Age'] >= 60)]
        age_count = age.groupby(['Tribue'])["Prénom"].count()
        age_count60 = age_count.rename('ع 60-80 سنة')
        ## number of people +80 years old in each group
        age = df[80 <= df['Age']]
        age_count = age.groupby(['Tribue'])["Prénom"].count()
        age_count80 = age_count.rename('ع +80 سنة')
        ## median age
        median_age = df.groupby('Tribue')['Age'].median()
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
        family_df['المنطقة'] = family_df.index
        ### fixing columns order
        col = ['المنطقة',
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
        if select_x == 'المنطقة':
            axe_x = list([get_display(arabic_reshaper.reshape(x)) for x in axe_x])
        axe_y = df[select_y]
        if select_y == 'المنطقة':
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
            sort_value = 'المنطقة'
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
        columns = list(self.family_df)
        self.ui.comboBox_3.clear()
        value = self.ui.comboBox_2.currentText()
        if value == 'رسم بياني دائري':
            columns.remove('المنطقة')
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
        self.setWindowTitle(self.family_name)
        self.ui.tableView.setMinimumHeight(200)
        # setting the region info
        self.ui.label.setText('<h1>' + self.family_name + '<\\h1>')
        self.ui.label_13.setText(str(self.info['ع الذكور'][0]))
        self.ui.label_17.setText(str(self.info['ع الاناث'][0]))
        self.ui.label_5.setText(str(self.info['ع الافراد'][0]))
        self.ui.label_7.setText(str(self.info['ع المناطق'][0]))
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
