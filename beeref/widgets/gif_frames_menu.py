"""Floating menu showing GIF frames timeline."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from PyQt6 import QtCore, QtGui, QtWidgets

from beeref import constants

if TYPE_CHECKING:  # pragma: no cover
    from beeref.view import BeeGraphicsView
    from beeref.items import BeeGifItem

logger = logging.getLogger(__name__)


class GifFrameThumbnail(QtWidgets.QWidget):
    """Виджет для отображения одного кадра GIF."""
    
    FRAME_SIZE = 96  # Размер миниатюры кадра
    
    def __init__(self, frame_number: int, pixmap: QtGui.QPixmap, 
                 delay_ms: int, frames_menu: "GifFramesMenu", parent=None):
        super().__init__(parent)
        self.frame_number = frame_number
        self.pixmap = pixmap
        self.delay_ms = delay_ms
        self.is_selected = False
        self.frames_menu = frames_menu  # Сохраняем ссылку на меню кадров
        
        self.setFixedSize(self.FRAME_SIZE + 8, self.FRAME_SIZE + 24)
        self.setToolTip(f"Frame: {frame_number}\nDelay: {delay_ms / 1000:.2f}s")
        self.drag_start_position = None
        self.is_dragging = False
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        
        # Рамка выделения
        if self.is_selected:
            pen = QtGui.QPen(QtGui.QColor(*constants.COLORS['Scene:Selection']))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.setBrush(QtGui.QBrush())
            painter.drawRect(2, 2, self.FRAME_SIZE + 4, self.FRAME_SIZE + 4)
        
        # Миниатюра кадра
        scaled_pixmap = self.pixmap.scaled(
            self.FRAME_SIZE, self.FRAME_SIZE,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )
        x = (self.width() - scaled_pixmap.width()) // 2
        y = 4
        painter.drawPixmap(x, y, scaled_pixmap)
        
        # Номер кадра
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        text_rect = QtCore.QRect(0, self.FRAME_SIZE + 8, self.width(), 16)
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, 
                        str(self.frame_number))
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            # Сохраняем позицию начала перетаскивания
            self.drag_start_position = event.position().toPoint()
            self.is_dragging = False
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Обработка начала перетаскивания кадра."""
        if not (event.buttons() & QtCore.Qt.MouseButton.LeftButton):
            return
        
        if self.drag_start_position is None:
            return
        
        # Проверяем, достаточно ли переместили мышь для начала drag
        if ((event.position().toPoint() - self.drag_start_position).manhattanLength() 
                < QtWidgets.QApplication.startDragDistance()):
            return
        
        # Помечаем, что началось перетаскивание
        self.is_dragging = True
        
        # Создаем QDrag объект
        drag = QtGui.QDrag(self)
        mime_data = QtCore.QMimeData()
        
        # Конвертируем pixmap в QImage для передачи через drag
        image = self.pixmap.toImage()
        mime_data.setImageData(image)
        
        drag.setMimeData(mime_data)
        
        # Устанавливаем визуальное представление при перетаскивании
        # Используем оригинальный pixmap, но уменьшенный для предпросмотра
        preview_pixmap = self.pixmap.scaled(
            128, 128,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )
        drag.setPixmap(preview_pixmap)
        drag.setHotSpot(event.position().toPoint() - self.drag_start_position)
        
        # Начинаем drag операцию
        drag.exec(QtCore.Qt.DropAction.CopyAction)
        
        # Сбрасываем состояние после завершения drag
        self.drag_start_position = None
        self.is_dragging = False
        
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Обработка клика по кадру (если не было перетаскивания)."""
        if (event.button() == QtCore.Qt.MouseButton.LeftButton 
                and not self.is_dragging 
                and self.drag_start_position is not None):
            # Если не было перетаскивания, выбираем кадр
            if self.frames_menu:
                self.frames_menu.select_frame(self.frame_number)
        
        self.drag_start_position = None
        self.is_dragging = False
        super().mouseReleaseEvent(event)


class GifFramesMenu(QtWidgets.QWidget):
    """Плавающее меню с кадрами GIF."""
    
    def __init__(self, parent: QtWidgets.QWidget, view: "BeeGraphicsView",
                 gif_menu: "GifFloatingMenu"):
        super().__init__(parent)
        self.setObjectName("GifFramesMenu")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint, True)
        self.setWindowFlag(QtCore.Qt.WindowType.ToolTip, False)
        
        self.view = view
        self.gif_menu = gif_menu
        self.current_item: Optional["BeeGifItem"] = None
        
        # Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        # Scroll area для кадров
        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 4px;
                background-color: rgba(40, 40, 40, 240);
            }
            QScrollBar:horizontal {
                height: 8px;
                background: rgba(60, 60, 60, 200);
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(140, 140, 140, 200);
                border-radius: 4px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background: rgba(180, 180, 180, 200);
            }
        """)
        
        # Контейнер для кадров
        self.frames_container = QtWidgets.QWidget()
        self.frames_layout = QtWidgets.QHBoxLayout(self.frames_container)
        self.frames_layout.setContentsMargins(4, 4, 4, 4)
        self.frames_layout.setSpacing(4)
        
        scroll_area.setWidget(self.frames_container)
        layout.addWidget(scroll_area)
        
        # Применяем стиль с скруглением как у других плавающих панелей
        bg = constants.COLORS['Active:Window']
        border = constants.COLORS['Active:Base']
        bg_r, bg_g, bg_b = bg[:3]
        border_r, border_g, border_b = border[:3]
        self.setStyleSheet(f"""
            QWidget#GifFramesMenu {{
                background-color: rgba({bg_r}, {bg_g}, {bg_b}, 255);
                border-radius: 8px;
                border: 1px solid rgba({border_r}, {border_g}, {border_b}, 255);
            }}
        """)
        self.hide()
        
        self.frame_widgets = []
    
    def load_frames(self, item: "BeeGifItem"):
        """Загружает все кадры из GIF."""
        self.current_item = item
        self.frame_widgets.clear()
        
        # Очищаем старые виджеты
        while self.frames_layout.count():
            child = self.frames_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not item.movie or item.frame_count == 0:
            return
        
        # Сохраняем текущий кадр
        current_frame = item.current_frame
        was_playing = item.is_playing
        if was_playing:
            item.pause_animation()
        
        # Загружаем все кадры
        for frame_num in range(item.frame_count):
            if item.movie.jumpToFrame(frame_num):
                pixmap = item.movie.currentPixmap()
                if not pixmap.isNull():
                    # Получаем задержку кадра (в миллисекундах)
                    delay_ms = item.movie.nextFrameDelay()
                    if delay_ms <= 0:
                        delay_ms = 100  # Значение по умолчанию
                    
                    frame_widget = GifFrameThumbnail(
                        frame_num + 1, pixmap, delay_ms, self, self.frames_container)
                    frame_widget.is_selected = (frame_num == current_frame)
                    self.frames_layout.addWidget(frame_widget)
                    self.frame_widgets.append(frame_widget)
        
        # Восстанавливаем текущий кадр
        if item.movie.jumpToFrame(current_frame):
            item.current_frame = current_frame
            pixmap = item.movie.currentPixmap()
            if not pixmap.isNull():
                item.setPixmap(pixmap)
        
        if was_playing:
            item.play_animation()
        
        self.frames_container.adjustSize()
        self.adjustSize()
    
    def select_frame(self, frame_number: int):
        """Выбирает кадр и отображает его в item."""
        if not self.current_item or not self.current_item.movie:
            return
        
        frame_index = frame_number - 1  # Номера кадров начинаются с 1
        
        # Обновляем выделение в виджетах
        for i, widget in enumerate(self.frame_widgets):
            widget.is_selected = (i == frame_index)
            widget.update()
        
        # Переходим к выбранному кадру в item
        was_playing = self.current_item.is_playing
        if was_playing:
            self.current_item.pause_animation()
        
        if self.current_item.movie.jumpToFrame(frame_index):
            self.current_item.current_frame = frame_index
            pixmap = self.current_item.movie.currentPixmap()
            if not pixmap.isNull():
                self.current_item.setPixmap(pixmap)
                self.current_item.update()
        
        if was_playing:
            self.current_item.play_animation()
    
    def show_menu(self):
        """Показывает меню над основным GIF меню."""
        if not self.current_item:
            return
        
        self.adjustSize()
        self.show()
        self.raise_()
        self.update_position()
        self.raise_()
    
    def update_position(self):
        """Обновляет позицию меню над основным GIF меню."""
        if not self.isVisible():
            return
        
        parent = self.parentWidget()
        view = self.view
        if parent is None or view is None:
            return
        
        viewport = view.viewport()
        if viewport is None:
            return
        
        view_rect = viewport.rect()
        bottom_left_global = viewport.mapToGlobal(view_rect.bottomLeft())
        bottom_right_global = viewport.mapToGlobal(view_rect.bottomRight())
        
        bottom_left_parent = parent.mapFromGlobal(bottom_left_global)
        bottom_right_parent = parent.mapFromGlobal(bottom_right_global)
        
        # Ширина на всю ширину холста
        available_width = bottom_right_parent.x() - bottom_left_parent.x()
        
        # Устанавливаем ширину на всю ширину
        self.setFixedWidth(available_width)
        
        # Получаем естественную высоту контента
        self.adjustSize()
        height = self.height()
        
        # Позиционируем над основным меню с отступом 8px
        if self.gif_menu.isVisible():
            gif_menu_pos = self.gif_menu.pos()
            y = gif_menu_pos.y() - height - 8
        else:
            # Если основное меню не видно, позиционируем относительно viewport
            y = bottom_left_parent.y() - height - 8
        
        # Проверяем, не выходит ли за границы экрана
        if y < 0:
            if self.gif_menu.isVisible():
                y = self.gif_menu.pos().y() + self.gif_menu.height() + 8
            else:
                y = 8
        
        # Позиционируем по левому краю
        x = bottom_left_parent.x()
        
        self.move(x, y)
    
    def hide_menu(self):
        """Скрывает меню."""
        self.current_item = None
        self.hide()
    
    def toggle_menu(self, item: "BeeGifItem"):
        """Переключает видимость меню."""
        if self.isVisible():
            self.hide_menu()
        else:
            self.load_frames(item)
            self.show_menu()

