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

from PyQt6 import QtCore, QtWidgets
from beeref import constants
from beeref.styles import BeeRefStyles


class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle(f'About {constants.APPNAME}')
        self.setFixedSize(400, 300)
        self.setStyleSheet(BeeRefStyles.get_dialog_style() + BeeRefStyles.get_button_style())
        
        # Main layout
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # App title and version
        title_label = QtWidgets.QLabel(f"<h2>{constants.APPNAME} {constants.VERSION}</h2>")
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # App description
        desc_label = QtWidgets.QLabel(f"<p>{constants.APPNAME_FULL}</p>")
        desc_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Copyright
        copyright_label = QtWidgets.QLabel(f"<p>{constants.COPYRIGHT}</p>")
        copyright_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright_label)
        
        # Website link
        website_label = QtWidgets.QLabel(f"<p><a href='{constants.WEBSITE}' style='{BeeRefStyles.get_html_link_style()}'>Visit the {constants.APPNAME} website</a></p>")
        website_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        website_label.setOpenExternalLinks(True)
        layout.addWidget(website_label)
        
        # Add stretch to push content to top
        layout.addStretch()
        
        # Close button
        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(self.accept)
        close_button.setFixedWidth(100)
        layout.addWidget(close_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
        self.show()
