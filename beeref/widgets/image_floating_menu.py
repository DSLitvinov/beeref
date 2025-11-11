"""Floating menu shown when a single image item is selected."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6 import QtWidgets

from beeref.widgets.floating_menu import FloatingMenu

if TYPE_CHECKING:  # pragma: no cover
    from beeref.view import BeeGraphicsView
    from beeref.items import BeePixmapItem


class ImageFloatingMenu(FloatingMenu):
    """Contextual floating toolbar for image items."""

    def __init__(self, parent: QtWidgets.QWidget, view: "BeeGraphicsView"):
        super().__init__(parent, view)

        self.opacity_btn = self.add_button(
            "Opacity",
            callback=self.view.on_action_change_opacity,
        )
        self.add_separator()

        self.grayscale_btn = self.add_button(
            "Grayscale",
            callback=self.view.on_action_grayscale,
            checkable=True,
        )
        self.add_button(
            "Color Gamut",
            callback=self.view.on_action_show_color_gamut,
        )
        self.add_separator()

        self.add_button(
            "Flip H",
            callback=self.view.on_action_flip_horizontally,
        )
        self.add_button(
            "Flip V",
            callback=self.view.on_action_flip_vertically,
        )
        self.add_separator()

        self.add_button(
            "Delete",
            callback=self.view.on_action_delete_items,
        )

    def show_for_item(self, item: "BeePixmapItem") -> None:
        self.grayscale_btn.setChecked(getattr(item, "grayscale", False))
        super().show_for_item(item)
