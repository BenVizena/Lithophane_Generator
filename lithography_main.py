import numpy as np
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, Qt
from PIL import Image, ImageFilter
import re as regex
from lithophane_generator import generate_lithophane

#TODO:80 Change all pixel values to constants like: WIDTH_SELECTION_LINE_POSITION = (20, 30)




class GUI(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'lithophane Generator'
        self.left = 100
        self.top = 100
        self.width = self.logicalDpiX() * 10
        self.height = self.logicalDpiY() * 7
        self.path_to_file = ''
        self.path_to_sample_image = self.get_path_to_sample_image()
        self.initUI()

    def get_path_to_sample_image(self):
        path_to_this_program = os.path.realpath(__file__)
        return regex.sub(r"lithography_main.py", 'big-bend.jpg', path_to_this_program)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.add_select_file_button()
        self.add_file_selection_line()

        self.add_width_selection_button()
        self.add_height_selection_button()
        self.add_width_selection_line()
        self.add_height_selection_line()

        self.setup_image_preview()
        self.add_setup_summary_label()

        self.add_run_button()

        self.show()

    def add_select_file_button(self):
        select_file_button = QPushButton('SELECT FILE', self)
        select_file_button.setToolTip('Select the file to be lithographized!')
        select_file_button.move(4, self.height - 35)
        select_file_button.clicked.connect(self.select_and_set_file_button_clicked)

    def add_file_selection_line(self):
        self.file_selection_line = QLineEdit(self)
        self.file_selection_line.move(80, self.height - 40)
        self.file_selection_line.resize(600,32)

    def add_width_selection_button(self):
        self.width_selection_button = QPushButton('ENTER WIDTH (mm):  ', self)
        self.width_selection_button.move(10, 200)
        self.width_selection_button.clicked.connect(self.width_selection_button_clicked)

    def add_height_selection_button(self):
        self.height_selection_button = QPushButton('ENTER HEIGHT (mm): ', self)
        self.height_selection_button.move(10, 230)
        self.height_selection_button.clicked.connect(self.height_selection_button_clicked)

    def width_selection_button_clicked(self):
        if self.path_to_file == '':
            self.make_dialog_box('Please select a file before clicking that!')
        elif self.width_selection_line.text() == '':
            self.make_dialog_box('Please enter a width value if you want to press the width button!')
        else:
            height, width = self.heights_of_stl_structures.shape
            height_width_ratio = float(height) / float(width)
            self.print_width = float(self.width_selection_line.text())
            self.print_height = float(self.width_selection_line.text()) * height_width_ratio
            self.add_setup_summary()

    def height_selection_button_clicked(self):
        if self.path_to_file == '':
            self.make_dialog_box('Please select a file before clicking that!')
        elif self.height_selection_line.text() == '':
            self.make_dialog_box('Please enter a height value if you want to press the height button!')
        else:
            height, width = self.heights_of_stl_structures.shape
            width_height_ratio = float(width) / float(height)
            self.print_height = float(self.height_selection_line.text())
            self.print_width = float(self.height_selection_line.text()) * width_height_ratio
            self.add_setup_summary()

    def add_setup_summary_label(self):
        self.setup_summary_label = QLabel(self)

    def add_setup_summary(self):
        self.setup_summary_label.setText('Press "RUN" to make lithophane for... \n \
            image:  ' + str(self.path_to_file) + '\n \
            height: ' + str(self.print_height) + ' mm\n \
            width:  ' + str(self.print_width) + ' mm')
        self.setup_summary_label.move(10,10)
        self.setup_summary_label.resize(500,200)
        self.setup_summary_label.setAlignment(Qt.AlignTop)

    def make_dialog_box(self, dialog_string):
        dialog_box = QMessageBox()
        dialog_box.setWindowTitle("Lithography Utility")
        dialog_box.setIcon(QMessageBox.Information)
        dialog_box.setText(dialog_string)
        dialog_box.exec_()

    def add_width_selection_line(self):
        self.width_selection_line = QLineEdit(self)
        self.width_selection_line.move(130, 202)
        self.width_selection_line.resize(40,20)

    def add_height_selection_line(self):
        self.height_selection_line = QLineEdit(self)
        self.height_selection_line.move(130, 232)
        self.height_selection_line.resize(40,20)

    def setup_image_preview(self):
        self.image_preview = QLabel(self)
        self.image_preview_pixmap = QPixmap(self.path_to_sample_image)
        self.image_preview_pixmap = self.image_preview_pixmap.scaledToWidth(self.width / 2)
        self.image_preview.setPixmap(self.image_preview_pixmap)
        self.image_preview.move(self.width - self.image_preview_pixmap.width() - 10, 10)
        self.image_preview.show()

    def set_image_preview(self):
        self.image_preview_pixmap = QPixmap(self.path_to_file)
        self.image_preview_pixmap = self.image_preview_pixmap.scaled(self.width/2,self.height/2, Qt.KeepAspectRatio)
        self.image_preview.setPixmap(self.image_preview_pixmap)

        self.image_preview.move(self.width - self.image_preview_pixmap.width() - 10, 10)

        self.image_preview.show()

    def select_and_set_file_button_clicked(self):
        self.select_file()
        self.set_file()
        self.file_selection_line.setText(self.path_to_file)
        self.set_image_preview()

    def select_file(self):
        self.path_to_file = regex.split(',' , str(QFileDialog.getOpenFileName(self, '', '/')))[0]
        self.path_to_file = regex.split('\'', self.path_to_file)[1]
        self.set_file()

    def set_file(self):
        try:
            input_image = np.asarray(Image.open(self.path_to_file).convert('LA'))
        except:
            self.make_dialog_box("Error opening image!")

        pixel_intensities = np.array(np.copy(input_image))
        # make the darkest parts of the image into the tallest parts of the lithophane.
        self.heights_of_stl_structures = (pixel_intensities[:,:,0].astype(np.int) - 255) * -1

    def set_file_selection_line_text(self, path_to_file):
        self.file_selection_line.setText(self.path_to_file)

    def add_run_button(self):
        self.run_button = QPushButton('RUN', self)
        self.run_button.move(10, 75)
        self.run_button.clicked.connect(self.run_button_clicked)

    def run_button_clicked(self):
        if self.setup_summary_label.text() != "":
            generate_lithophane(self.print_width, self.print_height, self.heights_of_stl_structures)
        else:
            self.make_dialog_box("Select an image and enter a width or height before pressing this button.")

if __name__ == '__main__':
        gui = QApplication(sys.argv)
        ex = GUI()
        sys.exit(gui.exec_())
