import os
from unittest.mock import MagicMock

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt

from beeref.config import logfile_name
from beeref.widgets import DebugLogDialog, RecentFilesModel


def test_debug_log_dialog(qtbot, settings, view):
    # Ensure the log directory exists
    log_path = logfile_name()
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    with open(log_path, 'w') as f:
        f.write('my log output')

    dialog = DebugLogDialog(view)
    dialog.show()
    qtbot.addWidget(dialog)
    assert dialog.log.toPlainText() == 'my log output'
    qtbot.mouseClick(dialog.copy_button, Qt.MouseButton.LeftButton)
    clipboard = QtWidgets.QApplication.clipboard()
    assert clipboard.text() == 'my log output'


def test_recent_files_model_rowcount(view):
    model = RecentFilesModel(['foo.png', 'bar.png'])
    assert model.rowCount(None) == 2


def test_recent_files_model_data_diplayrole(view):
    model = RecentFilesModel(['foo.png', 'bar.png'])
    index = MagicMock()
    index.row.return_value = 1
    assert model.data(index, QtCore.Qt.ItemDataRole.DisplayRole) == 'bar.png'


def test_recent_files_model_data_fontrole(view):
    model = RecentFilesModel(['foo.png', 'bar.png'])
    index = MagicMock()
    index.row.return_value = 1
    font = model.data(index, QtCore.Qt.ItemDataRole.FontRole)
    assert font.underline() is True
