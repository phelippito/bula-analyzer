import streamlit as st                     # biblioteca para criar a interface web
from ai_analyzer import analisar_remedios  # importa a função de análise com IA
from pdf_reader import extrair_texto_pdf   # importa a função de leitura de PDF
from ocr_reader import extrair_texto_foto  # importa a função de leitura de foto
from reportlab.lib.pagesizes import A4     # tamanho da página A4
from reportlab.lib.styles import getSampleStyleSheet  # estilos padrão de texto
from reportlab.lib.units import cm         # unidade de medida em centímetros
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer  # elementos do PDF
import io                                  # biblioteca para manipular arquivos em memória

st.set_page_config(
    page_title="Bula Analyzer",            # título que aparece na aba do navegador
    page_icon="💊",                         # ícone que aparece na aba do navegador
    layout="centered",                     # layout centralizado, melhor para mobile
    initial_sidebar_state="collapsed"      # sidebar fechada por padrão
)

def gerar_pdf(remedio1, remedio2, resultado):   # função que gera o PDF com o resultado
    buffer = io.BytesIO()                        # cria um buffer em memória para o PDF
    doc = SimpleDocTemplate(                     # cria o documento PDF
        buffer,
        pagesize=A4,                             # tamanho A4
        rightMargin=2*cm,                        # margem direita
        leftMargin=2*cm,                         # margem esquerda
        topMargin=2*cm,                          # margem superior
        bottomMargin=2*cm                        # margem inferior
    )

    styles = getSampleStyleSheet()               # carrega os estilos padrão
    elementos = []                               # lista de elementos do PDF

    elementos.append(Paragraph("Bula Analyzer", styles["Title"]))  # título
    elementos.append(Spacer(1, 0.3*cm))          # espaço em branco
    elementos.append(Paragraph(f"Análise: {remedio1} + {remedio2}", styles["Heading2"]))  # subtítulo
    elementos.append(Spacer(1, 0.5*cm))          # espaço em branco

    for linha in resultado.split("\n"):          # percorre cada linha do resultado
        if linha.strip() == "":                  # se a linha estiver vazia
            elementos.append(Spacer(1, 0.2*cm)) # adiciona espaço em branco
        else:
            elementos.append(Paragraph(linha, styles["Normal"]))  # adiciona a linha no PDF

    doc.build(elementos)                         # gera o PDF com todos os elementos
    buffer.seek(0)                               # volta para o início do buffer
    return buffer                                # retorna o buffer com o PDF pronto

st.title("💊 Bula Analyzer")               # título principal da página
st.write("Análise inteligente de bulas de remédios") # subtítulo da página

st.divider()                               # linha separadora visual

if "resultado" not in st.session_state:    # verifica se o resultado já existe na sessão
    st.session_state.resultado = ""        # inicializa o resultado como vazio
if "remedio1" not in st.session_state:    # verifica se o remédio 1 já existe na sessão
    st.session_state.remedio1 = ""        # inicializa o remédio 1 como vazio
if "remedio2" not in st.session_state:    # verifica se o remédio 2 já existe na sessão
    st.session_state.remedio2 = ""        # inicializa o remédio 2 como vazio

col1, col2 = st.columns(2)                # divide a tela em duas colunas iguais

with col1:                                # conteúdo da coluna da esquerda
    st.subheader("Remédio 1")             # subtítulo da coluna
    remedio1 = st.text_input(
        "Nome do remédio 1",              # rótulo do campo
        placeholder="Ex: Ibuprofeno 600mg", # texto de exemplo dentro do campo
        value=st.session_state.remedio1   # valor atual salvo na sessão
    )
    tipo_entrada1 = st.radio(             # botões de seleção do tipo de entrada
        "Como deseja inserir a bula?",    # pergunta para o usuário
        ["Apenas o nome", "PDF", "Foto"], # opções disponíveis
        key="tipo1"                       # identificador único do componente
    )
    pdf1 = None                           # inicializa o PDF como vazio
    foto1 = None                          # inicializa a foto como vazia

    if tipo_entrada1 == "PDF":            # se o usuário escolheu PDF
        pdf1 = st.file_uploader(
            "Upload da bula em PDF",      # rótulo do upload
            type="pdf",                   # aceita apenas arquivos PDF
            key="pdf1"                    # identificador único do componente
        )
    elif tipo_entrada1 == "Foto":         # se o usuário escolheu Foto
        foto1 = st.file_uploader(
            "Upload da foto da bula",     # rótulo do upload
            type=["jpg", "jpeg", "png"],  # aceita apenas imagens
            key="foto1"                   # identificador único do componente
        )

with col2:                                # conteúdo da coluna da direita
    st.subheader("Remédio 2")             # subtítulo da coluna
    remedio2 = st.text_input(
        "Nome do remédio 2",
        placeholder="Ex: Paracetamol 750mg",
        value=st.session_state.remedio2   # valor atual salvo na sessão
    )
    tipo_entrada2 = st.radio(             # botões de seleção do tipo de entrada
        "Como deseja inserir a bula?",
        ["Apenas o nome", "PDF", "Foto"],
        key="tipo2"                       # identificador único do componente
    )
    pdf2 = None                           # inicializa o PDF como vazio
    foto2 = None                          # inicializa a foto como vazia

    if tipo_entrada2 == "PDF":            # se o usuário escolheu PDF
        pdf2 = st.file_uploader(
            "Upload da bula em PDF",
            type="pdf",
            key="pdf2"                    # identificador único do componente
        )
    elif tipo_entrada2 == "Foto":         # se o usuário escolheu Foto
        foto2 = st.file_uploader(
            "Upload da foto da bula",
            type=["jpg", "jpeg", "png"],
            key="foto2"                   # identificador único do componente
        )

st.divider()                              # linha separadora visual

col_analisar, col_limpar = st.columns(2)  # divide os botões em duas colunas

with col_analisar:                        # botão de analisar na coluna da esquerda
    analisar = st.button("Analisar", use_container_width=True)

with col_limpar:                          # botão de limpar na coluna da direita
    limpar = st.button("Nova pesquisa", use_container_width=True)

if limpar:                                # se o botão de limpar foi clicado
    st.session_state.resultado = ""       # limpa o resultado salvo na sessão
    st.session_state.remedio1 = ""        # limpa o remédio 1 salvo na sessão
    st.session_state.remedio2 = ""        # limpa o remédio 2 salvo na sessão
    st.rerun()                            # reinicia a página com os campos limpos

if analisar:                              # se o botão de analisar foi clicado
    with st.spinner("Analisando bulas..."):  # mostra animação de carregamento
        try:                                 # tenta executar o código abaixo
            texto_bula1 = ""                 # inicializa o texto da bula 1 como vazio
            texto_bula2 = ""                 # inicializa o texto da bula 2 como vazio

            if pdf1:                         # se o usuário enviou PDF do remédio 1
                texto_bula1 = extrair_texto_pdf(pdf1)   # extrai o texto do PDF
            elif foto1:                      # se o usuário enviou foto do remédio 1
                texto_bula1 = extrair_texto_foto(foto1) # extrai o texto da foto

            if pdf2:                         # se o usuário enviou PDF do remédio 2
                texto_bula2 = extrair_texto_pdf(pdf2)   # extrai o texto do PDF
            elif foto2:                      # se o usuário enviou foto do remédio 2
                texto_bula2 = extrair_texto_foto(foto2) # extrai o texto da foto

            nome1 = remedio1 if remedio1 else "Remédio 1"
            # usa o nome digitado ou um nome genérico se veio por foto ou PDF

            nome2 = remedio2 if remedio2 else "Remédio 2"
            # usa o nome digitado ou um nome genérico se veio por foto ou PDF

            tem_entrada1 = remedio1 or pdf1 or foto1
            # verifica se o usuário forneceu alguma entrada para o remédio 1

            tem_entrada2 = remedio2 or pdf2 or foto2
            # verifica se o usuário forneceu alguma entrada para o remédio 2

            if not tem_entrada1 or not tem_entrada2:  # se faltou alguma entrada
                st.warning("Forneça pelo menos o nome, PDF ou foto dos dois remédios!")
            else:
                resultado = analisar_remedios(nome1, nome2, texto_bula1, texto_bula2)
                # chama a IA passando os nomes e os textos das bulas

                st.session_state.resultado = resultado   # salva o resultado na sessão
                st.session_state.remedio1 = nome1        # salva o remédio 1 na sessão
                st.session_state.remedio2 = nome2        # salva o remédio 2 na sessão

        except Exception as e:               # se der qualquer erro, captura aqui
            st.error(f"Erro ao analisar: {e}") # mostra o erro na tela em vermelho

if st.session_state.resultado:             # se existe um resultado salvo na sessão
    st.success("Análise concluída!")       # mensagem de sucesso em verde
    st.divider()
    st.markdown(st.session_state.resultado) # exibe o resultado formatado na tela
    st.divider()

    pdf_gerado = gerar_pdf(                # gera o PDF com o resultado
        st.session_state.remedio1,
        st.session_state.remedio2,
        st.session_state.resultado
    )

    st.download_button(                    # botão de download do PDF
        label="Baixar resultado em PDF",   # texto do botão
        data=pdf_gerado,                   # arquivo PDF gerado
        file_name=f"analise_{st.session_state.remedio1}_{st.session_state.remedio2}.pdf",
        mime="application/pdf",            # tipo do arquivo
        use_container_width=True           # botão ocupa a largura toda
    )