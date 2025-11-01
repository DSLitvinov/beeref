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

"""Custom title bar with Client Side Decorations for frameless windows."""

import logging
from typing import Optional

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

from beeref.constants import COLORS


logger = logging.getLogger(__name__)


class TitleBarButton(QtWidgets.QPushButton):
    """Custom button for CSD title bar."""
    
    def __init__(self, icon_char: Optional[str] = None, tooltip: Optional[str] = None, 
                 parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self._hovered = False
        
        if icon_char:
            self.setText(icon_char)
        
        if tooltip:
            self.setToolTip(tooltip)
            
        self.setFixedSize(40, 30)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Style
        self.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                color: rgb(200, 200, 200);
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 20);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 30);
            }
        """)
    
    def enterEvent(self, event):
        self._hovered = True
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self._hovered = False
        super().leaveEvent(event)


class TitleBar(QtWidgets.QWidget):
    """Custom title bar with minimize, maximize, and close buttons.
    
    This widget provides Client Side Decorations (CSD) for frameless windows,
    including window controls and drag-to-move functionality.
    """
    
    TITLE_BAR_HEIGHT = 30
    BTN_WIDTH = 40
    
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)
        self.parent_window = parent
        self._dragging = False
        self._drag_position: Optional[QtCore.QPoint] = None
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self) -> None:
        """Setup the title bar UI."""
        self.setFixedHeight(self.TITLE_BAR_HEIGHT)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        
        # Layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(0)
        
        # Title
        self.title_label = QtWidgets.QLabel()
        self.title_label.setStyleSheet("""
            QLabel {
                color: rgb(200, 200, 200);
                background-color: transparent;
                border: none;
            }
        """)
        layout.addWidget(self.title_label)
        layout.addStretch()
        
        # Window buttons
        self.minimize_btn = TitleBarButton("−", "Minimize")
        self.maximize_btn = TitleBarButton("□", "Maximize")
        self.close_btn = TitleBarButton("✕", "Close")
        
        # Style close button differently
        self.close_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                color: rgb(200, 200, 200);
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 20);
                color: white;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 20);
            }
        """)
        
        layout.addWidget(self.minimize_btn)
        layout.addWidget(self.maximize_btn)
        layout.addWidget(self.close_btn)
    
    def _connect_signals(self) -> None:
        """Connect button signals."""
        self.minimize_btn.clicked.connect(self._on_minimize)
        self.maximize_btn.clicked.connect(self._on_maximize_restore)
        self.close_btn.clicked.connect(self._on_close)
    
    def set_title(self, title: str) -> None:
        """Set the title text.
        
        :param title: Window title to display
        """
        self.title_label.setText(title)
    
    def _on_minimize(self) -> None:
        """Minimize the window."""
        self.parent_window.showMinimized()
    
    def _on_maximize_restore(self) -> None:
        """Toggle maximize/restore."""
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.maximize_btn.setText("□")
        else:
            self.parent_window.showMaximized()
            self.maximize_btn.setText("▢")
    
    def _on_close(self) -> None:
        """Close the window."""
        self.parent_window.close()
    
    def mousePressEvent(self, event) -> None:
        """Handle mouse press for dragging.
        
        :param event: Mouse event
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            self._drag_position = event.globalPosition().toPoint() - self.parent_window.frameGeometry().topLeft()
            event.accept()
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event) -> None:
        """Handle mouse move for dragging.
        
        :param event: Mouse event
        """
        if self._dragging and self._drag_position is not None:
            self.parent_window.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event) -> None:
        """Handle mouse release.
        
        :param event: Mouse event
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False
            self._drag_position = None
            event.accept()
        super().mouseReleaseEvent(event)
    
    def mouseDoubleClickEvent(self, event) -> None:
        """Handle double click to maximize/restore.
        
        :param event: Mouse event
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self._on_maximize_restore()
            event.accept()
        super().mouseDoubleClickEvent(event)
    
    def paintEvent(self, event) -> None:
        """Paint the title bar background.
        
        :param event: Paint event
        """
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        # Background
        bg_color = QtGui.QColor(*COLORS['Scene:Canvas'])
        painter.fillRect(self.rect(), bg_color)
        

