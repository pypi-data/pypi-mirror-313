import pandas as pd
import numpy as np

from itertools import combinations
import pingouin as pg

import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from tabulate import tabulate

from factor_analyzer import FactorAnalyzer, Rotator
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo



def analisar_consistencia_interna(df, variaveis, n_factors=3, exibir_correlacoes=False, exibir_resumo=False, exibir_heatmap=False):
    """
    Analisa o alfa de Cronbach, Ômega de MacDonald e as correlações para um conjunto específico de variaveis de um DataFrame.
    
    Parâmetros:
        df (pd.DataFrame): DataFrame contendo os dados a serem analisados.
        variaveis (list): Lista de variaveis a serem incluídas na análise.
        exibir_correlacoes (bool): Se True, imprime a matriz de correlações.
        exibir_resumo (bool): Se True, imprime o resumo do alfa de Cronbach com e sem cada coluna.
        exibir_heatmap (bool): Se True, exibe um heatmap das correlações.

    Retorna:
        tuple: Retorna o alfa de Cronbach original, o Ômega de MacDonald, a matriz de correlações e o resumo do alfa de Cronbach se cada coluna for removida.
    """

    def calcular_cronbach_alpha(data, variaveis):
        data = data[variaveis]
        item_vars = data.var(axis=0, ddof=1)
        total_var = data.sum(axis=1).var(ddof=1)
        n_items = data.shape[1]
        alpha = n_items / (n_items - 1) * (1 - item_vars.sum() / total_var)
        return alpha

    def calcular_omega(data, variaveis, rotation='oblimin', method='minres', n_factors=3):
        """
        Calcula o ômega total de um conjunto de dados fornecido.

        :param data: pd.DataFrame. O conjunto de dados bruto.
        :param variaveis: list. As variáveis a serem consideradas na análise.
        :param rotation: str. A rotação a ser usada na análise fatorial. Padrão é 'oblimin'.
        :param method: str. O método de análise fatorial a ser usado. Padrão é 'minres'.
        :param n_factors: int. O número de fatores a serem considerados. Padrão é 3.
        :return: float. O valor de ômega total.
        """
        # Selecionar as variáveis
        data = data[variaveis]

        # Imputar valores ausentes, se necessário
        if data.isnull().values.any():
            data = data.fillna(data.median())

        # Realizar a análise fatorial
        fa = FactorAnalyzer(rotation=rotation, method=method, n_factors=n_factors)
        fa.fit(data)

        # Calcular as cargas fatoriais
        loadings = fa.loadings_

        # Calcular o ômega total
        omega_total = np.sum(np.square(loadings)) / (np.sum(np.square(loadings)) + np.sum(np.square(fa.get_uniquenesses())))

        return omega_total
    
    df_filtrado = df[variaveis]
    correlacoes = df_filtrado.corr()

    # Calcula o alfa de Cronbach original
    alfa_original = None
    if len(variaveis) > 1:
        alfa_original = calcular_cronbach_alpha(data=df, variaveis=variaveis)

    # Calcula o Ômega de MacDonald original
    omega_total = None
    if len(variaveis) > 1:
        omega_total = calcular_omega(data=df, variaveis=variaveis, n_factors=n_factors)

    # Exibe o alfa de Cronbach original e o Ômega de MacDonald
    resultados = []
    if alfa_original is not None:
        resultados.append(['Alfa de Cronbach Original', round(alfa_original, 3)])
    if omega_total is not None:
        resultados.append(['Ômega de MacDonald Original', round(omega_total, 3)])

    if resultados:
        print(tabulate(resultados, headers=['Métrica', 'Valor'], tablefmt='grid'))

    if len(variaveis) > 1:
        # Calcula o alfa de Cronbach e Ômega se cada variavel for removida
        alfas_removidos = {}
        omegas_removidos = {}

        for variavel in variaveis:
            temp_df = df_filtrado.drop(columns=[variavel])
            alfas_removidos[variavel] = None
            omegas_removidos[variavel] = None
            if len(temp_df.columns) > 1:
                try:
                    alfa_removido = calcular_cronbach_alpha(data=temp_df, variaveis=temp_df.columns)
                    alfas_removidos[variavel] = alfa_removido

                    omega_removido = calcular_omega(data=temp_df, variaveis=temp_df.columns, n_factors=n_factors)
                    omegas_removidos[variavel] = omega_removido

                except Exception as e:
                    print(f"Erro ao calcular os valores removendo a variavel {variavel}: {e}")

        # Exibe o resumo do alfa de Cronbach e Ômega de MacDonald se item removido
        if exibir_resumo:
            resumo = pd.DataFrame({
                'Alfa se item removido': alfas_removidos,
                'Ômega se item removido': omegas_removidos
            })
            #resumo_tabela = [[variavel, round(alfa, 3), round(omega, 3)] for variavel, (alfa, omega) in resumo.iterrows()]
            resumo_tabela = [
                [variavel, round(alfa, 3) if alfa is not None else None, round(omega, 3) if omega is not None else None]
                for variavel, (alfa, omega) in resumo.iterrows()
            ]
            print("\nAlfa e Ômega se item removido:")
            print(tabulate(resumo_tabela, headers=['Coluna', 'Alfa', 'Ômega'], tablefmt='grid'))      

    # Exibe a matriz de correlações
    if exibir_correlacoes:
        correlacoes_tabela = correlacoes.round(3).reset_index().values.tolist()
        correlacoes_tabela.insert(0, [''] + list(correlacoes.columns))
        print("\nCorrelações:")
        print(tabulate(correlacoes_tabela, headers='firstrow', tablefmt='grid'))

    # Exibe o heatmap das correlações
    if exibir_heatmap:
        sns.heatmap(correlacoes, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title("\nMatriz de Correlações")
        plt.show()

def display_kmo_bartlett_results(df, variables):
    """
    Calcula e exibe os resultados da Medida de Adequação de Amostragem de Kaiser-Meyer-Olkin (KMO)
    e do Teste de Esfericidade de Bartlett para as variáveis fornecidas.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    variables (list): Lista de variáveis para analisar.

    Retorna:
    None: Exibe uma tabela formatada com os resultados.
    """
    # Selecionar as variáveis a serem analisadas
    data = df[variables].dropna()

    # Calcular o KMO
    kmo_all, kmo_model = calculate_kmo(data)

    # Calcular o Teste de Esfericidade de Bartlett
    chi_square_value, p_value = calculate_bartlett_sphericity(data)

    # Calcular os graus de liberdade
    num_vars = len(variables)
    df_value = (num_vars * (num_vars - 1)) / 2
   
    # Formatar a tabela de resultados
    table = [
        ["Kaiser-Meyer-Olkin Measure (KMO) of Sampling Adequacy.", f"{kmo_model:.3f}"],
        ["", ""],
        ["Bartlett's Test of Sphericity", ""],
        ["Approx. Chi-Square", f"{chi_square_value:.3f}"],
        ["df", f"{df_value:.0f}"],
        ["Sig.", f"{p_value:.3f}"]
    ]

    kmo_individual_table = [["Individual KMO", ""]]
    kmo_individual_table += [[var, f"{kmo_all[i]:.3f}"] for i, var in enumerate(variables)]

    print(tabulate(table, tablefmt="grid"))
    print()
    print(tabulate(kmo_individual_table, tablefmt="grid"))
    print("Note: Individual KMO from Anti-Image Correlation Diagonal")


def display_eigenvalues_and_variance_explained(df, variables, method, rotation, n_factors=None):
    """
    Calcula e exibe os resultados da Análise de Componentes Principais (PCA) ou outro método de extração
    para as variáveis fornecidas, incluindo autovalores, variância explicada, e um gráfico de Scree Plot.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    variables (list): Lista de variáveis para analisar.
    method (str): Método de extração a ser usado ('principal', 'ml', etc.).
    rotation (str): Método de rotação a ser usado ('varimax', 'promax', etc.).
    n_factors (int, opcional): Número de fatores a serem extraídos. Se None, o número de fatores será determinado automaticamente.

    Retorna:
    None: Exibe uma tabela formatada com os resultados e um gráfico de Scree Plot.
    """

    # Selecionar as variáveis a serem analisadas
    data = df[variables].dropna()

    ## Cálculos sem rotação e com method = 'principal' ##
    # Ajustar o fator analisador
    fa = FactorAnalyzer(rotation=None, method="principal", n_factors=len(variables))
    fa.fit(data)
    # Extrair autovalores
    eigenvalues, vectors = fa.get_eigenvalues()
    # Extrair as cargas fatoriais
    loadings = fa.loadings_
    # Calcular variância explicada e variância acumulada
    variance_explained, proportional_variance_explained, cumulative_variance_explained = fa.get_factor_variance()

    n_factors_extracted = next((index for index, value in enumerate(variance_explained) if value < 1), len(variance_explained))

    if n_factors is None:
        ## Identificar o primeiro índice onde variance_explained < 1 ##
        n_factors = n_factors_extracted

    ## Cálculos sem rotação com extração ##
    # Ajustar o fator analisador para PCA
    fa_ex = FactorAnalyzer(rotation=None, method=method, n_factors=n_factors)
    fa_ex.fit(data)
    # Extrair autovalores
    eigenvalues_ex, vectors_ex = fa_ex.get_eigenvalues()
    # Extrair as cargas fatoriais
    loadings_ex = fa_ex.loadings_
    # Calcular variância explicada e variância acumulada
    variance_explained_ex, proportional_variance_explained_ex, cumulative_variance_explained_ex = fa_ex.get_factor_variance()

    ## Cálculos com rotação com extração ##
    # Ajustar o fator analisador para PCA
    fa_rotated_ex = FactorAnalyzer(rotation=rotation, method=method, n_factors=n_factors)
    fa_rotated_ex.fit(data)
    # Extrair autovalores
    eigenvalues_rotated_ex, vectors_rotated_ex = fa_rotated_ex.get_eigenvalues()
    # Extrair as cargas fatoriais
    loadings_rotated_ex = fa_rotated_ex.loadings_
    # Calcular variância explicada e variância acumulada
    variance_explained_rotated_ex, proportional_variance_explained_rotated_ex, cumulative_variance_explained_rotated_ex = fa_rotated_ex.get_factor_variance()

    # Preparar tabela de resultados
    rows = []
    for i in range(len(variables)):
        if i < n_factors:
            rows.append([
                i + 1,
                f"{eigenvalues[i]}", f"{proportional_variance_explained[i]*100}", f"{cumulative_variance_explained[i]*100}",
                f"{variance_explained_ex[i]}", f"{proportional_variance_explained_ex[i]*100}", f"{cumulative_variance_explained_ex[i]*100}",
                f"{variance_explained_rotated_ex[i]}", f"{proportional_variance_explained_rotated_ex[i]*100}", f"{cumulative_variance_explained_rotated_ex[i]*100}"
            ])
        else:
            rows.append([
                i + 1,
                f"{variance_explained[i]}", f"{proportional_variance_explained[i]*100}", f"{cumulative_variance_explained[i]*100:.3f}",
                None, None, None,
                None, None, None
            ])

    headers = ["Component", "Total\nInitial\nEigenvalues", "% of Variance", "Cumulative %",
               "Total\nExtraction\nSS Loadings", "% of Variance", "Cumulative %",
               "Total\nRotation\nSS Loadings", "% of Variance", "Cumulative %"]

    floatfmt = (".0f", ".3f", ".2f", ".2f",
                ".3f", ".2f", ".2f",
                ".3f", ".2f", ".2f",)
    elements_name = {
        'principal': ('Principal Component Analysis', 'PCA'),
        'minres': ('Principal Axis Factoring', 'PAF'),
        'ml': ('Maximum Likelihood', 'ML'),
    }

    print("Total Variance Explained")
    print(tabulate(rows, headers, tablefmt="grid", floatfmt=floatfmt))
    print(f"Extraction Method: {elements_name[method][0]}.")
    print(f"Rotation Method: {rotation} with Kaiser Normalization.")
  
    # Gerar o gráfico de Scree Plot
    x_values = list(range(1, len(eigenvalues) + 1))
    fig = px.line(x=x_values, y=eigenvalues, markers=True, title="")
    fig.update_layout(
        xaxis_title="Component Number",
        yaxis_title="Eigenvalue",
        template="plotly_white",
        width=500,
        height=400,
        xaxis=dict(
            tickmode='array',
            tickvals=x_values,
            ticktext=x_values
        ),
    )
    fig.show()

def display_communality_matrix(df, variables, method, n_factors):
    """
    Calcula e exibe as comunalidades para as variáveis fornecidas.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    variables (list): Lista de variáveis para analisar.
    method (str): Método de extração a ser usado ('principal', 'minres', 'ml', etc.).
    n_factors (int): Número de fatores a serem extraídos.

    Retorna:
    None: Exibe tabelas formatadas com os resultados.
    """
    from factor_analyzer import FactorAnalyzer
    from tabulate import tabulate

    # Selecionar as variáveis a serem analisadas
    data = df[variables].dropna()

    # Ajustar o fator analisador
    fa = FactorAnalyzer(rotation=None, method=method, n_factors=n_factors)
    fa.fit(data)

    # Extrair as comunalidades
    communalities = fa.get_communalities()

    # Preparar tabela de comunalidades
    communality_rows = []
    for i, var in enumerate(variables):
        communality_rows.append([var, f"{communalities[i]:.3f}"])

    communality_headers = ["Variable", "Communality"]

    # Mapeamento da extração
    elements_name = {
        'principal': 'Components',
        'minres': 'Factors',
        'ml': 'Factors'
    }

    # Mapeamento de métodos para seus nomes completos
    method_names = {
        'principal': 'Principal Component Analysis',
        'minres': 'Principal Axis Factoring',
        'ml': 'Maximum Likelihood'
    }
    print(f"Communalities")
    print(tabulate(communality_rows, communality_headers, tablefmt="grid"))
    print(f"Extraction Method: {method_names.get(method, 'Unknown Method')}.")
    print(f"{n_factors} {elements_name.get(method, 'Unknown Method')} extracted.")


def display_component_matrix(df, variables, method, n_factors):
    """
    Calcula e exibe a matriz de componentes para as variáveis fornecidas.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    variables (list): Lista de variáveis para analisar.
    method (str): Método de extração a ser usado ('principal', 'minres', 'ml', etc.).
    n_factors (int): Número de fatores a serem extraídos.

    Retorna:
    None: Exibe tabelas formatadas com os resultados.
    """
    from factor_analyzer import FactorAnalyzer
    from tabulate import tabulate

    # Selecionar as variáveis a serem analisadas
    data = df[variables].dropna()

    # Ajustar o fator analisador
    fa = FactorAnalyzer(rotation=None, method=method, n_factors=n_factors)
    fa.fit(data)

    # Extrair a matriz de componentes
    loadings = fa.loadings_

    # Preparar tabela de matriz de componentes
    component_rows = []
    for i, var in enumerate(variables):
        component_rows.append([var] + [f"{loadings[i, j]:.3f}" for j in range(loadings.shape[1])])

    # Mapeamento da extração
    elements_name = {
        'principal': 'Components',
        'minres': 'Factors',
        'ml': 'Factors'
    }

    component_headers = ["Variable"] + [f"Factor {i + 1}" for i in range(loadings.shape[1])]

    # Mapeamento de métodos para seus nomes completos
    method_names = {
        'principal': 'Principal Component Analysis',
        'minres': 'Principal Axis Factoring',
        'ml': 'Maximum Likelihood'
    }
    # Exibir tabela de matriz de componentes
    print(f"Factor Matrix")
    print(tabulate(component_rows, component_headers, tablefmt="grid"))
    print(f"Extraction Method: {method_names.get(method, 'Unknown Method')}.")
    print(f"{n_factors} {elements_name.get(method, 'Unknown Method')} extracted.")


def display_communality_and_component_matrix_OLD(df, variables, method, n_factors):
    """
    Calcula e exibe as comunalidades e a matriz de componentes para as variáveis fornecidas.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    variables (list): Lista de variáveis para analisar.
    method (str): Método de extração a ser usado ('principal', 'minres', 'ml', etc.).
    n_factors (int): Número de fatores a serem extraídos.

    Retorna:
    None: Exibe tabelas formatadas com os resultados.
    """
    # Selecionar as variáveis a serem analisadas
    data = df[variables].dropna()

    # Ajustar o fator analisador para PCA
    fa = FactorAnalyzer(rotation=None, method=method, n_factors=n_factors)
    fa.fit(data)

    # Extrair as comunalidades
    communalities = fa.get_communalities()

    # Ajustar o fator analisador para PCA com rotação Varimax
    fa = FactorAnalyzer(rotation=None, method=method, n_factors=n_factors)
    fa.fit(data)

    # Extrair a matriz de componentes
    loadings = fa.loadings_

    # Preparar tabela de comunalidades
    communality_rows = []
    for i, var in enumerate(variables):
        communality_rows.append([var, f"{communalities[i]:.3f}"])

    communality_headers = ["Communalities", "Extraction"]

    # Preparar tabela de matriz de componentes
    component_rows = []
    for i, var in enumerate(variables):
        component_rows.append([var] + [f"{loadings[i, j]:.3f}" for j in range(loadings.shape[1])])

    # Mapeamento da extração
    elements_name = {
        'principal': 'Components',
        'minres': 'Factors',
        'ml': 'Factors'
    }

    component_headers = [f"{elements_name.get(method, 'Unknown Method')}"] + [str(i + 1) for i in range(loadings.shape[1])]

    ## Exibir tabelas formatadas ##

    # Mapeamento de métodos para seus nomes completos
    method_names = {
        'principal': 'Principal Component Analysis',
        'minres': 'Principal Axis Factoring',
        'ml': 'Maximum Likelihood'
    }
    print(f"Communalities")
    print(tabulate(communality_rows, communality_headers, tablefmt="grid"))
    print(f"Extraction Method: {method_names.get(method, 'Unknown Method')}.")
    print(f"{n_factors} {elements_name.get(method, 'Unknown Method')} extracted.")
    print()
    print(f"Factor Matrix")
    print(tabulate(component_rows, component_headers, tablefmt="grid"))
    print(f"Extraction Method: {method_names.get(method, 'Unknown Method')}.")
    print(f"{n_factors} {elements_name.get(method, 'Unknown Method')} extracted.")


def display_rotated_component_matrix(df, variables, method, n_factors, rotation, plot=False):
    """
    Calcula e exibe a matriz de componentes rotacionada para as variáveis fornecidas
    usando Análise de Componentes Principais (PCA) com rotação especificada.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    variables (list): Lista de variáveis para analisar.
    method (str): Método de extração a ser usado ('principal', 'minres', 'ml', etc.).
    n_factors (int): Número de fatores a serem extraídos.
    rotation (str): Método de rotação a ser usado ('varimax', 'promax', etc.).
    plot (bool): Se True, gera gráficos de dispersão das cargas fatoriais rotacionadas para todas as combinações de fatores.

    Retorna:
    None: Exibe uma tabela formatada com os resultados e, opcionalmente, gráficos de dispersão.
    """
    # Selecionar as variáveis a serem analisadas
    data = df[variables].dropna()

    # Ajustar o fator analisador para PCA com rotação especificada
    fa_rotated = FactorAnalyzer(rotation=rotation, method=method, n_factors=n_factors)
    fa_rotated.fit(data)

    # Extrair a matriz de componentes rotacionada
    loadings_rotated = fa_rotated.loadings_

    # Preparar tabela de matriz de componentes rotacionada
    component_rows = []
    for i, var in enumerate(variables):
        component_rows.append([var] + [loadings_rotated[i, j] for j in range(loadings_rotated.shape[1])])

    # Ordenar as linhas pelo módulo das maiores cargas fatoriais
    component_rows.sort(key=lambda row: tuple(-abs(row[i + 1]) for i in range(n_factors)))

    # Formatando os valores para exibição
    formatted_rows = [[row[0]] + [f"{value:.3f}" for value in row[1:]] for row in component_rows]

    # Mapeamento da extração
    elements_name = {
        'principal': 'Component',
        'minres': 'Factor',
        'ml': 'Factor'
    }

    component_headers = [f"{elements_name.get(method, 'Unknown Method')}"] + [str(i + 1) for i in range(loadings_rotated.shape[1])]

    print(f"Rotated Factor Matrix")
    # Exibir tabela formatada
    print(tabulate(formatted_rows, component_headers, tablefmt="grid"))

    # Mapeamento de métodos para seus nomes completos
    method_names = {
        'principal': 'Principal Component Analysis',
        'minres': 'Principal Axis Factoring',
        'ml': 'Maximum Likelihood'
    }

    print(f"Extraction Method: {method_names.get(method, 'Unknown Method')}.")
    print(f"Rotation Method: {rotation}.")

    # Gerar gráficos de dispersão para todas as combinações de fatores se plot=True
    if plot:
        for (i, j) in combinations(range(n_factors), 2):
            x_values = loadings_rotated[:, i]
            y_values = loadings_rotated[:, j]

            # Adicionar um pequeno deslocamento aleatório aos labels
            offset = np.random.uniform(-0.05, 0.05, size=len(x_values))
            
            # Calcular os limites dos eixos
            margin = 0.2
            x_min, x_max = min(x_values), max(x_values) + margin
            y_min, y_max = min(y_values), max(y_values) + margin
            x_range = max(abs(x_min), abs(x_max))
            y_range = max(abs(y_min), abs(y_max))
           
            fig = px.scatter(
                x=x_values, 
                y=y_values, 
                text=variables, 
                title=f"{method_names.get(method, 'Unknown Method')} {i+1} vs {method_names.get(method, 'Unknown Method')} {j+1} in Rotated Space"
            )
            fig.update_layout(
                xaxis_title=f"{elements_name.get(method, 'Unknown Method')} {i+1}",
                yaxis_title=f"{elements_name.get(method, 'Unknown Method')} {j+1}",
                template="plotly_white",
                width=600,
                height=600,
                xaxis=dict(range=[-x_range, x_range], zeroline=True, zerolinewidth=1, zerolinecolor='black'),
                yaxis=dict(range=[-y_range, y_range], zeroline=True, zerolinewidth=1, zerolinecolor='black')
            )
            fig.update_traces(marker=dict(size=12))
            
            # Ajustar a posição dos labels
            fig.for_each_trace(lambda trace: trace.update(textposition='top right'))

            fig.show()

def display_and_store_component_matrices_OLD(df, variables, method, n_factors, rotation, print_results=False):
    """
    Calcula e exibe a matriz de transformação dos componentes e a matriz de coeficientes de pontuação dos componentes
    para as variáveis fornecidas usando Análise de Componentes Principais (PCA) com rotação especificada, e armazena
    os scores resultantes no DataFrame original.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    variables (list): Lista de variáveis para analisar.
    method (str): Método de extração a ser usado ('principal', 'minres', 'ml', etc.).
    n_factors (int): Número de fatores a serem extraídos.
    rotation (str): Método de rotação a ser usado ('varimax', 'promax', etc.).

    Retorna:
    pd.DataFrame: DataFrame original com os scores dos componentes/fatores adicionados.
    """
    # Selecionar as variáveis a serem analisadas
    data = df[variables].dropna()

    # Ajustar o fator analisador para PCA com rotação especificada
    fa_rotated = FactorAnalyzer(rotation=rotation, method=method, n_factors=n_factors)
    fa_rotated.fit(data)

    # Extrair a matriz de transformação dos componentes
    transformation_matrix = fa_rotated.rotation_matrix_

    # Extrair a matriz de componentes rotacionada
    loadings_rotated = fa_rotated.loadings_

    # Calcular a matriz de correlação das variáveis
    corr_matrix = np.corrcoef(data.T)

    # Calcular a matriz de coeficientes de pontuação dos componentes
    inv_corr_matrix = np.linalg.inv(corr_matrix)
    component_scores_matrix = np.dot(inv_corr_matrix, loadings_rotated)

    # Preparar tabela de matriz de transformação dos componentes
    transformation_rows = []
    for i in range(n_factors):
        transformation_rows.append([f"{i + 1}"] + [f"{transformation_matrix[i, j]:.3f}" for j in range(n_factors)])

    # Preparar tabela de matriz de coeficientes de pontuação dos componentes
    score_rows = []
    for i, var in enumerate(variables):
        score_rows.append([var] + [f"{component_scores_matrix[i, j]:.3f}" for j in range(n_factors)])

    # Mapeamento da extração
    elements_name = {
        'principal': ('Principal Component Analysis', 'PCA'),
        'minres': ('Principal Axis Factoring', 'PAF'),
        'ml': ('Maximum Likelihood', 'ML'),
    }

    #transformation_headers = ["Component Transformation Matrix"] + [f"{i + 1}" for i in range(n_factors)]
    score_headers = ["Component Score Coefficient Matrix"] + [f"{i + 1}" for i in range(n_factors)]

    if print_results:
        # Exibir tabelas formatadas
        #print(tabulate(transformation_rows, transformation_headers, tablefmt="grid"))
        #print(f"Extraction Method: {elements_name.get(method, 'Unknown Method')}.")
        #print(f"Rotation Method: {rotation} with Kaiser Normalization.")
        #print()
        print(tabulate(score_rows, score_headers, tablefmt="grid"))
        print(f"Extraction Method: {elements_name[method][0]}.")
        print(f"Rotation Method: {rotation} with Kaiser Normalization.")


    # Armazenar os scores numa cópia do DataFrame original
    df2 = df.copy(deep=True)
    scores = fa_rotated.transform(data)
    for i in range(n_factors):
        df2[f"{elements_name[method][1]}_{i + 1}"] = np.nan
        df2.loc[data.index, f"{elements_name[method][1]}_{i + 1}"] = scores[:, i]
    
    return df2



def store_and_display_factor_score_coefficient_matrix(df, variables, method, n_factors, rotation, print_results=False):
    """
    Realiza análise fatorial no DataFrame fornecido, armazena os escores fatoriais e, opcionalmente, exibe a matriz de coeficientes de escores dos componentes.
    
    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados a serem analisados.
    variables (list): Lista de nomes das colunas no DataFrame a serem incluídas na análise fatorial.
    method (str): Método de extração dos fatores ('principal', 'minres', 'ml').
    n_factors (int): Número de fatores a serem extraídos.
    rotation (str): Método de rotação ('varimax', 'promax', etc.).
    print_results (bool): Se True, imprime a matriz de coeficientes de escores dos componentes.
    
    Retorna:
    pd.DataFrame: Uma cópia do DataFrame original com os escores fatoriais adicionados.
    """
    # Remove quaisquer linhas com valores ausentes nas variáveis especificadas
    data = df[variables].dropna()

    # Inicializa e ajusta o analisador fatorial com o método, número de fatores e rotação especificados
    fa_rotated = FactorAnalyzer(rotation=rotation, method=method, n_factors=n_factors)
    fa_rotated.fit(data)

    # Obtém a matriz de rotação e a matriz de cargas fatoriais
    transformation_matrix = fa_rotated.rotation_matrix_
    loadings_rotated = fa_rotated.loadings_

    # Calcula a matriz de correlação dos dados
    corr_matrix = np.corrcoef(data.T)

    # Calcula a inversa da matriz de correlação
    inv_corr_matrix = np.linalg.inv(corr_matrix)

    # Calcula a matriz de coeficientes de escores dos componentes
    component_scores_matrix = np.dot(inv_corr_matrix, loadings_rotated)

    # Prepara as linhas para a tabela da matriz de transformação
    transformation_rows = []
    for i in range(n_factors):
        transformation_rows.append([f"{i + 1}"] + [f"{transformation_matrix[i, j]:.3f}" for j in range(n_factors)])

    # Prepara as linhas para a tabela da matriz de coeficientes de escores dos componentes
    score_rows = []
    for i, var in enumerate(variables):
        score_rows.append([var] + [f"{component_scores_matrix[i, j]:.3f}" for j in range(n_factors)])

    # Define um dicionário para nomear os métodos
    elements_name = {
        'principal': ('Principal Component Analysis', 'PCA'),
        'minres': ('Principal Axis Factoring', 'PAF'),
        'ml': ('Maximum Likelihood', 'ML'),
    }

    # Prepara os cabeçalhos para a tabela da matriz de coeficientes de escores dos componentes
    score_headers = ["Variables"] + [f"{i + 1}" for i in range(n_factors)]

    if print_results:
        print("Component/Factor Score Coefficient Matrix")
        # Imprime a matriz de coeficientes de escores dos componentes formatada
        print(tabulate(score_rows, score_headers, tablefmt="grid"))
        print(f"Extraction Method: {elements_name[method][0]}.")
        print(f"Rotation Method: {rotation} with Kaiser Normalization.")

    # Armazena os escores fatoriais numa cópia do DataFrame original
    df2 = df.copy(deep=True)
    scores = fa_rotated.transform(data)
    for i in range(n_factors):
        df2[f"{elements_name[method][1]}_{i + 1}"] = np.nan
        df2.loc[data.index, f"{elements_name[method][1]}_{i + 1}"] = scores[:, i]
    
    return df2

def calculate_reproduced_correlations_and_fit_indices_OLD(df, variables, method, n_factors, rotation, print_rc=False, print_fi=False):
    """
    Calcula e interpreta a matriz das correlações reproduzidas ou estimadas e os índices de bondade do ajustamento GFI, AGFI e RMSR.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    variables (list): Lista de variáveis para analisar.
    method (str): Método de extração a ser usado ('principal', 'minres', 'ml', etc.).
    n_factors (int): Número de fatores a serem extraídos.
    rotation (str): Método de rotação a ser usado ('varimax', 'promax', etc.).

    Retorna:
    None: Exibe tabelas formatadas com os resultados.
    """
    # Selecionar as variáveis a serem analisadas
    data = df[variables].dropna()

    # Ajustar o fator analisador para PCA ou PAF com rotação especificada
    fa = FactorAnalyzer(rotation=rotation, method=method, n_factors=n_factors)
    fa.fit(data)
    
    # Extrair a matriz de componentes rotacionada
    loadings = fa.loadings_

    # Calcular a matriz de correlação observada
    observed_corr_matrix = np.corrcoef(data.T)
    
    # Calcular a matriz das correlações reproduzidas
    reproduced_corr_matrix = np.dot(loadings, loadings.T)
    
    # Calcular a matriz residual
    residual_matrix = observed_corr_matrix - reproduced_corr_matrix

    # Preencher diagonal principal com np.nan, pois é a variância numa matriz de correlações
    np.fill_diagonal(residual_matrix, np.nan)

    # Converter matriz residual em DataFrame
    residual_df = pd.DataFrame(residual_matrix, index=variables, columns=variables)

    # Substituir NaN por strings vazias
    residual_df = residual_df.map(lambda x: "" if pd.isna(x) else x)
    
    # Preparar tabela combinada
    headers = ["Reproduced Correlation"] + variables
    combined_rows = []

    combined_rows.append(["Correlation"] + [""] * len(variables))
    for i, var in enumerate(variables):
        combined_rows.append([var] + [f"{reproduced_corr_matrix[i, j]:.3f}" for j in range(len(variables))])

    combined_rows.append(["Residual"] + [""] * len(variables))
    for i, var in enumerate(variables):
        combined_rows.append([var] + [f"{residual_df.iloc[i, j]}" if residual_df.iloc[i, j] == "" else f"{residual_df.iloc[i, j]:.3f}" for j in range(len(variables))])
    
    # Mapeamento da extração
    elements_name = {
        'principal': ('Principal Component Analysis', 'PCA'),
        'minres': ('Principal Axis Factoring', 'PAF'),
        'ml': ('Maximum Likelihood', 'ML'),
    }
    
    if print_rc:
        # Exibir tabela formatada
        print(tabulate(combined_rows, headers, tablefmt="grid"))
        print(f"Extraction Method: {elements_name[method][0]}.")
        print(f"Rotation Method: {rotation} with Kaiser Normalization.")
        print("Note 1: The main diagonal of the correlation matrix represents reproduced communalities.")

        # Calcular o número de resíduos não redundantes com valores absolutos > 0.05
        residual_matrix_no_diag = np.copy(residual_matrix)
        np.fill_diagonal(residual_matrix_no_diag, 0)
        nonredundant_residuals = np.abs(residual_matrix_no_diag[np.triu_indices_from(residual_matrix_no_diag, k=1)])
        count_nonredundant_residuals = np.sum(nonredundant_residuals > 0.05)
        percentage_nonredundant_residuals = (count_nonredundant_residuals / len(nonredundant_residuals)) * 100

        print(f"Note 2: Residuals are computed between observed and reproduced correlations. There are {count_nonredundant_residuals} ({percentage_nonredundant_residuals:.1f}%) nonredundant residuals with absolute values greater than 0.05.")
    
    # Calcular índices de bondade do ajustamento
    p = observed_corr_matrix.shape[0]
    q = n_factors
    
    # GFI
    # Criar cópias das matrizes para não modificar os originais
    observed_corr_matrix_no_diag = np.copy(observed_corr_matrix)
    reproduced_corr_matrix_no_diag = np.copy(reproduced_corr_matrix)

    # Remover a diagonal principal (definir como zero)
    np.fill_diagonal(observed_corr_matrix_no_diag, 0)
    np.fill_diagonal(reproduced_corr_matrix_no_diag, 0)

    # Calcular o GFI sem a diagonal principal
    numerator = np.sum(np.square(observed_corr_matrix_no_diag - reproduced_corr_matrix_no_diag))
    denominator = np.sum(np.square(observed_corr_matrix_no_diag))
    GFI = 1 - (numerator / denominator)

    # AGFI
    AGFI = 1 - ((p * (p + 1) / (2 * q * (p - 1))) * (1 - GFI))

    # RMSR
    residual_matrix_no_diag = observed_corr_matrix_no_diag - reproduced_corr_matrix_no_diag
    RMSR = np.sqrt(np.mean(np.square(residual_matrix_no_diag)))

    GFI = f"{GFI:.4f}"
    AGFI = f"{AGFI:.4f}"
    RMSR = f"{RMSR:.4f}"

    # Exibir índices de bondade do ajustamento
    fit_indices = {
        'GFI': GFI,
        'AGFI': AGFI,
        'RMSR': RMSR
    }

    if print_fi: 
        print("\nFit Indices:")
        print(tabulate(fit_indices.items(), headers=['Index', 'Value'], tablefmt="grid"))



def calculate_observed_reproduced_correlations_OLD(df, variables, method, n_factors, rotation):
    """
    Calcula a matriz das correlações reproduzidas ou estimadas.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    variables (list): Lista de variáveis para analisar.
    method (str): Método de extração a ser usado ('principal', 'minres', 'ml', etc.).
    n_factors (int): Número de fatores a serem extraídos.
    rotation (str): Método de rotação a ser usado ('varimax', 'promax', etc.).

    Retorna:
    tuple: Matrizes de correlações observadas e reproduzidas.
    """
    # Selecionar as variáveis a serem analisadas
    data = df[variables].dropna()

    # Ajustar o fator analisador para PCA ou PAF com rotação especificada
    fa = FactorAnalyzer(rotation=rotation, method=method, n_factors=n_factors)
    fa.fit(data)
    
    # Extrair a matriz de componentes rotacionada
    loadings = fa.loadings_

    # Calcular a matriz de correlação observada
    observed_corr_matrix = np.corrcoef(data.T)
    
    # Calcular a matriz das correlações reproduzidas
    reproduced_corr_matrix = np.dot(loadings, loadings.T)
    
    # Calcular a matriz residual
    residual_matrix = observed_corr_matrix - reproduced_corr_matrix

    # Preencher diagonal principal com np.nan, pois é a variância numa matriz de correlações
    np.fill_diagonal(residual_matrix, np.nan)

    # Converter matriz residual em DataFrame
    residual_df = pd.DataFrame(residual_matrix, index=variables, columns=variables)

    # Substituir NaN por strings vazias
    residual_df = residual_df.map(lambda x: "" if pd.isna(x) else x)

    # Preparar tabela combinada
    headers = [""] + variables
    combined_rows = []

    combined_rows.append(["Observed Correlation"] + [""] * len(variables))
    for i, var in enumerate(variables):
        combined_rows.append([var] + [f"{observed_corr_matrix[i, j]:.3f}" for j in range(len(variables))])

    combined_rows.append(["Reproduced Correlation"] + [""] * len(variables))
    for i, var in enumerate(variables):
        combined_rows.append([var] + [f"{reproduced_corr_matrix[i, j]:.3f}" for j in range(len(variables))])

    combined_rows.append(["Residual"] + [""] * len(variables))
    for i, var in enumerate(variables):
        combined_rows.append([var] + [f"{residual_df.iloc[i, j]}" if pd.isna(residual_df.iloc[i, j]) else f"{residual_df.iloc[i, j]:.3f}" for j in range(len(variables))])
    
    # Mapeamento da extração
    elements_name = {
        'principal': ('Principal Component Analysis', 'PCA'),
        'minres': ('Principal Axis Factoring', 'PAF'),
        'ml': ('Maximum Likelihood', 'ML'),
    }

    # Exibir tabela formatada
    print(tabulate(combined_rows, headers, tablefmt="grid"))
    print(f"Extraction Method: {elements_name[method][0]}.")
    print(f"Rotation Method: {rotation} with Kaiser Normalization.")
    print("Note 1: The main diagonal of the reproduced correlation matrix represents reproduced communalities.")

    # Calcular o número de resíduos não redundantes com valores absolutos > 0.05
    residual_matrix_no_diag = np.copy(residual_matrix)
    np.fill_diagonal(residual_matrix_no_diag, 0)
    nonredundant_residuals = np.abs(residual_matrix_no_diag[np.triu_indices_from(residual_matrix_no_diag, k=1)])
    count_nonredundant_residuals = np.sum(nonredundant_residuals > 0.05)
    percentage_nonredundant_residuals = (count_nonredundant_residuals / len(nonredundant_residuals)) * 100

    print(f"Note 2: Residuals are computed between observed and reproduced correlations. There are {count_nonredundant_residuals} ({percentage_nonredundant_residuals:.1f}%) nonredundant residuals with absolute values greater than 0.05.")

    return observed_corr_matrix, reproduced_corr_matrix


def calculate_observed_reproduced_correlations_nodiagnalresidual(df, variables, method, n_factors, rotation):
    """
    Calcula a matriz das correlações reproduzidas ou estimadas.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    variables (list): Lista de variáveis para analisar.
    method (str): Método de extração a ser usado ('principal', 'minres', 'ml', etc.).
    n_factors (int): Número de fatores a serem extraídos.
    rotation (str): Método de rotação a ser usado ('varimax', 'promax', etc.).

    Retorna:
    tuple: Matrizes de correlações observadas e reproduzidas.
    """
    # Selecionar as variáveis a serem analisadas
    data = df[variables].dropna()

    # Ajustar o fator analisador para PCA ou PAF com rotação especificada
    fa = FactorAnalyzer(rotation=rotation, method=method, n_factors=n_factors)
    fa.fit(data)
    
    # Extrair a matriz de componentes rotacionada
    loadings = fa.loadings_

    # Calcular a matriz de correlação observada
    observed_corr_matrix = np.corrcoef(data.T)
    
    # Calcular a matriz das correlações reproduzidas
    reproduced_corr_matrix = np.dot(loadings, loadings.T)
    
    # Calcular a matriz residual
    residual_matrix = observed_corr_matrix - reproduced_corr_matrix

    # Preparar tabela combinada
    headers = [""] + variables
    combined_rows = []

    combined_rows.append(["Observed Correlation"] + [""] * len(variables))
    for i, var in enumerate(variables):
        combined_rows.append([var] + [f"{observed_corr_matrix[i, j]:.3f}" for j in range(len(variables))])

    combined_rows.append(["Reproduced Correlation"] + [""] * len(variables))
    for i, var in enumerate(variables):
        combined_rows.append([var] + [f"{reproduced_corr_matrix[i, j]:.3f}" for j in range(len(variables))])

    combined_rows.append(["Residual"] + [""] * len(variables))
    for i, var in enumerate(variables):
        row = [var]
        for j in range(len(variables)):
            if i == j:
                row.append("")
            else:
                value = residual_matrix[i, j]
                row.append(f"{value:.3f}" if not np.isnan(value) else "")
        combined_rows.append(row)
    
    # Mapeamento da extração
    elements_name = {
        'principal': ('Principal Component Analysis', 'PCA'),
        'minres': ('Principal Axis Factoring', 'PAF'),
        'ml': ('Maximum Likelihood', 'ML'),
    }

    # Exibir tabela formatada
    print(tabulate(combined_rows, headers, tablefmt="grid"))
    print(f"Extraction Method: {elements_name[method][0]}.")
    print(f"Rotation Method: {rotation} with Kaiser Normalization.")
    print("Note 1: The main diagonal of the reproduced correlation matrix represents reproduced communalities.")

    # Calcular o número de resíduos não redundantes com valores absolutos > 0.05
    residual_matrix_no_diag = np.copy(residual_matrix)
    np.fill_diagonal(residual_matrix_no_diag, 0)
    nonredundant_residuals = np.abs(residual_matrix_no_diag[np.triu_indices_from(residual_matrix_no_diag, k=1)])
    count_nonredundant_residuals = np.sum(nonredundant_residuals > 0.05)
    percentage_nonredundant_residuals = (count_nonredundant_residuals / len(nonredundant_residuals)) * 100

    print(f"Note 2: Residuals are computed between observed and reproduced correlations. There are {count_nonredundant_residuals} ({percentage_nonredundant_residuals:.1f}%) nonredundant residuals with absolute values greater than 0.05.")

    return observed_corr_matrix, reproduced_corr_matrix

def calculate_observed_reproduced_correlations(df, variables, method, n_factors, rotation):
    """
    Calcula a matriz das correlações reproduzidas ou estimadas.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    variables (list): Lista de variáveis para analisar.
    method (str): Método de extração a ser usado ('principal', 'minres', 'ml', etc.).
    n_factors (int): Número de fatores a serem extraídos.
    rotation (str): Método de rotação a ser usado ('varimax', 'promax', etc.).

    Retorna:
    tuple: Matrizes de correlações observadas e reproduzidas.
    """
    # Selecionar as variáveis a serem analisadas
    data = df[variables].dropna()

    # Ajustar o fator analisador para PCA ou PAF com rotação especificada
    fa = FactorAnalyzer(rotation=rotation, method=method, n_factors=n_factors)
    fa.fit(data)
    
    # Extrair a matriz de componentes rotacionada
    loadings = fa.loadings_

    # Calcular a matriz de correlação observada
    observed_corr_matrix = np.corrcoef(data.T)
    
    # Calcular a matriz das correlações reproduzidas
    reproduced_corr_matrix = np.dot(loadings, loadings.T)
    
    # Calcular a matriz residual
    residual_matrix = observed_corr_matrix - reproduced_corr_matrix

    # Preparar tabela combinada
    headers = [""] + variables
    combined_rows = []

    combined_rows.append(["Observed Correlation"] + [""] * len(variables))
    for i, var in enumerate(variables):
        combined_rows.append([var] + [f"{observed_corr_matrix[i, j]:.3f}" for j in range(len(variables))])

    combined_rows.append(["Reproduced Correlation"] + [""] * len(variables))
    for i, var in enumerate(variables):
        combined_rows.append([var] + [f"{reproduced_corr_matrix[i, j]:.3f}" for j in range(len(variables))])

    combined_rows.append(["Residual"] + [""] * len(variables))
    for i, var in enumerate(variables):
        row = [var]
        for j in range(len(variables)):
            value = residual_matrix[i, j]
            row.append(f"{value:.3f}" if not np.isnan(value) else "")
        combined_rows.append(row)
    
    # Mapeamento da extração
    elements_name = {
        'principal': ('Principal Component Analysis', 'PCA'),
        'minres': ('Principal Axis Factoring', 'PAF'),
        'ml': ('Maximum Likelihood', 'ML'),
    }

    # Exibir tabela formatada
    print(tabulate(combined_rows, headers, tablefmt="grid"))
    print(f"Extraction Method: {elements_name[method][0]}.")
    print(f"Rotation Method: {rotation} with Kaiser Normalization.")
    print("Note 1: The main diagonal of the reproduced correlation matrix represents reproduced communalities.")

    # Calcular o número de resíduos não redundantes com valores absolutos > 0.05
    residual_matrix_no_diag = np.copy(residual_matrix)
    np.fill_diagonal(residual_matrix_no_diag, 0)
    nonredundant_residuals = np.abs(residual_matrix_no_diag[np.triu_indices_from(residual_matrix_no_diag, k=1)])
    count_nonredundant_residuals = np.sum(nonredundant_residuals > 0.05)
    percentage_nonredundant_residuals = (count_nonredundant_residuals / len(nonredundant_residuals)) * 100

    print(f"Note 2: Residuals are computed between observed and reproduced correlations. There are {count_nonredundant_residuals} ({percentage_nonredundant_residuals:.1f}%) nonredundant residuals with absolute values greater than 0.05.")

def calculate_fit_indices(df, variables, method='principal', n_factors=2, rotation='varimax'):
    # Seleciona as variáveis para a análise fatorial
    data = df[variables]

    # Calcula a esfericidade de Bartlett
    bartlett_test, bartlett_p_value = calculate_bartlett_sphericity(data)

    # Calcula a medida de adequação de KMO
    kmo_all, kmo_model = calculate_kmo(data)

    # Verifica a singularidade da matriz de correlação
    corr_matrix = np.corrcoef(data, rowvar=False)
    if np.linalg.cond(corr_matrix) < 1 / np.finfo(corr_matrix.dtype).eps:
        # Realiza a análise fatorial
        fa = FactorAnalyzer(n_factors=n_factors, method=method, rotation=None)
        fa.fit(data)
        
        # Aplica a rotação
        if rotation:
            rotator = Rotator(rotation)
            loadings = rotator.fit_transform(fa.loadings_)
        else:
            loadings = fa.loadings_

        # Funções manuais para calcular os índices de ajuste
        def calculate_gfi(corr_matrix, loadings):
            s = corr_matrix
            sigma_hat = loadings @ loadings.T + np.diag(np.diag(s - loadings @ loadings.T))
            return 1 - (np.sum((s - sigma_hat) ** 2) / np.sum(s ** 2))
        
        def calculate_agfi(gfi, n, p):
            return gfi - (p * (p + 1) / (2 * n * (n - 1))) * (1 - gfi)
        
        def calculate_rmsr(corr_matrix, loadings):
            sigma_hat = loadings @ loadings.T + np.diag(np.diag(corr_matrix - loadings @ loadings.T))
            residuals = corr_matrix - sigma_hat
            return np.sqrt(np.sum(residuals[np.tril_indices_from(residuals)] ** 2) / (corr_matrix.shape[0] * (corr_matrix.shape[0] - 1) / 2))
        
        def calculate_srmr(corr_matrix, loadings):
            sigma_hat = loadings @ loadings.T + np.diag(np.diag(corr_matrix - loadings @ loadings.T))
            residuals = corr_matrix - sigma_hat
            return np.sqrt(np.sum(residuals ** 2) / (corr_matrix.shape[0] * (corr_matrix.shape[0] + 1) / 2))
        
        gfi = calculate_gfi(corr_matrix, loadings)
        agfi = calculate_agfi(gfi, data.shape[0], data.shape[1])
        rmsr = calculate_rmsr(corr_matrix, loadings)
        srmr = calculate_srmr(corr_matrix, loadings)

        # Calcula os índices de ajuste
        fit_indices = {
            'GFI': gfi,
            'AGFI': agfi,
            'RMSR': rmsr,
            'SRMR': srmr
        }

        # Exibir tabela formatada para Bartlett e KMO
        bartlett_headers = ["Test", "Value"]
        bartlett_table = [
            ["Bartlett's Test: Chi-square", f"{bartlett_test:.4f}"],
            ["Bartlett's Test: p-value", f"{bartlett_p_value:.4e}"],
            ["Kaiser-Meyer-Olkin (KMO)", f"{kmo_model:.4f}"]
        ]
        print("\nBartlett and KMO Tests:")
        print(tabulate(bartlett_table, bartlett_headers, tablefmt="grid"))

        # Dicionário de nomes completos dos índices
        index_names = {
            'GFI': 'Goodness of Fit Index (GFI)',
            'AGFI': 'Adjusted Goodness of Fit Index (AGFI)',
            'RMSR': 'Root Mean Square Residual (RMSR)',
            'SRMR': 'Standardized Root Mean Square Residual (SRMR)'
        }

        # Exibir tabela formatada para fit indices
        headers = ["Index", "Value"]
        table = [[index_names[key], f"{value:.4f}"] for key, value in fit_indices.items()]
        print("Fit Indices:")
        print(tabulate(table, headers, tablefmt="grid"))

    else:
        raise ValueError("A matriz de correlação é singular e não pode ser invertida. Verifique os dados de entrada.")
    
    
def calculate_icc(df, column_targets, column_raters, ratings_label, column_items=None, method='all'):
    """
    Calculate Intraclass Correlation Coefficients (ICC) for given ratings data.

    Parameters:
    df (DataFrame): The dataframe containing the ratings data.
    column_targets (str): The name of the column with the targets (e.g., subjects being rated).
    column_raters (str): The name of the column with the raters.
    ratings_label (str): The name of the column with the ratings.
    column_items (str, optional): The name of the column with the items, if applicable. Default is None.
    method (str): The ICC method to use. Options are 'ICC1', 'ICC2', 'ICC3', 'ICC1k', 'ICC2k', 'ICC3k', or 'all'. Default is 'all'.

    Returns:
    None: Prints a formatted table of ICC results and a summary note.
    """
    results = []
    valid_methods = ['ICC1', 'ICC2', 'ICC3', 'ICC1k', 'ICC2k', 'ICC3k']
    
    # Define quais métodos incluir com base no método escolhido
    if method == 'all':
        selected_methods = valid_methods
    else:
        selected_methods = [m for m in valid_methods if m.startswith(method)]
    
    # Verifica se a coluna de itens foi especificada
    if column_items is not None:
        items = df[column_items].unique()
        for item in items:
            # Filtra o DataFrame para o item atual
            df_item = df[df[column_items] == item]
            # Calcula a correlação intra-classe
            icc = pg.intraclass_corr(data=df_item, targets=column_targets, raters=column_raters, ratings=ratings_label)
            icc['Item'] = item
            results.append(icc)
    else:
        # Calcula a correlação intra-classe para o DataFrame inteiro se não houver itens específicos
        icc = pg.intraclass_corr(data=df, targets=column_targets, raters=column_raters, ratings=ratings_label)
        icc['Item'] = 'All'
        results.append(icc)
    
    # Combina todos os resultados em um único DataFrame
    combined_results = pd.concat(results)
    
    # Reordena as colunas para colocar 'Item' na primeira posição
    columns_order = ['Item'] + [col for col in combined_results.columns if col != 'Item']
    combined_results = combined_results[columns_order]
    
    # Filtra os resultados de acordo com os métodos selecionados
    combined_results = combined_results[combined_results['Type'].isin(selected_methods)]
    
    # Ordena os resultados para que os métodos 'ICC1k', 'ICC2k', 'ICC3k' fiquem logo abaixo dos correspondentes 'ICC1', 'ICC2', 'ICC3'
    combined_results = combined_results.sort_values(by=['Item', 'Type'])
    
    # Formata a saída usando tabulate
    print(tabulate(combined_results, headers='keys', tablefmt='grid', showindex=False))
    print("\nNote:\nICC1 - Different raters rate each target, one-way ANOVA fixed effects. \nICC2 - Random sample of k raters, absolute agreement. \nICC3 - Fixed set of k raters, no generalization to larger population. \nReliability can be estimated for a single rating or average of k ratings.")
