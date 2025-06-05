import pandas as pd
import streamlit as st

from joblib import load

from notebooks.src.config import DADOS_TRATADOS, MODELO_FINAL
from notebooks.src.auxiliares import (
    niveis_educacionais_texto,
    area_fomacao_texto,
    niveis_satisfacao_texto,
    niveis_vida_trabalho_texto,
    generos_texto,
    departamentos_texto,
    cargos_texto,
    viagem_texto
    )

@st.cache_data
def carregar_dados():
    return pd.read_parquet(DADOS_TRATADOS)

@st.cache_data
def carregar_modelo():
    return load(MODELO_FINAL)

df = carregar_dados()
modelo = carregar_modelo()

generos = sorted(df["Gender"].unique())
niveis_educacionais = sorted(df["Education"].unique())
area_fomacao = sorted(df["EducationField"].unique())
departamentos = sorted(df["Department"].unique())
viagem_negocios = sorted(df["BusinessTravel"].unique())
hora_extra = sorted(df["OverTime"].unique())
satisfacao_trabalho = sorted(df["JobSatisfaction"].unique())
satisfacao_colegas = sorted(df["RelationshipSatisfaction"].unique())
satisfacao_ambiente = sorted(df["EnvironmentSatisfaction"].unique())
vida_trabalho = sorted(df["WorkLifeBalance"].unique())
opcao_acoes = sorted(df["StockOptionLevel"].unique())
envolvimento_trabalho = sorted(df["JobInvolvement"].unique())

colunas_slider =[
    "DistanceFromHome",
    "MonthlyIncome",
    "NumCompaniesWorked",
    "PercentSalaryHike",
    "TotalWorkingYears",
    "TrainingTimesLastYear",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager",
]

colunas_slider_min_max ={
    coluna: {"min_value": df[coluna].min(), "max_value": df[coluna].max()}
    for coluna in colunas_slider
}

colunas_ignoradas = (
    "Age",
    "DailyRate",
    "JobLevel",
    "HourlyRate",
    "MonthlyRate",
    "PerformanceRating",
)

mediana_colunas_ignoradas = {
    coluna: df[coluna].median() for coluna in colunas_ignoradas
}

st.title("Previsão de Atrito")

with st.container(border=True):
    st.write("### Informações pessoais:")
    coluna_esquerda, coluna_direita = st.columns(2)

    with coluna_esquerda:
        
        widget_nivel_edu = st.selectbox(
            "Nível Educacional",
            niveis_educacionais,
            format_func= lambda numero: niveis_educacionais_texto[numero]
        )
        widget_area_formacao = st.selectbox(
            "Área de Formação",
            area_fomacao,
            format_func= lambda texto: area_fomacao_texto[texto]
        )
    
    with coluna_direita:
        widget_genero = st.radio("Gêneros", generos, horizontal=True, format_func= lambda texto: generos_texto[texto])
        

    widget_distancia = st.slider("Distância de Casa", **colunas_slider_min_max["DistanceFromHome"])

with st.container(border=True):
    st.write("### Rotina na empresa:")

    coluna_esquerda, coluna_direita = st.columns(2)

    with coluna_esquerda:
        widget_departamento = st.selectbox("Departamento", departamentos,format_func= lambda texto: departamentos_texto[texto])
        widget_viagem_negocios = st.selectbox("Viagem Negócios", viagem_negocios, format_func=lambda viagem: viagem_texto[viagem])

    with coluna_direita:
        widget_cargo = st.selectbox(
            "Cargo",
            sorted(df[df["Department"] == widget_departamento]["JobRole"].unique()),
            format_func= lambda cargo: cargos_texto[cargo]
        )

        widget_hora_extra = st.radio("Horas extras", hora_extra, horizontal=True)
    widget_salario_mensal = st.slider("Salário Mensal", **colunas_slider_min_max["MonthlyIncome"])



with st.container(border=True):
    st.write("### Experiência profissional:")

    coluna_esquerda, coluna_direita = st.columns(2)

    with coluna_esquerda:
        widget_empresas_trabalhadas = st.slider(
            "Empresas trabalhadas", **colunas_slider_min_max["NumCompaniesWorked"])
        widget_anos_trabalhados = st.slider(
            "Anos trabalhadas", **colunas_slider_min_max["TotalWorkingYears"])
        widget_anos_empresa = st.slider(
            "Anos na empresa", **colunas_slider_min_max["YearsAtCompany"])

    with coluna_direita:
        widget_cargo_atual = st.slider(
            "Anos no cargo atual", **colunas_slider_min_max["YearsInCurrentRole"])
        widget_mesmo_superior = st.slider(
            "Anos com o mesmo Superior", **colunas_slider_min_max["YearsWithCurrManager"])
        widget_ultima_promocao = st.slider(
            "Anos desde última promoção", **colunas_slider_min_max["YearsSinceLastPromotion"])



with st.container(border=True):
    st.write("### Incentivos e Métricas:")
    coluna_esquerda, coluna_direita = st.columns(2)

    with coluna_esquerda:
        widget_satisfacao_trabalho = st.selectbox(
            "Satisfação no Trabalho",
            satisfacao_trabalho,
            format_func=lambda numero: niveis_satisfacao_texto[numero]
        )

        widget_satisfacao_colegas = st.selectbox(
            "Satisfação com colegas",
            satisfacao_colegas,
            format_func=lambda numero: niveis_satisfacao_texto[numero]
        )
        widget_opcoes_acoes = st.radio("Opções de Ações", opcao_acoes, horizontal=True)

    with coluna_direita:

        widget_satisfacao_ambiente = st.selectbox(
            "Satisfação com Ambiente",
            satisfacao_ambiente,
            format_func=lambda numero: niveis_satisfacao_texto[numero]
        )

        widget_balanco_vida_trabalho = st.selectbox(
            "Balanço vida-trabalho",
            vida_trabalho,
            format_func=lambda numero: niveis_vida_trabalho_texto[numero]
        )

        widget_envolvimento_trabalho = st.selectbox("Envolvimento no Trabalho", envolvimento_trabalho)
        

    widget_aumento_salarial = st.slider(
        "Aumento Salarial (%)",
        **colunas_slider_min_max["PercentSalaryHike"]
    )

    widget_treinamentos_ultimo_ano = st.slider(
        "Treinamentos último ano",
        **colunas_slider_min_max["TrainingTimesLastYear"]
    )

entrada_modelo = {
    "Age": mediana_colunas_ignoradas["Age"],
    "BusinessTravel": widget_viagem_negocios,
    "DailyRate": mediana_colunas_ignoradas["DailyRate"],
    "Department": widget_departamento,
    "DistanceFromHome": widget_distancia,
    "Education": widget_nivel_edu,
    "EducationField": widget_area_formacao,
    "EnvironmentSatisfaction": widget_satisfacao_ambiente,
    "Gender": widget_genero,
    "HourlyRate": mediana_colunas_ignoradas["HourlyRate"],
    "JobInvolvement": widget_envolvimento_trabalho,
    "JobLevel":mediana_colunas_ignoradas["JobLevel"],
    "JobRole": widget_cargo,
    "JobSatisfaction": widget_satisfacao_trabalho,
    "MaritalStatus": "Single",
    "MonthlyIncome": widget_salario_mensal,
    "MonthlyRate":mediana_colunas_ignoradas["MonthlyRate"],
    "NumCompaniesWorked": widget_empresas_trabalhadas,
    "PerformanceRating": mediana_colunas_ignoradas["PerformanceRating"],
    "OverTime": widget_hora_extra,
    "PercentSalaryHike": widget_aumento_salarial,
    "RelationshipSatisfaction": widget_satisfacao_colegas,
    "StockOptionLevel": widget_opcoes_acoes,
    "TotalWorkingYears": widget_anos_trabalhados,
    "TrainingTimesLastYear": widget_treinamentos_ultimo_ano,
    "WorkLifeBalance": widget_balanco_vida_trabalho,
    "YearsAtCompany": widget_anos_empresa,
    "YearsInCurrentRole": widget_cargo_atual,
    "YearsSinceLastPromotion": widget_ultima_promocao,
    "YearsWithCurrManager": widget_mesmo_superior,
}


df_entrada_modelo = pd.DataFrame([entrada_modelo])

botao_previsao = st.button("Prever Atrito")

if botao_previsao:
    previsao = modelo.predict(df_entrada_modelo)[0]
    probabilidade_atrito = modelo.predict_proba(df_entrada_modelo)[0][1]

    cor = ":red" if previsao == 1 else ":green"

    texto_probabilidade = (
        f"### Probabilidade de atrito: {cor}[{probabilidade_atrito:.1%}]"
    )

    texto_atrito = f"### Atrito : {cor}[{'Sim' if previsao == 1 else 'Não'}]"

    st.markdown(texto_atrito)
    st.markdown(texto_probabilidade)