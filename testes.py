import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage

class ImageFilterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.image = None

    def initUI(self):
        self.setWindowTitle('Image Filter Application')
        
        self.layout = QVBoxLayout()
        
        self.filter_button = QPushButton('Filtros', self)
        self.filter_button.clicked.connect(self.show_filter_buttons)
        self.layout.addWidget(self.filter_button)
        
        self.filter1_button = QPushButton('Filtro 1', self)
        self.filter1_button.clicked.connect(self.apply_filter1)
        self.filter1_button.hide()
        
        self.filter2_button = QPushButton('Filtro 2', self)
        self.filter2_button.clicked.connect(self.apply_filter2)
        self.filter2_button.hide()
        
        self.layout.addWidget(self.filter1_button)
        self.layout.addWidget(self.filter2_button)
        
        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)
        
        self.open_button = QPushButton('Abrir Imagem', self)
        self.open_button.clicked.connect(self.open_image)
        self.layout.addWidget(self.open_button)
        
        self.setLayout(self.layout)
        self.resize(400, 300)
    
    def show_filter_buttons(self):
        self.filter1_button.show()
        self.filter2_button.show()
    
    def open_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir Imagem", "", "Imagens (*.png *.xpm *.jpg);;Todos os Arquivos (*)", options=options)
        if file_name:
            self.image = cv2.imread(file_name)
            self.display_image(self.image)
    
    def display_image(self, img):
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        self.image_label.setPixmap(QPixmap.fromImage(q_img))
    
    def apply_filter1(self):
        if self.image is not None:
            kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])
            filtered_image = cv2.filter2D(self.image, -1, kernel)
            self.display_image(filtered_image)
    
    def apply_filter2(self):
        if self.image is not None:
            kernel = np.array([[-1, -1, -1],
                               [-1, 8, -1],
                               [-1, -1, -1]])
            filtered_image = cv2.filter2D(self.image, -1, kernel)
            self.display_image(filtered_image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageFilterApp()
    ex.show()
    sys.exit(app.exec_())