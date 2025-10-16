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


class HelpDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Help')
        self.setFixedSize(500, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                background-color: transparent;
            }
            QPushButton {
                background-color: transparent;
                color: #0078d4;
                text-decoration: underline;
                border: none;
                padding: 0px;
                text-align: left;
            }
            QPushButton:hover {
                color: #106ebe;
            }
        """)
        
        # Main layout
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Controls section
        controls_title = QtWidgets.QLabel("Controls")
        controls_title.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 10px;")
        layout.addWidget(controls_title)
        
        # Controls intro text
        controls_intro = QtWidgets.QLabel("For more in depth help refer to the <a href='#' style='color: #0078d4; text-decoration: underline;'>handbook</a>.")
        controls_intro.setWordWrap(True)
        controls_intro.setOpenExternalLinks(False)
        layout.addWidget(controls_intro)
        
        controls_intro2 = QtWidgets.QLabel("These are BeeRef's most basic controls:")
        layout.addWidget(controls_intro2)
        
        # Controls table
        controls_table = QtWidgets.QTableWidget()
        controls_table.setRowCount(6)
        controls_table.setColumnCount(2)
        controls_table.setHorizontalHeaderLabels(["Action", "Input"])
        controls_table.horizontalHeader().setStyleSheet("font-weight: bold;")
        controls_table.verticalHeader().setVisible(False)
        controls_table.setShowGrid(False)
        controls_table.setAlternatingRowColors(False)
        controls_table.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                border: none;
                gridline-color: transparent;
            }
            QTableWidget::item {
                padding: 5px;
                border: none;
            }
            QHeaderView::section {
                background-color: transparent;
                border: none;
                padding: 5px;
            }
        """)
        
        # Populate controls table
        controls_data = [
            ("Move window", "right click drag"),
            ("Open menu", "right click"),
            ("Select images", "left click/drag"),
            ("Focus images", "double left click"),
            ("Zoom to pointer", "scroll wheel"),
            ("Pan Scene", "scroll click drag")
        ]
        
        for i, (action, input_method) in enumerate(controls_data):
            action_item = QtWidgets.QTableWidgetItem(action)
            input_item = QtWidgets.QTableWidgetItem(f"- {input_method}")
            controls_table.setItem(i, 0, action_item)
            controls_table.setItem(i, 1, input_item)
        
        controls_table.resizeColumnsToContents()
        controls_table.setMaximumHeight(200)
        layout.addWidget(controls_table)
        
        # Additional controls info
        controls_info = QtWidgets.QLabel("To see all controls and set them yourself, check out <a href='#' style='color: #0078d4; text-decoration: underline;'>keyboard shortcuts</a> and the <a href='#' style='color: #0078d4; text-decoration: underline;'>default shortcuts</a> web page for more details.")
        controls_info.setWordWrap(True)
        controls_info.setOpenExternalLinks(False)
        layout.addWidget(controls_info)
        
        # Support section
        support_title = QtWidgets.QLabel("Support")
        support_title.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 20px; margin-bottom: 10px;")
        layout.addWidget(support_title)
        
        support_text = QtWidgets.QLabel("For troubleshooting, please consult the <a href='#' style='color: #0078d4; text-decoration: underline;'>FAQ</a>. For additional help, submitting bug reports, suggestions, or anything else you might want to tell us, visit the <a href='#' style='color: #0078d4; text-decoration: underline;'>forums</a>.")
        support_text.setWordWrap(True)
        support_text.setOpenExternalLinks(False)
        layout.addWidget(support_text)
        
        # About link
        about_link = QtWidgets.QLabel("<a href='#' style='color: #0078d4; text-decoration: underline;'>About BeeRef</a>")
        about_link.setOpenExternalLinks(False)
        layout.addWidget(about_link)
        
        # Add stretch to push content to top
        layout.addStretch()
        
        self.setLayout(layout)
        self.show()
