# Copyright (C) 2022 Istituto Italiano di Tecnologia (IIT). All rights reserved.
# This software may be modified and distributed under the terms of the
# Released under the terms of the BSD 3-Clause License

# PyQt5
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSlot, Qt, QMutex, QMutexLocker
from PyQt5.QtWidgets import (
    QFileDialog,
    QTreeWidgetItem,
    QToolButton,
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QDialogButtonBox,
    QTableWidgetItem,
)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

from robot_log_visualizer.ui.plot_item import PlotItem
from robot_log_visualizer.ui.video_item import VideoItem
from robot_log_visualizer.ui.text_logging import TextLoggingItem

from robot_log_visualizer.utils.utils import PeriodicThreadState

import sys
import os
import pathlib
import re

import numpy as np

# QtDesigner generated classes
from robot_log_visualizer.ui.autogenerated.visualizer import Ui_MainWindow
from robot_log_visualizer.ui.autogenerated.about import Ui_aboutWindow

# for logging
from time import localtime, strftime

# Matplotlib class
from pyqtconsole.console import PythonConsole
import pyqtconsole.highlighter as hl


class About(QtWidgets.QMainWindow):
    def __init__(self):
        # call QMainWindow constructor
        super().__init__()
        self.ui = Ui_aboutWindow()
        self.ui.setupUi(self)


def build_plot_title_box_dialog():
    dlg = QDialog()
    dlg.setWindowTitle("Plot title")
    la = QVBoxLayout(dlg)
    line_edit = QLineEdit()
    la.addWidget(line_edit)
    bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    bb.clicked.connect(dlg.accept)
    bb.rejected.connect(dlg.reject)
    la.addWidget(bb)
    dlg.setLayout(la)
    return dlg, line_edit


def get_icon(icon_name):

    icon = QtGui.QIcon()
    icon.addPixmap(
        QtGui.QPixmap(str(pathlib.Path(__file__).parent / "misc" / icon_name)),
        QtGui.QIcon.Normal,
        QtGui.QIcon.Off,
    )
    return icon


class RobotViewerMainWindow(QtWidgets.QMainWindow):
    def __init__(self, signal_provider, meshcat_provider, animation_period):
        # call QMainWindow constructor
        super().__init__()

        self.animation_period = animation_period

        # set up the user interface
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set all the icons
        self.ui.startButton.setIcon(get_icon("play-outline.svg"))
        self.ui.pauseButton.setIcon(get_icon("pause-outline.svg"))
        self.ui.pauseButton.setIcon(get_icon("pause-outline.svg"))
        self.ui.meshcatAndVideoTab.setTabIcon(
            0, get_icon("game-controller-outline.svg")
        )
        self.ui.tabWidget.setTabIcon(0, get_icon("calendar-outline.svg"))
        self.ui.tabWidget.setTabIcon(1, get_icon("terminal-outline.svg"))
        self.ui.tabWidget.setTabIcon(2, get_icon("document-text-outline.svg"))

        self.ui.actionQuit.setIcon(get_icon("close-circle-outline.svg"))
        self.ui.actionQuit.setIcon(get_icon("close-circle-outline.svg"))
        self.ui.actionOpen.setIcon(get_icon("folder-open-outline.svg"))
        self.setWindowIcon(get_icon("icon.png"))

        self.about = About()

        self.signal_provider = signal_provider
        self.signal_size = len(self.signal_provider)
        self.signal_provider.register_update_index(self.update_slider)

        self.meshcat_provider = meshcat_provider

        self.tool_button = QToolButton()
        self.tool_button.setText("+")
        self.ui.tabPlotWidget.setCornerWidget(self.tool_button)
        self.tool_button.clicked.connect(self.toolButton_on_click)

        self.plot_items = []
        self.video_items = []

        self.toolButton_on_click()

        # instantiate the Logger
        self.logger = Logger(self.ui.logLabel, self.ui.logScrollArea)
        # print welcome message
        self.logger.write_to_log("Robot Viewer started.")

        self.text_logger = TextLoggingItem(self.ui.yarpTextLogTableWidget)

        self._slider_pressed_mutex = QMutex()
        self._slider_pressed = False

        self.dataset_loaded = False

        # connect action
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionOpen.triggered.connect(self.open_mat_file)
        self.ui.actionAbout.triggered.connect(self.open_about)

        self.ui.meshcatView.setUrl(
            QUrl(meshcat_provider.meshcat_visualizer.viewer.url())
        )

        self.ui.pauseButton.clicked.connect(self.pauseButton_on_click)
        self.ui.startButton.clicked.connect(self.startButton_on_click)
        self.ui.timeSlider.sliderReleased.connect(self.timeSlider_on_release)
        self.ui.timeSlider.sliderPressed.connect(self.timeSlider_on_pressed)
        self.ui.timeSlider.sliderMoved.connect(self.timeSlider_on_sliderMoved)

        self.ui.variableTreeWidget.itemClicked.connect(self.variableTreeWidget_on_click)
        self.ui.yarpTextLogTreeWidget.itemClicked.connect(
            self.textLogTreeWidget_on_click
        )

        self.ui.tabPlotWidget.tabCloseRequested.connect(
            self.plotTabCloseButton_on_click
        )
        self.ui.tabPlotWidget.tabBarDoubleClicked.connect(
            self.plotTabBar_on_doubleClick
        )
        self.ui.tabPlotWidget.currentChanged.connect(self.plotTabBar_currentChanged)

        self.pyconsole = PythonConsole(
            parent=self.ui.pythonWidget,
            formats={
                "keyword": hl.format("#204a87", "bold"),
                "operator": hl.format("#ce5c00"),
                # 'brace':      hl.format('#eeeeec'),
                "defclass": hl.format("#000000", "bold"),
                "string": hl.format("#8f5902"),
                "string2": hl.format("#8f5902"),
                "comment": hl.format("#8f5902", "italic"),
                "self": hl.format("#000000", "italic"),
                "numbers": hl.format("#0000cf"),
                "inprompt": hl.format("#8f5902", "bold"),
                "outprompt": hl.format("#8f5902", "bold"),
            },
        )
        self.pyconsole.edit.setStyleSheet("font-size: 12px;")
        self.ui.pythonWidgetLayout.addWidget(self.pyconsole)
        self.pyconsole.eval_in_thread()

        # self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # self.media_player.setVideoOutput(self.ui.webcamView)
        # self.media_loaded = False

    @property
    def slider_pressed(self):
        locker = QMutexLocker(self._slider_pressed_mutex)
        value = self._slider_pressed
        return value

    @slider_pressed.setter
    def slider_pressed(self, slider_pressed):
        locker = QMutexLocker(self._slider_pressed_mutex)
        self._slider_pressed = slider_pressed

    def keyPressEvent(self, event):
        if not self.dataset_loaded:
            return

        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_B:
                self.slider_pressed = True
                new_index = int(self.ui.timeSlider.value()) - 1
                self.signal_provider.update_index(new_index)
                self.ui.timeLabel.setText(f"{self.signal_provider.current_time:.2f}")
                self.text_logger.highlight_cell(
                    self.find_text_log_index(self.get_text_log_item_path())
                )

                # for every video item we set the instant
                for video_item in self.video_items:
                    if video_item.media_loaded:
                        video_item.media_player.setPosition(
                            new_index
                            / self.ui.timeSlider.maximum()
                            * video_item.media_player.duration()
                        )

                # update the time slider
                self.ui.timeSlider.setValue(new_index)
                self.slider_pressed = False
            elif event.key() == Qt.Key_F:
                self.slider_pressed = True
                new_index = int(self.ui.timeSlider.value()) + 1
                self.signal_provider.update_index(new_index)
                self.ui.timeLabel.setText(f"{self.signal_provider.current_time:.2f}")
                self.text_logger.highlight_cell(
                    self.find_text_log_index(self.get_text_log_item_path())
                )

                # for every video item we set the instant
                for video_item in self.video_items:
                    if video_item.media_loaded:
                        video_item.media_player.setPosition(
                            new_index
                            / self.ui.timeSlider.maximum()
                            * video_item.media_player.duration()
                        )

                self.ui.timeSlider.setValue(new_index)
                self.slider_pressed = False

    def toolButton_on_click(self):
        self.plot_items.append(
            PlotItem(signal_provider=self.signal_provider, period=self.animation_period)
        )
        self.ui.tabPlotWidget.addTab(self.plot_items[-1], "Plot")

        if self.ui.tabPlotWidget.count() == 1:
            self.ui.tabPlotWidget.setTabsClosable(False)
        else:
            self.ui.tabPlotWidget.setTabsClosable(True)

    def timeSlider_on_pressed(self):
        self.slider_pressed = True

    def timeSlider_on_sliderMoved(self):
        index = int(self.ui.timeSlider.value())

        for video_item in self.video_items:
            if video_item.media_loaded:
                video_item.media_player.setPosition(
                    index
                    / self.ui.timeSlider.maximum()
                    * video_item.media_player.duration()
                )

        self.signal_provider.update_index(index)
        self.ui.timeLabel.setText(f"{self.signal_provider.current_time:.2f}")
        self.text_logger.highlight_cell(
            self.find_text_log_index(self.get_text_log_item_path())
        )

    def timeSlider_on_release(self):
        index = int(self.ui.timeSlider.value())

        for video_item in self.video_items:
            if video_item.media_loaded:
                video_item.media_player.setPosition(
                    index
                    / self.ui.timeSlider.maximum()
                    * video_item.media_player.duration()
                )

        self.signal_provider.update_index(index)
        self.ui.timeLabel.setText(f"{self.signal_provider.current_time:.2f}")
        self.text_logger.highlight_cell(
            self.find_text_log_index(self.get_text_log_item_path())
        )
        self.slider_pressed = False

    def startButton_on_click(self):
        self.ui.startButton.setEnabled(False)
        self.ui.pauseButton.setEnabled(True)

        ## TODO its better to start the video only if the tab is active. This will improve the peroformances
        for video_item in self.video_items:
            if video_item.media_loaded:
                video_item.media_player.play()

        self.signal_provider.state = PeriodicThreadState.running
        # self.meshcat_provider.state = PeriodicThreadState.running

        self.logger.write_to_log("Dataset started.")

    def pauseButton_on_click(self):
        self.ui.pauseButton.setEnabled(False)
        self.ui.startButton.setEnabled(True)

        for video_item in self.video_items:
            if video_item.media_loaded:
                video_item.media_player.pause()

        self.signal_provider.state = PeriodicThreadState.pause
        # self.meshcat_provider.state = PeriodicThreadState.pause

        self.logger.write_to_log("Dataset paused.")

    def plotTabCloseButton_on_click(self, index):

        self.ui.tabPlotWidget.removeTab(index)
        self.plot_items[index].canvas.quit_animation()
        del self.plot_items[index]

        if self.ui.tabPlotWidget.count() == 1:
            self.ui.tabPlotWidget.setTabsClosable(False)

    def plotTabBar_on_doubleClick(self, index):

        dlg, plot_title = build_plot_title_box_dialog()
        if dlg.exec() == QDialog.Accepted:
            self.ui.tabPlotWidget.setTabText(index, plot_title.text())

    def variableTreeWidget_on_click(self):
        paths = []
        legends = []
        for index in self.ui.variableTreeWidget.selectedIndexes():
            path = []
            legend = []
            is_leaf = True
            while index.data() is not None:
                legend.append(index.data())
                if not is_leaf:
                    path.append(index.data())
                else:
                    path.append(str(index.row()))
                    is_leaf = False

                index = index.parent()
            path.reverse()
            legend.reverse()

            paths.append(path)
            legends.append(legend)
        self.plot_items[self.ui.tabPlotWidget.currentIndex()].canvas.update_plots(
            paths, legends
        )

    def find_text_log_index(self, path):
        current_time = self.signal_provider.current_time
        initial_time = self.signal_provider.initial_time

        path = self.get_text_log_item_path()
        if path:
            ref = self.signal_provider.text_logging_data
            for key in path:
                ref = ref[key]

            s = np.flatnonzero(ref["timestamps"] <= current_time + initial_time)
            if len(s) == 1:
                return s[0]
            elif not s.any():
                return None
            else:
                return s[-1]

        return None

    def show_text_log(self, path):
        initial_time = self.signal_provider.initial_time
        ref = self.signal_provider.text_logging_data
        for key in path:
            ref = ref[key]

        self.text_logger.clean()
        logs = ref["data"]
        timestamps = ref["timestamps"]
        for i in range(len(ref["data"])):
            self.text_logger.add_entry(
                logs[i].text, timestamps[i] - initial_time, font_color=logs[i].color()
            )

    def get_text_log_item_path(self):
        paths = []
        for index in self.ui.yarpTextLogTreeWidget.selectedIndexes():
            path = []
            is_leaf = True
            while index.data() is not None:
                if not is_leaf:
                    path.append(index.data())
                else:
                    path.append(index.data())
                    is_leaf = False

                index = index.parent()

            path.reverse()
            paths.append(path)
        if paths:
            return paths[0]
        else:
            return None

    def textLogTreeWidget_on_click(self):
        path = self.get_text_log_item_path()
        if path:
            self.show_text_log(path)
            self.text_logger.highlight_cell(self.find_text_log_index(path))

    def plotTabBar_currentChanged(self, index):

        # clear the selection to prepare a new one
        self.ui.variableTreeWidget.clearSelection()
        for active_path_str in self.plot_items[index].canvas.active_paths.keys():
            path = active_path_str.split("/")
            item = self.ui.variableTreeWidget.topLevelItem(0)
            for subpath in path[1:]:
                for child_id in range(item.childCount()):
                    if item.child(child_id).text(0) == subpath:
                        item = item.child(child_id)
                        break
            item.setSelected(True)

    @pyqtSlot()
    def update_slider(self):
        if not self.slider_pressed:
            self.ui.timeSlider.setValue(self.signal_provider.index)
            self.ui.timeLabel.setText(f"{self.signal_provider.current_time:.2f}")
            self.text_logger.highlight_cell(
                self.find_text_log_index(self.get_text_log_item_path())
            )

    def closeEvent(self, event):
        # close the window
        self.pyconsole.close()
        for video_item in self.video_items:
            del video_item.media_player

        self.meshcat_provider.state = PeriodicThreadState.closed
        self.meshcat_provider.wait()

        self.signal_provider.state = PeriodicThreadState.closed
        self.signal_provider.wait()

        event.accept()

    def __populate_variable_tree_widget(self, obj, parent) -> QTreeWidgetItem:
        if not isinstance(obj, dict):
            return parent
        if "data" in obj.keys() and "timestamps" in obj.keys():
            temp_array = obj["data"]
            try:
                n_cols = temp_array.shape[1]
            except IndexError:
                # This happens in the case the variable is a scalar.
                n_cols = 1

            # In yarp telemetry v0.4.0 the elements_names was saved.
            if "elements_names" in obj.keys():
                for name in obj["elements_names"]:
                    item = QTreeWidgetItem([name])
                    parent.addChild(item)
            else:
                for i in range(n_cols):
                    item = QTreeWidgetItem(["Element " + str(i)])
                    parent.addChild(item)
            return parent
        for key, value in obj.items():
            item = QTreeWidgetItem([key])
            item = self.__populate_variable_tree_widget(value, item)
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            parent.addChild(item)
        return parent

    def __populate_text_logging_tree_widget(self, obj, parent) -> QTreeWidgetItem:
        if not isinstance(obj, dict):
            return parent

        if "data" in obj.keys() and "timestamps" in obj.keys():
            return parent

        for key, value in obj.items():
            item = QTreeWidgetItem([key])
            item = self.__populate_text_logging_tree_widget(value, item)
            if "data" not in value.keys():
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            parent.addChild(item)
        return parent

    def open_mat_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open a mat file", ".", filter="*.mat"
        )
        if file_name:
            self.signal_provider.open_mat_file(file_name)
            self.signal_size = len(self.signal_provider)

            # populate tree
            root = list(self.signal_provider.data.keys())[0]
            root_item = QTreeWidgetItem([root])
            root_item.setFlags(root_item.flags() & ~Qt.ItemIsSelectable)
            items = self.__populate_variable_tree_widget(
                self.signal_provider.data[root], root_item
            )
            self.ui.variableTreeWidget.insertTopLevelItems(0, [items])

            # populate text logging tree
            if self.signal_provider.text_logging_data:
                root = list(self.signal_provider.text_logging_data.keys())[0]
                root_item = QTreeWidgetItem([root])
                root_item.setFlags(root_item.flags() & ~Qt.ItemIsSelectable)
                items = self.__populate_text_logging_tree_widget(
                    self.signal_provider.text_logging_data[root], root_item
                )
                self.ui.yarpTextLogTreeWidget.insertTopLevelItems(0, [items])

            # spawn the console
            self.pyconsole.push_local_ns("data", self.signal_provider.data)

            self.ui.timeSlider.setMaximum(self.signal_size)
            self.ui.startButton.setEnabled(True)
            self.ui.timeSlider.setEnabled(True)

            # get all the video associated to the dataset

            filename_without_path = pathlib.Path(file_name).name
            (prefix, sep, suffix) = filename_without_path.rpartition(".")

            video_filenames = [
                str(pathlib.Path(file_name).parent.absolute() / pathlib.Path(f))
                for f in os.listdir(pathlib.Path(file_name).parent.absolute())
                if re.search(prefix + "_[a-zA-Z0-9_]*\.mp4$", f)
            ]

            # for every video we create a video item and we append it to the tab
            for video_filename in video_filenames:
                video_prefix, _, _ = pathlib.Path(video_filename).name.rpartition(".")
                video_label = str(video_prefix).replace(prefix + "_", "")
                self.video_items.append(VideoItem(video_filename=video_filename))
                self.ui.meshcatAndVideoTab.addTab(
                    self.video_items[-1], get_icon("videocam-outline.svg"), video_label
                )
                self.logger.write_to_log("Video '" + video_filename + "' opened.")
            # load the model
            self.meshcat_provider.load_model(
                self.signal_provider.joints_name, self.signal_provider.robot_name
            )

            self.meshcat_provider.state = PeriodicThreadState.running

            self.dataset_loaded = True

            # write something in the log
            self.logger.write_to_log("File '" + file_name + "' opened.")
            self.logger.write_to_log(
                "Robot name: '" + self.signal_provider.robot_name + "'."
            )

    def open_about(self):
        self.about.show()


class Logger:
    """
    Logger class shows events during the execution of the viewer.
    """

    def __init__(self, log_widget, scroll_area, add_time=True):
        # set log widget from main window
        self.log_widget = log_widget

        # set scroll area form main window
        self.scroll_area = scroll_area

        self.add_time = add_time

    def write_to_log(self, text, font_color=None, background_color=None):
        """
        Log the text "text" with a timestamp.
        """

        # extract current text from the log widget
        current_text = self.log_widget.text()

        if font_color is not None:
            text = '<font color="' + str(font_color) + '">' + text + "</font>"

        if background_color is not None:
            text = (
                '<span style="background-color:'
                + str(background_color)
                + '">'
                + text
                + "</span>"
            )

        # compose new text
        # convert local time to string
        if self.add_time:
            time_str = strftime(" [%H:%M:%S] ", localtime())
            #
            new_text = current_text + time_str + text + "<br>"
        else:
            new_text = current_text + text + "<br>"

        # log into the widget
        self.log_widget.setText(new_text)

        # scroll down text
        self.scroll_down()

    def clean(self):
        self.log_widget.clear()

    def scroll_down(self):
        """
        Scroll down the slider of the scroll area
        linked to this logger
        """
        # extract scroll bar from the scroll area
        scroll_bar = self.scroll_area.verticalScrollBar()

        # set maximum value of the slider, 1000 is enough
        scroll_bar.setMaximum(1000)
        scroll_bar.setValue(scroll_bar.maximum())


if __name__ == "__main__":
    # construct a QApplication
    app = QtWidgets.QApplication(sys.argv)

    # instantiate the main window and add the Matplotlib canvas
    gui = RobotViewerMainWindow()

    # show the main window
    gui.show()

    sys.exit(app.exec_())
