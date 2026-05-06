import os
import pandas as pd
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
cliente_ia = OpenAI()


# ====================================================================
# TODO 1: LEITURA DO "PDF" (Lendo o texto sujo)
# ====================================================================
# Leia o arquivo 'fatura_suja_01.txt' e guarde todo o conteúdo 
# em uma variável chamada 'texto_bruto'.


caminho_arquivo = r'C:\Users\23.00696-0\PAE-IA\dev\nota-fiscal-notebook-dell.pdf'
def extrair_texto_pdf(caminho_arquivo):
    reader = PdfReader(caminho_arquivo)
    texto_bruto = ""

    for pagina in reader.pages:
        conteudo = pagina.extract_text()
        if conteudo:
            texto_bruto += conteudo + "\n"

    return texto_bruto

texto_bruto = extrair_texto_pdf(caminho_arquivo)


# ====================================================================
# TODO 2: EXTRAÇÃO INTELIGENTE COM IA (Structured Output)
# ====================================================================
# Use a API da OpenAI para analisar o 'texto_bruto'.
# CRIE UM SYSTEM PROMPT EXTREMAMENTE RÍGIDO pedindo que a IA 
# devolva a resposta NO FORMATO JSON com as chaves:
# "nome_empresa", "data_vencimento", "valor" (só os números).

prompt_sistema = """ Você é um extrator de dados de notas fiscais.

Sua tarefa:
Extrair APENAS os seguintes campos e retornar em JSON válido:

{
  "nome_empresa": "",
  "data_vencimento": "DD-MM-YYYY",
  "valor": 0.0
}

Regras obrigatórias:
- Retorne SOMENTE JSON (sem explicações)
- Valor deve ser número (sem R$, sem vírgula)
- Data no formato DD-MM-YYYY
- Se não encontrar algum campo, deixe como null """

resposta = cliente_ia.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0.1,
    messages=[
        {"role": "system", "content": prompt_sistema},
        {"role": "user", "content": texto_bruto}
    ]
)

resposta_texto = resposta.choices[0].message.content

print("\n RESPOSTA DA IA:")
print(resposta_texto)

# ====================================================================
# TODO 3: CONSOLIDANDO NO PANDAS
# ====================================================================
# 1. Pegue a resposta em JSON gerada pela IA (que é uma string).
# 2. Converta ela em um dicionário Python (use a biblioteca 'json').
# 3. Transforme esse dicionário em uma linha de um DataFrame do Pandas.

try:
    json_extraido = json.loads(resposta_texto)
except:
    print(" Erro ao converter JSON")
    json_extraido = {}

df_resultado = pd.DataFrame([json_extraido])

print("\n Dado Extraído e Estruturado:")
print(df_resultado)

import json
json_extraido = json.loads(...)
df_resultado = pd.DataFrame([json_extraido])
print("\n📊 Dado Extraído e Estruturado:")
print(df_resultado)