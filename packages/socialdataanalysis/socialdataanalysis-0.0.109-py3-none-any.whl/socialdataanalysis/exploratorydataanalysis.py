import pandas as pd
import numpy as np

import scipy.stats as stats
from statsmodels.stats.diagnostic import lilliefors
from scipy.stats import pearsonr

from tabulate import tabulate

import plotly.graph_objs as go
import plotly.io as pio
import plotly.express as px


def gerar_tabela_frequencias_OLD(df, meta, coluna):

    """
    Gera uma tabela de frequência para uma coluna específica de um DataFrame.

    Parâmetros:
    df (pandas.DataFrame): DataFrame contendo os dados.
    meta (pyreadstat.Meta): Metadados do arquivo SAV.
    coluna (str): Nome da coluna para a qual a tabela de frequência será gerada.

    Exibe:
    Tabela de frequência com os valores, frequências, percentuais e percentuais cumulativos.
    """

    df[coluna] = df[coluna].round(2)

    # Mapear os valores para labels usando meta.variable_value_labels
    value_labels = meta.variable_value_labels.get(coluna, {})

    # Criar a tabela de frequência
    frequency_table = df[coluna].value_counts(dropna=False).sort_index().reset_index()
    frequency_table.columns = [coluna, 'Frequency']
    frequency_table['Value Labels'] = frequency_table[coluna].map(value_labels)

    # Reordenar as colunas
    frequency_table = frequency_table[[coluna, 'Value Labels', 'Frequency']]

    # Calcular os percentuais
    total_cases = len(df)
    frequency_table['Percent'] = (frequency_table['Frequency'] / total_cases * 100).round(2)
    frequency_table['Cumulative Percent'] = frequency_table['Percent'].cumsum().round(2)

    # Adicionar linha de Total
    total_row = pd.DataFrame({
        coluna: ['Total'], 
        'Value Labels': [''], 
        'Frequency': [frequency_table['Frequency'].sum()], 
        'Percent': [''], 
        'Cumulative Percent': ['']
    })
    frequency_table = pd.concat([frequency_table, total_row], ignore_index=True)

    # Exibir a tabela
    print(tabulate(frequency_table, headers='keys', tablefmt='grid', showindex=False))

def gerar_tabela_frequencias(df, meta, variaveis):
    """
    Gera uma tabela de frequência combinada para variáveis específicas de um DataFrame.

    Parâmetros:
    df (pandas.DataFrame): DataFrame contendo os dados.
    meta (pyreadstat.Meta): Metadados do arquivo SAV.
    variaveis (list): Lista de nomes das variáveis para as quais a tabela de frequência será gerada.

    Exibe:
    Tabela de frequência com os valores, frequências, percentuais e percentuais cumulativos combinados.
    """
    df2 = df.copy(deep=True)

    # Se for apenas uma variável, transforme em lista
    if isinstance(variaveis, str):
        variaveis = [variaveis]

    # Lista para armazenar os DataFrames individuais
    frequency_tables = []

    for var in variaveis:
        df2[var] = df2[var].round(2)

        # Mapear os valores para labels usando meta.variable_value_labels
        value_labels = meta.variable_value_labels.get(var, {})

        # Criar a tabela de frequência para a variável atual
        frequency_table = df2[var].value_counts(dropna=False).sort_index().reset_index()
        frequency_table.columns = ['Value', 'Frequency']
        frequency_table['Value Labels'] = frequency_table['Value'].map(value_labels)
        
        # Adicionar a variável à lista de DataFrames
        frequency_tables.append(frequency_table)

    # Concatenar todos os DataFrames individuais
    frequency_combined = pd.concat(frequency_tables, ignore_index=True)

    if len(variaveis) > 1:
        # Combinar as frequências das variáveis
        frequency_combined = frequency_combined.groupby(['Value', 'Value Labels']).agg({'Frequency': 'sum'}).reset_index()
    else:
        # Reordenar as colunas
        frequency_combined = frequency_combined[['Value', 'Value Labels', 'Frequency']]

    # Calcular os percentuais
    total_cases = len(df2) * len(variaveis)  # total de casos é multiplicado pelo número de variáveis
    frequency_combined['Percent'] = (frequency_combined['Frequency'] / total_cases * 100).round(2)
    frequency_combined['Cumulative Percent'] = frequency_combined['Percent'].cumsum().round(2)

    # Adicionar linha de Total
    total_row = pd.DataFrame({
        'Value': ['Total'], 
        'Value Labels': [''], 
        'Frequency': [frequency_combined['Frequency'].sum()], 
        'Percent': [''], 
        'Cumulative Percent': ['']
    })
    frequency_combined = pd.concat([frequency_combined, total_row], ignore_index=True)

    # Exibir a tabela
    print(tabulate(frequency_combined, headers='keys', tablefmt='grid', showindex=False))



def gerar_tabela_estatisticas_descritivas_OLD(df, variables):
    """
    Gera uma tabela de estatísticas descritivas para as variáveis especificadas em um DataFrame.
    
    Parâmetros:
    df (pd.DataFrame): O DataFrame contendo os dados a serem analisados.
    variaveis (list): Uma lista de nomes de colunas (strings) no DataFrame a serem analisadas.
    
    Retorna:
    str: Uma tabela formatada com as estatísticas descritivas.
    """
    results = []
    for var in variables:
        n = df[var].count()
        mean = f"{df[var].mean()}"
        std_dev = f"{df[var].std()}"
        skewness = f"{df[var].skew()}"
        std_err_skew = ((6 * n * (n - 1)) / ((n - 2)*(n + 1)*(n + 3))) ** 0.5
        std_err_kurt = ((4 * (n ** 2 - 1)) * (std_err_skew ** 2) / ((n - 3) * (n + 5))) ** 0.5
        std_err_skew = f"{(std_err_skew)}"
        kurtosis = f"{df[var].kurtosis()}"
        std_err_kurt = f"{(std_err_kurt)}"
        results.append([
            var, n, mean, std_dev, skewness, std_err_skew, kurtosis, std_err_kurt
        ])
    
    headers = ["Variable", "Valid\nN", "Mean", "Std.\nDeviation",
               "Skewness", "Std. Error\nof Skewness",
               "Kurtosis", "Std. Error\nof Kurtosis"]
    floatfmt = ("", ".0f", ".3f", ".3f",
                ".3f", ".3f",
                ".3f", ".3f")

    table = tabulate(results, headers, tablefmt="grid", floatfmt=floatfmt)
    
    print(table)

def gerar_tabela_estatisticas_descritivas(df, variaveis):
    """
    Gera uma tabela de estatísticas descritivas para as variáveis especificadas em um DataFrame.
    
    Parâmetros:
    df (pd.DataFrame): O DataFrame contendo os dados a serem analisados.
    variaveis (list): Uma lista de nomes de colunas (strings) no DataFrame a serem analisadas.
    
    Retorna:
    str: Uma tabela formatada com as estatísticas descritivas.
    """
    results = []
    for var in variaveis:
        n = df[var].count()
        mean = df[var].mean()
        std_dev = df[var].std()
        skewness = df[var].skew()
        std_err_skew = ((6 * n * (n - 1)) / ((n - 2)*(n + 1)*(n + 3))) ** 0.5
        skewness_ratio = skewness / std_err_skew
        kurtosis = df[var].kurtosis()
        std_err_kurt = ((4 * (n ** 2 - 1)) * (std_err_skew ** 2) / ((n - 3) * (n + 5))) ** 0.5
        kurtosis_ratio = kurtosis / std_err_kurt
        min_value = df[var].min()
        max_value = df[var].max()
        results.append([
            var, n, mean, std_dev, skewness, std_err_skew, skewness_ratio, kurtosis, std_err_kurt, kurtosis_ratio, min_value, max_value
        ])
    
    headers = ["Variable", "Valid\nN", "Mean", "Std.\nDeviation",
               "Skewness", "Std. Error\nof Skewness", "Skewness / \nStd. Error",
               "Kurtosis", "Std. Error\nof Kurtosis", "Kurtosis / \nStd. Error", "Minimum", "Maximum"]
    floatfmt = ("", ".0f", ".3f", ".3f",
                ".3f", ".3f", ".3f",
                ".3f", ".3f", ".3f", ".3f", ".3f")

    table = tabulate(results, headers, tablefmt="grid", floatfmt=floatfmt)
    
    print(table)


def gerar_tabela_normalidade(df, variables):
    """
    Realiza testes de normalidade (Kolmogorov-Smirnov com correção de Lilliefors e Shapiro-Wilk) 
    nas variáveis especificadas em um DataFrame e gera uma tabela formatada com os resultados.
    
    Parâmetros:
    df (pd.DataFrame): O DataFrame contendo os dados a serem testados.
    variables (list): Uma lista de nomes de colunas (strings) no DataFrame a serem testadas.
    
    Retorna:
    str: Uma tabela formatada com os resultados dos testes de normalidade.
    """
    results = []
    for var in variables:
        # Normalize the data
        normalized_data = (df[var] - df[var].mean()) / df[var].std()
        
        # Kolmogorov-Smirnov com correção de Lilliefors
        k_stat, k_p = lilliefors(normalized_data, dist='norm')
        
        # Shapiro-Wilk
        s_stat, s_p = stats.shapiro(normalized_data)
        
        # Número de graus de liberdade
        df_k = len(normalized_data)
        df_s = len(normalized_data)
        
        results.append([var, round(k_stat, 3), df_k, round(k_p, 3), round(s_stat, 3), df_s, round(s_p, 3)])
    
    headers = ["Variable", "Kolmogorov-Smirnov\nStatistic", "df", "Sig.", 
               "Shapiro-Wilk\nStatistic", "df", "Sig."]
    table = tabulate(results, headers, tablefmt="grid")
    print("Tests of Normality")
    print(table)
    print('Note: Lilliefors Significance Correction to Kolmogorov-Smirnov.')

def display_correlation_matrix(df, variables):
    """
    Calcula e exibe a matriz de correlação e os valores de significância (1-tailed)
    para as variáveis fornecidas.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    variables (list): Lista de variáveis para analisar.

    Retorna:
    None: Exibe uma tabela formatada com os resultados.
    """
    # Selecionar as variáveis a serem analisadas
    data = df[variables].dropna()

    # Calcular a matriz de correlação
    corr_matrix = data.corr()

    # Calcular os valores de significância
    p_values = np.zeros((len(variables), len(variables)))
    for i in range(len(variables)):
        for j in range(len(variables)):
            if i != j:
                _, p_value = pearsonr(data.iloc[:, i], data.iloc[:, j])
                p_values[i, j] = p_value / 2  # 1-tailed
            else:
                p_values[i, j] = 0  # Na diagonal, o valor de p é 0

    # Formatar a tabela de correlação
    headers = ["Correlation Matrix"] + variables
    rows = []

    rows.append(["Correlation"] + [""] * len(variables))
    for i, var in enumerate(variables):
        rows.append([var] + [f"{corr_matrix.iloc[i, j]:.3f}" for j in range(len(variables))])

    rows.append(["Sig. (1-tailed)"] + [""] * len(variables))
    for i, var in enumerate(variables):
        rows.append([var] + [f"{p_values[i, j]:.3f}" for j in range(len(variables))])

    # Calcular o determinante da matriz de correlação
    determinant = np.linalg.det(corr_matrix.values)

    # Exibir a tabela formatada
    print(tabulate(rows, headers, tablefmt="grid"))
    print(f"Determinant = {determinant:.3f}")

def plot_boxplot(df, variables, x_axis_title, y_axis_title):
    """
    Gera um gráfico de caixas interativo para as variáveis especificadas e identifica outliers.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados a serem analisados.
    variables (list): Lista de nomes de colunas (strings) no DataFrame a serem analisadas.
    x_axis_title (str): Título para o eixo X do gráfico.
    y_axis_title (str): Título para o eixo Y do gráfico.

    Retorna:
    None: Exibe um gráfico interativo com caixas para cada variável, incluindo pontos de outliers.
    """

    # Preparar dados para Plotly
    df_melted = df[variables].melt(var_name='Variable', value_name='Z-score')
    df_melted['ID'] = df_melted.index + 1

    # Criar gráfico de caixas interativo
    fig = px.box(df_melted, x='Variable', y='Z-score', points='all', hover_data=['ID'], color='Variable')

    # Atualizar layout para melhor apresentação
    fig.update_layout(
        title="",
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
        template="plotly_white",
        showlegend=False
    )

    fig.show()

def plot_profile(df, variables, category_var='categoria', category_values=None):
    """
    Gera gráficos de perfil interativos para cada categoria especificada e exibe a tabela de comparação.
    
    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    variables (list): Lista de variáveis para análise.
    category_var (str): Nome da variável da categoria.
    category_values (list): Lista de valores específicos da categoria para geração dos gráficos.
    
    Retorna:
    None: Exibe os gráficos de perfil interativos e a tabela de comparação.
    """
    pio.renderers.default = 'notebook'  # Define o renderizador padrão para o Jupyter Notebook
    
    if category_values is None:
        category_values = df[category_var]
    
    # Verificar se as categorias especificadas existem no DataFrame
    for value in category_values:
        if value not in df[category_var].values:
            raise ValueError(f"Categoria '{value}' não encontrada na variável '{category_var}'.")
    
    # Calcular a média das variáveis para cada categoria
    means = df.groupby(category_var)[variables].mean()
    
    # Criar o gráfico interativo
    fig = go.Figure()
    
    for value in category_values:
        fig.add_trace(go.Scatter(
            x=variables,
            y=means.loc[value, variables],
            mode='lines+markers',
            name=value
        ))
    
    # Ajustar layout do gráfico
    fig.update_layout(
        title='Perfil das Categorias',
        xaxis_title='Variáveis',
        yaxis_title='Média',
        template='plotly_white',
        legend_title_text=category_var,
        width=800,
        height=600
    )
    
    fig.show()
    
    # Criar e exibir a tabela de comparação
    comparison_table = means.loc[category_values].reset_index()

    # Formatar os números para três casas decimais
    formatted_table = comparison_table.map(lambda x: f"{x:.3f}" if isinstance(x, (int, float)) else x)

    # Obter os dados da tabela e os cabeçalhos
    table_data = formatted_table.values.tolist()
    table_headers = formatted_table.columns.tolist()

    # Exibir a tabela formatada usando tabulate
    print(tabulate(table_data, headers=table_headers, tablefmt="grid"))


def plot_scatter(df, x_var, y_var, category_var, category_values=None):
    """
    Gera um gráfico de dispersão interativo para as categorias especificadas.
    
    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    x_var (str): Nome da variável para o eixo x.
    y_var (str): Nome da variável para o eixo y.
    category_var (str): Nome da variável categórica.
    category_values (list): Lista de valores específicos da categoria para geração dos gráficos. Se None, plota todas as categorias.
    
    Retorna:
    None: Exibe o gráfico de dispersão interativo.
    """
    pio.renderers.default = 'notebook'  # Define o renderizador padrão para o Jupyter Notebook

    if category_values is not None:
        df = df[df[category_var].isin(category_values)]
    
    # Criar o gráfico de dispersão interativo
    fig = px.scatter(df, x=x_var, y=y_var, text=category_var, color=category_var,
                     labels={x_var: x_var, y_var: y_var},
                     title="")
    
    # Adicionar as anotações para as categorias
    fig.update_traces(textposition='top center')
   
    # Adicionar linhas de referência nos eixos
    fig.add_shape(type='line', x0=0, x1=0, y0=min(df[y_var]), y1=max(df[y_var]),
                  line=dict(color='Black', width=0))
    fig.add_shape(type='line', x0=min(df[x_var]), x1=max(df[x_var]), y0=0, y1=0,
                  line=dict(color='Black', width=0))
    
    # Ocultar a legenda
    fig.update_layout(showlegend=False)
    
    # Mostrar o gráfico
    fig.show()

    # Criar e exibir a tabela de comparação com três casas decimais
    comparison_table = df[[category_var, x_var, y_var]].groupby(category_var).mean().reset_index()
    comparison_table = comparison_table.round(3)  # Arredondar para três casas decimais
    display(comparison_table)

def casos_menores_desvios_padrao(df, variaveis, id_coluna=None, limite_desvio=0.5):
    """
    Exibe os casos com desvios padrões populacionais calculados sobre as linhas para as variáveis especificadas
    que são menores que um limite especificado e os ordena do menor para o maior desvio padrão.
    
    Parâmetros:
    df (pd.DataFrame): O DataFrame contendo os dados a serem analisados.
    variaveis (list): Uma lista de nomes de colunas (strings) no DataFrame a serem analisadas.
    id_coluna (str, opcional): O nome da coluna que contém os IDs dos casos. Se None, a coluna ID não é utilizada.
    limite_desvio (float): O limite superior para o desvio padrão. Padrão é 0.5.
    
    Retorna:
    pd.DataFrame: DataFrame com os casos e seus respectivos desvios padrões que são menores que o limite especificado.
    """
    # Calcular o desvio padrão populacional para cada linha nas variáveis especificadas
    df['std_dev_cases'] = df[variaveis].std(axis=1, ddof=0)
    
    # Filtrar os casos com desvio padrão menor que o limite especificado
    menores_desvios = df[df['std_dev_cases'] <= limite_desvio]
    
    # Ordenar pelo desvio padrão em ordem crescente
    menores_desvios = menores_desvios.sort_values(by='std_dev_cases')
    
    # Reordenar as colunas para mostrar o ID (se fornecido) e o desvio padrão ao final
    if id_coluna:
        cols = [id_coluna] + variaveis + ['std_dev_cases']
    else:
        cols = variaveis + ['std_dev_cases']
    
    menores_desvios = menores_desvios[cols]

    display(menores_desvios)

    print("N. Cases:", len(menores_desvios))