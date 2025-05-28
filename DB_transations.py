
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from uuid import uuid4

# Recriar variáveis auxiliares para geração de transações
MESES_HISTORICO = 12
TRANSACOES_POR_CLIENTE = (50, 300)
PERCENTUAL_SUSPEITAS = 0.05

cnae_padroes = {
    "47.81-4/00": {"min": 10, "max": 200, "inicio": 9, "fim": 20},
    "56.11-2/01": {"min": 15, "max": 120, "inicio": 10, "fim": 23},
    "96.02-5/01": {"min": 20, "max": 150, "inicio": 8, "fim": 19},
    "95.11-8/00": {"min": 30, "max": 250, "inicio": 9, "fim": 18},
    "81.21-4/00": {"min": 25, "max": 180, "inicio": 8, "fim": 18},
    "49.30-2/01": {"min": 50, "max": 300, "inicio": 7, "fim": 19},
}

formas_pagamento = ["Crédito", "Débito", "PIX"]
bandeiras = ["Visa", "Mastercard", "Elo", "Hipercard"]
status_transacao = ["Aprovada", "Negada", "Estornada"]

municipios_coords = {
    "Foz do Iguaçu": (-25.5469, -54.5882),
    "Corumbá": (-19.0089, -57.6510),
    "Santana do Livramento": (-30.8773, -55.5392),
    "Curitiba": (-25.4284, -49.2733),
    "São Paulo": (-23.5505, -46.6333),
    "Belo Horizonte": (-19.9167, -43.9345),
    "Salvador": (-12.9714, -38.5014),
    "Fortaleza": (-3.7172, -38.5433),
}

# Função para gerar transações por cliente
def gerar_transacoes_para_cliente(cliente, total_transacoes):
    transacoes = []
    cnae = cliente["cnae_codigo"]
    receita = cliente["receita_declarada"]
    municipio = cliente["municipio"]
    base_lat, base_lon = municipios_coords.get(municipio, (-15.0, -47.0))

    padrao = cnae_padroes.get(cnae, {"min": 20, "max": 200, "inicio": 8, "fim": 20})
    qtd_suspeitas = int(total_transacoes * PERCENTUAL_SUSPEITAS)
    qtd_normais = total_transacoes - qtd_suspeitas

    for i in range(total_transacoes):
        suspeita = i >= qtd_normais
        dias_atras = random.randint(0, MESES_HISTORICO * 30)
        data = datetime.now() - timedelta(days=dias_atras)

        if suspeita:
            hora = random.choice(list(range(0, padrao["inicio"])) + list(range(padrao["fim"] + 1, 24)))
        else:
            hora = random.randint(padrao["inicio"], padrao["fim"])
        minuto = random.randint(0, 59)
        segundo = random.randint(0, 59)
        data_hora = data.replace(hour=hora, minute=minuto, second=segundo)

        if suspeita:
            valor = random.uniform(receita * 0.2, receita * 5.0)
        else:
            valor = random.uniform(padrao["min"], padrao["max"])
        valor = round(valor, 2)

        transacoes.append({
            "id_transacao": str(uuid4()),
            "id_cliente": cliente["id_cliente"],
            "data_hora": data_hora.strftime("%Y-%m-%d %H:%M:%S"),
            "valor_transacao": valor,
            "forma_pagamento": random.choice(formas_pagamento),
            "parcelas": random.randint(1, 12),
            "bandeira_cartao": random.choice(bandeiras),
            "status_transacao": random.choices(status_transacao, weights=[0.94, 0.03, 0.03])[0],
            "latitude": base_lat + random.uniform(-0.01, 0.01),
            "longitude": base_lon + random.uniform(-0.01, 0.01),
            "suspeita": 1 if suspeita else 0,
            "regiao_fronteira": 1 if cliente["fronteira"] == "Sim" else 0
        })
    print(f"Transacoes: {transacoes}")
    return transacoes

# Gerar em blocos
def gerar_transacoes_em_blocos(df_clientes, bloco_tamanho=1000):
    todas_transacoes = []
    total_clientes = df_clientes.shape[0]
    blocos = [df_clientes.iloc[i:i + bloco_tamanho] for i in range(0, total_clientes, bloco_tamanho)]

    for bloco in blocos:
        print(f"Rodando bloco: {bloco}")
        bloco_transacoes = []
        for _, cliente in bloco.iterrows():
            n = random.randint(*TRANSACOES_POR_CLIENTE)
            bloco_transacoes.extend(gerar_transacoes_para_cliente(cliente, n))
        todas_transacoes.extend(bloco_transacoes)

    return pd.DataFrame(todas_transacoes)


df_clientes_5000 = pd.read_csv("/var/home/talita/Documents/MBA/base_clientes_maquininha_5000.csv")

# Gerar as transações para os 5000 clientes
df_transacoes_5000 = gerar_transacoes_em_blocos(df_clientes_5000, bloco_tamanho=1000)
df_transacoes_5000.to_csv("/var/home/talita/Documents/MBA/base_transactions_maquininha_5000.csv", index=False)
