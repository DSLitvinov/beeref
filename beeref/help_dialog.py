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

from PyQt6 import QtWidgets
from beeref.localization import tr
from beeref.styles import BeeRefStyles


class HelpDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle(tr('help_title'))
        self.setFixedSize(500, 600)
        self.setStyleSheet(BeeRefStyles.get_dialog_style())
        
        # Main layout
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Controls section
        controls_title = QtWidgets.QLabel(tr('controls_title'))
        controls_title.setStyleSheet(BeeRefStyles.get_section_title_style())
        layout.addWidget(controls_title)
        
        # Controls intro text
        controls_intro = QtWidgets.QLabel(f"{tr('controls_intro')} <a href='#' style='{BeeRefStyles.get_html_link_style()}'>handbook</a>.")
        controls_intro.setWordWrap(True)
        controls_intro.setOpenExternalLinks(False)
        layout.addWidget(controls_intro)
        
        controls_intro2 = QtWidgets.QLabel(tr('controls_intro2'))
        layout.addWidget(controls_intro2)
        
        # Controls table
        controls_table = QtWidgets.QTableWidget()
        controls_table.setRowCount(6)
        controls_table.setColumnCount(2)
        controls_table.setHorizontalHeaderLabels([tr('controls_action_header'), tr('controls_input_header')])
        controls_table.horizontalHeader().setStyleSheet("font-weight: bold;")
        controls_table.verticalHeader().setVisible(False)
        controls_table.setShowGrid(False)
        controls_table.setAlternatingRowColors(False)
        controls_table.setStyleSheet(BeeRefStyles.get_table_style())
        
        # Populate controls table
        controls_data = [
            (tr('controls_move_window'), tr('controls_input_right_click_drag')),
            (tr('controls_open_menu'), tr('controls_input_right_click')),
            (tr('controls_select_images'), tr('controls_input_left_click_drag')),
            (tr('controls_focus_images'), tr('controls_input_double_left_click')),
            (tr('controls_zoom_to_pointer'), tr('controls_input_scroll_wheel')),
            (tr('controls_pan_scene'), tr('controls_input_scroll_click_drag'))
        ]
        
        for i, (action, input_method) in enumerate(controls_data):
            action_item = QtWidgets.QTableWidgetItem(action)
            input_item = QtWidgets.QTableWidgetItem(f"- {input_method}")
            controls_table.setItem(i, 0, action_item)
            controls_table.setItem(i, 1, input_item)
        
        controls_table.resizeColumnsToContents()
        controls_table.setMaximumHeight(300)
        layout.addWidget(controls_table)
        
        # Additional controls info
        controls_info = QtWidgets.QLabel(f"{tr('controls_info')} <a href='#' style='{BeeRefStyles.get_html_link_style()}'>keyboard shortcuts</a> and the <a href='#' style='{BeeRefStyles.get_html_link_style()}'>default shortcuts</a> web page for more details.")
        controls_info.setWordWrap(True)
        controls_info.setOpenExternalLinks(False)
        layout.addWidget(controls_info)
        
        # Support section
        support_title = QtWidgets.QLabel(tr('support_title'))
        support_title.setStyleSheet(BeeRefStyles.get_section_title_with_margin_style())
        layout.addWidget(support_title)
        
        support_text = QtWidgets.QLabel(f"{tr('support_text')} <a href='#' style='{BeeRefStyles.get_html_link_style()}'>FAQ</a>. For additional help, submitting bug reports, suggestions, or anything else you might want to tell us, visit the <a href='#' style='{BeeRefStyles.get_html_link_style()}'>forums</a>.")
        support_text.setWordWrap(True)
        support_text.setOpenExternalLinks(False)
        layout.addWidget(support_text)
        
        # About link
        about_link = QtWidgets.QLabel(f"<a href='#' style='{BeeRefStyles.get_html_link_style()}'>{tr('about_link')}</a>")
        about_link.setOpenExternalLinks(False)
        about_link.linkActivated.connect(self.on_about_clicked)
        layout.addWidget(about_link)
        
        # Add stretch to push content to top
        layout.addStretch()
        
        self.setLayout(layout)
        self.show()

    def on_about_clicked(self):
        """Handle the about link click."""
        from beeref.about_dialog import AboutDialog
        AboutDialog(self)
