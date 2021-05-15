import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QHeaderView, QWidget
import numpy as np
import matplotlib
from ui import Ui_Form, Help_Ui, Help_Widget
from family_tree import Family

matplotlib.use('Qt5Agg')

from ui import error_screen
import math
from dateutil.relativedelta import relativedelta
from PyQt5.QtCore import QObject, pyqtSignal
import pandas as pd
import datetime
from functools import partial
from PyQt5.QtCore import QAbstractTableModel, Qt
import arabic_reshaper
from bidi.algorithm import get_display
import tempfile


# class responsible of responding to the user and extracting data
class Controller(object):

    def __init__(self, view):
        self.view = view
        self._connect()

    def load_app(self, path):
        result = self.init_dataframe(path)
        if result:
            self.init_tribes_df()
            self.init_families_df()
            self.load_people()
            self.load_tribes()
            self.load_familes()
            self.load_general()
            self.init_tribe_ui()
            self.init_family_ui()
            self.update_family_widget()
            return True
        else:
            return False

    def tab_changed(self):
        index = self.view.tabs.currentIndex()
        if index == 1:
            self.view.rows_count.show()
            pass
        else:
            self.view.rows_count.hide()

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

        # fix the gender column to correcnte data
        def fix_gender(gender):
            gender = gender.strip()
            if gender in ['ذ', 'د']:
                return 'ذكر'
            elif gender in ['أ', 'ا']:
                return 'انثى'
            else:
                return 'غير محدد'

        # add month and date when there is only year
        def fix_year_only(time):
            time = str(time)
            time = time.strip()
            if len(time) == 4:
                return '01/01/' + time
            elif time.startswith('00/00'):
                return '01/01/' + time[-4:]
            else:
                return time

        # return how many years between two dates
        def yearsago(years, from_date=None):
            if from_date is None:
                from_date = datetime.datetime.now()
            return from_date - relativedelta(years=years)

        result = 0
        try:
            # initiliasing the data base file path
            self.path = path
            # creating a data frame for the file
            df = pd.read_excel(path)

            columns_list = ['Nom', 'Prénom', 'Date de naissanace', 'Prénon père', 'Sexe', 'Tribue']
            print(bool(list(df.columns) == columns_list))
            # preparing the dataframe
            # fixing the 'Sexe' values
            df["Sexe"] = df["Sexe"].apply(fix_gender)
            df["Sexe"] = pd.Categorical(df["Sexe"])
            # changing bithdate to datetime type
            df["Date de naissanace"] = df["Date de naissanace"].apply(fix_year_only)
            df["Date de naissanace"] = pd.to_datetime(df["Date de naissanace"],errors='coerce')
            df.dropna(inplace=True)
            # remove rows that containe wrong date
            df.drop(df[df['Date de naissanace'] > '2020'].index, inplace=True)
            # remove exta white space on the string columns
            df['Nom'] = [x.strip() for x in df["Nom"]]
            df['Prénom'] = [x.strip() for x in df["Prénom"]]
            df['Tribue'] = [x.strip() for x in df["Tribue"]]
            df['Prénon père'] = [x.strip() for x in df["Prénon père"]]
            df['Age'] = [yearsago(x).year for x in df['Date de naissanace'].dt.year]
            # saving the dataframe
            self.dataframe = df
            result = True
        # something wrong with the input dataframe
        except:
            result = False
        finally:
            return result

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

    def load_general(self):
        def make_pies(self, sexe_list, age_list):
            fig = self.view.general_ui.widget.axes
            fig.set_aspect('auto')
            fig.clear()
            fig.cla()
            fig1 = self.view.general_ui.widget_2.axes
            fig1.set_aspect('auto')
            fig1.clear()
            fig1.cla()

            sexe_labels = [get_display(arabic_reshaper.reshape('ذكور')),
                           get_display(arabic_reshaper.reshape('اناث'))]

            df_1 = pd.DataFrame(list(zip(sexe_labels, sexe_list)),
                                columns=['name', 'val'])
            df_1 = df_1[df_1['val'] != 0]

            self.view.general_ui.widget.axes.pie(df_1['val'], labels=df_1['name'], autopct='%1.1f%%')

            age_labels = [get_display(arabic_reshaper.reshape('20-00')),
                          get_display(arabic_reshaper.reshape('40-20')),
                          get_display(arabic_reshaper.reshape('60-40')),
                          get_display(arabic_reshaper.reshape('80-60')),
                          get_display(arabic_reshaper.reshape('80+')),
                          ]
            df = pd.DataFrame(list(zip(age_labels, age_list)),
                              columns=['name', 'val'])
            df = df[df['val'] != 0]
            self.view.general_ui.widget_2.axes.pie(df['val'], labels=df['name'], autopct='%1.1f%%')

            self.view.general_ui.widget.fig.tight_layout()
            self.view.general_ui.widget.draw()

            self.view.general_ui.widget_2.fig.tight_layout()
            self.view.general_ui.widget_2.draw()

        ui = self.view.general_ui

        family_df = self.dataframe.copy()

        people_count = family_df.shape[0]
        male_count = family_df[family_df['Sexe'] == 'ذكر'].shape[0]
        female_count = family_df[family_df['Sexe'] == 'انثى'].shape[0]
        family_count = len(family_df['Nom'].unique())
        tribue_count = len(family_df['Tribue'].unique())
        age_median = family_df['Age'].median()
        age00 = family_df[(family_df['Age'] < 20) & (family_df['Age'] >= 0)].shape[0]
        age20 = family_df[(family_df['Age'] < 40) & (family_df['Age'] >= 20)].shape[0]
        age40 = family_df[(family_df['Age'] < 60) & (family_df['Age'] >= 40)].shape[0]
        age60 = family_df[(family_df['Age'] < 80) & (family_df['Age'] >= 60)].shape[0]
        age80 = family_df[family_df['Age'] >= 80].shape[0]
        print(age80)

        ui.label_2.setText(str(people_count))
        ui.label_23.setText(str(age_median))
        ui.label_4.setText(str(family_count))
        ui.label_6.setText(str(tribue_count))
        ui.label_10.setText(str(male_count))
        ui.label_12.setText(str(female_count))
        ui.label_21.setText(str(age00))
        ui.label_19.setText(str(age20))
        ui.label_17.setText(str(age40))
        ui.label_13.setText(str(age60))
        ui.label_15.setText(str(age80))

        make_pies(self, [male_count, female_count], [age00, age20, age40, age60, age80])

    def search_family(self):
        family_selected = self.view.family_widget.comboBox.currentText()
        region_selected = self.view.family_widget.comboBox_2.currentText()
        famlies = self.dataframe['Nom'].unique()
        df = self.dataframe[self.dataframe['Nom'] == family_selected]
        regions = df['Tribue'].unique()
        if family_selected not in famlies or region_selected not in regions:
            self.screen = error_screen(text='اللقب او القبيلة غير موجود')

        else:
            self.load_family(family_selected, region_selected)

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

    def load_family(self, family, region):

        def make_pies(self, sexe_list, age_list):
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
        family_df = family_df[family_df['Nom'] == family]
        family_df = family_df[family_df['Tribue'] == region]
        self.view.family_widget.label_4.setText('<h2> ' + family + '-- ' + region + '</h2>')

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
        self.family_dicto = df_for_family.to_dict(orient='index')

        make_pies(self, [male_count, female_count], [age00, age20, age40, age60, age80])

    def generate_tree(self):

        myfamily = Family()
        myfamily.members.clear()
        myfamily.populate(self.family_dicto.values())
        myfamily.add_fathers()
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
                                     columns[4]: args[4], columns[5]: args[5],columns[6]: args[6], })
        return renamed

    # updating the rows count in statu bar
    def update_rows_count(self, rows):
        string = self.view.texts['found_message'] + ' ' + str(rows) + ' نتائج '
        self.view.rows_count.setText(string)

    # connect widgets with methodes using singnals
    def _connect(self):
        # connect search people action
        self.view.people_options['search'].clicked.connect(self.search_people)
        # connect the region view widgets
        self.view.tribe_option_widget.cb_view_few.stateChanged.connect(self.change_button_state)
        self.view.tribe_option_widget.pushButton_refresh.clicked.connect(self.load_tribes)
        self.view.tribe_option_widget.checkBox.stateChanged.connect(self.change_button_state2)
        self.view.tribe_option_widget.pushButton_chart.clicked.connect(self.load_matplotlib_tribe_fig)
        self.view.tribe_option_widget.comboBox_chart.activated.connect(self.change_chart_state)
        self.view.tribe_option_widget.pushButton_find_tribe.clicked.connect(self.show_region_widget)
        self.view.tribe_option_widget.toolButton.clicked.connect(self.show_help)
        # connect the family view widgets
        self.view.family_option_widget.cb_view_few.stateChanged.connect(self.change_button_state_family)
        self.view.family_option_widget.pushButton_refresh.clicked.connect(self.load_familes)
        self.view.family_option_widget.checkBox.stateChanged.connect(self.change_button_state2_family)
        self.view.family_option_widget.pushButton_chart.clicked.connect(self.load_matplotlib_family_fig)
        self.view.family_option_widget.comboBox_chart.activated.connect(self.change_chart_state_family)
        self.view.family_option_widget.pushButton_find_tribe.clicked.connect(self.show_family_widget)
        self.view.family_option_widget.toolButton.clicked.connect(self.show_help)

        self.view.family_widget.comboBox.currentIndexChanged.connect(self.change_family_combobox)
        self.view.family_widget.pushButton.clicked.connect(self.search_family)
        self.view.family_widget.pushButton_2.clicked.connect(self.generate_tree)
        # when tabs view change
        self.view.tabs.currentChanged.connect(self.tab_changed)
        pass

    # tribe table many checkbox activated
    def change_button_state(self):
        if self.view.tribe_option_widget.cb_view_few.isChecked():
            self.view.tribe_option_widget.spinBox_view_few.setEnabled(True)
        else:
            self.view.tribe_option_widget.spinBox_view_few.setEnabled(False)

    def show_help(self):
        self.help = Help_Widget()

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
            self.screen = error_screen(text='المنطقة غير موجود')

    def show_family_widget(self):
        print(1)
        family_selected = self.view.family_option_widget.comboBox_find_tribe.currentText()
        families = self.dataframe['Nom'].unique()
        print(2)
        if family_selected in families:
            print(3)
            self.window = specific_family_widget(family=family_selected, dataframe=self.dataframe,
                                                 family_dataframe=self.family_dataframe)
            print(4)
            self.window.show()
            print(5)
        else:
            self.screen = error_screen(text='العائلة غير موجود')

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


# class gets dataframe and transform it into a tableview model
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


# class gets dataframe and transform it into a tableview model
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


# class that load data in another thread
class Worker(QObject):
    finished = pyqtSignal()
    finished1 = pyqtSignal(bool)

    def __init__(self, controller, path):
        super().__init__()
        self.controller = controller
        self.path = path

    def run(self):
        # load data bse

        result = self.controller.load_app(path=self.path)
        if result:
            self.finished1.emit(True)
        else:
            self.finished1.emit(False)
        self.finished.emit()


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
        self.ui.toolButton.clicked.connect(self.show_help)

    def show_help(self):
        self.help = Help_Widget()

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

    def show_help(self):
        self.help = Help_Widget()

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
        self.ui.toolButton.clicked.connect(self.show_help)

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




