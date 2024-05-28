# tela_upload.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QCursor, QIcon
from PyQt5.QtCore import QFile, QTextStream, Qt, QSize

class TelaUpload(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        # Carregar a imagem de fundo usando QPixmap
        pixmap = QPixmap("images/prototipo/Fundo_inicial.jpg")

        # Configurar a janela principal
        self.setWindowTitle("Tela com Background")
        self.setWindowFlag(Qt.FramelessWindowHint)  # Remove as bordas da janela
        self.setFixedSize(pixmap.size())  # Define o tamanho da janela para o tamanho da imagem

        # Centralizar a janela na tela
        self.center_window()

        # Load external CSS style sheet
        self.loadStyleSheet("css/style.css")

        # Criar um QLabel para exibir a imagem de fundo
        self.background = QLabel(self)
        self.background.setPixmap(pixmap)
        self.background.setGeometry(0, 0, self.width(), self.height())  # Define o tamanho do QLabel para preencher a janela

        # Layout vertical para organizar os widgets
        layout_inicio = QVBoxLayout()

        # Carregar um ícone usando QIcon
        icon_path = 'icons/upload.png'  # Substitua com o caminho para o seu ícone
        icon = QIcon(icon_path)

        # Criar os botões e definir largura máxima
        self.btn_upload = QPushButton("  ENVIAR IMAGEM", self)
        self.btn_upload.setFixedWidth(250)  # Definir largura máxima para 200 pixels
        self.btn_upload.setFixedHeight(50)
        self.btn_upload.move(470, 300)  # Define a posição x e y do botão na janela
        self.btn_upload.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_upload.setObjectName("btn_upload")
        # Definir o ícone para o botão
        self.btn_upload.setIcon(icon)
        # Definir o tamanho do ícone (opcional)
        self.btn_upload.setIconSize(icon.actualSize(QSize(24, 24)))  # Definir o tamanho do ícone
        self.btn_upload.setCursor(QCursor(Qt.CursorShape.PointingHandCursor)) # Altera o Cursor para clique
        self.btn_upload.clicked.connect(self.upload_image)

        self.btn_next = QPushButton("CONTINUAR", self)
        self.btn_next.setFixedWidth(150)  # Definir largura máxima para 200 pixels
        self.btn_next.setFixedHeight(40)
        self.btn_next.move(520, 370)  # Define a posição x e y do botão na janela
        self.btn_next.setCursor(QCursor(Qt.CursorShape.PointingHandCursor)) # Altera o Cursor para clique
        self.btn_next.clicked.connect(self.show_next_screen)
        self.btn_next.setEnabled(False)  # Disable initially

        self.btn_back = QPushButton("VOLTAR", self)
        self.btn_back.move(20, 625)
        self.btn_back.setFixedWidth(100)
        self.btn_back.setFixedHeight(30)
        self.btn_back.setObjectName("btn_back")
        self.btn_back.clicked.connect(self.goBackToPreviousScreen)
        self.btn_back.setCursor(QCursor(Qt.CursorShape.PointingHandCursor)) # Altera o Cursor para clique

        # Adicionar os botões ao layout
        layout_inicio.addWidget(self.btn_upload)
        layout_inicio.addWidget(self.btn_back)
        layout_inicio.addWidget(self.btn_next)
    
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
        from tela_inicial import MainWindow

        self.tela_inicial = MainWindow()
        self.tela_inicial.show()
        self.close()  # Fecha a janela atual (segunda tela)

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Escolha uma Imagem", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_name:
            self.image_path = file_name
            self.btn_next.setEnabled(True)

    def show_next_screen(self):
        from tela_manipulacao import TelaManipulacao

        if self.image_path:
            self.next_screen = TelaManipulacao(self.image_path)
            self.next_screen.show()
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TelaUpload()
    window.show()
    sys.exit(app.exec_())