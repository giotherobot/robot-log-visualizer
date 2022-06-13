# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'robot_log_visualizer/ui/misc/visualizer.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1127, 569)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setChildrenCollapsible(False)
        self.splitter_2.setObjectName("splitter_2")
        self.dataVisualizationFrame = QtWidgets.QFrame(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.dataVisualizationFrame.sizePolicy().hasHeightForWidth())
        self.dataVisualizationFrame.setSizePolicy(sizePolicy)
        self.dataVisualizationFrame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.dataVisualizationFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.dataVisualizationFrame.setObjectName("dataVisualizationFrame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dataVisualizationFrame)
        self.gridLayout_3.setContentsMargins(-1, 9, -1, -1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.timeSlider = QtWidgets.QSlider(self.dataVisualizationFrame)
        self.timeSlider.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeSlider.sizePolicy().hasHeightForWidth())
        self.timeSlider.setSizePolicy(sizePolicy)
        self.timeSlider.setPageStep(1)
        self.timeSlider.setTracking(True)
        self.timeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.timeSlider.setObjectName("timeSlider")
        self.gridLayout_3.addWidget(self.timeSlider, 1, 0, 1, 2)
        self.startButton = QtWidgets.QPushButton(self.dataVisualizationFrame)
        self.startButton.setEnabled(False)
        self.startButton.setMaximumSize(QtCore.QSize(40, 16777215))
        self.startButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.startButton.setText("")
        icon = QtGui.QIcon.fromTheme("media-playback-start")
        self.startButton.setIcon(icon)
        self.startButton.setObjectName("startButton")
        self.gridLayout_3.addWidget(self.startButton, 1, 2, 1, 1)
        self.pauseButton = QtWidgets.QPushButton(self.dataVisualizationFrame)
        self.pauseButton.setEnabled(False)
        self.pauseButton.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pauseButton.setText("")
        icon = QtGui.QIcon.fromTheme("media-playback-pause")
        self.pauseButton.setIcon(icon)
        self.pauseButton.setCheckable(False)
        self.pauseButton.setDefault(False)
        self.pauseButton.setFlat(False)
        self.pauseButton.setObjectName("pauseButton")
        self.gridLayout_3.addWidget(self.pauseButton, 1, 3, 1, 1)
        self.splitter = QtWidgets.QSplitter(self.dataVisualizationFrame)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(True)
        self.splitter.setObjectName("splitter")
        self.variableTreeWidget = QtWidgets.QTreeWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.variableTreeWidget.sizePolicy().hasHeightForWidth())
        self.variableTreeWidget.setSizePolicy(sizePolicy)
        self.variableTreeWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.variableTreeWidget.setSizeIncrement(QtCore.QSize(0, 0))
        self.variableTreeWidget.setBaseSize(QtCore.QSize(0, 0))
        self.variableTreeWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.variableTreeWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.variableTreeWidget.setAnimated(True)
        self.variableTreeWidget.setObjectName("variableTreeWidget")
        self.variableTreeWidget.header().setVisible(False)
        self.variableTreeWidget.header().setDefaultSectionSize(100)
        self.tabPlotWidget = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabPlotWidget.sizePolicy().hasHeightForWidth())
        self.tabPlotWidget.setSizePolicy(sizePolicy)
        self.tabPlotWidget.setTabsClosable(True)
        self.tabPlotWidget.setMovable(False)
        self.tabPlotWidget.setTabBarAutoHide(False)
        self.tabPlotWidget.setObjectName("tabPlotWidget")
        self.meshcatAndVideoTab = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.meshcatAndVideoTab.sizePolicy().hasHeightForWidth())
        self.meshcatAndVideoTab.setSizePolicy(sizePolicy)
        self.meshcatAndVideoTab.setTabPosition(QtWidgets.QTabWidget.East)
        self.meshcatAndVideoTab.setDocumentMode(False)
        self.meshcatAndVideoTab.setObjectName("meshcatAndVideoTab")
        self.meshcatTab = QtWidgets.QWidget()
        self.meshcatTab.setObjectName("meshcatTab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.meshcatTab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.meshcatView = QtWebEngineWidgets.QWebEngineView(self.meshcatTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.meshcatView.sizePolicy().hasHeightForWidth())
        self.meshcatView.setSizePolicy(sizePolicy)
        self.meshcatView.setObjectName("meshcatView")
        self.horizontalLayout.addWidget(self.meshcatView)
        icon = QtGui.QIcon.fromTheme("input-gaming")
        self.meshcatAndVideoTab.addTab(self.meshcatTab, icon, "")
        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 4)
        self.tabWidget = QtWidgets.QTabWidget(self.splitter_2)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.logScrollArea = QtWidgets.QScrollArea(self.tab_5)
        self.logScrollArea.setMinimumSize(QtCore.QSize(0, 120))
        self.logScrollArea.setAutoFillBackground(False)
        self.logScrollArea.setStyleSheet("background: white")
        self.logScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.logScrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.logScrollArea.setWidgetResizable(True)
        self.logScrollArea.setObjectName("logScrollArea")
        self.logScrollAreaWidgetContents = QtWidgets.QWidget()
        self.logScrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1058, 118))
        self.logScrollAreaWidgetContents.setObjectName("logScrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.logScrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.logLabel = QtWidgets.QLabel(self.logScrollAreaWidgetContents)
        self.logLabel.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.logLabel.setText("")
        self.logLabel.setObjectName("logLabel")
        self.gridLayout.addWidget(self.logLabel, 1, 0, 1, 1)
        self.logScrollArea.setWidget(self.logScrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.logScrollArea)
        icon = QtGui.QIcon.fromTheme("document")
        self.tabWidget.addTab(self.tab_5, icon, "")
        self.pythonWidget = QtWidgets.QWidget()
        self.pythonWidget.setAutoFillBackground(False)
        self.pythonWidget.setObjectName("pythonWidget")
        self.pythonWidgetLayout = QtWidgets.QVBoxLayout(self.pythonWidget)
        self.pythonWidgetLayout.setObjectName("pythonWidgetLayout")
        icon = QtGui.QIcon.fromTheme("terminal")
        self.tabWidget.addTab(self.pythonWidget, icon, "")
        self.verticalLayout.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1127, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("exit")
        self.actionQuit.setIcon(icon)
        self.actionQuit.setObjectName("actionQuit")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabPlotWidget.setCurrentIndex(-1)
        self.meshcatAndVideoTab.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Robot Log Visualizer"))
        self.variableTreeWidget.headerItem().setText(0, _translate("MainWindow", "Variables"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionOpen.setText(_translate("MainWindow", "&Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
from PyQt5 import QtWebEngineWidgets
