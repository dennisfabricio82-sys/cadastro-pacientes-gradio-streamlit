
# %% [markdown]
# ============================================================
# CADASTRO DE PACIENTES - STREAMLIT
# Atividade Prática - Aula 1
#
# Funcionalidades:
# 1. Formulário de cadastro de pacientes
# 2. Registro automático de data e hora
# 3. Armazenamento em arquivo CSV
# 4. Exibição dos últimos 5 pacientes
# 5. Gerenciamento com st.session_state
# 6. Download dos cadastros em CSV
# ============================================================


# %%
# ETAPA 1 - IMPORTAÇÃO DAS BIBLIOTECAS

import streamlit as st
import pandas as pd

from datetime import datetime
from pathlib import Path


# %%
# ETAPA 2 - CONFIGURAÇÃO DA PÁGINA

st.set_page_config(
    page_title="Cadastro de Pacientes",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Cadastro de Pacientes")
st.write("Sistema de cadastro - Consultório Médico")


# %%
# ETAPA 3 - CONFIGURAÇÃO DO ARQUIVO CSV

PASTA_PROJETO = Path(__file__).resolve().parent

ARQUIVO_CSV = PASTA_PROJETO / "pacientes.csv"

COLUNAS = [
    "timestamp",
    "nome",
    "idade",
    "convenio",
    "prioridade",
    "motivo"
]


# %%
# ETAPA 4 - FUNÇÃO PARA CARREGAR OS PACIENTES

def carregar_pacientes():

    if ARQUIVO_CSV.exists():

        try:
            return pd.read_csv(
                ARQUIVO_CSV,
                encoding="utf-8-sig"
            )

        except (OSError, pd.errors.EmptyDataError):
            pass

    return pd.DataFrame(columns=COLUNAS)


# %%
# ETAPA 5 - FUNÇÃO PARA SALVAR NO CSV

def salvar_paciente(paciente):

    novo = pd.DataFrame(
        [paciente],
        columns=COLUNAS
    )

    arquivo_existe = ARQUIVO_CSV.exists()

    novo.to_csv(
        ARQUIVO_CSV,
        mode="a" if arquivo_existe else "w",
        header=not arquivo_existe,
        index=False,
        encoding="utf-8-sig"
    )


# %%
# ETAPA 6 - INICIALIZAÇÃO DO SESSION_STATE

if "pacientes" not in st.session_state:

    st.session_state.pacientes = carregar_pacientes()


# %%
# ETAPA 7 - FORMULÁRIO DE CADASTRO

with st.form("formulario_pacientes"):

    nome = st.text_input(
        "Nome do paciente",
        placeholder="Digite o nome completo"
    )

    idade = st.number_input(
        "Idade",
        min_value=0,
        max_value=120,
        value=0,
        step=1
    )

    convenio = st.selectbox(
        "Convênio",
        [
            "Particular",
            "Unimed",
            "Bradesco Saúde",
            "SulAmérica",
            "Outro"
        ]
    )

    prioridade = st.slider(
        "Prioridade do atendimento (5 = urgente)",
        min_value=1,
        max_value=5,
        value=1,
        step=1
    )

    motivo = st.text_area(
        "Motivo da consulta / observações",
        placeholder="Descreva o motivo da consulta"
    )

    cadastrar = st.form_submit_button(
        "Cadastrar",
        use_container_width=True
    )


# %%
# ETAPA 8 - PROCESSAMENTO DO CADASTRO

if cadastrar:

    if not nome.strip():

        st.error(
            "Informe o nome do paciente."
        )

    elif idade < 0 or idade > 120:

        st.error(
            "Informe uma idade válida."
        )

    else:

        paciente = {
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "nome": nome.strip(),
            "idade": int(idade),
            "convenio": convenio,
            "prioridade": int(prioridade),
            "motivo": motivo
        }

        novo = pd.DataFrame(
            [paciente],
            columns=COLUNAS
        )

        # Salva o registro no CSV quando possível.
        try:
            salvar_paciente(paciente)

        except OSError:
            st.warning(
                "Não foi possível salvar no arquivo local. "
                "O cadastro permanecerá disponível nesta sessão."
            )

        # Atualiza a tabela da sessão.
        st.session_state.pacientes = pd.concat(
            [
                st.session_state.pacientes,
                novo
            ],
            ignore_index=True
        )

        st.success(
            f"Paciente {nome.strip()} cadastrado com sucesso!"
        )


# %%
# ETAPA 9 - EXIBIÇÃO DOS ÚLTIMOS 5 PACIENTES

st.divider()

st.subheader(
    "Últimos 5 pacientes cadastrados"
)

dados = st.session_state.pacientes

if dados.empty:

    st.info(
        "Nenhum paciente cadastrado ainda."
    )

else:

    st.dataframe(
        dados.tail(5),
        use_container_width=True,
        hide_index=True
    )

    st.write(
        f"Total de pacientes: {len(dados)}"
    )


# %%
# ETAPA 10 - DOWNLOAD DO ARQUIVO CSV

st.divider()

st.subheader("Exportar cadastros")

st.write(
    "Baixe os registros em formato CSV "
    "para armazená-los no seu computador."
)

csv_download = dados.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="📥 Baixar pacientes.csv",
    data=csv_download,
    file_name="pacientes.csv",
    mime="text/csv",
    disabled=dados.empty,
    use_container_width=True
)
