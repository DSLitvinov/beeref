"""Floating menu shown when a single GIF item is selected."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from PyQt6 import QtGui, QtWidgets

from beeref import constants
from beeref.assets import BeeAssets
from beeref.widgets.floating_menu import FloatingMenu

logger = logging.getLogger(__name__)

if TYPE_CHECKING:  # pragma: no cover
    from beeref.view import BeeGraphicsView
    from beeref.items import BeeGifItem
    from beeref.widgets.gif_frames_menu import GifFramesMenu


class GifFloatingMenu(FloatingMenu):
    """Contextual floating toolbar for GIF items."""

    SPEED_VALUES = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]

    def __init__(self, parent: QtWidgets.QWidget, view: "BeeGraphicsView"):
        super().__init__(parent, view)
        
        # Инициализируем меню кадров после создания виджета
        self.frames_menu: Optional["GifFramesMenu"] = None
        try:
            from beeref.widgets.gif_frames_menu import GifFramesMenu
            self.frames_menu = GifFramesMenu(parent, view, self)
        except Exception as e:
            logger.warning(f'Failed to initialize frames menu: {e}')
            self.frames_menu = None

        # Загружаем иконки
        assets = BeeAssets()
        icons_path = assets.PATH.joinpath('icons')
        prev_frame_icon = QtGui.QIcon(str(icons_path.joinpath('prev-frame.svg')))
        play_icon = QtGui.QIcon(str(icons_path.joinpath('play.svg')))
        pause_icon = QtGui.QIcon(str(icons_path.joinpath('pause.svg')))
        next_frame_icon = QtGui.QIcon(str(icons_path.joinpath('next-frame.svg')))
        frames_icon = QtGui.QIcon(str(icons_path.joinpath('frames.svg')))

        # Combobox для выбора скорости воспроизведения
        self.speed_combo = QtWidgets.QComboBox(self)
        self.speed_combo.setObjectName("FloatingMenuGifSpeed")
        # Используем общий стиль из constants.py, но устанавливаем фиксированную ширину
        self.speed_combo.setFixedWidth(40)  # Фиксированная ширина для самого combobox
        for speed in self.SPEED_VALUES:
            # Отображаем скорость как "0.25x", "0.5x", "1x", "2x" и т.д.
            if speed < 1.0:
                label = f"{speed:.2f}x"
            else:
                # Для скоростей >= 1.0 убираем лишние нули
                speed_str = f"{speed:.2f}".rstrip('0').rstrip('.')
                label = f"{speed_str}x"
            self.speed_combo.addItem(label, speed)
        # Устанавливаем значение по умолчанию (1.0x)
        default_index = self.SPEED_VALUES.index(1.0)
        self.speed_combo.setCurrentIndex(default_index)
        self.speed_combo.currentIndexChanged.connect(self._on_speed_changed)
        self.speed_combo.setToolTip("Playback speed")
        self.add_widget(self.speed_combo)
        # Устанавливаем размер после добавления в layout для гарантированного применения
        self.speed_combo.setFixedWidth(40)
        self.speed_combo.setMinimumWidth(40)
        self.speed_combo.setMaximumWidth(40)

        # Кнопка "Кадр назад"
        self.prev_frame_btn = self.add_button(
            "",
            icon=prev_frame_icon,
            callback=self.on_previous_frame,
        )
        self.prev_frame_btn.setToolTip("Previous frame")

        # Кнопка Play/Pause
        self.play_pause_btn = self.add_button(
            "",
            icon=play_icon,
            callback=self.on_toggle_play_pause,
        )
        self.play_pause_btn.setToolTip("Play/Pause")
        self.play_icon = play_icon
        self.pause_icon = pause_icon

        # Кнопка "Кадр вперед"
        self.next_frame_btn = self.add_button(
            "",
            icon=next_frame_icon,
            callback=self.on_next_frame,
        )
        self.next_frame_btn.setToolTip("Next frame")

        # Кнопка для открытия меню кадров
        self.frames_btn = self.add_button(
            "",
            icon=frames_icon,
            callback=self.on_toggle_frames_menu,
        )
        self.frames_btn.setToolTip("Show frames timeline")

    def show_for_item(self, item: "BeeGifItem") -> None:
        super().show_for_item(item)
        # Обновляем состояние кнопки Play/Pause
        self.update_play_pause_button()
        # Обновляем скорость воспроизведения в combobox
        self.update_speed_combo()
        # Скрываем меню кадров при показе основного меню
        if self.frames_menu:
            self.frames_menu.hide_menu()

    def update_speed_combo(self) -> None:
        """Обновляет значение скорости в combobox в соответствии с текущим элементом."""
        if self.current_item and hasattr(self.current_item, 'get_speed'):
            current_speed = self.current_item.get_speed()
            # Находим ближайшее значение из списка
            closest_speed = min(self.SPEED_VALUES, key=lambda x: abs(x - current_speed))
            index = self.SPEED_VALUES.index(closest_speed)
            self.speed_combo.blockSignals(True)
            self.speed_combo.setCurrentIndex(index)
            self.speed_combo.blockSignals(False)

    def _on_speed_changed(self, index: int) -> None:
        """Обработчик изменения скорости воспроизведения."""
        if self.current_item and hasattr(self.current_item, 'set_speed'):
            speed = self.speed_combo.currentData()
            if speed is not None:
                self.current_item.set_speed(speed)

    def update_play_pause_button(self) -> None:
        """Обновляет иконку кнопки Play/Pause в зависимости от состояния."""
        if self.current_item and hasattr(self.current_item, 'is_playing'):
            if self.current_item.is_playing:
                self.play_pause_btn.setIcon(self.pause_icon)
                self.play_pause_btn.setToolTip("Pause")
            else:
                self.play_pause_btn.setIcon(self.play_icon)
                self.play_pause_btn.setToolTip("Play")

    def on_toggle_play_pause(self) -> None:
        """Переключает воспроизведение/паузу GIF."""
        if self.current_item and hasattr(self.current_item, 'toggle_animation'):
            self.current_item.toggle_animation()
            self.update_play_pause_button()

    def on_previous_frame(self) -> None:
        """Переходит к предыдущему кадру."""
        if self.current_item and hasattr(self.current_item, 'previous_frame'):
            self.current_item.previous_frame()
            self.update_play_pause_button()
            # Обновляем выделение в меню кадров если оно открыто
            if self.frames_menu and self.frames_menu.isVisible():
                self.frames_menu.load_frames(self.current_item)

    def on_next_frame(self) -> None:
        """Переходит к следующему кадру."""
        if self.current_item and hasattr(self.current_item, 'next_frame'):
            self.current_item.next_frame()
            self.update_play_pause_button()
            # Обновляем выделение в меню кадров если оно открыто
            if self.frames_menu and self.frames_menu.isVisible():
                self.frames_menu.load_frames(self.current_item)

    def on_toggle_frames_menu(self) -> None:
        """Переключает видимость меню кадров."""
        if self.current_item and self.frames_menu:
            self.frames_menu.toggle_menu(self.current_item)

    def hide_menu(self) -> None:
        """Скрывает меню и меню кадров."""
        if self.frames_menu:
            self.frames_menu.hide_menu()
        super().hide_menu()

    def update_position(self) -> None:
        """Обновляет позицию меню и меню кадров."""
        super().update_position()
        if self.frames_menu and self.frames_menu.isVisible():
            self.frames_menu.update_position()

