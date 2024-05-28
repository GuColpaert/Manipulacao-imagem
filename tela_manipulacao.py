import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QMessageBox, QInputDialog, QMenu
from PyQt5.QtGui import QPixmap, QCursor, QImage
from PyQt5.QtCore import QFile, QTextStream, Qt
from tela_upload import TelaUpload
from PIL import Image
import numpy as np
from tkinter import filedialog
import cv2

class TelaManipulacao(QMainWindow):
    def __init__(self, image_path):
        super().__init__() 

        # Carregar a imagem de fundo usando QPixmap
        pixmap = QPixmap("images/prototipo/Fundo_manipulacao.jpg")

        # Configurar a janela principal
        self.setWindowTitle("Tela com Background")
        self.setWindowFlag(Qt.FramelessWindowHint)  # Remove as bordas da janela
        self.setFixedSize(pixmap.size())  # Define o tamanho da janela para o tamanho da imagem

        # Criar um QLabel para exibir a imagem de fundo
        self.background = QLabel(self)
        self.background.setPixmap(pixmap)
        self.background.setGeometry(0, 0, self.width(), self.height())  # Define o tamanho do QLabel para preencher a janela

        # Load external CSS style sheet
        self.loadStyleSheet("css/style.css")

        # Centralizar a janela na tela
        self.center_window()

        self.image_path = image_path
        self.original_image = QImage(image_path)

        central_widget = QWidget()  # Criar um widget central para conter o layout
        self.setCentralWidget(central_widget)  # Definir este widget como o central na QMainWindow

        self.image_label = QLabel(self)
        pixmap = QPixmap(self.image_path)

        if not pixmap.isNull():  # Verificar se o QPixmap foi carregado corretamente
            self.image_label.setPixmap(pixmap.scaledToWidth(300))
            self.image_label.setGeometry(450, 200, pixmap.width(), pixmap.height())
            self.image_label.setFixedSize(700, 300)  # largura: 400 pixels, altura: 300 pixels
        else:
            print(f"Erro: Não foi possível carregar a imagem em {self.image_path}")

        # Criar os botões e definir largura máxima
        self.btn_blackwhite = QPushButton("PRETO E BRANCO", self)
        self.btn_blackwhite.setFixedWidth(150)  # Definir largura máxima para 200 pixels
        self.btn_blackwhite.setFixedHeight(35)
        self.btn_blackwhite.move(100, 520)  # Define a posição x e y do botão na janela
        self.btn_blackwhite.setObjectName("btn_opcao")
        self.btn_blackwhite.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_blackwhite.clicked.connect(self.pretoBranco)

        self.btn_rotacion = QPushButton("ROTAÇÃO", self)
        self.btn_rotacion.setFixedWidth(150)  # Definir largura máxima para 200 pixels
        self.btn_rotacion.setFixedHeight(35)
        self.btn_rotacion.move(270, 520)  # Define a posição x e y do botão na janela
        self.btn_rotacion.setObjectName("btn_opcao")
        self.btn_rotacion.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_rotacion.clicked.connect(self.rotate_image)

        self.btn_translacion = QPushButton("TRANSLAÇÃO", self)
        self.btn_translacion.setFixedWidth(150)  # Definir largura máxima para 200 pixels
        self.btn_translacion.setFixedHeight(35)
        self.btn_translacion.move(440, 520)  # Define a posição x e y do botão na janela
        self.btn_translacion.setObjectName("btn_opcao")
        self.btn_translacion.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_translacion.clicked.connect(self.translate_image)

        self.btn_width = QPushButton("ESCALAR IMAGEM", self)
        self.btn_width.setFixedWidth(150)  # Definir largura máxima para 200 pixels
        self.btn_width.setFixedHeight(35)
        self.btn_width.move(620, 520)  # Define a posição x e y do botão na janela
        self.btn_width.setObjectName("btn_opcao")
        self.btn_width.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_width.clicked.connect(self.scale_image)

        self.btn_espelhar = QPushButton("ESPELHAR", self)
        self.btn_espelhar.setFixedWidth(150)  # Definir largura máxima para 200 pixels
        self.btn_espelhar.setFixedHeight(35)
        self.btn_espelhar.move(800, 520)  # Define a posição x e y do botão na janela
        self.btn_espelhar.setObjectName("btn_opcao")
        self.btn_espelhar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_espelhar.clicked.connect(self.mirror_image)

        self.btn_reset = QPushButton("RESET", self)
        self.btn_reset.setFixedWidth(150)  # Definir largura máxima para 200 pixels
        self.btn_reset.setFixedHeight(35)
        self.btn_reset.move(970, 520)  # Define a posição x e y do botão na janela
        self.btn_reset.setObjectName("btn_opcao")
        self.btn_reset.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_reset.clicked.connect(self.resetarImagem)

        self.filter_button = QPushButton('Filtros', self)
        self.filter_button.setFixedWidth(150)  # Definir largura máxima para 200 pixels
        self.filter_button.setFixedHeight(35)
        self.filter_button.move(540, 570)  # Define a posição x e y do botão na janela
        self.filter_button.setObjectName("btn_opcao")
        self.filter_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.filter_menu = QMenu(self)
        
        self.filter1_action = self.filter_menu.addAction('Nitidez')
        self.filter1_action.triggered.connect(self.apply_filter1)
        
        self.filter2_action = self.filter_menu.addAction('Alto relevo')
        self.filter2_action.triggered.connect(self.apply_filter2)

        self.filter2_action = self.filter_menu.addAction('Desenho a lápis')
        self.filter2_action.triggered.connect(self.apply_filter3)
        
        self.filter_button.setMenu(self.filter_menu)

        self.btn_back = QPushButton("VOLTAR", self)
        self.btn_back.move(20, 625)
        self.btn_back.setFixedWidth(100)
        self.btn_back.setFixedHeight(30)
        self.btn_back.setObjectName("btn_back")
        self.btn_back.clicked.connect(self.goBackToPreviousScreen)
        self.btn_back.setCursor(QCursor(Qt.CursorShape.PointingHandCursor)) # Altera o Cursor para clique

        self.btn_concluded = QPushButton("CONCLUIR", self)
        self.btn_concluded.move(1070, 625)
        self.btn_concluded.setFixedWidth(100)
        self.btn_concluded.setFixedHeight(30)
        self.btn_concluded.setObjectName("btn_concluded")
        self.btn_concluded.setCursor(QCursor(Qt.CursorShape.PointingHandCursor)) # Altera o Cursor para clique
        self.btn_concluded.clicked.connect(self.download_image)

        self.btn_close = QPushButton("SAIR", self)
        self.btn_close.move(960, 625)
        self.btn_close.setFixedWidth(100)
        self.btn_close.setFixedHeight(30)
        self.btn_close.setObjectName("btn_close")
        self.btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_close.clicked.connect(self.fechar_aplicacao)

    def fechar_aplicacao(self):
        self.close()

    def center_window(self):
            # Obter a geometria da tela principal
            screen_geometry = QApplication.desktop().screenGeometry()

            # Calcular a posição central da janela
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2

            # Definir a posição da janela centralizada
            self.move(x, y)

    def loadStyleSheet(self, filename):
        styleFile = QFile(filename)
        if not styleFile.open(QFile.ReadOnly | QFile.Text):
            print(f"Erro ao abrir o arquivo CSS: {filename}")
            return

        # Leia o conteúdo do arquivo CSS
        stream = QTextStream(styleFile)
        style = stream.readAll()

        # Aplique o estilo à aplicação PyQt
        self.setStyleSheet(style)
        print("Estilo aplicado com sucesso!")

    def goBackToPreviousScreen(self):
        self.tela_upload = TelaUpload()
        self.tela_upload.show()
        self.close()  # Fecha a janela atual (segunda tela)

    def pretoBranco(self):
        # Abrir a imagem usando PIL (Pillow)
        image = Image.open(self.image_path)

        # Obter as dimensões da imagem
        width, height = image.size

        # Obter os dados dos pixels da imagem
        pixels = list(image.getdata())

        # Converter a imagem para preto e branco
        for i in range(len(pixels)):
            # Calcular o valor de escala de cinza médio dos canais RGB
            gray_value = sum(pixels[i][:3]) // 3  # Média dos valores RGB
            # Definir o pixel como escala de cinza (R = G = B = gray_value)
            pixels[i] = (gray_value, gray_value, gray_value)

        # Criar uma nova imagem a partir dos pixels modificados
        black_white_image = Image.new("RGB", (width, height))
        black_white_image.putdata(pixels)

        # Converter a imagem do PIL para o formato QImage
        qt_image = QImage(black_white_image.tobytes(), width, height, QImage.Format_RGB888)

        # Mostrar a imagem convertida na interface
        self.image_label.setPixmap(QPixmap.fromImage(qt_image).scaledToWidth(300))
        self.original_image = qt_image

    def rotate_image(self):
        angle, ok = QInputDialog.getInt(self, "Rotação de Imagem", "Digite o ângulo de rotação (graus):", 0, -180, 180, 1)
        if not ok:
            return

        # Carregar a imagem usando OpenCV
        image = cv2.imread(self.image_path)

        if image is None:
            QMessageBox.warning(self, "Erro", "Erro ao abrir a imagem.")
            return

        # Obter dimensões da imagem
        height, width = image.shape[:2]
        center = (width // 2, height // 2)

        # Calcular a matriz de rotação
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

        # Calcular os limites da nova imagem
        abs_cos = abs(rotation_matrix[0, 0])
        abs_sin = abs(rotation_matrix[0, 1])
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # Ajustar a matriz de rotação para levar em conta a translação
        rotation_matrix[0, 2] += bound_w / 2 - center[0]
        rotation_matrix[1, 2] += bound_h / 2 - center[1]

        # Realizar a rotação
        rotated_image = cv2.warpAffine(image, rotation_matrix, (bound_w, bound_h), flags=cv2.INTER_CUBIC)

        # Converter a imagem rotacionada para QImage
        height, width, channels = rotated_image.shape
        bytes_per_line = channels * width
        qt_image = QImage(rotated_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

        # Mostrar a imagem rotacionada na interface
        self.image_label.setPixmap(QPixmap.fromImage(qt_image).scaledToWidth(300))
        self.original_image = qt_image

    def translate_image(self):
        # Perguntar ao usuário a quantidade de pixels para transladar na horizontal e vertical
        tx, ok1 = QInputDialog.getInt(self, "Translação", "Quantos pixels para transladar na horizontal:", 0, -1000, 1000, 1)
        if not ok1:
            return

        ty, ok2 = QInputDialog.getInt(self, "Translação", "Quantos pixels para transladar na vertical:", 0, -1000, 1000, 1)
        if not ok2:
            return

        # Abrir a imagem usando Pillow
        image = Image.open(self.image_path)

        # Obter as dimensões da imagem
        width, height = image.size

        # Criar uma matriz de translação
        translation_matrix = [
            [1, 0, tx],
            [0, 1, ty]
        ]

        # Criar uma nova imagem para a imagem transladada
        translated_image = Image.new("RGB", (width, height))

        # Iterar sobre todos os pixels da imagem original
        for y in range(height):
            for x in range(width):
                # Calcular a nova posição do pixel após a translação
                new_x = x + tx
                new_y = y + ty

                # Verificar se a nova posição está dentro dos limites da imagem
                if 0 <= new_x < width and 0 <= new_y < height:
                    # Obter o pixel da imagem original e colocá-lo na nova posição
                    pixel = image.getpixel((x, y))
                    translated_image.putpixel((new_x, new_y), pixel)

        # Converter a imagem do Pillow para QImage
        qt_image = QImage(translated_image.tobytes(), width, height, QImage.Format_RGB888)

        # Atualizar a imagem exibida na interface
        self.image_label.setPixmap(QPixmap.fromImage(qt_image).scaledToWidth(300))
        self.original_image = qt_image

    def scale_image(self):
        if self.image_path:
            # Obter valores de largura e altura da escala usando QInputDialog
            new_width, ok1 = QInputDialog.getInt(self, "Escalar Imagem", "Nova Largura:")
            new_height, ok2 = QInputDialog.getInt(self, "Escalar Imagem", "Nova Altura:")

            if not ok1 or not ok2:
                return

            # Abrir a imagem original com Pillow
            original_image = Image.open(self.image_path)

            # Redimensionar a imagem mantendo sua proporção
            scaled_image = original_image.resize((new_width, new_height), Image.BICUBIC)

            # Converter a imagem do Pillow para o formato QImage
            if scaled_image.mode == "RGB":
                qt_image = QImage(scaled_image.tobytes(), scaled_image.width, scaled_image.height, QImage.Format_RGB888)
            elif scaled_image.mode == "RGBA":
                qt_image = QImage(scaled_image.tobytes(), scaled_image.width, scaled_image.height, QImage.Format_RGBA8888)
            else:
                qt_image = QImage(scaled_image.tobytes(), scaled_image.width, scaled_image.height, QImage.Format_ARGB32)

            # Atualizar a imagem exibida
            self.image_label.setPixmap(QPixmap.fromImage(qt_image).scaledToWidth(300))
            self.original_image = qt_image

    def mirror_image(self):

        # Abrir a imagem usando Pillow (PIL)
        image = Image.open(self.image_path)

        # Obter as dimensões da imagem
        width, height = image.size

        # Criar uma nova imagem para a imagem espelhada
        mirrored_image = Image.new("RGB", (width, height))

        # Espelhar a imagem horizontalmente
        for y in range(height):
            for x in range(width):
                # Obter o pixel da imagem original
                pixel_color = image.getpixel((x, y))

                # Inverter a posição horizontal do pixel
                mirrored_x = width - 1 - x

                # Definir o pixel na imagem espelhada
                mirrored_image.putpixel((mirrored_x, y), pixel_color)

        # Converter a imagem do Pillow (PIL) para QPixmap
        mirrored_pixmap = QImage(mirrored_image.tobytes(), width, height, QImage.Format_RGB888)

        # Atualizar a imagem exibida
        self.image_label.setPixmap(QPixmap.fromImage(mirrored_pixmap).scaledToWidth(300))
        self.original_image=mirrored_pixmap


    def resetarImagem(self):
        # Mostrar a imagem convertida na interface
        self.image_label.setPixmap(QPixmap(self.image_path).scaledToWidth(300))
        self.original_image=QImage(self.image_path)

    def download_image(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("All Files","*.*")])
        if filepath:
            self.original_image.save(filepath)
            QMessageBox.information(self, "Download Concluído", "Imagem convertida baixada com sucesso!")
    
    def apply_filter1(self):
        if self.image_path:
            # Carregar a imagem usando OpenCV
            image = cv2.imread(self.image_path)
            
            if image is None:
                QMessageBox.warning(self, "Erro", "Erro ao abrir a imagem.")
                return

            # Definir o kernel para o filtro de nitidez
            kernel = np.array([[0, -1, 0],
                            [-1, 5, -1],
                            [0, -1, 0]])

            # Aplicar o filtro à imagem
            filtered_image = cv2.filter2D(image, -1, kernel)

            # Converter a imagem filtrada para o formato QImage
            height, width, channels = filtered_image.shape
            bytes_per_line = channels * width
            qt_image = QImage(filtered_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

            # Atualizar a imagem exibida na interface
            self.image_label.setPixmap(QPixmap.fromImage(qt_image).scaledToWidth(300))
            self.original_image = qt_image

    def apply_filter2(self):
        # Carregar a imagem original usando OpenCV
        image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            QMessageBox.warning(self, "Erro", "Erro ao abrir a imagem.")
            return

        # Definir a matriz do filtro de emboss
        emboss_kernel = np.array([
            [-2, -1, 0],
            [-1,  1, 1],
            [ 0,  1, 2]
        ], dtype=np.float32)

        # Aplicar o filtro de emboss
        embossed_image = cv2.filter2D(image, -1, emboss_kernel)

        # Normalizar a imagem
        embossed_image = cv2.normalize(embossed_image, None, 0, 255, cv2.NORM_MINMAX)

        # Converter a imagem para o formato QImage
        height, width = embossed_image.shape
        qt_image = QImage(embossed_image.data, width, height, width, QImage.Format_Grayscale8)

        # Mostrar a imagem convertida na interface
        self.image_label.setPixmap(QPixmap.fromImage(qt_image).scaledToWidth(300))
        self.original_image = qt_image
        
    def apply_filter3(self):
        # Carregar a imagem original usando OpenCV
        image = cv2.imread(self.image_path, cv2.IMREAD_COLOR)

        if image is None:
            QMessageBox.warning(self, "Erro", "Erro ao abrir a imagem.")
            return

        # Converter a imagem para escala de cinza
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Inverter a imagem em escala de cinza
        inverted_image = cv2.bitwise_not(gray_image)

        # Aplicar um blur (desfoque) gaussiano à imagem invertida
        blurred_image = cv2.GaussianBlur(inverted_image, (21, 21), sigmaX=0, sigmaY=0)

        # Inverter a imagem borrada
        inverted_blurred_image = cv2.bitwise_not(blurred_image)

        # Criar a imagem final de desenho a lápis usando a técnica de divisão
        pencil_sketch_image = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)

        # Converter a imagem resultante para o formato QImage
        height, width = pencil_sketch_image.shape
        qt_image = QImage(pencil_sketch_image.data, width, height, width, QImage.Format_Grayscale8)

        # Mostrar a imagem convertida na interface
        self.image_label.setPixmap(QPixmap.fromImage(qt_image).scaledToWidth(300))
        self.original_image = qt_image
        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Criar e exibir a janela da TelaManipulacao
    window = TelaManipulacao()
    window.show()

    sys.exit(app.exec_())