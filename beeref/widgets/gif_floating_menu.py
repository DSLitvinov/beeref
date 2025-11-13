"""Floating menu shown when a single GIF item is selected."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6 import QtWidgets

from beeref.widgets.floating_menu import FloatingMenu

if TYPE_CHECKING:  # pragma: no cover
    from beeref.view import BeeGraphicsView
    from beeref.items import BeeGifItem


class GifFloatingMenu(FloatingMenu):
    """Contextual floating toolbar for GIF items."""

    def __init__(self, parent: QtWidgets.QWidget, view: "BeeGraphicsView"):
        super().__init__(parent, view)

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

