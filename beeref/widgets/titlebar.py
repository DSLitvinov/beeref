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

from beeref.constants import COLORS, get_csd_button_style, get_csd_close_button_style, get_csd_title_style


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
        self.setStyleSheet(get_csd_button_style())
    
    def enterEvent(self, event):
        self._hovered = True
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self._hovered = False
        super().leaveEvent(event)


class CloseButton(QtWidgets.QPushButton):
    """Close button for CSD title bar with special styling."""
    
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self.setText("✕")
        self.setToolTip("Close")
        
        self.setFixedSize(40, 30)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Style with red hover
        self.setStyleSheet(get_csd_close_button_style())
    
    def enterEvent(self, event):
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        super().leaveEvent(event)


class BaseTitleBar(QtWidgets.QWidget):
    """Base class for all CSD title bars with common functionality.
    
    Provides drag-to-move, background painting, and common UI setup.
    Subclasses should implement _setup_buttons() to add specific buttons.
    """
    
    TITLE_BAR_HEIGHT = 30
    BTN_WIDTH = 40
    
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)
        self.parent_window = parent
        self._dragging = False
        self._drag_position: Optional[QtCore.QPoint] = None
        
        self._setup_ui()
        self._setup_buttons()
        self._connect_signals()
    
    def _setup_ui(self) -> None:
        """Setup the title bar UI."""
        self.setFixedHeight(self.TITLE_BAR_HEIGHT)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        
        # Layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(0)
        
        # Title label
        self.title_label = QtWidgets.QLabel()
        self.title_label.setStyleSheet(get_csd_title_style())
        layout.addWidget(self.title_label)
        layout.addStretch()
        
        # Buttons will be added by _setup_buttons() in subclasses
        self._buttons_layout = layout
    
    def _setup_buttons(self) -> None:
        """Setup buttons. Must be implemented by subclasses.
        
        Subclasses should add buttons to self._buttons_layout.
        """
        raise NotImplementedError("Subclasses must implement _setup_buttons()")
    
    def _connect_signals(self) -> None:
        """Connect button signals. Override in subclasses if needed."""
        pass
    
    def set_title(self, title: str) -> None:
        """Set the title text.
        
        :param title: Window title to display
        """
        self.title_label.setText(title)
    
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
    
    def _on_maximize_restore(self) -> None:
        """Toggle maximize/restore. Override if not applicable."""
        pass
    
    def paintEvent(self, event) -> None:
        """Paint the title bar background.
        
        :param event: Paint event
        """
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        # Background
        bg_color = QtGui.QColor(*COLORS['Scene:Canvas'])
        painter.fillRect(self.rect(), bg_color)


class TitleBar(BaseTitleBar):
    """Title bar for main windows with minimize, maximize, and close buttons.
    
    Provides full window controls for main application windows.
    """
    
    def _setup_buttons(self) -> None:
        """Setup window control buttons."""
        # Window buttons
        self.minimize_btn = TitleBarButton("−", "Minimize")
        self.maximize_btn = TitleBarButton("□", "Maximize")
        self.close_btn = CloseButton()
        
        self._buttons_layout.addWidget(self.minimize_btn)
        self._buttons_layout.addWidget(self.maximize_btn)
        self._buttons_layout.addWidget(self.close_btn)
    
    def _connect_signals(self) -> None:
        """Connect button signals."""
        self.minimize_btn.clicked.connect(self._on_minimize)
        self.maximize_btn.clicked.connect(self._on_maximize_restore)
        self.close_btn.clicked.connect(self._on_close)
    
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


class DialogTitleBar(BaseTitleBar):
    """Simplified title bar for dialogs with only close button."""
    
    def _setup_buttons(self) -> None:
        """Setup close button only."""
        self.close_btn = CloseButton()
        self._buttons_layout.addWidget(self.close_btn)
    
    def _connect_signals(self) -> None:
        """Connect button signals."""
        self.close_btn.clicked.connect(self._on_close)
