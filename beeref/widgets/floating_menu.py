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
    CORNER_RADIUS = 8

    def __init__(self, parent: QtWidgets.QWidget, view: "BeeGraphicsView"):
        # Create as independent window to prevent event blocking
        super().__init__(None)
        self.setObjectName("FloatingMenu")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        # Make it a tool window that stays on top
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint, True)
        self.setWindowFlag(QtCore.Qt.WindowType.Tool, True)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)
        # Store parent for positioning
        self._parent_widget = parent
        self.view = view
        self.current_item: Optional[QtWidgets.QGraphicsItem] = None
        
        # Cache for update_position optimization
        self._cached_position: Optional[QtCore.QPoint] = None
        self._cached_viewport_size: Optional[QtCore.QSize] = None
        self._cached_window_pos: Optional[QtCore.QPoint] = None

        # Таймер для отслеживания перемещения главного окна
        self._position_timer = QtCore.QTimer(self)
        self._position_timer.timeout.connect(self._check_window_position)
        self._position_timer.setInterval(50)  # Проверка каждые 50мс

        # Main layout with uniform spacing
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(8, 6, 8, 6)
        self._layout.setSpacing(6)
        self._layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.setStyleSheet(constants.get_floating_menu_style())

        self.hide()

    def _check_window_position(self) -> None:
        """Проверяет позицию viewport и обновляет позицию меню при необходимости."""
        if not self.isVisible():
            return
        
        view = self.view
        if view is None:
            return
        
        viewport = view.viewport()
        if viewport is None:
            return
        
        # Получаем позицию viewport в глобальных координатах
        view_rect = viewport.rect()
        current_viewport_pos = viewport.mapToGlobal(view_rect.topLeft())
        
        # Если позиция viewport изменилась, обновляем позицию меню
        if self._cached_window_pos is not None and self._cached_window_pos != current_viewport_pos:
            self.update_position()
        
        self._cached_window_pos = current_viewport_pos

    def _apply_rounded_mask(self) -> None:
        """
        Применяет закругленную маску к виджету с антиалиасингом.
        Реализация на основе подхода из статьи VK Teams.
        """
        size = self.size()
        if size.width() == 0 or size.height() == 0:
            return
        
        # Для более плавного сглаживания используем QBitmap с антиалиасингом
        # Создаем изображение с увеличенным разрешением (как в статье)
        scale_factor = 2
        scaled_size = QtCore.QSize(
            int(size.width() * scale_factor),
            int(size.height() * scale_factor)
        )
        
        # Создаем QPixmap для рисования с антиалиасингом
        pixmap = QtGui.QPixmap(scaled_size)
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(QtCore.Qt.GlobalColor.black)  # Черный для маски
        
        # Рисуем закругленный прямоугольник на увеличенном разрешении
        scaled_rect = QtCore.QRectF(0, 0, scaled_size.width(), scaled_size.height())
        scaled_radius = self.CORNER_RADIUS * scale_factor
        painter.drawRoundedRect(scaled_rect, scaled_radius, scaled_radius)
        painter.end()
        
        # Масштабируем обратно с сглаживанием
        pixmap = pixmap.scaled(
            size,
            QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )
        
        # Преобразуем в QBitmap для маски
        # В маске: непрозрачные пиксели = видимые области, прозрачные = невидимые
        image = pixmap.toImage()
        # Создаем маску из непрозрачных пикселей
        bitmap = QtGui.QBitmap.fromImage(image.createAlphaMask())
        
        # Применяем маску
        self.setMask(bitmap)

    def add_widget(self, widget: QtWidgets.QWidget) -> QtWidgets.QWidget:
        widget.setParent(self)
        self._layout.addWidget(widget)
        return widget

    def add_button(
        self,
        text: str,
        icon: Optional[QtGui.QIcon] = None,
        callback: Optional[Callable[[], None]] = None,
        checkable: bool = False,
    ) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(text, self)
        button.setCheckable(checkable)
        if icon:
            button.setIcon(icon)
        button.setProperty("floatingButton", True)
        if callback:
            # Connect directly - button events are handled independently
            button.clicked.connect(callback)
        self._layout.addWidget(button)
        return button

    def add_separator(self) -> None:
        separator = QtWidgets.QFrame(self)
        separator.setObjectName("FloatingMenuSeparator")
        separator.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        separator.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        separator.setFixedWidth(1)
        self._layout.addWidget(separator)

    def show_for_item(self, item: QtWidgets.QGraphicsItem) -> None:
        self.current_item = item
        self.show_menu()

    def show_menu(self) -> None:
        self.adjustSize()
        self._apply_rounded_mask()
        self.show()
        self.raise_()
        # Reset cache when showing menu to ensure position update
        self._cached_position = None
        self._cached_viewport_size = None
        self._cached_window_pos = None
        self.update_position()
        # Запускаем таймер для отслеживания перемещения окна
        self._position_timer.start()
        # Ensure menu is on top after positioning
        self.raise_()
        # Возвращаем фокус view, чтобы события клавиатуры обрабатывались правильно
        # FloatingMenu не должен перехватывать фокус, так как он имеет NoFocus
        if self.view:
            self.view.setFocus()

    def hide_menu(self) -> None:
        self.current_item = None
        # Останавливаем таймер
        self._position_timer.stop()
        # Clear cache when hiding menu
        self._cached_position = None
        self._cached_viewport_size = None
        self._cached_window_pos = None
        self.hide()

    def update_position(self) -> None:
        if not self.isVisible():
            return

        parent = self._parent_widget
        view = self.view
        if parent is None or view is None:
            return

        viewport = view.viewport()
        if viewport is None:
            return

        view_rect = viewport.rect()
        viewport_size = view_rect.size()
        
        # Получаем текущую позицию viewport для проверки изменений
        current_viewport_pos = viewport.mapToGlobal(view_rect.topLeft())
        
        # Check if viewport size and position changed
        if (self._cached_viewport_size is not None and 
            self._cached_viewport_size == viewport_size and
            self._cached_window_pos is not None and
            self._cached_window_pos == current_viewport_pos and
            self._cached_position is not None):
            # If viewport size and position haven't changed, check menu position
            current_pos = self.pos()
            if current_pos == self._cached_position:
                # Position hasn't changed, skip update
                return

        size = self.sizeHint()
        width = self.width() or size.width()
        height = self.height() or size.height()

        # Calculate position in global coordinates (independent window)
        top_left_global = viewport.mapToGlobal(view_rect.topLeft())
        bottom_left_global = viewport.mapToGlobal(view_rect.bottomLeft())
        bottom_right_global = viewport.mapToGlobal(view_rect.bottomRight())
        top_right_global = viewport.mapToGlobal(view_rect.topRight())

        # Получаем границы viewport в глобальных координатах
        viewport_left = top_left_global.x()
        viewport_right = top_right_global.x()
        viewport_top = top_left_global.y()
        viewport_bottom = bottom_left_global.y()
        viewport_width = viewport_right - viewport_left

        # Вычисляем позицию по X (центрируем, но не выходим за границы)
        x = viewport_left + max(0, (viewport_width - width) // 2)
        # Ограничиваем, чтобы меню не выходило за левую и правую границы
        x = max(viewport_left, min(x, viewport_right - width))

        # Вычисляем позицию по Y (снизу с отступом)
        y = viewport_bottom - height - self.BOTTOM_MARGIN
        # Ограничиваем, чтобы меню не выходило за верхнюю границу
        # Если меню не помещается снизу, размещаем его сверху
        if y < viewport_top:
            y = viewport_top + self.BOTTOM_MARGIN
        # Также проверяем, что меню не выходит за нижнюю границу
        if y + height > viewport_bottom:
            y = viewport_bottom - height - self.BOTTOM_MARGIN
            # Если и так не помещается, размещаем сверху
            if y < viewport_top:
                y = viewport_top + self.BOTTOM_MARGIN

        new_position = QtCore.QPoint(x, y)
        
        # Update position only if it actually changed
        if self._cached_position != new_position:
            self.move(new_position)
            self._cached_position = new_position
            self._cached_viewport_size = viewport_size
            self._cached_window_pos = current_viewport_pos
            # Обновляем маску после изменения размера/позиции
            self._apply_rounded_mask()

    def parentWidget(self):
        """Override to return stored parent widget for compatibility."""
        return self._parent_widget

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        """Intercept mouse events to prevent them from reaching view."""
        # Accept event to prevent propagation
        event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        """Intercept mouse events to prevent them from reaching view."""
        event.accept()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        """Intercept mouse events to prevent them from reaching view."""
        event.accept()
        super().mouseReleaseEvent(event)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """Обновляет маску при изменении размера виджета."""
        super().resizeEvent(event)
        self._apply_rounded_mask()
