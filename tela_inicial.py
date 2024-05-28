import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QMessageBox, QScrollArea
from PyQt5.QtGui import QPixmap, QCursor, QIcon
from PyQt5.QtCore import QFile, QTextStream, Qt, QSize
from tela_upload import TelaUpload  # Importar a classe da segunda tela


class MainWindow(QMainWindow):
    def __init__(self):
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

        # Criar um widget central para conter os elementos
        #central_widget = QWidget(self)
        #self.setCentralWidget(central_widget)

        # Layout vertical para organizar os widgets
        layout_inicio = QVBoxLayout()

        # Carregar um ícone usando QIcon
        icon_path = 'icons/ajuda.png'  # Substitua com o caminho para o seu ícone
        icon = QIcon(icon_path)

        # Criar os botões e definir largura máxima
        btn_init = QPushButton("INICIAR", self)
        btn_init.setFixedWidth(250)  # Definir largura máxima para 200 pixels
        btn_init.setFixedHeight(50)
        btn_init.move(470, 300)  # Define a posição x e y do botão na janela
        btn_init.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_init.setObjectName("btn_init")
        btn_init.clicked.connect(self.openSecondScreen)

        btn_close = QPushButton("SAIR", self)
        btn_close.move(525, 375)
        btn_close.setFixedWidth(140)
        btn_close.setFixedHeight(35)
        btn_close.setObjectName("btn_close")
        btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_close.clicked.connect(self.fechar_aplicacao)

        btn_help = QPushButton("  MATRIZES", self)
        btn_help.move(20, 625)
        btn_help.setFixedWidth(100)
        btn_help.setFixedHeight(27)
        btn_help.setObjectName("btn_help")
        #Definir o ícone para o botão
        btn_help.setIcon(icon)
        # Definir o tamanho do ícone (opcional)
        btn_help.setIconSize(icon.actualSize(QSize(18, 18)))  # Definir o tamanho do ícone
        btn_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor)) # Altera o Cursor para clique
        btn_help.clicked.connect(self.show_matrices_popup)

        # Adicionar os botões ao layout
        layout_inicio.addWidget(btn_init)
        layout_inicio.addWidget(btn_close)
        #layout_inicio.addWidget(btn_help)

    def center_window(self):
            # Obter a geometria da tela principal
            screen_geometry = QApplication.desktop().screenGeometry()

            # Calcular a posição central da janela
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2

            # Definir a posição da janela centralizada
            self.move(x, y)

    def fechar_aplicacao(self):
        self.close()

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

    def openSecondScreen(self):
        # Criar uma instância da segunda tela (SecondScreen)
        self.tela_upload = TelaUpload()
        self.tela_upload.tela_inicial = self  # Passa a referência da janela principal para a SecondaryWindow
        self.tela_upload.show()  # Mostrar a segunda tela
        # Esconder a tela principal (opcional)
        self.hide()

    def show_matrices_popup(self):
        # Definir o texto do pop-up com HTML
        matrices_text = """
        <h2 style='font-family: Arial; font-size: 18px;'>Matrizes Utilizadas:</h2>
        <p style='font-family: Arial; font-size: 14px;'>
        <b>Preto e Branco:</b> 
        <br>
        Matriz de Média
        <br><br>
        Ela é usada para calcular a média dos valores dos pixels ao redor de cada pixel na imagem, resultando em um efeito de suavização ou borramento na imagem. <br>
        Quando aplicada em imagens em tons de cinza, como no caso da conversão para preto e branco, ela ajuda a suavizar transições abruptas de cores, <br>
        criando uma aparência mais uniforme e menos granulada na imagem.
        <br><br>
        <b>Rotação:</b> 
        <br>
        Matriz de rotação
        <br><br>
        A matriz usada para essa função de rotação de imagem não é uma matriz estática, mas sim uma matriz de transformação afim de rotação que é
        calculada dinamicamente com base no ângulo de rotação fornecido pelo usuário.
        <br><br>
        <b>Translação</b> 
        <br>
        Matriz de translação
        <br><br>
        A matriz utilizada para realizar a translação é uma matriz de 2x3, onde os elementos definem o deslocamento horizontal (tx) e vertical (ty) que será aplicado a cada pixel da imagem. Aqui está a representação da matriz:
        <br><br>
        | 1 0 tx |
        <br>
        | 0 1 ty |
        <br><br>
        <b>Escalamento de imagem</b> 
        <br>
        Matriz de transformação
        <br><br>
        A matriz de transformação utilizada é uma matriz de redimensionamento, que é uma matriz diagonal com os fatores de escala na diagonal principal.
        </p>
        """

        # Criar o diálogo de mensagem
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Matrizes Utilizadas")
        msg_box.setTextFormat(Qt.RichText)  # Definir o formato do texto como RichText para usar HTML
        msg_box.setText(matrices_text)
        
        # Adicionar um botão "Next"
        next_button = msg_box.addButton("Next", QMessageBox.AcceptRole)
        msg_box.exec_()

        # Verificar se o botão "Next" foi clicado
        if msg_box.clickedButton() == next_button:
            self.show_matrices_popup2()

    def show_matrices_popup2(self):
        # Definir o texto do pop-up com HTML para o segundo pop-up
        matrices_text2 = """
        <<h2 style='font-family: Arial; font-size: 18px;'>Matrizes Utilizadas:</h2>
        <p style='font-family: Arial; font-size: 14px;'>
        <b>Espelhamento:</b> 
        <br>
        Matriz de espelhamento horizontal
        <br><br>
        inverte a posição dos pixels ao longo do eixo horizontal. Como a imagem está sendo espelhada horizontalmente, a posição de cada pixel ao longo do eixo X é invertida.
        Para espelhar a imagem horizontalmente, a posição do pixel na coluna original x é transformada em mirrored_x, que é calculada como width - 1 - x
        <br><br>
        <b>Nitidez:</b> 
        <br>
        Kernel
        <br><br>
        O kernel é uma matriz 3x3 que define como cada pixel na imagem será ajustado para criar o efeito de nitidez.
        Este kernel define como os valores dos pixels na imagem serão ponderados e combinados para produzir o efeito de nitidez. 
        Ele realça os detalhes da imagem, aumentando a diferença entre os valores dos pixels vizinhos.
        <br><br>
        <b>Alto contraste: </b> 
        <br>
        Matriz de convolução
        <br><br>
        É aplicada à imagem original para realçar as bordas e detalhes.
        Essa matriz é convoluída com a imagem original usando a função cv2.filter2D do OpenCV para aplicar o efeito de emboss na imagem. </br>
        Depois, a imagem é normalizada para garantir que os valores estejam no intervalo de 0 a 255
        </p>
        """

        # Criar o segundo diálogo de mensagem
        msg_box2 = QMessageBox()
        msg_box2.setWindowTitle("Segundo Pop-up de Matrizes")
        msg_box2.setTextFormat(Qt.RichText)  # Definir o formato do texto como RichText para usar HTML
        msg_box2.setText(matrices_text2)
        msg_box2.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())