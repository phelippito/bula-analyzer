import pdfplumber  # biblioteca para extrair texto de arquivos PDF

def extrair_texto_pdf(arquivo):  # função que recebe o arquivo PDF enviado pelo usuário
    texto = ""                   # variável que vai acumular todo o texto extraído
    
    with pdfplumber.open(arquivo) as pdf:  # abre o PDF com o pdfplumber
        for pagina in pdf.pages:           # percorre cada página do PDF
            conteudo = pagina.extract_text()  # extrai o texto da página atual
            if conteudo:                      # verifica se a página tem texto
                texto += conteudo + "\n"      # adiciona o texto da página com quebra de linha
    
    return texto  # retorna todo o texto extraído do PDF