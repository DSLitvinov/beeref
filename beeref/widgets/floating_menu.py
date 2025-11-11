"""Floating menu widgets shown for single item selections."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Callable

from PyQt6 import QtCore, QtGui, QtWidgets

from beeref import constants


if TYPE_CHECKING:  # pragma: no cover - type checking only
    from beeref.view import BeeGraphicsView


class FloatingMenu(QtWidgets.QWidget):
    """Base widget for floating menus pinned to the bottom centre."""

    BOTTOM_MARGIN = 8

    def __init__(self, parent: QtWidgets.QWidget, view: "BeeGraphicsView"):
        super().__init__(parent)
        self.setObjectName("FloatingMenu")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint, True)
        self.setWindowFlag(QtCore.Qt.WindowType.ToolTip, False)
        self.view = view
        self.current_item: Optional[QtWidgets.QGraphicsItem] = None

        # Главный layout с равномерными отступами
        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setContentsMargins(12, 12, 12, 12)
        self._layout.setSpacing(0)

        # Контейнер для кнопок с равномерными вертикальными отступами
        self.button_container = QtWidgets.QWidget()
        self.button_container.setObjectName("FloatingMenuButtonContainer")
        
        # Горизонтальный layout для кнопок
        self.button_layout = QtWidgets.QHBoxLayout(self.button_container)
        self.button_layout.setContentsMargins(0, 0, 0, 0)  # Равномерные отступы
        self.button_layout.setSpacing(8)
        self.button_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        # Добавляем контейнер с кнопками в главный layout
        self._layout.addWidget(self.button_container)

        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.setStyleSheet(constants.get_floating_menu_style())

        self.hide()

    def add_widget(self, widget: QtWidgets.QWidget) -> QtWidgets.QWidget:
        widget.setParent(self.button_container)
        self.button_layout.addWidget(widget)
        return widget

    def add_button(
        self,
        text: str,
        icon: Optional[QtGui.QIcon] = None,
        callback: Optional[Callable[[], None]] = None,
        checkable: bool = False,
    ) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(text, self.button_container)
        button.setCheckable(checkable)
        if icon:
            button.setIcon(icon)
        button.setProperty("floatingButton", True)
        if callback:
            button.clicked.connect(callback)
        self.button_layout.addWidget(button)
        return button

    def add_separator(self) -> None:
        separator = QtWidgets.QFrame(self.button_container)
        separator.setObjectName("FloatingMenuSeparator")
        separator.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        separator.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        separator.setFixedWidth(1)
        self.button_layout.addWidget(separator)

    def show_for_item(self, item: QtWidgets.QGraphicsItem) -> None:
        self.current_item = item
        self.show_menu()

    def show_menu(self) -> None:
        self.adjustSize()
        self.show()
        self.raise_()
        self.update_position()
        # Ensure menu is on top after positioning
        self.raise_()

    def hide_menu(self) -> None:
        self.current_item = None
        self.hide()

    def update_position(self) -> None:
        if not self.isVisible():
            return

        parent = self.parentWidget()
        view = self.view
        if parent is None or view is None:
            return

        size = self.sizeHint()
        width = self.width() or size.width()
        height = self.height() or size.height()

        viewport = view.viewport()
        view_rect = viewport.rect()
        bottom_left_global = viewport.mapToGlobal(view_rect.bottomLeft())
        bottom_right_global = viewport.mapToGlobal(view_rect.bottomRight())

        bottom_left_parent = parent.mapFromGlobal(bottom_left_global)
        bottom_right_parent = parent.mapFromGlobal(bottom_right_global)

        available_width = bottom_right_parent.x() - bottom_left_parent.x()
        x = bottom_left_parent.x() + max(0, (available_width - width) // 2)
        x = max(bottom_left_parent.x(), min(x, bottom_right_parent.x() - width))

        y = bottom_left_parent.y() - height - self.BOTTOM_MARGIN

        self.move(x, y)