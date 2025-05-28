import pandas as pd

from DB_costumers import gerar_clientes
from DB_transations import gerar_transacoes_em_blocos


def main():
    # Gerar e salvar a nova base de 5000 clientes
    df_clientes_5000 = gerar_clientes(5000)
    path_clientes_5000 = "base_clientes_maquininha_5000.csv"
    df_clientes_5000.to_csv(path_clientes_5000, index=False)
    path_clientes_5000

    df_clientes_5000 = pd.read_csv(
        "/var/home/talita/Documents/MBA/base_clientes_maquininha_5000.csv"
    )

    # Gerar as transações para os 5000 clientes
    df_transacoes_5000 = gerar_transacoes_em_blocos(
        df_clientes_5000, bloco_tamanho=1000
    )
    df_transacoes_5000.to_csv(
        "/var/home/talita/Documents/MBA/base_transactions_maquininha_5000.csv",
        index=False,
    )


if __name__ == "__main__":
    main()
