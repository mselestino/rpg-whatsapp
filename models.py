def get_habilidades_raca(raca):
    if raca == "Executivo":
        return {"forca": 4, "destreza": 5, "inteligencia": 8, "furia": 3, "carisma": 9, "disciplina": 7, "constituicao": 4, "agilidade": 6, "sorte": 5}
    elif raca == "Analítico":
        return {"forca": 3, "destreza": 7, "inteligencia": 9, "furia": 2, "carisma": 5, "disciplina": 8, "constituicao": 5, "agilidade": 7, "sorte": 4}
    elif raca == "Técnico":
        return {"forca": 5, "destreza": 6, "inteligencia": 7, "furia": 3, "carisma": 6, "disciplina": 8, "constituicao": 5, "agilidade": 5, "sorte": 4}
    # Adicione outras raças conforme necessário

def get_habilidades_classe(classe):
    if classe == "Gerente de Vendas":
        return {"forca": 6, "destreza": 7, "inteligencia": 8, "furia": 6, "carisma": 10, "disciplina": 8, "constituicao": 6, "agilidade": 7, "sorte": 4}
    elif classe == "Analista de Mercado":
        return {"forca": 4, "destreza": 8, "inteligencia": 10, "furia": 2, "carisma": 5, "disciplina": 9, "constituicao": 5, "agilidade": 6, "sorte": 7}
    # Adicione outras classes conforme necessário
