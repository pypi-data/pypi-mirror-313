import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler


def inverter_escala(df, colunas, escalas):
    """
    Inverte as escalas de colunas especificadas em um DataFrame.

    Parâmetros:
    - df (pandas.DataFrame): DataFrame contendo os dados.
    - colunas (list): Lista de colunas para as quais a escala deve ser invertida.
    - escalas (list): Lista de valores máximos das escalas correspondentes às colunas.

    Retorna:
    - DataFrame modificado, e opcionalmente, os metadados.
    """
    if not isinstance(colunas, list) or not isinstance(escalas, list) or len(colunas) != len(escalas):
        return "Erro: 'colunas' e 'escalas' devem ser listas de mesmo tamanho.", None

    for coluna, escala in zip(colunas, escalas):
        if coluna in df.columns:
            df[coluna + '_R'] = escala + 1 - df[coluna]
            print(f"Coluna '{coluna + '_R'}' criada.")
        else:
            return f"Erro: A coluna '{coluna}' não existe no DataFrame.", None
        
    return df
        
def transformar_escala(df, coluna, nova_escala_min, nova_escala_max):
    """
    Transforma os valores de uma coluna de um DataFrame de sua escala original para uma nova escala especificada.

    Parâmetros:
    - df (pandas.DataFrame): DataFrame contendo os dados.
    - coluna (str): Nome da coluna a ser transformada.
    - nova_escala_min (int): Valor mínimo da nova escala.
    - nova_escala_max (int): Valor máximo da nova escala.
    
    Retorna:
    - DataFrame com a coluna transformada.
    """
    # Extrair os valores mínimo e máximo originais da coluna
    orig_min = df[coluna].min()
    orig_max = df[coluna].max()

    # Verificar se os valores mínimos e máximos não são nulos
    if pd.isna(orig_min) or pd.isna(orig_max):
        raise ValueError("A coluna contém apenas valores nulos.")

    # Aplicar a transformação linear para a nova escala
    df[coluna + '_Nova_Escala'] = df[coluna].apply(
        lambda x: (x - orig_min) / (orig_max - orig_min) * (nova_escala_max - nova_escala_min) + nova_escala_min
        if pd.notnull(x) else None
    )

    print(f"Coluna '{coluna + '_Nova_Escala'}' criada.")

    return df

def padronizar_colunas(df, colunas):
    """
    Padroniza as colunas especificadas de um DataFrame.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    colunas (list): Lista de colunas a serem padronizadas.

    Retorna:
    pd.DataFrame: DataFrame original com as colunas padronizadas adicionadas.
    """
    df2 = df.copy(deep=True)

    # Inicializar o StandardScaler
    scaler = StandardScaler()

    # Ajustar e transformar os dados
    colunas_padronizadas = scaler.fit_transform(df2[colunas])

    # Criar novos nomes para as colunas padronizadas
    colunas_padronizadas_nomes = [f"z_{col}" for col in colunas]

    # Adicionar colunas padronizadas ao DataFrame original
    df2[colunas_padronizadas_nomes] = colunas_padronizadas

    return df2

def apply_case_weights(df, freq_column, seed=42):
    """
    Cria um novo DataFrame ponderado repetindo as linhas de acordo com os pesos.
    
    Args:
    df (pd.DataFrame): DataFrame original.
    freq_column (str): Nome da coluna que contém as frequências (pesos).
    seed (int, optional): Semente para o gerador de números aleatórios.
    
    Returns:
    pd.DataFrame: Novo DataFrame com os casos ponderados.
    """
    # Defina a semente para garantir resultados consistentes
    np.random.seed(seed)
    
    # Verifica se a coluna de frequências está no DataFrame
    if freq_column not in df.columns:
        raise ValueError(f"A coluna de pesos '{freq_column}' não está presente no DataFrame.")
    
    # Cria uma lista para armazenar as linhas ponderadas
    weighted_rows = []
    
    for i, row in df.iterrows():
        # Adiciona a parte inteira das linhas
        integer_part = int(np.floor(row[freq_column]))
        weighted_rows.extend([row.to_dict()] * integer_part)
        
        # Adiciona a parte decimal das linhas
        decimal_part = row[freq_column] - integer_part
        if np.random.rand() < decimal_part:
            weighted_rows.append(row.to_dict())
    
    # Cria um novo DataFrame com as linhas ponderadas
    df_weighted = pd.DataFrame(weighted_rows).reset_index(drop=True)
    
    return df_weighted
