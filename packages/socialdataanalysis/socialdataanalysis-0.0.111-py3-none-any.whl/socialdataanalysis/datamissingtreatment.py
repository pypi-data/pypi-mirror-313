import pandas as pd
from tabulate import tabulate
from scipy import stats
import numpy as np
from scipy.stats import chi2
from sklearn.experimental import enable_iterative_imputer  # Habilitar IterativeImputer antes de IterativeImputer, pois é uma funcionalidade experimental
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge # Mais se aproxima de uma normal
from statsmodels.imputation import mice
from scipy.stats import pearsonr

def generate_absent_present_ttest(df, variaveis):
    """
    Gera uma tabela de t-test de variâncias separadas para as variáveis especificadas em um DataFrame.
    
    Parâmetros:
    df (pd.DataFrame): O DataFrame contendo os dados a serem analisados.
    variaveis (list): Uma lista de nomes de colunas (strings) no DataFrame a serem analisadas.
    
    Retorna:
    str: Uma tabela formatada com os resultados dos t-testes.
    """
    results = []
    for var in variaveis:
        row_t = [var, "t"]
        row_df = ["", "df"]
        row_p = ["", "P(2-tail)"]
        row_present = ["", "# Present"]
        row_missing = ["", "# Missing"]
        row_mean_present = ["", "Mean(Present)"]
        row_mean_missing = ["", "Mean(Missing)"]
        
        for compare_var in variaveis:
            if var == compare_var:
                row_t.append(".")
                row_df.append(".")
                row_p.append(".")
                row_present.append(df[var].count())
                row_missing.append(".")
                row_mean_present.append(f"{df[var].mean():.2f}")
                row_mean_missing.append(".")
            else:
                complete_cases = df[~df[var].isna() & ~df[compare_var].isna()]
                missing_cases = df[df[var].isna() & ~df[compare_var].isna()]
                if len(complete_cases) > 1 and len(missing_cases) > 1:
                    t_stat, p_val = stats.ttest_ind(complete_cases[compare_var], missing_cases[compare_var], equal_var=False)
                    n1 = len(complete_cases)
                    n2 = len(missing_cases)
                    s1 = complete_cases[compare_var].var()
                    s2 = missing_cases[compare_var].var()
                    df_val = ((s1 / n1 + s2 / n2) ** 2) / (((s1 / n1) ** 2) / (n1 - 1) + ((s2 / n2) ** 2) / (n2 - 1))
                    row_t.append(f"{t_stat:.1f}")
                    row_df.append(f"{df_val:.1f}")
                    row_p.append(f"{p_val:.3f}")
                else:
                    row_t.append(".")
                    row_df.append(".")
                    row_p.append(".")
                row_present.append(len(complete_cases))
                row_missing.append(len(missing_cases))
                row_mean_present.append(f"{complete_cases[compare_var].mean():.2f}" if len(complete_cases) > 0 else ".")
                row_mean_missing.append(f"{missing_cases[compare_var].mean():.2f}" if len(missing_cases) > 0 else ".")
        
        results.append(row_t)
        results.append(row_df)
        results.append(row_p)
        results.append(row_present)
        results.append(row_missing)
        results.append(row_mean_present)
        results.append(row_mean_missing)
    
    headers = [""] + variaveis
    
    table = tabulate(results, headers, tablefmt="grid")
    
    print(table)
    
    
def generate_missing_extreme_table(df, variaveis, case_column):
    """
    Gera uma tabela de padrões de valores ausentes e extremos para as variáveis especificadas em um DataFrame.
    
    Parâmetros:
    df (pd.DataFrame): O DataFrame contendo os dados a serem analisados.
    variaveis (list): Uma lista de nomes de colunas (strings) no DataFrame a serem analisadas.
    case_column (str): O nome da coluna que identifica os casos (profissões).
    
    Retorna:
    str: Uma tabela formatada com os padrões de valores ausentes e extremos.
    """
    results = []
    
    # Calcula os limites para valores extremos
    limits = {}
    for var in variaveis:
        q1 = df[var].quantile(0.25)
        q3 = df[var].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        limits[var] = (lower_bound, upper_bound)
    
    # Analisar padrões de missings e valores extremos
    for idx, row in df.iterrows():
        missing_pattern = []
        num_missing = 0
        for var in variaveis:
            if pd.isna(row[var]):
                num_missing += 1
                missing_pattern.append('S')
            elif row[var] < limits[var][0]:
                missing_pattern.append('-')
            elif row[var] > limits[var][1]:
                missing_pattern.append('+')
            else:
                missing_pattern.append('')
        if num_missing > 0:
            case_name = row[case_column]
            percent_missing = (num_missing / len(variaveis)) * 100
            results.append([case_name, num_missing, percent_missing] + missing_pattern)
    
    # Ordenar os resultados por número de valores ausentes e nome das profissões
    results = sorted(results, key=lambda x: (-x[1], x[0]))
    
    headers = ["Case", "# Missing", "% Missing"] + variaveis
    
    table = tabulate(results, headers, tablefmt="grid", floatfmt=(".0f", ".1f"))
    
    footnote = "- indicates an extreme low value, while + indicates an extreme high value. The range used is (Q1 - 1.5*IQR, Q3 + 1.5*IQR)."
    
    print(table, f"\n{footnote}")
    


def generate_tabular_missing_table(df, variaveis):
    """
    Gera uma tabela de padrões tabulares de valores ausentes para as variáveis especificadas em um DataFrame.
    
    Parâmetros:
    df (pd.DataFrame): O DataFrame contendo os dados a serem analisados.
    variaveis (list): Uma lista de nomes de colunas (strings) no DataFrame a serem analisadas.
    
    Retorna:
    str: Uma tabela formatada com os padrões tabulares de valores ausentes.
    """
    # Cria uma coluna de padrão de missings
    df['missing_pattern'] = df[variaveis].isnull().dot(1 << np.arange(len(variaveis) - 1, -1, -1)).astype(str)
    
    # Conta os padrões de missings
    padroes_contagem = df['missing_pattern'].value_counts().reset_index()
    padroes_contagem.columns = ['missing_pattern', 'num_cases']
    
    # Cria a tabela de padrões
    patterns = []
    for _, row in padroes_contagem.iterrows():
        pattern_bin = format(int(row['missing_pattern']), f'0{len(variaveis)}b')
        pattern = ['X' if char == '1' else '' for char in pattern_bin]
        complete_cases = len(df.dropna(subset=[var for var, mark in zip(variaveis, pattern) if mark == '']))
        patterns.append([row['num_cases']] + pattern + [complete_cases])
    
    headers = ["Number of\n Cases"] + variaveis + ["Complete if\n ...\u1d43"]
    
    table = tabulate(patterns, headers, tablefmt="grid")
    
    title = "Tabulated Patterns of Missing Values"
    footnote = "Number of complete cases if variables missing in that pattern (marked with X) are not used."
    
    print(title)
    print(table)
    print(footnote)
    


def analyze_missing_data(df, variaveis):
    """
    Analisa dados faltantes em um DataFrame, calculando médias imputadas, realizando o teste MCAR de Little
    e gerando uma tabela de resumo e correlações imputadas.

    Parameters:
    df (pd.DataFrame): DataFrame contendo os dados a serem analisados.
    variaveis (list): Lista de nomes de colunas a serem analisadas.

    Returns:
    None: Imprime as tabelas formatadas e o resultado do teste MCAR de Little.
    """
    def calcular_media_imputada(df, variaveis):
        imputer = IterativeImputer(random_state=42, estimator=BayesianRidge())
        imputed_data = imputer.fit_transform(df[variaveis])
        return imputed_data, np.mean(imputed_data, axis=0)
    

    def little_mcar_test(X):
        dataset = X.copy()
        vars = dataset.columns
        n_var = dataset.shape[1]

        gmean = dataset.mean()
        gcov = dataset.cov()

        r = dataset.isnull().astype(int)
        mdp = np.dot(r, 2**np.arange(n_var))
        sorted_mdp = sorted(np.unique(mdp))
        n_pat = len(sorted_mdp)
        correct_mdp = np.searchsorted(sorted_mdp, mdp)
        dataset["mdp"] = correct_mdp

        pj = 0
        d2 = 0
        for i in range(n_pat):
            dataset_temp = dataset[dataset["mdp"] == i][vars]
            select_vars = ~dataset_temp.isnull().any()
            pj += select_vars.sum()
            select_vars = vars[select_vars]
            means = dataset_temp[select_vars].mean() - gmean[select_vars]
            select_cov = gcov.loc[select_vars, select_vars]
            mj = len(dataset_temp)
            parta = means.T @ np.linalg.solve(select_cov, np.eye(select_cov.shape[0]))
            d2 += mj * (parta @ means)

        df = pj - n_var
        pvalue = 1 - chi2.cdf(d2, df)
        return d2, df, pvalue

    original_means = df[variaveis].mean()
    imputed_data, imputed_means = calcular_media_imputada(df, variaveis)
    
    chi_square_stat, degree_f, p_value = little_mcar_test(df[variaveis])
    
    means_data = [
        ["Original Means"] + list(original_means),
        ["Imputed Means"] + list(imputed_means)
    ]
    
    headers = [""] + variaveis
    table_means = tabulate(means_data, headers, tablefmt="grid", floatfmt=".3f")
    
    footnote = f"a. Little's MCAR test: Chi-Square= {chi_square_stat:.3f}, DF = {degree_f}, P-value = {p_value:.3f}"
    
    print("Summary of Estimated Means")
    print(table_means)
    print(footnote)
    
    # Calculando a matriz de correlação com dados imputados
    corr_matrix = np.corrcoef(imputed_data, rowvar=False)
    corr_df = pd.DataFrame(corr_matrix, index=variaveis, columns=variaveis)
    
    # Formatando a tabela de correlações
    print("\nEM Correlations")
    print(tabulate(corr_df, headers=variaveis, tablefmt="grid", floatfmt=".3f"))
    


def summarize_missing_data(df, variaveis):
    """
    Gera uma tabela resumida de dados faltantes para variáveis especificadas em um DataFrame.

    Parâmetros:
    df (pd.DataFrame): O DataFrame contendo os dados a serem analisados.
    variaveis (list): Uma lista de nomes de colunas (strings) no DataFrame a serem analisadas.

    Retorna:
    str: Uma tabela formatada com o resumo de dados faltantes.
    """
    # Filtrando apenas as variáveis desejadas
    analysis_df = df[variaveis]

    # Calculando estatísticas de dados faltantes
    total_cases = df.shape[0]
    total_variables = analysis_df.shape[1]
    complete_cases = analysis_df.dropna().shape[0]
    incomplete_cases = total_cases - complete_cases
    total_values = total_cases * total_variables
    missing_values = analysis_df.isnull().sum().sum()
    complete_values = total_values - missing_values

    variables_with_missing = analysis_df.isnull().sum()
    variables_with_missing = variables_with_missing[variables_with_missing > 0].count()
    variables_without_missing = total_variables - variables_with_missing

    # Preparando dados para a tabela
    results = [
        ["Variáveis com missings", variables_with_missing, f"{(variables_with_missing / total_variables * 100):.2f}%"],
        ["Variáveis sem missings", variables_without_missing, f"{(variables_without_missing / total_variables * 100):.2f}%"],
        ["Casos completos", complete_cases, f"{(complete_cases / total_cases * 100):.2f}%"],
        ["Casos incompletos", incomplete_cases, f"{(incomplete_cases / total_cases * 100):.2f}%"],
        ["Valores completos", complete_values, f"{(complete_values / total_values * 100):.2f}%"],
        ["Valores com missings", missing_values, f"{(missing_values / total_values * 100):.2f}%"]
    ]

    headers = ["Descrição", "Número", "Percentagem"]
    table = tabulate(results, headers=headers, tablefmt="grid")

    print(table)
    

def perform_multiple_imputation(df, iteracoes=100):
    """
    Realiza a imputação múltipla utilizando o método Fully Conditional Specification (FCS)
    e retorna os dados imputados junto com os dados originais.

    Parâmetros:
    df (pd.DataFrame): DataFrame com dados faltantes.
    iteracoes (int): Número de iterações de MCMC para imputação.

    Retorna:
    pd.DataFrame: DataFrame com os dados originais e os dados imputados.
    """

    # Inicialização e realização da imputação múltipla
    imputed_data = mice.MICEData(df)
    imputed_data.update_all(n_iter=iteracoes)  # Realizar 100 iterações de imputação

    # Média dos dados imputados
    imputed_means = imputed_data.data.groupby(level=0).mean()
    
    # Preparando a tabela de resultados
    resultados = df.copy()
    for col in df.columns:
        resultados[f'{col}_Imputed'] = imputed_means[col]
    
    return resultados



def display_listwise_statistics(df, variables):
    """
    Calculates and displays listwise statistics (Pearson correlations, means, and standard deviations)
    for a given list of variables in a dataframe using listwise deletion.

    Parameters:
    df (DataFrame): The dataframe containing the data.
    variables (list): The list of variables for which to calculate statistics.

    Returns:
    None: Prints formatted tables containing the listwise statistics.
    """
    
    # Eliminação listwise
    data = df[variables].dropna()

    # Prepare mean and standard deviation matrices
    mean_matrix = np.zeros((1, len(variables)))
    std_matrix = np.zeros((1, len(variables)))
    var_index = {var: idx for idx, var in enumerate(variables)}

    for i, var in enumerate(variables):
        mean_matrix[0, var_index[var]] = data[var].mean()
        std_matrix[0, var_index[var]] = data[var].std()

    # Calcular a matriz de correlação de Pearson e os valores p
    corr_matrix = data.corr(method='pearson').values
    p_matrix = np.zeros((len(variables), len(variables)))

    for i in range(len(variables)):
        for j in range(len(variables)):
            if i != j:
                _, p_value = pearsonr(data.iloc[:, i], data.iloc[:, j])
                p_matrix[i, j] = p_value / 2  # 1-tailed
            else:
                p_matrix[i, j] = 0

    headers = ["Matrix Type"] + variables
    rows = []

    # Adicionar correlações de Pearson
    rows.append(["Pearson Correlation"] + [""] * len(variables))
    for i, var in enumerate(variables):
        row = [var]
        for j in range(len(variables)):
            if j <= i:
                row.append(f"{corr_matrix[i, j]:.3f}")
            else:
                row.append("")
        rows.append(row)

    rows.append(["Pearson Sig. (1-tailed)"] + [""] * len(variables))
    for i, var in enumerate(variables):
        row = [var]
        for j in range(len(variables)):
            if j <= i:
                row.append(f"{p_matrix[i, j]:.3f}")
            else:
                row.append("")
        rows.append(row)

    # Calcular o determinante da matriz de correlação
    determinant_pearson = np.linalg.det(corr_matrix)

    # Exibir a tabela de médias no formato especificado
    mean_headers = ["Number of cases"] + variables
    mean_rows = [[len(data)] + [f"{mean_matrix[0, j]:.2f}" for j in range(len(variables))]]

    print("Listwise Means")
    print(tabulate(mean_rows, mean_headers, tablefmt="grid"))

    # Exibir a tabela de desvios padrão no formato especificado
    std_headers = ["Number of cases"] + variables
    std_rows = [[len(data)] + [f"{std_matrix[0, j]:.3f}" for j in range(len(variables))]]

    print("Listwise Standard Deviations")
    print(tabulate(std_rows, std_headers, tablefmt="grid"))

    # Exibir a tabela formatada
    print(tabulate(rows, headers, tablefmt="grid"))
    print(f"Determinant (Pearson) = {determinant_pearson:.3f}")
    
    
    
def display_pairwise_statistics(df, variables):
    """
    Calculates and displays pairwise statistics (Pearson correlations), frequencies, means, and standard deviations for a given list of variables in a dataframe.

    Parameters:
    df (DataFrame): The dataframe containing the data.
    variables (list): The list of variables for which to calculate pairwise statistics.

    Returns:
    None: Prints formatted tables containing the pairwise statistics, frequencies, means, and standard deviations.
    """
    results = []

    # Prepare frequency, mean, and standard deviation matrices
    freq_matrix = np.zeros((len(variables), len(variables)))
    mean_matrix = np.zeros((len(variables), len(variables)))
    std_matrix = np.zeros((len(variables), len(variables)))
    var_index = {var: idx for idx, var in enumerate(variables)}

    for i, var1 in enumerate(variables):
        for var2 in variables:
            if var1 == var2:
                data = df[[var1]].dropna()
                freq_matrix[var_index[var1], var_index[var2]] = len(data)
                mean_matrix[var_index[var1], var_index[var2]] = data[var1].mean()
                std_matrix[var_index[var1], var_index[var2]] = data[var1].std()
            elif var1 != var2:
                # Drop rows with NaN values in either column
                data = df[[var1, var2]].dropna()
                
                if len(data) > 0:
                    # Pearson correlation
                    pearson_corr, pearson_p = pearsonr(data[var1], data[var2])
                    
                    results.append({
                        'Variable 1': var1,
                        'Variable 2': var2,
                        'Pearson Correlation': pearson_corr,
                        'Pearson p-value': pearson_p / 2, # 1-tailed
                    })
                
                # Fill frequency, mean, and standard deviation matrices
                freq_matrix[var_index[var1], var_index[var2]] = freq_matrix[var_index[var2], var_index[var1]] = len(data)
                mean_matrix[var_index[var1], var_index[var2]] = data[var1].mean()
                mean_matrix[var_index[var2], var_index[var1]] = data[var2].mean()
                std_matrix[var_index[var1], var_index[var2]] = data[var1].std()
                std_matrix[var_index[var2], var_index[var1]] = data[var2].std()

    results_df = pd.DataFrame(results)
    
    # Prepare data for tabulate
    corr_matrix = np.eye(len(variables))
    p_matrix = np.zeros((len(variables), len(variables)))

    for _, row in results_df.iterrows():
        i = var_index[row['Variable 1']]
        j = var_index[row['Variable 2']]
        corr_matrix[i, j] = row['Pearson Correlation']
        corr_matrix[j, i] = row['Pearson Correlation']  # Ensure symmetry
        p_matrix[i, j] = row['Pearson p-value']
        p_matrix[j, i] = row['Pearson p-value']  # Ensure symmetry

    # Calcular o determinante da matriz de correlação usando a matriz completa
    determinant_pearson = np.linalg.det(corr_matrix)

    headers = ["Matrix Type"] + variables
    rows = []

    # Adicionar correlações de Pearson (apenas a diagonal principal e os valores abaixo dela)
    rows.append(["Pearson Correlation"] + [""] * len(variables))
    for i, var in enumerate(variables):
        row = [var]
        for j in range(len(variables)):
            if j <= i:
                row.append(f"{corr_matrix[i, j]:.3f}")
            else:
                row.append("")
        rows.append(row)

    rows.append(["Pearson Sig. (1-tailed)"] + [""] * len(variables))
    for i, var in enumerate(variables):
        row = [var]
        for j in range(len(variables)):
            if j <= i:
                row.append(f"{p_matrix[i, j]:.3f}")
            else:
                row.append("")
        rows.append(row)

    # Exibir a tabela de frequências
    freq_headers = [""] + variables
    freq_rows = []

    for i, var in enumerate(variables):
        row = [var]
        for j in range(len(variables)):
            if j <= i:
                row.append(int(freq_matrix[i, j]))
            else:
                row.append("")
        freq_rows.append(row)

    print("Pairwise Frequencies")
    print(tabulate(freq_rows, freq_headers, tablefmt="grid"))

    # Exibir a tabela de médias
    mean_headers = [""] + variables
    mean_rows = []

    for i, var in enumerate(variables):
        row = [var]
        for j in range(len(variables)):
            row.append(f"{mean_matrix[i, j]:.2f}")
        mean_rows.append(row)

    print("Pairwise Means")
    print(tabulate(mean_rows, mean_headers, tablefmt="grid"))

    # Exibir a tabela de desvios padrão
    std_headers = [""] + variables
    std_rows = []

    for i, var in enumerate(variables):
        row = [var]
        for j in range(len(variables)):
            row.append(f"{std_matrix[i, j]:.3f}")
        std_rows.append(row)

    print("Pairwise Standard Deviations")
    print(tabulate(std_rows, std_headers, tablefmt="grid"))

    # Exibir a tabela formatada
    print(tabulate(rows, headers, tablefmt="grid"))
    print(f"Determinant (Pearson) = {determinant_pearson:.3f}")