#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar a base de transações
df_transacoes = pd.read_csv("base_transactions_maquininha_5000.csv")

# Converter a coluna de data
df_transacoes["data_hora"] = pd.to_datetime(df_transacoes["data_hora"])

# Criar colunas auxiliares
df_transacoes["mes"] = df_transacoes["data_hora"].dt.to_period("M")
df_transacoes["hora"] = df_transacoes["data_hora"].dt.hour

# Estatísticas gerais
analise_geral = {
    "Total de transações": len(df_transacoes),
    "Total de clientes únicos": df_transacoes["id_cliente"].nunique(),
    "Valor médio das transações": df_transacoes["valor_transacao"].mean(),
    "Percentual de transações suspeitas": df_transacoes["suspeita"].mean() * 100,
    "Percentual em região de fronteira": df_transacoes["regiao_fronteira"].mean() * 100
}

# Gráfico 1: Distribuição dos valores das transações
plt.figure(figsize=(10, 5))
sns.histplot(df_transacoes["valor_transacao"], bins=50, kde=True)
plt.title("Distribuição dos Valores das Transações")
plt.xlabel("Valor (R$)")
plt.ylabel("Frequência")
plt.grid(True)
plt.tight_layout()
plt.savefig("plot_valores.png")
plt.close()

# Gráfico 2: Quantidade de transações por mês
plt.figure(figsize=(10, 5))
df_transacoes.groupby("mes").size().plot(kind="bar")
plt.title("Quantidade de Transações por Mês")
plt.xlabel("Mês")
plt.ylabel("Quantidade")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("plot_transacoes_mes.png")
plt.close()

# Gráfico 3: Proporção de transações suspeitas vs normais
plt.figure(figsize=(6, 6))
df_transacoes["suspeita"].value_counts().plot(kind="pie", labels=["Normais", "Suspeitas"], autopct="%1.1f%%", startangle=90, colors=["#66bb6a", "#ef5350"])
plt.title("Distribuição de Transações Suspeitas")
plt.ylabel("")
plt.tight_layout()
plt.savefig("plot_suspeitas.png")
plt.close()

# Gráfico 4: Transações por hora do dia
plt.figure(figsize=(10, 5))
sns.countplot(x="hora", data=df_transacoes, palette="viridis")
plt.title("Distribuição das Transações por Hora do Dia")
plt.xlabel("Hora")
plt.ylabel("Quantidade de Transações")
plt.grid(True)
plt.tight_layout()
plt.savefig("plot_horas.png")
plt.close()

# Mostrar a análise geral em tabela
df_analise_geral = pd.DataFrame(analise_geral, index=["Valor"])
df_analise_geral.describe()
