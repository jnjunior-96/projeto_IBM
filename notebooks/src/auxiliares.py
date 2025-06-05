import pandas as pd

# tradução de nome das colunas para o streamlit

niveis_educacionais_texto = {
    1: "Ensino Médio",
    2: "Tecnólogo",
    3: "Graduação",
    4: "Mestrado",
    5: "Doutorado",
}

area_fomacao_texto = {
    "Human Resources": "Recursos Humanos",
    "Life Sciences": "Ciências da Vida",
    "Marketing": "Marketing",
    "Medical": "Medicina",
    "Other": "Outros",
    "Technical Degree": "Diploma Técnico"
}

niveis_satisfacao_texto = {
    1: "Baixo",
    2: "Médio",
    3: "Alto",
    4: "Muito Alto",
}

niveis_vida_trabalho_texto = {
    1: "Ruim",
    2: "Bom",
    3: "Melhor",
    4: "Superior",
}

generos_texto = {
    "Female": "Feminino",
    "Male": "Masculino",
}

departamentos_texto = {
    "Sales": "Vendas",
    "Research & Development": "P&D",
    "Human Resources":"RH"
}

cargos_texto = {
    "Sales Executive":"Executivo de Vendas",
    "Research Scientist":"Cientista Pesquisador",
    "Laboratory Technician":"Técnico de Laboratório",
    "Manufacturing Director":"Diretor de Fabricação",
    "Healthcare Representative":"Representante de Saúde",
    "Manager":"Gerente",
    "Sales Representative":"Representante de vendas",
    "Research Director":"Diretor de Pesquisa",
    "Human Resources":"Recursos Humanos",
}

viagem_texto = {
    "Travel_Rarely":"Raramente viaja",
    "Travel_Frequently":"Frequentemente viaja",
    "Non-Travel":"Não viaja"
}

def dataframe_coeficientes(coefs, colunas):
    return pd.DataFrame(data=coefs, index=colunas, columns=["coeficiente"]).sort_values(
        by="coeficiente"
    )
