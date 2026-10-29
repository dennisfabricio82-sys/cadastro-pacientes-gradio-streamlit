
# %% [markdown]
# CADASTRO DE PACIENTES - GRADIO
# Atividade Prática - Aula 1
#
# Sistema de cadastro de pacientes de um consultório médico.
# Os dados são armazenados em um arquivo CSV.

# %%
# ETAPA 1 - IMPORTAÇÃO DAS BIBLIOTECAS

import gradio as gr
import pandas as pd

from datetime import datetime
from pathlib import Path


# %%
# ETAPA 2 - CONFIGURAÇÃO DO ARQUIVO CSV

# Identificar a pasta onde este arquivo Python está salvo
PASTA_PROJETO = Path(__file__).resolve().parent

# Definir o caminho do CSV
ARQUIVO_CSV = PASTA_PROJETO / "pacientes.csv"

# Definir as colunas do arquivo
COLUNAS = [
    "timestamp",
    "nome",
    "idade",
    "convenio",
    "prioridade",
    "motivo"
]


# %%
# ETAPA 3 - FUNÇÃO PARA CONSULTAR PACIENTES

def carregar_ultimos():

    if ARQUIVO_CSV.exists():

        dados = pd.read_csv(ARQUIVO_CSV)

        return dados.tail(5)

    return pd.DataFrame(columns=COLUNAS)


# %%
# ETAPA 4 - FUNÇÃO PARA CADASTRAR PACIENTES

def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):

    # Validar o nome
    if not nome or not nome.strip():
        return "Informe o nome do paciente.", carregar_ultimos()

    # Validar a idade
    if idade is None or idade < 0 or idade > 120:
        return "Informe uma idade válida (0 a 120).", carregar_ultimos()

    # Criar um dicionário com os dados
    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome.strip(),
        "idade": int(idade),
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": motivo
    }

    # Transformar em DataFrame
    novo = pd.DataFrame([linha], columns=COLUNAS)

    # Gravar no CSV
    if ARQUIVO_CSV.exists():

        novo.to_csv(
            ARQUIVO_CSV,
            mode="a",
            header=False,
            index=False,
            encoding="utf-8-sig"
        )

    else:

        novo.to_csv(
            ARQUIVO_CSV,
            mode="w",
            header=True,
            index=False,
            encoding="utf-8-sig"
        )

    return "Paciente cadastrado com sucesso!", carregar_ultimos()


# %%
# ETAPA 5 - CONSTRUÇÃO DA INTERFACE GRADIO

with gr.Blocks() as demo:

    gr.Markdown("# Cadastro de Pacientes")
    gr.Markdown("Sistema de cadastro - Consultório Médico")

    nome = gr.Textbox(
        label="Nome do paciente",
        placeholder="Digite o nome completo"
    )

    idade = gr.Number(
        label="Idade",
        minimum=0,
        maximum=120,
        precision=0
    )

    convenio = gr.Dropdown(
        choices=[
            "Particular",
            "Unimed",
            "Bradesco Saúde",
            "SulAmérica",
            "Outro"
        ],
        label="Convênio",
        value="Particular"
    )

    prioridade = gr.Slider(
        minimum=1,
        maximum=5,
        step=1,
        value=1,
        label="Prioridade do atendimento (5 = urgente)"
    )

    motivo = gr.Textbox(
        label="Motivo da consulta / observações",
        placeholder="Descreva o motivo da consulta",
        lines=3
    )

    botao = gr.Button(
        "Cadastrar",
        variant="primary"
    )

    saida_msg = gr.Textbox(
        label="Status do cadastro",
        interactive=False
    )

    tabela = gr.Dataframe(
        value=carregar_ultimos(),
        label="Últimos 5 pacientes cadastrados",
        interactive=False
    )

    # Conectar o botão à função de cadastro
    botao.click(
        fn=cadastrar_paciente,
        inputs=[nome, idade, convenio, prioridade, motivo],
        outputs=[saida_msg, tabela]
    )


# %%
# ETAPA 6 - INICIAR A APLICAÇÃO

if __name__ == "__main__":
    demo.launch(inbrowser=True)
