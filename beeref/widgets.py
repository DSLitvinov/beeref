# This file is part of BeeRef.
#
# BeeRef is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BeeRef is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BeeRef.  If not, see <https://www.gnu.org/licenses/>.

import logging
import os.path

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

from beeref import constants
from beeref.config import logfile_name, BeeSettings
from beeref.main_controls import MainControlsMixin
from beeref.styles import BeeRefStyles


logger = logging.getLogger(__name__)


class RecentFilesModel(QtCore.QAbstractListModel):
    """An entry in the 'Recent Files' list."""

    def __init__(self, files):
        super().__init__()
        self.files = files

    def rowCount(self, parent):
        return len(self.files)

    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return os.path.basename(self.files[index.row()])
        if role == QtCore.Qt.ItemDataRole.FontRole:
            font = QtGui.QFont()
            font.setUnderline(True)
            return font


class RecentFilesView(QtWidgets.QListView):

    def __init__(self, files=None):
        super().__init__()
        self.files = files or []
        self.clicked.connect(self.on_clicked)
        self.setModel(RecentFilesModel(self.files))
        self.setMouseTracking(True)

    def on_clicked(self, index):
        self.parent().parent().open_from_file(self.files[index.row()])

    def update_files(self, files):
        self.files = files
        self.model().files = files
        self.reset()

    def sizeHint(self):
        size = QtCore.QSize()
        if (self.files):
            height = sum(
                (self.sizeHintForRow(i) + 2) for i in range(len(self.files)))
            size.setHeight(height)

            width = max(
                self.sizeHintForColumn(i) for i in range(len(self.files)))
            size.setWidth(width + 2)
        return size

    def mouseMoveEvent(self, event):
        index = self.indexAt(
            QtCore.QPoint(int(event.position().x()),
                          int(event.position().y())))
        if index.isValid():
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

        super().mouseMoveEvent(event)


class WelcomeOverlay(MainControlsMixin, QtWidgets.QWidget):
    """Some basic info to be displayed when the scene is empty."""

    def __init__(self, parent):
        super().__init__(parent)
        self.control_target = parent
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.init_main_controls()

        # Main vertical layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(12)
        
        # Add stretch to center content vertically
        self.layout.addStretch(2)
        
        # 256x256 placeholder icon
        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setFixedSize(256, 256)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Load the placeholder SVG icon
        icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'placeholder_icon.svg')
        if os.path.exists(icon_path):
            pixmap = QtGui.QPixmap(icon_path)
            self.icon_label.setPixmap(pixmap.scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            # Fallback: create a simple white rectangle
            pixmap = QtGui.QPixmap(256, 256)
            pixmap.fill(QtGui.QColor(255, 255, 255))
            self.icon_label.setPixmap(pixmap)
        
        self.layout.addWidget(self.icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # "Drag and drop images here" text
        drop_text = QtWidgets.QLabel("Drag and drop images here")
        drop_text.setStyleSheet(BeeRefStyles.get_welcome_text_style())
        drop_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(drop_text)
        
        # "or" separator
        or_label = QtWidgets.QLabel("or")
        or_label.setStyleSheet(BeeRefStyles.get_welcome_or_text_style())
        or_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(or_label)
        
        # Browse button
        self.browse_button = QtWidgets.QPushButton("Browse", self)
        self.browse_button.setFixedSize(120, 40)
        self.browse_button.setStyleSheet(BeeRefStyles.get_button_style())
        self.browse_button.clicked.connect(self.on_browse_clicked)
        self.layout.addWidget(self.browse_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add stretch before help link
        self.layout.addStretch(1)
        
        # Help link
        self.help_link = QtWidgets.QLabel(f'<a href="#" style="{BeeRefStyles.get_help_link_style()}">Help</a>')
        self.help_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.help_link.linkActivated.connect(self.on_help_clicked)
        self.layout.addWidget(self.help_link)
        
        # Add stretch at the end
        self.layout.addStretch(1)
        
        self.setLayout(self.layout)

        # Recent files (hidden by default, shown only when there are recent files)
        self.files_layout = QtWidgets.QVBoxLayout()
        self.files_layout.addStretch(50)
        self.files_layout.addWidget(
            QtWidgets.QLabel('<h3>Recent Files</h3>'))
        self.files_view = RecentFilesView()
        self.files_layout.addWidget(self.files_view)
        self.files_layout.addStretch(50)

    def on_browse_clicked(self):
        """Handle the browse button click to open file manager."""
        self.control_target.on_action_insert_images()

    def on_help_clicked(self):
        """Handle the help link click."""
        from beeref.help_dialog import HelpDialog
        HelpDialog(self)

    def show(self):
        files = BeeSettings().get_recent_files(existing_only=True)
        self.files_view.update_files(files)
        # Show recent files section if there are recent files
        if files and self.layout.indexOf(self.files_layout) < 0:
            # Insert recent files before the help link
            help_index = self.layout.indexOf(self.help_link)
            self.layout.insertLayout(help_index, self.files_layout)
        super().show()


class BeeProgressDialog(QtWidgets.QProgressDialog):

    def __init__(self, label, worker, maximum=0, parent=None):
        super().__init__(label, 'Cancel', 0, maximum, parent=parent)
        logger.debug('Initialised progress bar')
        self.setMinimumDuration(0)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setAutoReset(False)
        self.setAutoClose(False)
        worker.begin_processing.connect(self.on_begin_processing)
        worker.progress.connect(self.on_progress)
        worker.finished.connect(self.on_finished)
        self.canceled.connect(worker.on_canceled)

    def on_progress(self, value):
        logger.debug(f'Progress dialog: {value}')
        self.setValue(value)

    def on_begin_processing(self, value):
        logger.debug(f'Beginn progress dialog: {value}')
        self.setMaximum(value)

    def on_finished(self, filename, errors):
        logger.debug('Finished progress dialog')
        self.setValue(self.maximum())
        self.reset()
        self.hide()
        QtCore.QTimer.singleShot(100, self.deleteLater)


class DebugLogDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle(f'{constants.APPNAME} Debug Log')
        with open(logfile_name()) as f:
            self.log_txt = f.read()

        self.log = QtWidgets.QPlainTextEdit(self.log_txt)
        self.log.setReadOnly(True)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        self.copy_button = QtWidgets.QPushButton('Co&py To Clipboard')
        self.copy_button.released.connect(self.copy_to_clipboard)
        buttons.addButton(
            self.copy_button, QtWidgets.QDialogButtonBox.ButtonRole.ActionRole)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        name_widget = QtWidgets.QLabel(logfile_name())
        name_widget.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(name_widget)
        layout.addWidget(self.log)
        layout.addWidget(buttons)
        self.show()

    def copy_to_clipboard(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.log_txt)
