"""
Setif's people is a small application that allows to extract
information from microsoft excel worksheet file that contains a
data base of people
"""

__version__ = '1.0'
__author__ = 'khaled bouabdallah'
__email__ = 'bouabdallah.khaled@yahoo.com'

# import project modules
from ui import family_widget_ui, QVSeperationLine, Tribe_tools_widget_ui, MplCanvas, loading_screen, \
    starting_screen_ui, general_ui

import qrc_resources
from backend import Controller, Worker
# import other modules
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from text_strings import arabic
from PyQt5.QtCore import QRegExp, Qt, QThread
from PyQt5.QtGui import QIcon, QRegExpValidator
import sys

# import GUI components
from PyQt5.QtWidgets import (
    QToolBar,
    QAction,
    QTabWidget,
    QApplication,
    QMainWindow,
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
    QHeaderView,
    QFileDialog)


# main window
class Window(QMainWindow):

    def __init__(self, parent=None, text=arabic):
        self.texts = text
        super().__init__(parent)
        self.init_Ui()

    def init_Ui(self):
        self.setWindowTitle(self.texts['title'])
        self.setBaseSize(1280, 800)
        self.setMinimumWidth(1280)
        self.setMinimumHeight(800)
        self.setWindowIcon(QIcon(':icon.png'))
        # right to left for arabic
        self.setLayoutDirection(1)
        self.set_centralWidget()
        self.set_actions()
        #self.set_Menu()
        self.set_statuBar()

    def set_Menu(self):
        # getting the menubar object (already created by default empty)
        menuBar = self.menuBar()
        # add information menu
        self.helpMenu = menuBar.addMenu(QIcon(":help-content.svg"), self.texts['information'])
        self.helpMenu.addAction(self.help_action)
        self.helpMenu.addAction(self.about_action)
        # add actions to the information menu

    def set_statuBar(self):
        self.statusbar = QStatusBar()
        self.statusbar.setLayoutDirection(0)
        self.setStatusBar(self.statusbar)
        # self.statusbar.showMessage("Ready", 3000)
        self.rows_count = QLabel('0')
        self.statusbar.addPermanentWidget(self.rows_count)

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
        self.tabs.addTab(self.set_general_widget(), self.texts['general'])
        self.tabs.addTab(self.set_people_widget(), self.texts['people'])
        self.tabs.addTab(self.set_families_widget(), 'العائلات')
        self.tabs.addTab(self.set_names_widget(), 'الالقاب')
        self.tabs.addTab(self.set_regions_widget(), self.texts['regions'])


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
            #self.people_options['reset'] = QPushButton('اعادة الضبط')
            #vlayout.addWidget(self.people_options['reset'])
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
            w.setMaximumWidth(380)
            return w

        # building a table view
        self.familes_table_view = QTableView()
        self.familes_table_view.setMinimumWidth(900)
        self.familes_table_view.setMaximumHeight(380)

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
            w.setMaximumWidth(380)
            return w

        # building a table view
        self.tribes_table_view = QTableView()
        self.tribes_table_view.setMinimumWidth(900)
        self.tribes_table_view.setMaximumHeight(380)

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

    def set_general_widget(self):
        self.general_ui = general_ui()
        w = QWidget()
        self.general_ui.setupUi(w)
        return w

# starting widget
class StartingScreen(QWidget):

    def __init__(self, parent=None, view=None, controller=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon(':icon.png'))
        self.ui = starting_screen_ui()
        self.ui.setupUi(self)
        self.setWindowTitle('ناس سطيف')
        self.main_ui = view
        self.controller = controller
        # adding the loading screen widget
        self.loading_screen = loading_screen()
        layout = QVBoxLayout()
        layout.addWidget(self.loading_screen)
        self.ui.loading_widget.setLayout(layout)
        # connecting button
        self.ui.search_file_button.clicked.connect(self.load_file)
        self.ui.label.setText('')
        self.ui.label.setMinimumWidth(200)

    def load_file(self):

        fname = QFileDialog.getOpenFileName(self, 'اختر ملف',
                                            'c:\\', "قاعدة البيانات (*.xlsx)")
        self.ui.search_file_button.setEnabled(False)
        label = self.ui.label
        # check if user chose a file
        if fname[0]:
            # setting a worker and a thread for processing the file chosen
            self.thread = QThread()
            self.worker = Worker(self.controller, fname[0])
            # moving the worker to the therad and connecting them
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            # making sure to close the thread and the worker after they finish
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.finished1.connect(self.clean_ui)
            # start the worker thread
            self.loading_screen.start_animation()
            self.thread.start()
            label.setText('جاري تحميل')

    def clean_ui(self, result):
        if result:
            self.controller.search_family()
            self.controller.load_matplotlib_tribe_fig()
            self.controller.load_matplotlib_family_fig()
            self.loading_screen.stop_animation()
            self.hide()
            self.main_ui.show()
        else:
            self.loading_screen.stop_animation()
            self.ui.label.setText('لا يمكن استخدام قاعدة البيانات يرجي اخيار ملف اخر')
            self.ui.search_file_button.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    view = Window(text=arabic)
    controller = Controller(view)
    welcome = StartingScreen(view=view, controller=controller)
    welcome.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
