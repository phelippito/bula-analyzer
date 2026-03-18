import pytesseract                        # biblioteca para usar o Tesseract OCR
from PIL import Image                     # biblioteca para abrir e manipular imagens
import io                                 # biblioteca para manipular arquivos em memória

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# caminho onde o Tesseract foi instalado no Windows

def extrair_texto_foto(arquivo):          # função que recebe a foto enviada pelo usuário
    imagem = Image.open(arquivo)          # abre a imagem com o Pillow
    texto = pytesseract.image_to_string(  # extrai o texto da imagem com OCR
        imagem,
        lang="eng"                        # idioma inglês para leitura
    )
    return texto                          # retorna o texto extraído da imagem