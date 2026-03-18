import anthropic               # biblioteca oficial da Anthropic para usar a API do Claude
from dotenv import load_dotenv # biblioteca para carregar variáveis do arquivo .env
import os                      # biblioteca para acessar variáveis do sistema

load_dotenv()                  # lê o arquivo .env e carrega a ANTHROPIC_API_KEY no sistema

api_key = os.getenv("ANTHROPIC_API_KEY")  # pega a chave do arquivo .env

client = anthropic.Anthropic(api_key=api_key)  # cria o cliente passando a chave diretamente



def analisar_remedios(remedio1, remedio2, texto_bula1="", texto_bula2=""):
    # função que recebe os nomes dos remédios e opcionalmente o texto das bulas em PDF

    contexto_bula1 = f"Texto da bula do {remedio1}:\n{texto_bula1}" if texto_bula1 else ""
    # se o texto da bula 1 foi enviado, formata ele para incluir no prompt

    contexto_bula2 = f"Texto da bula do {remedio2}:\n{texto_bula2}" if texto_bula2 else ""
    # se o texto da bula 2 foi enviado, formata ele para incluir no prompt

    prompt = f"""
    Você é um assistente farmacêutico especializado em análise de bulas de remédios.
    
    Analise a combinação dos seguintes medicamentos e responda em português:
    - Remédio 1: {remedio1}
    - Remédio 2: {remedio2}
    
    {contexto_bula1}
    {contexto_bula2}
    
    Se o texto das bulas foi fornecido acima, use ele como base principal da análise.
    Caso contrário, use seu conhecimento farmacêutico para responder.
    
    Responda exatamente nesse formato:
    
    COMPATIBILIDADE: (Compatível / Incompatível / Usar com cautela)
    
    EFEITOS COLATERAIS PRINCIPAIS:
    - (liste os principais efeitos colaterais de cada remédio)
    
    INTERAÇÕES ENTRE OS REMÉDIOS:
    - (explique se há interação entre eles)
    
    INDICAÇÕES:
    - (para que cada remédio é indicado)
    
    CONTRAINDICAÇÕES:
    - (quem não deve usar essa combinação)
    
    RECOMENDAÇÃO FINAL:
    (um parágrafo resumindo se é seguro usar juntos)
    """

    message = client.messages.create(  # chama a API do Claude para gerar a resposta
        model="claude-sonnet-4-20250514",  # define qual modelo de IA vai ser usado
        max_tokens=1024,                   # limite máximo de palavras na resposta
        messages=[
            {"role": "user", "content": prompt}  # envia o prompt como mensagem do usuário
        ]
    )

    return message.content[0].text  # retorna só o texto da resposta da IA
