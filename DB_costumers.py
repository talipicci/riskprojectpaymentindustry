#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 11 09:55:41 2025

@author: talita
"""

# Reimportar bibliotecas e redefinir funções após reset
import pandas as pd
import numpy as np
import random


# Função para gerar clientes
def gerar_clientes(n=1000):
    random.seed(42)
    np.random.seed(42)

    lista_cnaes = [
        ("47.81-4/00", "Comércio varejista de artigos do vestuário"),
        ("56.11-2/01", "Restaurantes e similares"),
        ("96.02-5/01", "Cabeleireiros"),
        ("95.11-8/00", "Reparação de computadores"),
        ("81.21-4/00", "Limpeza em prédios e domicílios"),
        ("49.30-2/01", "Transporte rodoviário de carga municipal"),
    ]

    municipios_fronteira = ["Foz do Iguaçu", "Corumbá", "Santana do Livramento"]
    estados_fronteira = {
        "Foz do Iguaçu": "PR",
        "Corumbá": "MS",
        "Santana do Livramento": "RS",
    }

    municipios_normais = [
        "Curitiba",
        "São Paulo",
        "Belo Horizonte",
        "Salvador",
        "Fortaleza",
    ]
    estados_normais = {
        "Curitiba": "PR",
        "São Paulo": "SP",
        "Belo Horizonte": "MG",
        "Salvador": "BA",
        "Fortaleza": "CE",
    }

    clientes = []

    for i in range(n):
        id_cliente = f"CL{i:05d}"
        nome_fantasia = f"Empresa {i}"
        tipo_cliente = np.random.choice(["MEI", "EPP"], p=[0.9, 0.1])
        cnae_codigo, cnae_desc = random.choice(lista_cnaes)
        receita = (
            np.random.randint(20000, 80000)
            if tipo_cliente == "MEI"
            else np.random.randint(100000, 500000)
        )

        if random.random() < 0.1:
            municipio = random.choice(municipios_fronteira)
            fronteira = "Sim"
            cidade_gemea = "Sim"
            estado = estados_fronteira[municipio]
        else:
            municipio = random.choice(municipios_normais)
            fronteira = "Não"
            cidade_gemea = "Não"
            estado = estados_normais[municipio]

        risco_sofisticacao = np.random.randint(1, 8)
        risco_capacidade = np.random.randint(1, 8)
        risco_abrangencia = np.random.randint(1, 8)
        risco_proveito = np.random.randint(1, 8)
        risco_incidente = (
            2.0 if cidade_gemea == "Sim" else 1.5 if fronteira == "Sim" else 1.0
        )

        risco_bruto = (
            risco_sofisticacao + risco_capacidade + risco_abrangencia + risco_proveito
        )
        risco_ajustado = risco_bruto * risco_incidente

        if risco_ajustado <= 11:
            risco_final = "Baixo"
        elif risco_ajustado <= 18:
            risco_final = "Médio"
        elif risco_ajustado <= 25:
            risco_final = "Alto"
        else:
            risco_final = "Muito Alto"

        clientes.append(
            {
                "id_cliente": id_cliente,
                "nome_fantasia": nome_fantasia,
                "tipo_cliente": tipo_cliente,
                "cnae_codigo": cnae_codigo,
                "cnae_descricao": cnae_desc,
                "receita_declarada": receita,
                "municipio": municipio,
                "estado": estado,
                "fronteira": fronteira,
                "cidade_gemea": cidade_gemea,
                "risco_sofisticacao": risco_sofisticacao,
                "risco_capacidade": risco_capacidade,
                "risco_abrangencia": risco_abrangencia,
                "risco_proveito": risco_proveito,
                "risco_incidente": risco_incidente,
                "risco_final": risco_final,
            }
        )

    return pd.DataFrame(clientes)
