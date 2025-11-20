"""Floating menu for drawing items."""

from __future__ import annotations

import logging
from typing import Optional, TYPE_CHECKING

from PyQt6 import QtCore, QtGui, QtWidgets

from beeref import constants
from beeref import widgets
from beeref.assets import BeeAssets
from beeref.widgets.floating_menu import FloatingMenu

logger = logging.getLogger(__name__)

if TYPE_CHECKING:  # pragma: no cover - type checking only
    from beeref.view import BeeGraphicsView
    from beeref.items import BeeDrawItem


class UpwardComboBox(QtWidgets.QComboBox):
    """QComboBox that opens its dropdown menu upward."""
    
    def showPopup(self):
        """Override to show popup above the combobox."""
        super().showPopup()
        # Используем QTimer для получения popup после его создания
        QtCore.QTimer.singleShot(0, self._reposition_popup)
    
    def _reposition_popup(self):
        """Перемещает popup выше combobox."""
        # Ищем активный popup виджет
        popup = QtWidgets.QApplication.activePopupWidget()
        if not popup:
            # Альтернативный способ - найти через view
            view = self.view()
            if view:
                popup = view.parent()
                while popup and not isinstance(popup, QtWidgets.QFrame):
                    popup = popup.parent()
        
        if popup:
            # Получаем глобальную позицию combobox
            global_pos = self.mapToGlobal(QtCore.QPoint(0, 0))
            # Вычисляем новую позицию выше combobox
            popup_height = popup.height()
            new_y = global_pos.y() - popup_height
            popup.move(global_pos.x(), new_y)


class DrawFloatingMenu(FloatingMenu):
    """Floating menu for drawing tools."""

    def __init__(self, parent: QtWidgets.QWidget, view: "BeeGraphicsView"):
        super().__init__(parent, view)
        self.current_item: Optional["BeeDrawItem"] = None
        
        # Кнопка выбора цвета через colorpicker
        assets = BeeAssets()
        icons_path = assets.PATH.joinpath('icons')
        palette_icon = QtGui.QIcon(str(icons_path.joinpath('palette.svg')))
        
        self.color_btn = self.add_button(
            "",
            icon=palette_icon,
            callback=self._on_color_clicked,
        )
        self.color_btn.setToolTip("Color")
        
        # Combobox для выбора стиля линии
        self.add_separator()
        self.style_combo = self.add_style_combobox()
        
        # Селектор толщины пера
        self.add_separator()
        self.width_slider = self.add_width_slider()
        
        # Кнопка закрытия меню (отмена режима рисования)
        self.add_separator()
        close_icon = QtGui.QIcon(str(icons_path.joinpath('close.svg')))
        self.close_button = self.add_button(
            "",
            icon=close_icon,
            callback=self._on_close_clicked
        )
        self.close_button.setToolTip("Close")

    def add_style_combobox(self):
        """Добавляет combobox для выбора стиля линии."""
        assets = BeeAssets()
        icons_path = assets.PATH.joinpath('icons')
        
        # Загружаем иконки для стилей
        solid_icon = QtGui.QIcon(str(icons_path.joinpath('line-solid.svg')))
        dashed_icon = QtGui.QIcon(str(icons_path.joinpath('line-dashed.svg')))
        arrow_icon = QtGui.QIcon(str(icons_path.joinpath('line-arrow.svg')))
        arrow_left_icon = QtGui.QIcon(str(icons_path.joinpath('line-arrow-left.svg')))
        arrow_both_icon = QtGui.QIcon(str(icons_path.joinpath('line-arrow-both.svg')))
        
        combo = UpwardComboBox(self)
        combo.setObjectName("FloatingMenuLineStyle")
        combo.setMinimumWidth(40)
        combo.setIconSize(QtCore.QSize(32, 32))
        
        # Добавляем элементы с иконками
        combo.addItem(solid_icon, "", 'solid')
        combo.addItem(dashed_icon, "", 'dashed')
        combo.addItem(arrow_icon, "", 'arrow')
        combo.addItem(arrow_left_icon, "", '<-')
        combo.addItem(arrow_both_icon, "", '<->')
        # Устанавливаем иконки для элементов
        combo.setItemIcon(0, solid_icon)
        combo.setItemIcon(1, dashed_icon)
        combo.setItemIcon(2, arrow_icon)
        combo.setItemIcon(3, arrow_left_icon)
        combo.setItemIcon(4, arrow_both_icon)
        
        combo.setCurrentIndex(0)  # По умолчанию solid
        combo.currentIndexChanged.connect(self._on_style_changed)
        combo.setToolTip("Line style")
        
        self.add_widget(combo)
        return combo

    def _on_color_clicked(self) -> None:
        """Открывает диалог выбора цвета."""
        if not self.current_item:
            return
        
        initial = self.current_item.pen_color
        dialog = widgets.color_picker.ColorPickerDialog(self, initial)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        color = dialog.selectedColor()
        self.set_pen_color(color)

    def _on_style_changed(self, index: int) -> None:
        """Обработчик изменения стиля линии."""
        if not self.current_item:
            return
        style = self.style_combo.itemData(index)
        if style:
            self.set_pen_style(style)

    def add_width_slider(self):
        """Добавляет слайдер для выбора толщины пера."""
        container = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QtWidgets.QLabel("Width:")
        layout.addWidget(label)
        
        slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        slider.setRange(1, 20)
        slider.setValue(8)
        slider.valueChanged.connect(self.set_pen_width)
        layout.addWidget(slider)
        
        self.add_widget(container)
        return slider

    def show_for_item(self, item: "BeeDrawItem") -> None:
        """Показывает меню для выбранного элемента рисования."""
        self.current_item = item
        if item:
            self.width_slider.setValue(item.pen_width)
            # Устанавливаем текущий стиль в combobox
            style_index = self.style_combo.findData(item.pen_style)
            if style_index >= 0:
                self.style_combo.blockSignals(True)
                self.style_combo.setCurrentIndex(style_index)
                self.style_combo.blockSignals(False)
        super().show_for_item(item)

    def set_pen_color(self, color: QtGui.QColor):
        """Устанавливает цвет пера для выбранного элемента."""
        if self.current_item:
            self.current_item.set_pen_color(color)

    def set_pen_width(self, width: int):
        """Устанавливает толщину пера для выбранного элемента."""
        if self.current_item:
            self.current_item.set_pen_width(width)

    def set_pen_style(self, style: str):
        """Устанавливает стиль линии для выбранного элемента."""
        if self.current_item:
            self.current_item.set_pen_style(style)

    def _on_close_clicked(self) -> None:
        """Закрывает меню и отменяет режим рисования."""
        self.view.cancel_drawing_mode()
        self.hide_menu()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """Обрабатывает нажатия клавиш."""
        if event.key() == QtCore.Qt.Key.Key_Escape:
            # ESC закрывает меню и отменяет режим рисования
            self.view.cancel_drawing_mode()
            self.hide_menu()
            event.accept()
            return
        super().keyPressEvent(event)

