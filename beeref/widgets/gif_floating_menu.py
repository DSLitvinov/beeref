"""Floating menu shown when a single GIF item is selected."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6 import QtWidgets

from beeref import constants
from beeref.widgets.floating_menu import FloatingMenu

if TYPE_CHECKING:  # pragma: no cover
    from beeref.view import BeeGraphicsView
    from beeref.items import BeeGifItem


class GifFloatingMenu(FloatingMenu):
    """Contextual floating toolbar for GIF items."""

    SPEED_VALUES = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]

    def __init__(self, parent: QtWidgets.QWidget, view: "BeeGraphicsView"):
        super().__init__(parent, view)

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
            "◀◀",
            callback=self.on_previous_frame,
        )
        self.prev_frame_btn.setToolTip("Previous frame")

        # Кнопка Play/Pause
        self.play_pause_btn = self.add_button(
            "▶",
            callback=self.on_toggle_play_pause,
        )
        self.play_pause_btn.setToolTip("Play/Pause")

        # Кнопка "Кадр вперед"
        self.next_frame_btn = self.add_button(
            "▶▶",
            callback=self.on_next_frame,
        )
        self.next_frame_btn.setToolTip("Next frame")

    def show_for_item(self, item: "BeeGifItem") -> None:
        super().show_for_item(item)
        # Обновляем состояние кнопки Play/Pause
        self.update_play_pause_button()
        # Обновляем скорость воспроизведения в combobox
        self.update_speed_combo()

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
        """Обновляет текст кнопки Play/Pause в зависимости от состояния."""
        if self.current_item and hasattr(self.current_item, 'is_playing'):
            if self.current_item.is_playing:
                self.play_pause_btn.setText("⏸")
                self.play_pause_btn.setToolTip("Pause")
            else:
                self.play_pause_btn.setText("▶")
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

    def on_next_frame(self) -> None:
        """Переходит к следующему кадру."""
        if self.current_item and hasattr(self.current_item, 'next_frame'):
            self.current_item.next_frame()
            self.update_play_pause_button()

