import pandas as pd
# Configurações para garantir que a saída não seja truncada
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_colwidth', None)
#pd.set_option('display.expand_frame_repr', False)

from tabulate import tabulate
from IPython.display import display, HTML, Math
import plotly.express as px

import warnings
import itertools
from statsmodels.formula.api import glm

import numpy as np  # Suporta operações com arrays e matrizes, oferecendo uma vasta gama de funções matemáticas para operações com essas estruturas de dados.
from statsmodels.stats.contingency_tables import Table  # Analisa tabelas de contingência para estudo de variáveis categóricas, útil em testes de hipóteses e análises de associação entre variáveis.
import statsmodels.api as sm  # Utilizado para modelos estatísticos e testes em Python, incluindo regressões, testes de hipóteses e muito mais, oferecendo ferramentas robustas para análise estatística.
from scipy.stats import hypergeom  # Aplica a distribuição hipergeométrica para análises estatísticas, útil em testes de sobreposição e em situações onde se deseja calcular probabilidades sem reposição.
import matplotlib.pyplot as plt  # Gera gráficos para visualização de dados, permitindo a criação de uma ampla variedade de gráficos estáticos, animados e interativos em Python.
from scipy.stats import chi2_contingency  # Realiza o teste de independência do qui-quadrado para tabelas de contingência, utilizado para avaliar se há uma associação significativa entre duas variáveis categóricas.
from scipy.stats import fisher_exact  # Realiza o teste exato de Fisher, utilizado para análise de tabelas de contingência 2x2, especialmente útil em amostras pequenas onde o teste do qui-quadrado pode não ser apropriado.
from sympy import symbols # Útil para representar variáveis em expressões matemáticas quando não conhecemos seus valores ainda.
from sympy import Eq # Permite definir equações que serão usadas nas soluções de problemas matemáticos.
from sympy import solve # Retorna as soluções das variáveis das equações fornecidas.
from statsmodels.stats.contingency_tables import StratifiedTable


from scipy.stats import chi2
import prince # Importa a biblioteca para análise de correspondência
import altair as alt  # Altair é usado para a visualização

def analisar_independencia_variaveis_tabela_contingencia_OLD(tabela_contingencia, mostrar_pearson=True, mostrar_continuity=True, mostrar_likelihood=True, mostrar_fisher=True):
    """
    Realiza testes de independência estatística sobre uma tabela de contingência fornecida. Dependendo do tamanho
    da tabela, realiza o teste Qui-Quadrado de Pearson (com ou sem correção de continuidade), a Razão de Verossimilhança,
    e/ou o teste exato de Fisher. Fornece um resumo dos resultados e uma nota de rodapé sobre a adequação do teste Qui-Quadrado.

    Parâmetros:
    - tabela_contingencia (pd.DataFrame): Tabela de contingência contendo as frequências observadas.
    - mostrar_pearson (bool): Se True, inclui o teste Qui-Quadrado de Pearson na saída.
    - mostrar_continuity (bool): Se True, inclui a correção de continuidade na saída.
    - mostrar_likelihood (bool): Se True, inclui a razão de verossimilhança na saída.
    - mostrar_fisher (bool): Se True, inclui o teste exato de Fisher na saída.

    Retorna:
    - resultados_df (pd.DataFrame): DataFrame contendo os resultados dos testes, com valores formatados para apresentação.
    - nota_rodape (str): Nota de rodapé relevante para a interpretação dos resultados, se aplicável.
    """
    
    # Determinar o tamanho da tabela de contingência
    n_linhas, n_colunas = tabela_contingencia.shape

    resultados = []
    columns = ["Value", "df", "Asymp. Sig. (2-sided)"]

    # Teste Exato de Fisher apenas para tabelas 2x2 e Teste de Qui-Quadrado e Razão de Verossimilhança para qualquer tamanho de tabela
    if n_linhas == 2 and n_colunas == 2:
        if mostrar_pearson:
            res_chi2 = chi2_contingency(tabela_contingencia, correction=False)
            resultados.append(("Pearson Chi-Square", res_chi2[0], res_chi2[2], res_chi2[1]))
        if mostrar_continuity:
            res_chi2_corr = chi2_contingency(tabela_contingencia, correction=True)
            resultados.append(("Continuity Correction", res_chi2_corr[0], res_chi2_corr[2], res_chi2_corr[1]))
        if mostrar_likelihood:
            res_likelihood_ratio = chi2_contingency(tabela_contingencia, correction=False, lambda_="log-likelihood")
            resultados.append(("Likelihood Ratio", res_likelihood_ratio[0], res_likelihood_ratio[2], res_likelihood_ratio[1]))
        if mostrar_fisher:
            res_fisher_2sided = fisher_exact(tabela_contingencia, alternative='two-sided')
            res_fisher_1sided = fisher_exact(tabela_contingencia, alternative='greater')
            resultados.append(("Fisher`s Exact Test", res_fisher_2sided[0], "", "", res_fisher_2sided[1], res_fisher_1sided[1]))
            if "Exact Sig. (2-sided)" not in columns:
                columns.extend(["Exact Sig. (2-sided)", "Exact Sig. (1-sided)"])

    else:
        if mostrar_pearson:
            res_chi2 = chi2_contingency(tabela_contingencia, correction=False)
            resultados.append(("Pearson Chi-Square", res_chi2[0], res_chi2[2], res_chi2[1]))
        if mostrar_continuity:
            res_chi2_corr = chi2_contingency(tabela_contingencia, correction=True)
            resultados.append(("Continuity Correction", res_chi2_corr[0], res_chi2_corr[2], res_chi2_corr[1]))
        if mostrar_likelihood:
            res_likelihood_ratio = chi2_contingency(tabela_contingencia, correction=False, lambda_="log-likelihood")
            resultados.append(("Likelihood Ratio", res_likelihood_ratio[0], res_likelihood_ratio[2], res_likelihood_ratio[1]))

    # Criando um DataFrame com os resultados
    resultados_df = pd.DataFrame(resultados, columns=["Test"] + columns)
    resultados_df.set_index("Test", inplace=True)
    resultados_df.loc["N. of Valid Cases", "Value"] = tabela_contingencia.sum().sum()
    
    # Nota de rodapé para o teste Qui-Quadrado
    if mostrar_pearson or mostrar_continuity or mostrar_likelihood:
        res_chi2 = chi2_contingency(tabela_contingencia, correction=False)
        cells_below_5 = np.sum(res_chi2[3] < 5)
        total_cells = res_chi2[3].size
        percent_cells_below_5 = (cells_below_5 / total_cells) * 100
        min_expected_count = res_chi2[3].min()
        nota_rodape = (f"a. {cells_below_5} cells ({percent_cells_below_5:.2f}%) have expected count less than 5. "
                       f"The minimum expected count is {min_expected_count:.2f}.")
    else:
        nota_rodape = ""

    # Substituir NaN por strings vazias
    resultados_df.fillna("", inplace=True)
    
    # Formatação do DataFrame
    resultados_df_formated = resultados_df.copy(deep=True)
    resultados_df_formated = resultados_df_formated.map(lambda x: '{:.3f}'.format(x) if isinstance(x, (int, float)) else x)
    resultados_df_formated["Value"] = resultados_df["Value"].apply(lambda x: '{:.2f}'.format(x) if isinstance(x, (int, float)) else x)
    resultados_df_formated.loc['N. of Valid Cases', 'Value'] = '{:.0f}'.format(resultados_df.loc['N. of Valid Cases', 'Value'])
    resultados_df_formated["df"] = resultados_df["df"].apply(lambda x: '{:.0f}'.format(x) if isinstance(x, (int, float)) else x)
   
    # Visualização dos resultados
    display(resultados_df_formated)
    # Imprimindo a nota de rodapé
    print(nota_rodape)

def analisar_independencia_variaveis_tabela_contingencia(tabela_contingencia, mostrar_pearson=True, mostrar_continuity=True, mostrar_likelihood=True, mostrar_fisher=True):
    """
    Realiza testes de independência estatística sobre uma tabela de contingência fornecida. Dependendo do tamanho
    da tabela, realiza o teste Qui-Quadrado de Pearson (com ou sem correção de continuidade), a Razão de Verossimilhança,
    e/ou o teste exato de Fisher. Fornece um resumo dos resultados e uma nota de rodapé sobre a adequação do teste Qui-Quadrado.

    Parâmetros:
    - tabela_contingencia (pd.DataFrame): Tabela de contingência contendo as frequências observadas.
    - mostrar_pearson (bool): Se True, inclui o teste Qui-Quadrado de Pearson na saída.
    - mostrar_continuity (bool): Se True, inclui a correção de continuidade na saída.
    - mostrar_likelihood (bool): Se True, inclui a razão de verossimilhança na saída.
    - mostrar_fisher (bool): Se True, inclui o teste exato de Fisher na saída.

    Retorna:
    - resultados_df (pd.DataFrame): DataFrame contendo os resultados dos testes, com valores formatados para apresentação.
    - nota_rodape (str): Nota de rodapé relevante para a interpretação dos resultados, se aplicável.
    """
    
    # Determinar o tamanho da tabela de contingência
    n_linhas, n_colunas = tabela_contingencia.shape

    resultados = []
    columns = ["Value", "df", "Asymp. Sig. (2-sided)"]

    # Teste Exato de Fisher apenas para tabelas 2x2 e Teste de Qui-Quadrado e Razão de Verossimilhança para qualquer tamanho de tabela
    if n_linhas == 2 and n_colunas == 2:
        if mostrar_pearson:
            res_chi2 = chi2_contingency(tabela_contingencia, correction=False)
            resultados.append(("Pearson Chi-Square", res_chi2[0], res_chi2[2], res_chi2[1]))
        if mostrar_continuity:
            res_chi2_corr = chi2_contingency(tabela_contingencia, correction=True)
            resultados.append(("Continuity Correction", res_chi2_corr[0], res_chi2_corr[2], res_chi2_corr[1]))
        if mostrar_likelihood:
            res_likelihood_ratio = chi2_contingency(tabela_contingencia, correction=False, lambda_="log-likelihood")
            resultados.append(("Likelihood Ratio", res_likelihood_ratio[0], res_likelihood_ratio[2], res_likelihood_ratio[1]))
        if mostrar_fisher:
            res_fisher_2sided = fisher_exact(tabela_contingencia, alternative='two-sided')
            res_fisher_1sided = fisher_exact(tabela_contingencia, alternative='greater')
            resultados.append(("Fisher`s Exact Test", res_fisher_2sided[0], "", "", res_fisher_2sided[1], res_fisher_1sided[1]))
            if "Exact Sig. (2-sided)" not in columns:
                columns.extend(["Exact Sig. (2-sided)", "Exact Sig. (1-sided)"])

    else:
        if mostrar_pearson:
            res_chi2 = chi2_contingency(tabela_contingencia, correction=False)
            resultados.append(("Pearson Chi-Square", res_chi2[0], res_chi2[2], res_chi2[1]))
        if mostrar_continuity:
            res_chi2_corr = chi2_contingency(tabela_contingencia, correction=True)
            resultados.append(("Continuity Correction", res_chi2_corr[0], res_chi2_corr[2], res_chi2_corr[1]))
        if mostrar_likelihood:
            res_likelihood_ratio = chi2_contingency(tabela_contingencia, correction=False, lambda_="log-likelihood")
            resultados.append(("Likelihood Ratio", res_likelihood_ratio[0], res_likelihood_ratio[2], res_likelihood_ratio[1]))

    # Criando um DataFrame com os resultados
    resultados_df = pd.DataFrame(resultados, columns=["Test"] + columns)
    resultados_df.set_index("Test", inplace=True)
    resultados_df.loc["N. of Valid Cases", "Value"] = tabela_contingencia.sum().sum()
    
    # Nota de rodapé para o teste Qui-Quadrado
    if mostrar_pearson or mostrar_continuity or mostrar_likelihood:
        res_chi2 = chi2_contingency(tabela_contingencia, correction=False)
        cells_below_5 = np.sum(res_chi2[3] < 5)
        total_cells = res_chi2[3].size
        percent_cells_below_5 = (cells_below_5 / total_cells) * 100
        min_expected_count = res_chi2[3].min()
        nota_rodape = (f"a. {cells_below_5} cells ({percent_cells_below_5:.2f}%) have expected count less than 5. "
                       f"The minimum expected count is {min_expected_count:.2f}.")
    else:
        nota_rodape = ""

    # Substituir NaN por strings vazias para evitar problemas de dtype
    resultados_df = resultados_df.astype(object).where(pd.notnull(resultados_df), "")

    # Formatação do DataFrame
    resultados_df_formated = resultados_df.copy(deep=True)
    resultados_df_formated = resultados_df_formated.map(lambda x: '{:.3f}'.format(x) if isinstance(x, (int, float)) else x)
    resultados_df_formated["Value"] = resultados_df["Value"].apply(lambda x: '{:.2f}'.format(x) if isinstance(x, (int, float)) else x)
    resultados_df_formated.loc['N. of Valid Cases', 'Value'] = '{:.0f}'.format(resultados_df.loc['N. of Valid Cases', 'Value'])
    resultados_df_formated["df"] = resultados_df["df"].apply(lambda x: '{:.0f}'.format(x) if isinstance(x, (int, float)) else x)

    # Exibindo os resultados formatados como tabela usando tabulate
    print("\nResultados dos Testes de Independência: \n")
    print(tabulate(resultados_df_formated, headers='keys', tablefmt='grid'))
    
    # Imprimindo a nota de rodapé
    print(nota_rodape)

def calcular_odds_ratio_razao_risco_discrepancia(tabela_contingencia, print_discrepancy=False):
    """
    Calcula e exibe o Odds Ratio (OR), a Razão de Risco (RR) para ambas as categorias de um grupo, e a discrepância
    baseada numa tabela de contingência 2x2. A função também calcula a probabilidade condicionada para avaliar a
    discrepância entre dois eventos. Os resultados são exibidos em um DataFrame formatado e incluem os intervalos
    de confiança de 95% para o OR e RR, além do total de casos válidos.

    Parâmetros:
    - tabela_contingencia (pd.DataFrame): Tabela de contingência 2x2 contendo as frequências observadas.
                                          Os índices e as colunas devem ter nomes representando grupos e categorias.

    A função inicialmente identifica os nomes dos grupos e categorias envolvidos e, em seguida, usa a biblioteca
    statsmodels para calcular o OR e o RR, incluindo seus respectivos intervalos de confiança de 95%. Uma inversão
    da tabela de contingência é usada para calcular o RR para a segunda categoria. Além disso, calcula a discrepância
    entre as probabilidades condicionadas de dois eventos específicos, que é uma medida de diferença relativa entre
    as probabilidades de ocorrência de um evento sob diferentes condições. Os resultados são exibidos em um DataFrame
    formatado, e a discrepância é impressa separadamente.
    """
    
    # Nomes de grupos e categorias
    nome_grupo = [tabela_contingencia.index.name, tabela_contingencia.columns.name] 
    categorias_grupo1 = tabela_contingencia.index.tolist()
    categorias_grupo2 = tabela_contingencia.columns.tolist()
       
    # Cálculo do Odds Ratio (OR)
    table = sm.stats.Table2x2(tabela_contingencia.values)  # tabela_contingencia.values, pois a entrada é um array
    odds_ratio = table.oddsratio
    odds_ratio_ci = table.oddsratio_confint()

    # Cálculo da Razão de Risco (Risk Ratio - RR ou RP)
    risk_ratio_1 = table.riskratio
    risk_ratio_1_ci = table.riskratio_confint()

    # Para a 2ª categoria de X em relação à 2ª categoria de Y (inversão da tabela)
    tabela_contingencia_invertida = tabela_contingencia.iloc[:, ::-1]
    table_flip = sm.stats.Table2x2(tabela_contingencia_invertida.values)
    risk_ratio_2 = table_flip.riskratio
    risk_ratio_2_ci = table_flip.riskratio_confint()

    # Preparando um DataFrame para exibição dos resultados
    results_df = pd.DataFrame({
        'Value': [odds_ratio, risk_ratio_1, risk_ratio_2, tabela_contingencia.sum().sum()],
        '95% CI Lower': [odds_ratio_ci[0], risk_ratio_1_ci[0], risk_ratio_2_ci[0], ""],
        '95% CI Upper': [odds_ratio_ci[1], risk_ratio_1_ci[1], risk_ratio_2_ci[1], ""]
    }, index=[f'Odds Ratio for {nome_grupo[0]} ({categorias_grupo1[0]} / {categorias_grupo1[1]})', 
              f'RR (ou RP) for {nome_grupo[1]} = {categorias_grupo2[0]}', 
              f'RR (ou RP) for {nome_grupo[1]} = {categorias_grupo2[1]}',
              "N. of Valid Cases"])

    # Cálculo da Discrepância
    # Calcula as probabilidades condicionadas para o grupo 2 dado o grupo 1
    prob_cond_grupo2_dado_grupo1 = tabela_contingencia.div(tabela_contingencia.sum(axis=1), axis=0)   
    # Cálculo das probabilidades condicionadas de p21 e p11
    evento = categorias_grupo2[0]
    condicao = categorias_grupo1[1]
    p21 =prob_cond_grupo2_dado_grupo1.loc[condicao, evento]
    evento = categorias_grupo2[0]
    condicao = categorias_grupo1[0]
    p11 =prob_cond_grupo2_dado_grupo1.loc[condicao, evento]
    # Cálculo da discrepância
    discrepancy = (1 - p21)/(1 - p11) - 1

    # Formatação do DataFrame
    results_df_formated = results_df.map(lambda x: '{:.3f}'.format(x) if isinstance(x, (int, float)) else x)
    results_df_formated.loc['N. of Valid Cases', 'Value'] = '{:.0f}'.format(results_df.loc['N. of Valid Cases', 'Value'])

    if print_discrepancy==True:
        display(results_df_formated)
        print(f"Discrepância = {discrepancy:.3f} e (\u03B8 * p21) = {odds_ratio*p21:.3f}")
    else:  
        return results_df_formated

def calcular_odds_ratio_razao_risco_discrepancia_New(tabela_contingencia, print_discrepancy=False):
    """
    Calcula e exibe o Odds Ratio (OR), a Razão de Risco (RR) para ambas as categorias de um grupo, e a discrepância
    baseada numa tabela de contingência 2x2. A função também calcula a probabilidade condicionada para avaliar a
    discrepância entre dois eventos. Os resultados são exibidos em um DataFrame formatado e incluem os intervalos
    de confiança de 95% para o OR e RR, além do total de casos válidos.

    Parâmetros:
    - tabela_contingencia (pd.DataFrame): Tabela de contingência 2x2 contendo as frequências observadas.
                                          Os índices e as colunas devem ter nomes representando grupos e categorias.

    A função inicialmente identifica os nomes dos grupos e categorias envolvidos e, em seguida, usa a biblioteca
    statsmodels para calcular o OR e o RR, incluindo seus respectivos intervalos de confiança de 95%. Uma inversão
    da tabela de contingência é usada para calcular o RR para a segunda categoria. Além disso, calcula a discrepância
    entre as probabilidades condicionadas de dois eventos específicos, que é uma medida de diferença relativa entre
    as probabilidades de ocorrência de um evento sob diferentes condições. Os resultados são exibidos em um DataFrame
    formatado, e a discrepância é impressa separadamente.
    """
    
    # Nomes de grupos e categorias
    nome_grupo = [tabela_contingencia.index.name, tabela_contingencia.columns.name] 
    categorias_grupo1 = tabela_contingencia.index.tolist()
    categorias_grupo2 = tabela_contingencia.columns.tolist()
       
    # Cálculo do Odds Ratio (OR)
    table = sm.stats.Table2x2(tabela_contingencia.values)  # tabela_contingencia.values, pois a entrada é um array
    odds_ratio = table.oddsratio
    odds_ratio_ci = table.oddsratio_confint()

    # Cálculo da Razão de Risco (Risk Ratio - RR ou RP)
    risk_ratio_1 = table.riskratio
    risk_ratio_1_ci = table.riskratio_confint()

    # Para a 2ª categoria de X em relação à 2ª categoria de Y (inversão da tabela)
    tabela_contingencia_invertida = tabela_contingencia.iloc[:, ::-1]
    table_flip = sm.stats.Table2x2(tabela_contingencia_invertida.values)
    risk_ratio_2 = table_flip.riskratio
    risk_ratio_2_ci = table_flip.riskratio_confint()

    # Preparando um DataFrame para exibição dos resultados
    results_df = pd.DataFrame({
        'Value': [odds_ratio, risk_ratio_1, risk_ratio_2, tabela_contingencia.sum().sum()],
        '95% CI Lower': [odds_ratio_ci[0], risk_ratio_1_ci[0], risk_ratio_2_ci[0], ""],
        '95% CI Upper': [odds_ratio_ci[1], risk_ratio_1_ci[1], risk_ratio_2_ci[1], ""]
    }, index=[f'Odds Ratio for {nome_grupo[0]} ({categorias_grupo1[0]} / {categorias_grupo1[1]})', 
              f'RR (ou RP) for {nome_grupo[1]} = {categorias_grupo2[0]}', 
              f'RR (ou RP) for {nome_grupo[1]} = {categorias_grupo2[1]}',
              "N. of Valid Cases"])

    # Cálculo da Discrepância
    # Calcula as probabilidades condicionadas para o grupo 2 dado o grupo 1
    prob_cond_grupo2_dado_grupo1 = tabela_contingencia.div(tabela_contingencia.sum(axis=1), axis=0)   
    # Cálculo das probabilidades condicionadas de p21 e p11
    evento = categorias_grupo2[0]
    condicao = categorias_grupo1[1]
    p21 = prob_cond_grupo2_dado_grupo1.loc[condicao, evento]
    evento = categorias_grupo2[0]
    condicao = categorias_grupo1[0]
    p11 = prob_cond_grupo2_dado_grupo1.loc[condicao, evento]
    # Cálculo da discrepância
    discrepancy = (1 - p21)/(1 - p11) - 1

    # Formatação do DataFrame
    results_df_formated = results_df.map(lambda x: '{:.3f}'.format(x) if isinstance(x, (int, float)) else x)
    results_df_formated.loc['N. of Valid Cases', 'Value'] = '{:.0f}'.format(results_df.loc['N. of Valid Cases', 'Value'])

    if print_discrepancy:
        print("\nResultados dos Testes de Independência: \n")
        print(tabulate(results_df_formated, headers='keys', tablefmt='grid'))
        print(f"\nDiscrepância = {discrepancy:.3f} e (\u03B8 * p21) = {odds_ratio*p21:.3f}")
    else:  
        print("\nResultados dos Testes de Independência: \n")
        print(tabulate(results_df_formated, headers='keys', tablefmt='grid'))

def calcular_distribuicao_probabilidades_e_decisao_hipotese_OLD(tabela_contingencia, alpha):
    """
    Calcula a distribuição de probabilidades de eventos possíveis baseada em uma tabela de contingência 2x2 ou
    utiliza valores totais e marginais pré-definidos na tabela para determinar as regiões de aceitação e rejeição
    da hipótese nula (H0) com base em um valor alpha especificado.

    Parâmetros:
    - tabela_contingencia (pd.DataFrame): Tabela de contingência contendo as frequências observadas ou totais marginais.
                                          Espera-se uma tabela 2x2 para o cálculo direto ou uma tabela com valores totais
                                          e marginais pré-definidos nas posições [2,2], [0,2], e [2,0].
    - alpha (float): Nível de significância para o teste de hipótese.

    Retorna:
    - df_formated (pd.DataFrame): DataFrame contendo as probabilidades dos eventos possíveis, formatadas com 3 casas decimais,
                                   e a soma acumulada dessas probabilidades.
    - acceptance_range (list): Intervalo de valores que define a região de aceitação da hipótese nula.
    - rejection_range (str): Representação em string dos intervalos que definem a região de rejeição da hipótese nula.

    A função verifica a estrutura da tabela de contingência fornecida para determinar a abordagem de cálculo. Se a tabela
    for 2x2, os cálculos são baseados nos valores observados. Caso contrário, assume-se que os totais e totais marginais
    estão especificados na tabela. Utiliza-se a distribuição hipergeométrica para calcular as probabilidades dos eventos
    possíveis e, em seguida, determina-se as regiões de aceitação e rejeição de H0 com base no valor alpha fornecido.
    """
    
    # Verificando se a Tabela de Contingência está completa
    if tabela_contingencia.size == 4:
        # Valores observados na amostra
        a11 = tabela_contingencia.iloc[0, 0]
        a12 = tabela_contingencia.iloc[0, 1]
        a21 = tabela_contingencia.iloc[1, 0]
        a22 = tabela_contingencia.iloc[1, 1]
        
        # Definição dos totais marginais
        M = a11 + a12 + a21 + a22 # total da amostra
        n = a11 + a12 # total marginal da linha
        N = a11 + a21 # total marginal da coluna
    else:
        M = tabela_contingencia.iloc[2, 2]
        n = tabela_contingencia.iloc[0, 2]
        N = tabela_contingencia.iloc[2, 0]

    # Cálculo das probabilidades
    results = []
    for a11 in range(max(0, n + N - M), min(n, N) + 1):
        p_value = hypergeom.pmf(a11, M, n, N)
        results.append({'y_value': a11, 'p_value': p_value})
    
    # Conversão dos resultados em um DataFrame e ordenação pelas probabilidades de forma decrescente
    df_results = pd.DataFrame(results)
    
    # Ordenação pelas probabilidades de forma decrescente
    df_sorted = df_results.sort_values(by='p_value', ascending=False)
    df_reset = df_sorted.reset_index(drop=True)
    
    # Criando coluna de soma acumulada de p_value
    df_reset['cum_sum'] = df_reset['p_value'].cumsum()
    
    # Formatando a coluna p_value para 3 casas decimais
    df_formated = pd.DataFrame()
    df_formated['y_value'] = df_reset['y_value']
    df_formated[['p_value', 'cum_sum']] = df_reset[['p_value', 'cum_sum']].map("{:.3f}".format)

    ## Determinação da região de aceitação de H0 ##
    idx = (df_reset['cum_sum'] > (1 - alpha)).idxmax()
    #idx = idx - 1
    if df_reset['cum_sum'].iloc[0] > (1 - alpha):
        acceptance_region = df_reset.loc[:0]
    else:
        acceptance_region = df_reset.loc[:idx]
    acceptance_range = [acceptance_region['y_value'].min(), acceptance_region['y_value'].max()]

    ## Determinação da região de rejeição de H0 ##
    critical_left_range = [df_reset['y_value'].min(), acceptance_region['y_value'].min() - 1]
    critical_right_range = [acceptance_region['y_value'].max()+1, df_reset['y_value'].max()]
    rejection_range = f"{critical_left_range} U {critical_right_range}"
    
    return df_formated, acceptance_range, rejection_range

def calcular_distribuicao_probabilidades_e_decisao_hipotese(tabela_contingencia, alpha):
    """
    Calcula a distribuição de probabilidades de eventos possíveis baseada em uma tabela de contingência 2x2 ou
    utiliza valores totais e marginais pré-definidos na tabela para determinar as regiões de aceitação e rejeição
    da hipótese nula (H0) com base em um valor alpha especificado.

    Parâmetros:
    - tabela_contingencia (pd.DataFrame): Tabela de contingência contendo as frequências observadas ou totais marginais.
                                          Espera-se uma tabela 2x2 para o cálculo direto ou uma tabela com valores totais
                                          e marginais pré-definidos nas posições [2,2], [0,2], e [2,0].
    - alpha (float): Nível de significância para o teste de hipótese.

    Retorna:
    - df_formated (pd.DataFrame): DataFrame contendo as probabilidades dos eventos possíveis, formatadas com 3 casas decimais,
                                   e a soma acumulada dessas probabilidades.
    - acceptance_range (list): Intervalo de valores que define a região de aceitação da hipótese nula.
    - rejection_range (str): Representação em string dos intervalos que definem a região de rejeição da hipótese nula.
    """
    
    # Verificando se a Tabela de Contingência está completa
    if tabela_contingencia.size == 4:
        # Valores observados na amostra
        a11 = tabela_contingencia.iloc[0, 0]
        a12 = tabela_contingencia.iloc[0, 1]
        a21 = tabela_contingencia.iloc[1, 0]
        a22 = tabela_contingencia.iloc[1, 1]
        
        # Definição dos totais marginais
        M = a11 + a12 + a21 + a22 # total da amostra
        n = a11 + a12 # total marginal da linha
        N = a11 + a21 # total marginal da coluna
    else:
        M = tabela_contingencia.iloc[2, 2]
        n = tabela_contingencia.iloc[0, 2]
        N = tabela_contingencia.iloc[2, 0]

    # Cálculo das probabilidades
    results = []
    for a11 in range(max(0, n + N - M), min(n, N) + 1):
        p_value = hypergeom.pmf(a11, M, n, N)
        results.append({'y_value': a11, 'p_value': p_value})
    
    # Conversão dos resultados em um DataFrame e ordenação pelas probabilidades de forma decrescente
    df_results = pd.DataFrame(results)
    
    # Ordenação pelas probabilidades de forma decrescente
    df_sorted = df_results.sort_values(by='p_value', ascending=False)
    df_reset = df_sorted.reset_index(drop=True)
    
    # Criando coluna de soma acumulada de p_value
    df_reset['cum_sum'] = df_reset['p_value'].cumsum()
    
    # Formatando a coluna p_value para 3 casas decimais
    df_formated = pd.DataFrame()
    df_formated['y_value'] = df_reset['y_value']
    df_formated[['p_value', 'cum_sum']] = df_reset[['p_value', 'cum_sum']].map("{:.3f}".format)

    ## Determinação da região de aceitação de H0 ##
    idx = (df_reset['cum_sum'] > (1 - alpha)).idxmax()
    if df_reset['cum_sum'].iloc[0] > (1 - alpha):
        acceptance_region = df_reset.loc[:0]
    else:
        acceptance_region = df_reset.loc[:idx]
    acceptance_range = [int(acceptance_region['y_value'].min()), int(acceptance_region['y_value'].max())]

    ## Determinação da região de rejeição de H0 ##
    critical_left_range = [int(df_reset['y_value'].min()), int(acceptance_region['y_value'].min()) - 1]
    critical_right_range = [int(acceptance_region['y_value'].max()) + 1, int(df_reset['y_value'].max())]
    rejection_range = f"{critical_left_range} U {critical_right_range}"
    
    return df_formated, acceptance_range, rejection_range

def complementar_tabela_contingencia_com_analise_estatistica(tabela_contingencia, incluir_residuos=True):
    """
    Complementa uma tabela de contingência com análises estatísticas adicionais, incluindo
    frequências esperadas, probabilidades condicionais, percentuais totais, resíduos de Pearson não ajustados
    e resíduos ajustados estandardizados (se incluir_residuos for True). Também adiciona uma visualização estruturada dos dados
    com porcentagens dentro de grupos, porcentagens totais e soma de linhas e colunas aplicáveis.

    Parâmetros:
    - tabela_contingencia (pd.DataFrame): Tabela de contingência original com contagens observadas.
    - incluir_residuos (bool): Indica se os resíduos de Pearson não ajustados e ajustados estandardizados devem ser incluídos.

    Retorna:
    - combined_df (pd.DataFrame): DataFrame complementado com múltiplas camadas de índices representando
                                  diferentes análises estatísticas e formatações para melhor visualização e interpretação.
    """
    # Encapsulando a tabela para análises no statsmodels
    tabela_analise = Table(tabela_contingencia)
    
    # Calculando as frequências esperadas (fe)
    frequencias_esperadas = tabela_analise.fittedvalues
    
    # Calcula as probabilidades condicionadas
    prob_cond_grupo2_dado_grupo1 = tabela_contingencia.div(tabela_contingencia.sum(axis=1), axis=0)
    prob_cond_grupo1_dado_grupo2 = tabela_contingencia.div(tabela_contingencia.sum(axis=0), axis=1)
    
    # Calcula a percentagem total
    perc_total =  tabela_contingencia / tabela_contingencia.values.sum()
    
    # Calcula os Resíduos de Pearson (não ajustados)
    residuos_nao_ajustados = tabela_analise.resid_pearson
    
    # Calcula os Resíduos ajustados estandardizados
    residuos_estandardizados = tabela_analise.standardized_resids
    
    # Define nomes para os níveis de índice e colunas
    row_perc_name = f'% within {tabela_contingencia.index.name}'
    col_perc_name = f'% within {tabela_contingencia.columns.name}'
    index_keys = [
        'Count', 'Expected Count', row_perc_name, col_perc_name,
        '% of Total'
    ]
    
    # Cria uma lista de DataFrames a serem concatenados
    dfs_to_concat = [
        tabela_contingencia,  # Mantenha os dados numéricos aqui
        frequencias_esperadas,
        prob_cond_grupo2_dado_grupo1 * 100,
        prob_cond_grupo1_dado_grupo2 * 100,
        perc_total * 100
    ]
    
    # Concatenação dos DataFrames sem aplicar a formatação
    combined_df = pd.concat(dfs_to_concat, axis=0, keys=index_keys)
    
    if incluir_residuos:
        residuos_keys = ['Standardized Residual', 'Adjusted Residual']
        residuos_dfs = pd.concat([residuos_nao_ajustados, residuos_estandardizados], axis=0, keys=residuos_keys)
        combined_df = pd.concat([combined_df, residuos_dfs], axis=0)
        index_keys.extend(residuos_keys)
    
    # Reorganiza e ordena os níveis do índice para melhor visualização
    combined_df = combined_df.swaplevel(0, 1).sort_index()
    
    # Reordena as linhas para manter a consistência com os 'index_keys'
    combined_df = combined_df.reindex(index_keys, level=1)
    
    # Adicionando a coluna Total para soma das linhas aplicáveis
    combined_df.loc[(slice(None), 'Count'), 'Total'] = combined_df.loc[(slice(None), 'Count'), :].sum(axis=1)
    combined_df.loc[(slice(None), 'Expected Count'), 'Total'] = combined_df.loc[(slice(None), 'Expected Count'), :].sum(axis=1)
    combined_df.loc[(slice(None), row_perc_name), 'Total'] = combined_df.loc[(slice(None), row_perc_name), :].sum(axis=1)
    combined_df.loc[(slice(None), '% of Total'), 'Total'] = combined_df.loc[(slice(None), '% of Total'), :].sum(axis=1)
    primeiro_idx = combined_df.loc[(slice(None), col_perc_name), 'Total'].index[0]
    combined_df.loc[primeiro_idx, 'Total'] = combined_df.loc[(slice(None), '% of Total'), 'Total'].values[0]
    segundo_idx = combined_df.loc[(slice(None), col_perc_name), 'Total'].index[1]
    combined_df.loc[segundo_idx, 'Total'] = combined_df.loc[(slice(None), '% of Total'), 'Total'].values[1]
    
    # Adicionando a linha Total para soma das colunas aplicáveis
    combined_df.loc[('Total', 'Count'), :] = combined_df.loc[(slice(None), 'Count'), :].sum()
    combined_df.loc[('Total', 'Expected Count'), :] = combined_df.loc[(slice(None), 'Expected Count'), :].sum()
    combined_df.loc[('Total', row_perc_name), :] = combined_df.loc[(slice(None), '% of Total'), :].sum()
    combined_df.loc[('Total', col_perc_name), :] = combined_df.loc[(slice(None), col_perc_name), :].sum()
    combined_df.loc[('Total', '% of Total'), :] = combined_df.loc[(slice(None), '% of Total'), :].sum()
    
    # Formatação
    combined_df = combined_df.map(lambda x: f"{x:.1f}" if pd.notna(x) else "")

    return combined_df
    
def resolver_sistema_equacoes_dada_variavel_tabela_contingencia(tabela_contingencia, given_var):
    """
    Resolve um sistema de equações para uma tabela de contingência 2x2, considerando o valor de uma variável específica.
    Esta função aceita tanto uma tabela de contingência completa quanto especificações de totais e totais marginais
    diretamente na tabela. O valor de uma variável específica é fornecido como uma string no formato 'variável=valor'.

    Parâmetros:
    - tabela_contingencia (pd.DataFrame): Tabela de contingência 2x2 ou uma tabela contendo totais e totais marginais.
    - given_var (str): String contendo o nome da variável (a11, a12, a21, a22) e seu valor atribuído, separados por '='.

    Retorna:
    - solution (dict): Dicionário contendo as soluções para as variáveis da tabela de contingência, com chaves sendo
                       os nomes das variáveis em formato de string e seus valores correspondentes. Inclui a variável
                       fornecida e seu valor especificado.

    A função primeiro verifica o tamanho da tabela de contingência para determinar se os valores são diretamente observados
    ou se os totais/marginais são fornecidos. Em seguida, extrai o nome da variável e seu valor da string fornecida, define
    as variáveis simbólicas e as equações representando os totais e totais marginais. O sistema de equações é resolvido
    com o valor fornecido para a variável especificada, e a solução completa é convertida para um dicionário com chaves
    em formato de string antes de ser retornada.
    """
    
    # Verificando se a Tabela de Contingência está completa
    if tabela_contingencia.size == 4:
        # Valores observados na amostra
        a11 = tabela_contingencia.iloc[0, 0]
        a12 = tabela_contingencia.iloc[0, 1]
        a21 = tabela_contingencia.iloc[1, 0]
        a22 = tabela_contingencia.iloc[1, 1]
        
        # Definição dos totais marginais
        M = a11 + a12 + a21 + a22 # total da amostra
        n = a11 + a12 # total marginal da linha
        N = a11 + a21 # total marginal da coluna
    else:
        M = tabela_contingencia.iloc[2, 2]
        n = tabela_contingencia.iloc[0, 2]
        N = tabela_contingencia.iloc[2, 0]
        
    # Dividir a string pelo sinal de igual
    parts = given_var.split('=')
    
    # A primeira parte é o nome da variável, removendo espaços em branco
    given_var_name = parts[0].strip()
    
    # A segunda parte é o valor da variável, convertido para inteiro
    given_var_value = int(parts[1].strip())
        
    # Definindo as variáveis
    a11, a12, a21, a22 = symbols('a11 a12 a21 a22')
    
    # Equações dadas
    eq1 = Eq(a11 + a12 + a21 + a22, M)  # M: total da amostra
    eq2 = Eq(a11 + a12, N)  # N: total marginal da coluna
    eq3 = Eq(a11 + a21, n)  # n: total marginal da linha
    
    # Substituindo a variável fornecida
    given_var = {'a11': a11, 'a12': a12, 'a21': a21, 'a22': a22}[given_var_name]
    eq1_substituted = eq1.subs(given_var, given_var_value)
    eq2_substituted = eq2.subs(given_var, given_var_value)
    eq3_substituted = eq3.subs(given_var, given_var_value)
    
    # Determinando as variáveis a serem resolvidas com base na variável fornecida
    variables_to_solve = [a11, a12, a21, a22]
    variables_to_solve.remove(given_var)  # Remove a variável fornecida da lista
    
    # Resolvendo o sistema de equações
    solution = solve((eq1_substituted, eq2_substituted, eq3_substituted), variables_to_solve)
    
    # Adicionando a variável fornecida à solução
    solution[given_var] = given_var_value
    
    # Converter a solução para usar nomes de variáveis como strings
    solution_str_keys = {str(key): val for key, val in solution.items()}
    
    # Adicionando a variável fornecida à solução, garantindo que a chave esteja em formato string
    solution_str_keys[given_var_name] = given_var_value

    return solution_str_keys
    
def decompor_tabela_contingencia(tabela_contingencia):
    """
    Analisa a tabela de contingência, identifica os maiores resíduos,
    cria subtabelas para eles, calcula G^2 para cada subtabela e exibe os resultados.
    """
    
    def encontrar_maiores_valores(df):
        """
        Encontra os índices (linha, coluna) dos quatro maiores valores em módulo,
        superiores a um valor crítico, em ordem decrescente.
    
        Parâmetros:
        - df (pd.DataFrame): DataFrame para análise.
    
        Retorna:
        - list: Lista de tuplas com índices de linha e coluna para valores que
                excedem o valor crítico.
        """
        valor_critico = 1.96
        # Filtrar valores superiores ao valor crítico e ordenar em ordem decrescente
        valores_filtrados = df.abs().where(lambda x: x > valor_critico).stack().sort_values(ascending=False)
    
        resultados = [(df.index.get_loc(loc[0]), df.columns.get_loc(loc[1])) for loc in valores_filtrados.index[:4]]
        
        return resultados
    
    def criar_subtabela(dataframe, indice_linha, indice_coluna):
        # Calcula o índice da última linha
        ultimo_indice_linha = len(dataframe.index) - 1
        
        # Determina as linhas a serem utilizadas na nova tabela
        if indice_linha < ultimo_indice_linha:
            linhas_selecionadas = dataframe.iloc[indice_linha:ultimo_indice_linha+1].index.tolist()
        else:
            linhas_selecionadas = dataframe.iloc[indice_linha-1:ultimo_indice_linha+1].index.tolist()
        
        # Calcula o índice da última coluna
        ultimo_indice_coluna = len(dataframe.columns) - 1
        
        # Determina as colunas a serem utilizadas na nova tabela
        if indice_coluna < ultimo_indice_coluna:
            colunas_selecionadas = dataframe.iloc[:, indice_coluna:ultimo_indice_coluna+1].columns.tolist()
        else:
            colunas_selecionadas = dataframe.iloc[:, indice_coluna-1:ultimo_indice_coluna+1].columns.tolist()
        
        # Identifica a linha e coluna principal e as outras linhas e colunas
        linha_principal = dataframe.index[indice_linha]
        outras_linhas = linhas_selecionadas.copy()
        outras_linhas.remove(linha_principal)
        
        coluna_principal = dataframe.columns[indice_coluna]
        outras_colunas = colunas_selecionadas.copy()
        outras_colunas.remove(coluna_principal)
        
        # Constrói a nova tabela 2x2
        nova_tabela = pd.DataFrame({
            coluna_principal: dataframe.loc[linha_principal, coluna_principal],
            '&'.join(outras_colunas): dataframe.loc[linha_principal, outras_colunas].sum()
        }, index=[linha_principal])
        
        # Adiciona a segunda linha à nova tabela
        nova_tabela.loc['&'.join(outras_linhas)] = [
            dataframe.loc[outras_linhas, coluna_principal].sum(),
            dataframe.loc[outras_linhas, outras_colunas].sum().sum()
        ]
        
        # Define os nomes dos índices e colunas
        nova_tabela.index.name = dataframe.index.name
        nova_tabela.columns.name = dataframe.columns.name
       
        # Ordena as linhas e colunas da nova tabela
        nova_tabela = nova_tabela.sort_index()
        nova_tabela = nova_tabela.sort_index(axis=1)
        
        return nova_tabela
    
    # Cálculo de G^2 para a tabela original
    g2_tabela = chi2_contingency(tabela_contingencia, correction=False, lambda_="log-likelihood")[0]
    
    # Inicializando a string com o resultado da tabela original
    resultado_final = f'(G²_{{Tabela}} = {g2_tabela:.2f}) = '
    
    # Análise dos resíduos
    tabela_analise = Table(tabela_contingencia)
    residuos_estandardizados = tabela_analise.standardized_resids
    resultados = encontrar_maiores_valores(residuos_estandardizados)
    
    # inicializando listas
    subtabelas = []
    g2_subtabelas = []
    subtabelas_complementadas = []
    
    # Criação e análise de subtabelas
    for i, (idx_linha, idx_coluna) in enumerate(resultados):
        subtabela = criar_subtabela(tabela_contingencia, idx_linha, idx_coluna)
        subtabelas.append(subtabela)
        g2_subtabela = chi2_contingency(subtabela, correction=False, lambda_="log-likelihood")[0]
        g2_subtabelas.append(g2_subtabela)
        resultado_final += f'(G²_{{Subtabela\ {i+1}}} = {g2_subtabela:.2f})'
        if i < (len(resultados)-1):
            resultado_final += ' + '
        subtabela_complementada = complementar_tabela_contingencia_com_analise_estatistica(subtabela)
        subtabelas_complementadas.append(subtabela_complementada)
    
    # Impressão dos resultados
    display(Math(resultado_final))
    for i in range(len(resultados)):
        display(Math(f'G^2_{{Subtabela\ {i+1}}} = {g2_subtabelas[i]:.2f}'))
        display(subtabelas_complementadas[i])

    return subtabelas
    
def gerar_tabela_contingencia(dados, grupos, categorias):
    """
    Cria uma tabela de contingência com as frequências agregadas dos grupos fornecidos,
    renomeando os índices e colunas com base nas categorias especificadas.

    Parâmetros:
    - dados: DataFrame contendo os dados para análise.
    - grupos: Lista contendo os nomes das colunas que representam os grupos.
    - categorias: Dicionário com as colunas dos grupos como chaves e listas com nomes de categorias como valores.

    Retorna:
    - tabela_contingencia: DataFrame com a tabela de contingência gerada.
    """
    def criar_mapeamento_categorias(coluna, categorias):
        """
        Cria um mapeamento de categorias para uma coluna com valores únicos, atribuindo nomes de categoria
        especificados na lista `categorias` aos valores únicos, em ordem crescente.

        Parâmetros:
        - coluna (pd.Series): Coluna do DataFrame contendo os valores a serem mapeados.
        - categorias (list): Lista contendo os nomes das categorias a serem atribuídos aos valores únicos encontrados.

        Retorna:
        - mapeamento (dict): Dicionário contendo o mapeamento de valores únicos para os nomes de categoria especificados.

        Essa função é útil para redefinir ou renomear as categorias de uma coluna em um DataFrame pandas, especialmente
        quando se deseja converter valores numéricos ou códigos em rótulos mais descritivos para fins de análise ou
        visualização de dados.
        """
        
        valores_unicos = sorted(coluna.unique())  # Obtém e ordena os valores únicos
        if len(valores_unicos) > len(categorias):
            raise ValueError("Número de categorias fornecidas é menor que o número de valores únicos na coluna.")
        mapeamento = {val: nome for val, nome in zip(valores_unicos, categorias)}
        return mapeamento
    
    # Criando a tabela de contingência
    tabela_contingencia = pd.crosstab(
        index=[dados[grupo] for grupo in grupos[:-1]],
        columns=dados[grupos[-1]],
        values=dados.iloc[:, -1],
        aggfunc='sum',
        dropna=False
    )

    # Gerando mapeamentos para índices e colunas
    mapeamentos = {grupo: criar_mapeamento_categorias(dados[grupo], categorias[grupo]) for grupo in grupos[:-1]}
    colunas = criar_mapeamento_categorias(dados[grupos[-1]], categorias[grupos[-1]])

    # Aplicando mapeamentos aos índices e colunas
    for i, grupo in enumerate(grupos[:-1]):
        tabela_contingencia.rename(index=mapeamentos[grupo], level=i, inplace=True)
    tabela_contingencia.rename(columns=colunas, inplace=True)

    return tabela_contingencia
    
def complementar_e_filtrar_tabelas_contingencia_OLD(data_frame_multi_nivel, funcao_analise_estatistica):
    """
    Complementa tabelas de contingência em um DataFrame multi-nível com análise estatística e filtra resultados específicos.
    Este processo é feito agrupando o DataFrame por todos os níveis de índice, exceto o último, aplicando a análise estatística,
    e finalmente filtrando os resultados por critérios específicos.

    Parâmetros:
    - data_frame_multi_nivel (pd.DataFrame): DataFrame com índices multiníveis.
    - funcao_analise_estatistica (function): Função que complementa as tabelas de contingência com análise estatística.

    Retorna:
    - pd.DataFrame: DataFrame filtrado com as tabelas de contingência complementadas.
    """

    data_frame_complementado = pd.DataFrame()
    
    # Processar cada grupo definido pelos níveis de índice, exceto o último
    for nome, grupo in data_frame_multi_nivel.groupby(level=list(range(data_frame_multi_nivel.index.nlevels - 1))):
        # Garantir que o nome seja uma tupla
        nome = (nome,) if not isinstance(nome, tuple) else nome
        
        # Complementar a tabela de contingência do grupo com análise estatística
        grupo_analisado = funcao_analise_estatistica(grupo.droplevel(list(range(len(nome)))))
        
        # Reconstruir os índices multiníveis para cada grupo analisado
        for i in reversed(range(len(nome))):
            grupo_analisado = pd.concat({(nome[i],): grupo_analisado}, names=[data_frame_multi_nivel.index.names[i]])
        data_frame_complementado = pd.concat([data_frame_complementado, grupo_analisado])
    
    # Complementar o último nível de índice com análise estatística
    grupo_analisado = funcao_analise_estatistica(data_frame_multi_nivel.groupby(level=data_frame_multi_nivel.index.names[-1]).sum())
    for i in reversed(range(data_frame_multi_nivel.index.nlevels - 1)):
        grupo_analisado = pd.concat({('Total',): grupo_analisado}, names=[data_frame_multi_nivel.index.names[i]])
    data_frame_complementado = pd.concat([data_frame_complementado, grupo_analisado])
    
    # Filtrar resultados específicos baseados nos valores do último nível de índice
    resultados_filtrados = data_frame_complementado.loc[data_frame_complementado.index.get_level_values(-1).isin(['Count', 'Expected Count', f'% within {data_frame_multi_nivel.index.names[-1]}'])]

    return resultados_filtrados if not resultados_filtrados.empty else data_frame_complementado
    

def complementar_e_filtrar_tabelas_contingencia(data_frame_multi_nivel, funcao_analise_estatistica):
    """
    Complementa tabelas de contingência em um DataFrame multi-nível com análise estatística e filtra resultados específicos.
    Este processo é feito agrupando o DataFrame por todos os níveis de índice, exceto o último, aplicando a análise estatística,
    e finalmente filtrando os resultados por critérios específicos.

    Parâmetros:
    - data_frame_multi_nivel (pd.DataFrame): DataFrame com índices multiníveis.
    - funcao_analise_estatistica (function): Função que complementa as tabelas de contingência com análise estatística.

    Retorna:
    - pd.DataFrame: DataFrame filtrado com as tabelas de contingência complementadas.
    """

    data_frame_complementado = pd.DataFrame()
    
    # Definir os níveis de índice para agrupar, excluindo o último
    niveis_para_agrupar = list(range(data_frame_multi_nivel.index.nlevels - 1))
    nivel_para_agrupar = niveis_para_agrupar if len(niveis_para_agrupar) > 1 else niveis_para_agrupar[0]
    
    # Processar cada grupo definido pelos níveis de índice, exceto o último
    for nome, grupo in data_frame_multi_nivel.groupby(level=nivel_para_agrupar):
        # Garantir que o nome seja uma tupla
        nome = (nome,) if not isinstance(nome, tuple) else nome
        
        # Complementar a tabela de contingência do grupo com análise estatística
        grupo_analisado = funcao_analise_estatistica(grupo.droplevel(list(range(len(nome)))))
        
        # Reconstruir os índices multiníveis para cada grupo analisado
        for i in reversed(range(len(nome))):
            grupo_analisado = pd.concat({(nome[i],): grupo_analisado}, names=[data_frame_multi_nivel.index.names[i]])
        data_frame_complementado = pd.concat([data_frame_complementado, grupo_analisado])
    
    # Complementar o último nível de índice com análise estatística
    grupo_analisado = funcao_analise_estatistica(data_frame_multi_nivel.groupby(level=data_frame_multi_nivel.index.names[-1]).sum())
    for i in reversed(range(data_frame_multi_nivel.index.nlevels - 1)):
        grupo_analisado = pd.concat({('Total',): grupo_analisado}, names=[data_frame_multi_nivel.index.names[i]])
    data_frame_complementado = pd.concat([data_frame_complementado, grupo_analisado])
    
    # Filtrar resultados específicos baseados nos valores do último nível de índice
    resultados_filtrados = data_frame_complementado.loc[data_frame_complementado.index.get_level_values(-1).isin(['Count', 'Expected Count', f'% within {data_frame_multi_nivel.index.names[-1]}'])]

    return resultados_filtrados if not resultados_filtrados.empty else data_frame_complementado

    
def avaliar_homogeneidade_odds_ratio(data_frame) -> None:
    """
    Avalia a homogeneidade das razões de chances (odds ratios) utilizando os testes de Breslow-Day e Tarone.
    
    Esta função recebe um DataFrame, esperando que tenha uma estrutura específica adequada para
    a análise de razões de chances e realiza os testes de Breslow-Day e Tarone para avaliar a 
    homogeneidade das razões de chances entre diferentes estratos.

    Parâmetros:
    - data_frame (pd.DataFrame): Um DataFrame contendo os dados para análise.

    Retorna:
    - Nada: Imprime os resultados dos testes de homogeneidade no console.
    """
    
    # Reformatando o DataFrame de entrada para um array 3D para análise
    dados_reshaped = data_frame.values.reshape((2, -1, 2)).transpose(1, 2, 0)
    
    # Criando uma instância de StratifiedTable para os dados reformatados
    tabela_estratificada = StratifiedTable(dados_reshaped)
    
    # Realizando o teste de Breslow-Day para homogeneidade de odds ratio
    resultado_breslow_day = tabela_estratificada.test_equal_odds(adjust=False)
    
    # Realizando o teste de Tarone para homogeneidade de odds ratio com ajuste
    resultado_tarone = tabela_estratificada.test_equal_odds(adjust=True)
    
    # Formatando e imprimindo os resultados
    print(f'\nTeste de Breslow-Day:'
          f'\nChi-Squared: {resultado_breslow_day.statistic:.4f}'
          f'\nAsymp. Sig. (2-sided): {resultado_breslow_day.pvalue:.4f}'
          f'\n\nTeste de Tarone:'
          f'\nChi-Squared: {resultado_tarone.statistic:.4f}'
          f'\nAsymp. Sig. (2-sided): {resultado_tarone.pvalue:.4f}')
    

def avaliar_independencia_condicional(data_frame) -> None:
    """
    Avalia a independência condicional entre dois fatores em diferentes estratos,
    utilizando o teste de Mantel-Haenszel, tanto com quanto sem correção de continuidade (CC).
    
    Esta função recebe um DataFrame que deve estar em uma estrutura específica adequada para a
    análise de independência condicional. Ela realiza o teste de Mantel-Haenszel para avaliar
    a associação entre os estratos, com e sem a aplicação da correção de continuidade. Além disso,
    calcula e imprime o intervalo de confiança para a razão de chances comum estimada.

    Parâmetros:
    - data_frame (pd.DataFrame): DataFrame contendo os dados para a análise.

    Retorna:
    - Nada: Imprime os resultados do teste de Mantel-Haenszel e o intervalo de confiança
            para a razão de chances comum estimada no console.
    """
    
    # Reformatando o DataFrame para um array 3D para análise
    dados_reshaped = data_frame.values.reshape((2, -1, 2)).transpose(1, 2, 0)
    
    # Instanciando StratifiedTable com os dados reformatados
    tabela_estratificada = StratifiedTable(dados_reshaped)

    # Calculando os valores esperados e a soma das diferenças entre observados e esperados
    observados = data_frame.values
    _, _, _, esperados = chi2_contingency(observados, correction=False)
    diferenca = observados - esperados
    soma_diferencas = np.sum(np.abs(diferenca))
    
    # Decisão sobre o uso da correção de continuidade
    usar_cc = soma_diferencas != 0
    
    # Decisão e execução do teste de Mantel-Haenszel
    print("Correção de continuidade será utilizada." if usar_cc else "Correção de continuidade não será utilizada.")
    resultado_mh = tabela_estratificada.test_null_odds(correction=usar_cc)
    
    # Cálculo da razão de chances comum estimada e seu intervalo de confiança
    razao_chances_estimada, (lcb, ucb) = tabela_estratificada.oddsratio_pooled, tabela_estratificada.oddsratio_pooled_confint(alpha=0.05)
    
    # Formatando e imprimindo os resultados
    print(f'\nTeste de Mantel-Haenszel:'
          f'\nQui-Quadrado: {resultado_mh.statistic:.3f}'
          f'\nSignificância Assintótica (bilateral): {resultado_mh.pvalue:.3f}'
          f'\n\nRazão de Chances Comum Estimada (Mantel-Haenszel):'
          f'\nEstimativa: {razao_chances_estimada:.3f}'
          f'\nIntervalo de Confiança (95%): [{lcb:.3f}, {ucb:.3f}]')
          
          
          
def avaliar_associacao_condicional(df, calcular_significancia=True, calcular_ic=True) -> None:
    """
    Avalia a associação condicional entre dois fatores em diferentes estratos usando o teste de Mantel-Haenszel.
    Esta função suporta a avaliação com e sem correção de continuidade (CC) e calcula o intervalo de confiança (IC)
    para a razão de chances comum estimada.
    
    Parâmetros:
    - df (pd.DataFrame): DataFrame contendo os dados para a análise, assumindo uma estrutura específica.
    - calcular_significancia (bool): Se True, realiza o teste de Mantel-Haenszel e imprime os resultados.
    - calcular_ic (bool): Se True, calcula e imprime o intervalo de confiança para a razão de chances comum.
    
    Retorna:
    - None: Os resultados são impressos diretamente no console.
    """
    
    # Reformatando o DataFrame para um array 3D para análise
    dados_reshaped = df.values.reshape((2, -1, 2)).transpose(1, 2, 0)
    
    # Instanciando StratifiedTable com os dados reformatados
    tabela_estratificada = StratifiedTable(dados_reshaped)
    
    if calcular_significancia:
        # Calculando e avaliando a necessidade de correção de continuidade
        observados = df.values
        _, _, _, esperados = chi2_contingency(observados, correction=False)
        diferenca = observados - esperados
        soma_diferencas = np.sum(np.abs(diferenca))
        usar_cc = soma_diferencas > 0  # Decisão sobre o uso da correção de continuidade baseado na soma das diferenças
        
        # Executando o teste de Mantel-Haenszel com ou sem correção de continuidade
        resultado_mh = tabela_estratificada.test_null_odds(correction=usar_cc)
        
        # Imprimindo os resultados do teste
        cc_msg = "com" if usar_cc else "sem"
        print(f"\nTeste de Mantel-Haenszel {cc_msg} correção de continuidade:"
              f"\nQui-Quadrado: {resultado_mh.statistic:.3f}"
              f"\nSignificância Assintótica (bilateral): {resultado_mh.pvalue:.3f}")
    
    if calcular_ic:
        # Calculando e imprimindo o intervalo de confiança para a razão de chances comum
        razao_chances_estimada, (lcb, ucb) = tabela_estratificada.oddsratio_pooled, tabela_estratificada.oddsratio_pooled_confint(alpha=0.05)
        print(f"\nRazão de Chances Comum Estimada (Mantel-Haenszel):"
              f"\nEstimativa: {razao_chances_estimada:.3f}"
              f"\nIntervalo de Confiança (95%): [{lcb:.3f}, {ucb:.3f}]")
          

def analisar_frequencias_esperadas_OLD(dataframe_multi_nivel):
    """
    Analisa as frequências esperadas em um DataFrame multi-índice para cada combinação de níveis de índice,
    excluindo o total geral. Imprime os resultados e uma nota de rodapé com informações sobre células com
    frequências esperadas abaixo de 5.

    :param dataframe_multi_nivel: DataFrame multi-índice contendo as frequências observadas e esperadas.
    """
    
    # Excluir o último nível de índice que corresponde aos totais gerais
    niveis_para_agrupar = list(range(dataframe_multi_nivel.index.nlevels - 1))
    
    for indices, subgrupo in dataframe_multi_nivel.groupby(level=niveis_para_agrupar):
        # Certificar que 'indices' é uma tupla para consistência
        indices = (indices,) if not isinstance(indices, tuple) else indices
        
        # A função 'Table' deve ser definida externamente para calcular as frequências esperadas
        subgrupo_analisado = subgrupo.droplevel(list(range(len(indices))))
        tabela_de_analise = Table(subgrupo_analisado)  # Substituir 'Table' pela função apropriada
        frequencias_esperadas = tabela_de_analise.fittedvalues
        
        
        # Identificar células com frequências esperadas menores que 5
        mascara_celulas_abaixo_5 = frequencias_esperadas < 5
        celulas_abaixo_5 = frequencias_esperadas[mascara_celulas_abaixo_5]
        
        # Calcular o número total de células analisadas
        total_de_celulas = frequencias_esperadas.size
        
        # Encontrar o valor mínimo entre as frequências esperadas
        frequencia_esperada_minima = frequencias_esperadas.min().min()
        
        # Calcular a porcentagem de células com frequências esperadas abaixo de 5
        porcentagem_celulas_abaixo_5 = (celulas_abaixo_5.count().sum() / total_de_celulas) * 100
        
        # Formatar a nota de rodapé com os resultados
        nota_de_rodape = (f"a. {celulas_abaixo_5.count().sum()} células ({porcentagem_celulas_abaixo_5:.2f}%) "
                          f"têm uma frequência esperada menor que 5. "
                          f"A frequência esperada mínima é {frequencia_esperada_minima:.2f}.")
        
        # Imprimir os resultados para cada subgrupo de índices
        print(f'\nAnálise para: {indices[0]}\n')
        print('\nFo:', subgrupo_analisado)
        print('\nFe:', frequencias_esperadas.round(1))
        print('\n', nota_de_rodape)
        print("-" * 100)  # Separador visual para cada análise

def analisar_frequencias_esperadas(dataframe_multi_nivel):
    """
    Analisa as frequências esperadas em um DataFrame multi-índice para cada combinação de níveis de índice,
    excluindo o total geral. Imprime os resultados e uma nota de rodapé com informações sobre células com
    frequências esperadas abaixo de 5.

    :param dataframe_multi_nivel: DataFrame multi-índice contendo as frequências observadas e esperadas.
    """
    
    # Excluir o último nível de índice que corresponde aos totais gerais
    niveis_para_agrupar = list(range(dataframe_multi_nivel.index.nlevels - 1))
    
    for indices, subgrupo in dataframe_multi_nivel.groupby(level=niveis_para_agrupar if len(niveis_para_agrupar) > 1 else niveis_para_agrupar[0]):
        # Certificar que 'indices' é uma tupla para consistência
        indices = (indices,) if not isinstance(indices, tuple) else indices
        
        # A função 'Table' deve ser definida externamente para calcular as frequências esperadas
        subgrupo_analisado = subgrupo.droplevel(list(range(len(indices))))
        tabela_de_analise = Table(subgrupo_analisado)  # Substituir 'Table' pela função apropriada
        frequencias_esperadas = tabela_de_analise.fittedvalues
        
        # Identificar células com frequências esperadas menores que 5
        mascara_celulas_abaixo_5 = frequencias_esperadas < 5
        celulas_abaixo_5 = frequencias_esperadas[mascara_celulas_abaixo_5]
        
        # Calcular o número total de células analisadas
        total_de_celulas = frequencias_esperadas.size
        
        # Encontrar o valor mínimo entre as frequências esperadas
        frequencia_esperada_minima = frequencias_esperadas.min().min()
        
        # Calcular a porcentagem de células com frequências esperadas abaixo de 5
        porcentagem_celulas_abaixo_5 = (celulas_abaixo_5.count().sum() / total_de_celulas) * 100
        
        # Formatar a nota de rodapé com os resultados
        nota_de_rodape = (f"a. {celulas_abaixo_5.count().sum()} células ({porcentagem_celulas_abaixo_5:.2f}%) "
                          f"têm uma frequência esperada menor que 5. "
                          f"A frequência esperada mínima é {frequencia_esperada_minima:.2f}.")
        
        # Preparar as tabelas para impressão usando tabulate
        tabela_observada = tabulate(subgrupo_analisado.reset_index(), headers='keys', tablefmt='grid')
        tabela_esperada = tabulate(frequencias_esperadas.round(1).reset_index(), headers='keys', tablefmt='grid')
        
        # Usar display e HTML para formatar a saída
        display(HTML(f'<h3>Análise para: {indices[0]}</h3>'))
        display(HTML(f'<h4>Fo:</h4><pre>{tabela_observada}</pre>'))
        display(HTML(f'<h4>Fe:</h4><pre>{tabela_esperada}</pre>'))
        display(HTML(f'<p>{nota_de_rodape}</p>'))
        display(HTML('<hr style="border: 1px solid black;">'))

        
def eliminacao_reversa_com_comparacao_llm_OLD(dataframe, display_models=True, compare_models=True):
    """
    Realiza a eliminação para trás em um conjunto de dados para modelagem estatística,
    ajustando um modelo saturado e então removendo preditores com base nos valores-p,
    até que todos os preditores restantes tenham valores-p abaixo de 0.05.
    Além disso, compara o modelo ajustado com o modelo saturado usando o critério AIC e o teste LRT.

    :param dataframe: DataFrame contendo os dados para modelagem. Assume-se que as últimas colunas
                      representam a variável resposta e as demais são preditores.
    :param display_models: Se True, exibe os sumários dos modelos saturado e ajustado.
    :param compare_models: Se True, realiza comparação entre modelos saturado e ajustado, exibindo AICs
                           e resultado do teste de razão de verossimilhança.
    :return: Tupla contendo o modelo saturado e o modelo ajustado.
    """

    # Supressão de avisos
    from statsmodels.tools.sm_exceptions import PerfectSeparationWarning
    warnings.filterwarnings("ignore", message="divide by zero encountered in scalar divide")
    warnings.filterwarnings("ignore", category=PerfectSeparationWarning)

    # Define preditores e variável resposta
    predictors = dataframe.columns[:-1].tolist()
    response_variable = dataframe.columns[-1]

    # Função para gerar todas as interações possíveis entre preditores
    def gerar_interacoes(predictors):
        return [':'.join(combo) for i in range(2, len(predictors) + 1)
                for combo in itertools.combinations(predictors, i)]

    # Construção do modelo saturado
    all_predictors = predictors + gerar_interacoes(predictors)
    saturated_model_formula = f"{response_variable} ~ {' + '.join(all_predictors)}"
    saturated_model = glm(formula=saturated_model_formula, data=dataframe, family=sm.families.Poisson()).fit()

    # Exibição inicial do modelo saturado, se solicitado
    if display_models:
        display(HTML("<h2>Modelo Saturado:</h2>"))
        display(HTML(saturated_model.summary().as_html()))

    # Início da eliminação para trás
    adjusted_predictors = all_predictors[:]
    step = 1
    while True:
        adjusted_model_formula = f"{response_variable} ~ {' + '.join(adjusted_predictors)}"
        adjusted_model = glm(formula=adjusted_model_formula, data=dataframe, family=sm.families.Poisson()).fit()

        p_values = adjusted_model.pvalues.iloc[1:]  # Exclui intercepto
        max_p_value = p_values.max()

        # Condição de parada
        if max_p_value <= 0.05:
            break

        # Remoção do preditor com o maior valor-p
        worst_predictor = p_values.idxmax().split('[')[0]  # Ajuste para variáveis categóricas
        adjusted_predictors.remove(worst_predictor)
        if display_models:
            display(HTML(f"<p>Passo {step}: Removendo {worst_predictor} com p-valor {max_p_value:.3f}</p>"))
        step += 1

    # Exibição do modelo ajustado, se solicitado
    if display_models:
        display(HTML("<h2>Modelo Ajustado:</h2>"))
        display(HTML(adjusted_model.summary().as_html()))

    # Comparação entre modelos, se solicitado
    if compare_models:
        display(HTML("<h2>Comparação entre Modelos Saturado e Ajustado:</h2>"))
        display(HTML(f"<p>AIC Modelo Saturado: {saturated_model.aic:.2f}</p>"))
        display(HTML(f"<p>AIC Modelo Ajustado: {adjusted_model.aic:.2f}</p>"))

        # Teste de Razão de Verossimilhança (LRT)
        lr_stat = 2 * (saturated_model.llf - adjusted_model.llf)
        diff_num_params = len(saturated_model.params) - len(adjusted_model.params)
        p_value = chi2.sf(lr_stat, df=diff_num_params)

        display(HTML("<h2>Teste de Razão de Verossimilhança (LRT):</h2>"))
        display(HTML(f"<p>LR stat: {lr_stat:.3f}, Diferença no Número de Parâmetros: {diff_num_params}, p-value: {p_value:.3f}</p>"))

    return saturated_model, adjusted_model

def eliminacao_reversa_com_comparacao_llm(dataframe, display_models=True, compare_models=True, max_interaction_order=None, max_p_value=0.05):
    """
    Realiza a eliminação para trás em um conjunto de dados para modelagem estatística,
    ajustando um modelo saturado e então removendo preditores com base nos valores-p,
    até que todos os preditores restantes tenham valores-p abaixo de 0.05.
    Além disso, compara o modelo ajustado com o modelo saturado usando o critério AIC e o teste LRT.
    
    :param dataframe: DataFrame contendo os dados para modelagem. Assume-se que as últimas colunas
                      representam a variável resposta e as demais são preditores.
    :param display_models: Se True, exibe os sumários dos modelos saturado e ajustado.
    :param compare_models: Se True, realiza comparação entre modelos saturado e ajustado, exibindo AICs
                           e resultado do teste de razão de verossimilhança.
    :param max_interaction_order: Limite máximo para a ordem das interações a serem incluídas no modelo ajustado.
                                  Se None, não há restrição.
    :param max_p_value: Valor máximo de p para a eliminação de preditores.
    :return: Tupla contendo o modelo saturado e o modelo ajustado.
    """
    
    # Supressão de avisos
    from statsmodels.tools.sm_exceptions import PerfectSeparationWarning
    import warnings
    warnings.filterwarnings("ignore", message="divide by zero encountered in scalar divide")
    warnings.filterwarnings("ignore", category=PerfectSeparationWarning)

    import itertools
    import statsmodels.api as sm
    from statsmodels.formula.api import glm
    from scipy.stats import chi2
    from IPython.display import display, HTML

    # Define preditores e variável resposta
    predictors = dataframe.columns[:-1].tolist()
    response_variable = dataframe.columns[-1]

    # Função para gerar todas as interações possíveis entre preditores
    def gerar_interacoes(predictors, max_order):
        interactions = []
        for i in range(2, len(predictors) + 1):
            if max_order is not None and i > max_order:
                break
            interactions.extend([':'.join(combo) for combo in itertools.combinations(predictors, i)])
        return interactions

    # Construção do modelo saturado
    all_predictors = predictors + gerar_interacoes(predictors, None)
    saturated_model_formula = f"{response_variable} ~ {' + '.join(all_predictors)}"
    saturated_model = glm(formula=saturated_model_formula, data=dataframe, family=sm.families.Poisson()).fit()

    # Exibição inicial do modelo saturado, se solicitado
    if display_models:
        display(HTML("<h2>Modelo Saturado:</h2>"))
        display(HTML(saturated_model.summary().as_html()))

    # Início da eliminação para trás
    adjusted_predictors = predictors + gerar_interacoes(predictors, max_interaction_order)
    step = 1
    while True:
        adjusted_model_formula = f"{response_variable} ~ {' + '.join(adjusted_predictors)}"
        adjusted_model = glm(formula=adjusted_model_formula, data=dataframe, family=sm.families.Poisson()).fit()

        p_values = adjusted_model.pvalues.iloc[1:]  # Exclui intercepto
        p_value = p_values.max()

        # Condição de parada
        if p_value <= max_p_value:
            break

        # Remoção do preditor com o maior valor-p
        worst_predictor = p_values.idxmax().split('[')[0]  # Ajuste para variáveis categóricas
        adjusted_predictors.remove(worst_predictor)
        if display_models:
            display(HTML(f"<p>Passo {step}: Removendo {worst_predictor} com p-valor {p_value:.3f}</p>"))
        step += 1

    # Exibição do modelo ajustado, se solicitado
    if display_models:
        display(HTML("<h2>Modelo Ajustado:</h2>"))
        display(HTML(adjusted_model.summary().as_html()))

    # Comparação entre modelos, se solicitado
    if compare_models:
        display(HTML("<h2>Comparação entre Modelos Saturado e Ajustado:</h2>"))
        display(HTML(f"<p>AIC Modelo Saturado: {saturated_model.aic:.2f}</p>"))
        display(HTML(f"<p>AIC Modelo Ajustado: {adjusted_model.aic:.2f}</p>"))

        # Teste de Razão de Verossimilhança (LRT)
        lr_stat = 2 * (saturated_model.llf - adjusted_model.llf)
        diff_num_params = len(saturated_model.params) - len(adjusted_model.params)
        p_value = chi2.sf(lr_stat, df=diff_num_params)

        display(HTML("<h2>Teste de Razão de Verossimilhança (LRT):</h2>"))
        display(HTML(f"<p>LR stat: {lr_stat:.3f}, Diferença no Número de Parâmetros: {diff_num_params}, p-value: {p_value:.3f}</p>"))

    return saturated_model, adjusted_model

def calcular_e_exibir_odds_ratios_llm_OLD(model):
    """
    Calcula e exibe os Odds Ratios (ORs) e Intervalos de Confiança (ICs) de 95%
    para os coeficientes de um modelo estatístico.

    :param model: O modelo estatístico ajustado do qual os ORs e ICs serão calculados.
                  Espera-se que seja um modelo do tipo que tem métodos .params e .conf_int().
    """
    import numpy as np

    # Calcula os Odds Ratios (ORs) e os Intervalos de Confiança (ICs) de 95%
    odds_ratios = np.exp(model.params)
    confidence_intervals = np.exp(model.conf_int())

    # Início da apresentação formatada dos resultados
    print("\nOdds Ratios (ORs) e Intervalos de Confiança (ICs) de 95%: \n")
    print('-' * 80)
    
    # Iteração sobre cada variável para exibir seus ORs e ICs
    for var in odds_ratios.index:
        OR = odds_ratios[var]
        CI_lower, CI_upper = confidence_intervals.loc[var]
        print(f"{var}: OR={OR:.3f}, IC 95%=({CI_lower:.3f}, {CI_upper:.3f})")
        print('-' * 80)  # Linha separadora para melhor visualização

def calcular_e_exibir_odds_ratios_llm(model):
    """
    Calcula e exibe os Odds Ratios (ORs) e Intervalos de Confiança (ICs) de 95%
    para os coeficientes de um modelo estatístico.

    :param model: O modelo estatístico ajustado do qual os ORs e ICs serão calculados.
                  Espera-se que seja um modelo do tipo que tem métodos .params e .conf_int().
    """
    
    # Calcula os Odds Ratios (ORs) e os Intervalos de Confiança (ICs) de 95%
    odds_ratios = np.exp(model.params)
    confidence_intervals = np.exp(model.conf_int())

    # Cria uma lista de resultados para tabular
    resultados = []
    for var in odds_ratios.index:
        OR = odds_ratios[var]
        CI_lower, CI_upper = confidence_intervals.loc[var]
        resultados.append([var, f"{OR:.3f}", f"({CI_lower:.3f}, {CI_upper:.3f})"])
    
    # Exibe os resultados formatados como tabela usando tabulate
    print(tabulate(resultados, headers=["", "OR", "IC 95%"], tablefmt="grid"))
        
def criar_tabela_contingencia_expandida_llm_OLD(dados_df, grupos, categorias, model):
    """
    Cria uma tabela de contingência expandida para análise estatística, incorporando as frequências
    observadas (Freq), as esperadas (expected) e os resíduos (residuals), com base nos grupos e categorias especificados.
    Os índices e colunas são renomeados para refletir as categorias fornecidas para uma interpretação mais intuitiva dos resultados.
    
    Parâmetros:
    - dados_df: DataFrame contendo os dados para análise.
    - grupos: Lista contendo os nomes das colunas que representam os grupos para agrupamento.
    - categorias: Dicionário com as colunas dos grupos como chaves e listas com nomes de categorias como valores para renomeação.
    - model: Modelo para estimativa das frequências esperadas.
    
    Retorna:
    - tabela_final: DataFrame com a tabela de contingência expandida, incluindo as colunas Freq, expected e residuals.
    """

    # Calculando as frequências esperadas e resíduos
    dados_df['expected'] = model.predict(dados_df)
    dados_df['residuals'] = dados_df['Freq'] - dados_df['expected']
    dados_df['expected'] = dados_df['expected'].round(2)
    dados_df['residuals'] = dados_df['residuals'].round(2)

    tabelas = []
    valores = ['Freq', 'expected', 'residuals']

    for valor in valores:
        tabela_contingencia = pd.crosstab(
            index=[dados_df[grupo] for grupo in grupos[:-1]],
            columns=dados_df[grupos[-1]],
            values=dados_df[valor],
            aggfunc=np.sum,
            dropna=False
        ).rename_axis(columns=None)

        tabelas.append(tabela_contingencia)

    # Combinando as tabelas de Freq, expected e residuals
    tabela_final = pd.concat(tabelas, keys=valores, axis=1)

    # Atualizando os níveis de índices
    for i, grupo in enumerate(grupos[:-1]):
        new_index = tabela_final.index.levels[i].map(lambda x: categorias[grupo][x-1])
        tabela_final.index = tabela_final.index.set_levels(new_index, level=i)
    
    # Ajustando os nomes das categorias 'Feridos' diretamente sem acessar níveis inexistentes
    new_columns = [(valor, categorias[grupos[-1]][int(col)-1]) for valor in valores for col in tabela_final.columns.get_level_values(1).unique()]
    tabela_final.columns = pd.MultiIndex.from_tuples(new_columns, names=[None, grupos[-1]])

    tabela_final.columns = pd.MultiIndex.from_tuples([('observed' if col[0] == 'Freq' else col[0], col[1]) for col in tabela_final.columns])

    return tabela_final
    

def criar_tabela_contingencia_expandida_llm(data_df, grupos, categorias, modelo):
    
    """
    Cria uma tabela de contingência expandida para análise estatística, incorporando frequências observadas (Freq), frequências esperadas (esperado),
    resíduos comuns (residuos_comuns), resíduos padronizados (residuos_padronizados) e resíduos padronizados ajustados (residuos_ajustados) com base nos grupos e categorias especificados.
    Índices e colunas são renomeados para refletir as categorias fornecidas para uma interpretação mais intuitiva dos resultados.
    
    Parâmetros:
    - data_df: DataFrame contendo os dados para análise.
    - grupos: Lista contendo os nomes das colunas que representam os grupos para agrupamento.
    - categorias: Dicionário com colunas de grupo como chaves e listas com nomes de categorias como valores para renomeação.
    - modelo: Modelo para estimar frequências esperadas.
    
    Retorna:
    - tabela_final: DataFrame com a tabela de contingência expandida, incluindo as colunas Freq, esperado, residuos_comuns, residuos_padronizados e residuos_ajustados.
    """
    
    def rename_multiindex(df, grupos, categorias):
        for grupo in grupos:
            if grupo in df.index.names:
                level = df.index.names.index(grupo)
                df.index = df.index.set_levels(categorias[grupo], level=level)
        return df

    data_df = data_df.copy(deep=True)

    # Calculando frequências esperadas
    data_df['esperado'] = modelo.predict(data_df)
    
    # Calculando resíduos comuns
    data_df['residuos_comuns'] = data_df['Freq'] - data_df['esperado']
    
    # Calculando resíduos padronizados
    data_df['residuos_padronizados'] = data_df['residuos_comuns'] / np.sqrt(data_df['esperado'])
    
    # Ajustando resíduos padronizados
    n = data_df.shape[0]
    k = len(grupos)
    data_df['residuos_ajustados'] = data_df['residuos_padronizados'] / np.sqrt((n - 1) / (n - k))

    data_df['esperado'] = data_df['esperado'].round(2)
    data_df['residuos_comuns'] = data_df['residuos_comuns'].round(2)
    data_df['residuos_padronizados'] = data_df['residuos_padronizados'].round(2)
    data_df['residuos_ajustados'] = data_df['residuos_ajustados'].round(2)

    tabelas = []
    valores = ['Freq', 'esperado', 'residuos_comuns', 'residuos_padronizados', 'residuos_ajustados']

    for valor in valores:
        tabela_contingencia = pd.crosstab(
            index=[data_df[grupo] for grupo in grupos[:-1]],
            columns=data_df[grupos[-1]],
            values=data_df[valor],
            aggfunc="sum",
            dropna=False
        ).rename_axis(columns=None)

        tabelas.append(tabela_contingencia)

    # Combinando as tabelas de Freq, esperado, residuos_comuns, residuos_padronizados e residuos_ajustados
    tabela_final = pd.concat(tabelas, keys=valores, axis=1, names=[None, grupos[-1]])
    
    tabela_final = rename_multiindex(tabela_final, grupos, categorias)

    # Renomear as colunas conforme os valores e as categorias
    new_columns = []
    unique_cols = tabela_final.columns.get_level_values(1).unique()  # Obtem os valores únicos do segundo nível de índice

    for valor in valores:
        for idx, col in enumerate(unique_cols):
            categoria = categorias[grupos[-1]][idx]  # Acesso correto ao índice baseado na ordem dos elementos únicos
            new_columns.append((valor, categoria))

    tabela_final.columns = pd.MultiIndex.from_tuples(new_columns, names=[None, grupos[-1]])

    tabela_final.columns = tabela_final.columns.set_levels(['observado' if x == 'Freq' else x for x in tabela_final.columns.levels[0]], level=0)    

    return tabela_final

    
def plot_stacked_bar_chart_OLD(df, show_table=False):
    """
    Plots a stacked bar chart for the percentage distribution within categories in a multi-index DataFrame.
    
    Args:
    df (pd.DataFrame): Multi-index DataFrame with percentage data.
    """
    # Encontrar todas as subcategorias únicas, excluindo 'Total'
    y_categories = [col for col in df.columns.get_level_values(0).unique().to_list() if 'Total' not in col]
    
    # Extrair categorias únicas do índice, excluindo 'Total'
    x_categories = df.index.get_level_values(0).unique().to_list()

    # Encontrar o índice do elemento 'Total' na lista
    index_total = x_categories.index('Total')
    
    # Preparando o DataFrame para compilar as diferenças percentuais
    rows_percentages = pd.DataFrame(index=x_categories)

    for y_category in y_categories:
        # Extrair as porcentagens e converter para float
        row_percentage = df.loc[(slice(None), f'% within {df.index.names[0]}'), y_category].droplevel(1)
        rows_percentages[y_category] = row_percentage.astype(float)

    # Renomeando 'Total' para 'Média' no índice do DataFrame
    rows_percentages.rename(index={'Total': 'Mass'}, inplace=True)

    # Plotar o gráfico de barras empilhadas
    ax = rows_percentages.plot(kind='barh', stacked=True, colormap='coolwarm', figsize=(10, 7))

    # Inverter a ordem das categorias no eixo y
    ax.invert_yaxis()

    # Configurar os rótulos do eixo x e títulos
    plt.xlabel('Porcentagem [%]')
    plt.ylabel(f'{df.index.names[0]}')
    plt.title(f'Perfil de {df.index.names[0]} com {df.columns.name}')

    # Mover a legenda para fora do gráfico
    plt.legend(title=df.columns.name, bbox_to_anchor=(1.05, 1), loc='upper left')

    # Mostrar o gráfico
    plt.tight_layout()
    plt.show()

    if show_table:
        display(rows_percentages/100)

def plot_stacked_bar_chart(df, show_table=False):
    """
    Plots a stacked bar chart for the percentage distribution within categories in a multi-index DataFrame using Plotly.
    
    Args:
    df (pd.DataFrame): Multi-index DataFrame with percentage data.
    """
    # Encontrar todas as subcategorias únicas, excluindo 'Total'
    y_categories = [col for col in df.columns.get_level_values(0).unique().to_list() if 'Total' not in col]
    
    # Extrair categorias únicas do índice, excluindo 'Total'
    x_categories = df.index.get_level_values(0).unique().to_list()

    # Preparando o DataFrame para compilar as diferenças percentuais
    rows_percentages = pd.DataFrame(index=x_categories)

    for y_category in y_categories:
        # Extrair as porcentagens e converter para float
        row_percentage = df.loc[(slice(None), f'% within {df.index.names[0]}'), y_category].droplevel(1)
        rows_percentages[y_category] = row_percentage.astype(float)

    # Renomeando 'Total' para 'Mass' no índice do DataFrame
    rows_percentages.rename(index={'Total': 'Mass'}, inplace=True)
    rows_percentages.reset_index(inplace=True)
    rows_percentages_melted = rows_percentages.melt(id_vars=rows_percentages.columns[0], var_name='Pão', value_name='Porcentagem')

    # Plotar o gráfico de barras empilhadas usando Plotly
    fig = px.bar(rows_percentages_melted, 
                 x='Porcentagem', 
                 y=rows_percentages.columns[0], 
                 color='Pão', 
                 orientation='h',
                 title=f'Perfil de {df.index.names[0]} com {df.columns.name}',
                 labels={'Porcentagem': 'Porcentagem [%]', rows_percentages.columns[0]: df.index.names[0]})
    
    # Inverter a ordem das categorias no eixo y
    fig.update_layout(yaxis=dict(autorange="reversed"))
    fig.show()

    if show_table:
        display(rows_percentages)

        
def realizar_analise_correspondencia(df):
    """
    Realiza a Análise de Correspondência (CA) em um DataFrame de entrada e retorna
    um DataFrame formatado com os resultados, incluindo valor singular, inércia,
    chi quadrado, significância (p-valor) e proporções de inércia explicada.

    Args:
    df (pd.DataFrame): DataFrame contendo os dados de entrada para a análise.

    Returns:
    None: Exibe o DataFrame formatado sem retornar um objeto.
    """
    
    # Inicializar e ajustar o modelo de Análise de Correspondência com a biblioteca Prince
    ca = prince.CA(
        n_components=20,  # número máximo de componentes para extrair
        n_iter=10,         # número de iterações para a otimização
        copy=True,         # copiar os dados para preservar o original
        check_input=True,  # verificar a entrada para consistência
        engine='sklearn',  # usar a engine sklearn para cálculos internos
        random_state=42    # garantir reproducibilidade
    )
    ca.fit(df)

    # Calcular o total de observações no DataFrame
    total_observations = df.to_numpy().sum()

    # Calcular o qui-quadrado total com base na inércia total e no total de observações
    total_chi2 = ca.total_inertia_ * total_observations

    # Determinar os graus de liberdade como (número de linhas - 1) * (número de colunas - 1)
    n_rows, n_cols = df.shape
    degrees_of_freedom = (n_rows - 1) * (n_cols - 1)

    # Calcular o p-valor a partir da distribuição chi-quadrado
    p_value = chi2.sf(total_chi2, degrees_of_freedom)

    # Calcular a proporção da inércia para cada dimensão e a soma cumulativa
    eigenvalues = ca.eigenvalues_
    proportion_of_inertia = eigenvalues / ca.total_inertia_
    cumulative_inertia = proportion_of_inertia.cumsum()

    # Criar um DataFrame para exibir os resultados
    results = pd.DataFrame({
        'Dimension': range(1, len(eigenvalues) + 1),
        'Singular Value': ca.svd_.s,
        'Inertia': eigenvalues,
        'Chi Square': "", 
        'Sig.': "", 
        'Proportion of Inertia ': proportion_of_inertia,
        'Proportion of Inertia Cumulative': cumulative_inertia
    })

    # Adicionar uma linha de totais ao DataFrame
    total_row = pd.DataFrame({
        'Dimension': ['Total'],
        'Singular Value': "",
        'Inertia': [sum(eigenvalues)],
        'Chi Square': [total_chi2],
        'Sig.': [p_value],
        'Proportion of Inertia ': "", # [sum(proportion_of_inertia)]
        'Proportion of Inertia Cumulative': "" # [cumulative_inertia[-1]]
    })

    # Concatenar a linha de total ao DataFrame de resultados
    results = pd.concat([results, total_row], ignore_index=True)

    # Formatar o DataFrame para melhor visualização
    results_formated = results.copy(deep=True)
    results_formated = results.map(lambda x: '{:.3f}'.format(x) if isinstance(x, (float)) else x)   

    # Esconder o índice ao exibir
    display(results_formated.style.hide(axis='index'))
    
    
def detalhar_resultados_analise_correspondencia(df, n_components=2, focus='row', df_supplement=None):
    """
    Realiza a Análise de Correspondência em uma tabela de contingência com resultados detalhados.

    Parâmetros:
        df (pd.DataFrame): DataFrame da tabela de contingência.
        n_components (int): Número de dimensões para a análise, até um máximo de 20.
    
    Retorna:
        pd.DataFrame: DataFrame com os resultados da análise incluindo massas, scores por dimensão,
                      inércia, e contribuições de cada ponto para as dimensões especificadas.
    """
    # Inicializando o objeto Análise de Correspondência com a biblioteca prince
    ca = prince.CA(
        n_components=max(n_components, 20),
        n_iter=10,  # Número de iterações para otimização
        copy=True,
        check_input=True,
        engine='sklearn',  # Utilizar engine sklearn para cálculos
        random_state=42
    )
    
    # Ajustando o modelo ao DataFrame
    ca.fit(df)

    # Escolhendo entre linhas ou colunas para a análise
    if focus == 'row':
        masses = ca.row_masses_
        coordinates = ca.row_coordinates(df)
        point_contribution_dim = ca.row_contributions_
    elif focus == 'column':
        masses = ca.col_masses_
        coordinates = ca.column_coordinates(df)
        point_contribution_dim = ca.column_contributions_
    else:
        raise ValueError("Focus must be 'row' or 'column'")

    # Inércia total de cada ponto
    point_inertia = (coordinates**2).mul(masses, axis=0).sum(axis=1)

    # Preparando o DataFrame final com os resultados
    results_dict = {
        'Mass': masses,
    }
    
    # Adicionando colunas de score, contribuição e contribuição total para cada dimensão
    for dim in range(n_components):
        results_dict[f'Score in Dimension {dim+1}'] = coordinates.iloc[:, dim]

    results_dict['Inertia'] = point_inertia
        
    dimension_contribution = (coordinates**2).mul(masses, axis=0).div(point_inertia, axis=0)
    
    for dim in range(n_components):
        results_dict[f'Contribution of Point to Inertia of Dimension {dim+1}'] = point_contribution_dim.iloc[:, dim]

    for dim in range(n_components):
        results_dict[f'Contribution of Dimension {dim+1} to Inertia of Point'] = dimension_contribution.iloc[:, dim]
    
    # Total contribution to inertia (for the first n_components dimensions)
    total_contribution = 0
    for dim in range(n_components):
        total_contribution += dimension_contribution.iloc[:, dim]
    results_dict['Total Contribution to Inertia'] = total_contribution

    final_df = pd.DataFrame(results_dict).round(3)

    # Processamento para dados suplementares
    if df_supplement is not None and focus=='row':
        supplement_coordinates = ca.row_coordinates(df_supplement)
        ca.fit(df_supplement)
        supplement_masses = ca.row_masses_
        supplement_point_inertia = (supplement_coordinates**2).mul(supplement_masses, axis=0).sum(axis=1)
        
        supplement_dict = {
                'Mass': supplement_masses,
                'Inertia': supplement_point_inertia
        }
    
        for dim in range(n_components):
            supplement_dict[f'Score in Dimension {dim+1}'] = supplement_coordinates.iloc[:, dim]
    
        supplement_dimension_contribution = (supplement_coordinates**2).mul(supplement_masses, axis=0).div(supplement_point_inertia, axis=0)
    
        for dim in range(n_components):
            supplement_dict[f'Contribution of Point to Inertia of Dimension {dim+1}'] = ""
            supplement_dict[f'Contribution of Dimension {dim+1} to Inertia of Point'] = supplement_dimension_contribution.iloc[:, dim]
        
        # Total contribution to inertia (for the first n_components dimensions)
        total_contribution = 0
        for dim in range(n_components):
            total_contribution += supplement_dimension_contribution.iloc[:, dim]
        supplement_dict['Total Contribution to Inertia'] = total_contribution

        supplement_df = pd.DataFrame(supplement_dict)

        final_df = pd.concat([final_df, supplement_df], axis=0)

    # Formatação do DataFrame
    resultados_df_formated = final_df.map(lambda x: '{:.3f}'.format(x) if isinstance(x, (int, float)) else x)
        
    return resultados_df_formated
    
def analise_correspondencia_e_grafico(tabela_contingencia,  x_component=0, y_component=1, tabela_contingencia_suple=None):
    """
    Realiza a Análise de Correspondência usando a biblioteca prince e gera um gráfico dos resultados.

    Parâmetros:
        tabela_contingencia (pd.DataFrame): DataFrame principal da tabela de contingência.
        tabela_contingencia_suple (pd.DataFrame): DataFrame opcional da tabela de contingência suplementar.

    Retorna:
        Nada, apenas exibe o gráfico.
    """
    # Inicializando o objeto Análise de Correspondência com a biblioteca prince
    ca = prince.CA(
        n_components=20,  # Número máximo de dimensões para a análise
        n_iter=10,  # Número de iterações para otimização
        copy=True,
        check_input=True,
        engine='sklearn',  # Utilizar engine sklearn para cálculos
        random_state=42
    )

    # Ajustando o modelo ao DataFrame principal
    ca.fit(tabela_contingencia)

    # Verificar se o DataFrame suplementar é fornecido e combiná-lo com o principal
    if tabela_contingencia_suple is not None:
        tabela_combinada = pd.concat([tabela_contingencia, tabela_contingencia_suple], axis=0)
    else:
        tabela_combinada = tabela_contingencia

    # Gerando o gráfico
    chart = ca.plot(
        tabela_combinada,
        x_component=x_component,  # Primeira dimensão para o eixo X
        y_component=y_component,  # Segunda dimensão para o eixo Y
        show_row_markers=True,
        show_column_markers=True,
        show_row_labels=True,
        show_column_labels=True
    ).properties(
        width=720,  # Largura desejada do gráfico em pixels
        height=480  # Altura desejada do gráfico em pixels
    )

    # Exibe o gráfico com o novo tamanho
    #chart.display()
    
    # Criando as linhas de cruzamento manualmente
    x_rule = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(color='black').encode(
        x=alt.X('x', scale=alt.Scale(zero=False))
    )

    y_rule = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='black').encode(
        y=alt.Y('y', scale=alt.Scale(zero=False))
    )

    # Exibindo as linhas de cruzamento
    final_chart = chart + x_rule + y_rule

    # Exibindo o gráfico final
    final_chart.display()
    

def perfil_variaveis(df, meta, variaveis):
    # Criando uma lista para armazenar os dados da análise
    analise = []

    # Iterando sobre as variáveis selecionadas
    for var in variaveis:
        # Verificando se a variável está no DataFrame
        if var in df.columns:
            # Obtendo as categorias e os valores correspondentes da variável
            categorias = meta.variable_value_labels.get(var, {})
            valores_contagem = df[var].value_counts(dropna=False)
            total = len(df)
            
            # Iterando sobre as categorias e contagens
            for valor, contagem in valores_contagem.items():
                # Obtendo o rótulo da categoria
                rotulo_categoria = categorias.get(valor, 'Sem rótulo')
                # Calculando a porcentagem
                porcentagem = (contagem / total) * 100
                # Adicionando os resultados na lista de análise
                analise.append({
                    'Variable': var,
                    'Category': rotulo_categoria,
                    'Quantity': contagem,
                    'Percentage (%)': round(porcentagem, 2)
                })
    
    # Convertendo a lista de análise em DataFrame
    analise_df = pd.DataFrame(analise)
    
    return analise_df


def realizar_analise_correspondencia_multipla(variaveis_ativas, variaveis_suplementares=None, n_components=3):
    """
    Realiza a Análise de Correspondência Múltipla (MCA) em variáveis ativas e suplementares.
    Retorna um DataFrame formatado com os resultados.

    Args:
    variaveis_ativas (pd.DataFrame): DataFrame contendo as variáveis ativas.
    variaveis_suplementares (pd.DataFrame): DataFrame contendo as variáveis suplementares.
    n_components (int): Número de dimensões para a análise.

    Returns:
    None: Exibe o DataFrame formatado utilizando tabulate.
    """
    # Combinar variáveis ativas e suplementares
    if variaveis_suplementares is not None:
        data = pd.concat([variaveis_ativas, variaveis_suplementares], axis=1)
    else:
        data = variaveis_ativas.copy()
    data_encoded = pd.get_dummies(data)

    # Selecionar colunas correspondentes às variáveis ativas
    active_encoded_columns = pd.get_dummies(variaveis_ativas).columns

    # Inicializar e ajustar o modelo MCA nas variáveis ativas
    mca = prince.MCA(
        n_components=n_components,
        n_iter=10,
        copy=True,
        check_input=True,
        engine='sklearn',
        random_state=42
    )
    
    mca.fit(data_encoded[active_encoded_columns])

    # Calcular métricas gerais
    total_observations = data_encoded[active_encoded_columns].to_numpy().sum()
    total_chi2 = mca.total_inertia_ * total_observations
    n_rows, n_cols = data_encoded[active_encoded_columns].shape
    n_cols_encoded = len(active_encoded_columns) # Número de colunas após o one-hot encoding
    degrees_of_freedom = (n_rows - 1) * (n_cols_encoded - 1)
    p_value = chi2.sf(total_chi2, degrees_of_freedom)

    # Calcular inércia por dimensão
    eigenvalues = mca.eigenvalues_
    singular_values = mca.svd_.s
    total_inertia = sum(eigenvalues)
    proportion_of_inertia = eigenvalues / total_inertia
    cumulative_inertia = proportion_of_inertia.cumsum()

    # Criar um DataFrame com os resultados
    results = pd.DataFrame({
        'Dimension': range(1, len(eigenvalues) + 1),
        'Singular Value': singular_values,
        'Inertia': eigenvalues,
        'Chi Square': '',
        'Sig.': '',
        'Proportion of Inertia': proportion_of_inertia,
        'Cumulative Proportion': cumulative_inertia
    })
    total_row = pd.DataFrame({
        'Dimension': ['Total'],
        'Singular Value': [''],
        'Inertia': [total_inertia],
        'Chi Square': [total_chi2],
        'Sig.': [p_value],
        'Proportion of Inertia': [''],
        'Cumulative Proportion': ['']
    })
    results = pd.concat([results, total_row], ignore_index=True)
    
    # Formatar os números para três casas decimais
    results = results.map(lambda x: f"{x:.3f}" if isinstance(x, (float, int)) and not isinstance(x, int) else x)

    # Utilizar tabulate para exibir os resultados
    print(tabulate(results, headers='keys', tablefmt='grid', showindex=False))


def detalhar_resultados_analise_correspondencia_multipla(variaveis_ativas, variaveis_suplementares=None, n_components=2, focus='row'):
    """
    Realiza a Análise de Correspondência Múltipla e retorna resultados detalhados.

    Args:
    variaveis_ativas (pd.DataFrame): DataFrame contendo as variáveis ativas.
    variaveis_suplementares (pd.DataFrame): DataFrame contendo as variáveis suplementares.
    n_components (int): Número de dimensões para a análise.
    focus (str): 'row' para análise nas linhas ou 'column' para colunas.

    Returns:
    None: Exibe o DataFrame formatado utilizando tabulate.
    """
    if variaveis_suplementares is not None:
        data = pd.concat([variaveis_ativas, variaveis_suplementares], axis=1)
    else:
        data = variaveis_ativas.copy()
    data_encoded = pd.get_dummies(data)

    active_encoded_columns = pd.get_dummies(variaveis_ativas).columns

    mca = prince.MCA(
        n_components=max(n_components, 20),
        n_iter=10,
        copy=True,
        check_input=True,
        engine='sklearn',
        random_state=42
    )
    mca.fit(data_encoded[active_encoded_columns])

    if focus == 'row':
        masses = mca.row_masses_
        coordinates = mca.row_coordinates(data_encoded[active_encoded_columns])
        point_contribution_dim = mca.row_contributions_
    elif focus == 'column':
        masses = mca.col_masses_
        coordinates = mca.column_coordinates(data_encoded[active_encoded_columns])
        point_contribution_dim = mca.column_contributions_
    else:
        raise ValueError("Focus must be 'row' or 'column'")

    point_inertia = (coordinates**2).mul(masses, axis=0).sum(axis=1)

    results_dict = {'Mass': masses}
    for dim in range(n_components):
        results_dict[f'Score Dim {dim+1}'] = coordinates.iloc[:, dim]

    results_dict['Inertia'] = point_inertia

    dimension_contribution = (coordinates**2).mul(masses, axis=0).div(point_inertia, axis=0)

    for dim in range(n_components):
        results_dict[f'Contr. to Dim {dim+1}'] = point_contribution_dim.iloc[:, dim]

    for dim in range(n_components):
        results_dict[f'Contr. of Dim {dim+1}'] = dimension_contribution.iloc[:, dim]

    total_contribution = dimension_contribution.iloc[:, :n_components].sum(axis=1)
    results_dict['Total Contr.'] = total_contribution

    final_df = pd.DataFrame(results_dict).round(3)

    # Exibir resultados detalhados com tabulate
    print(tabulate(final_df, headers='keys', tablefmt='grid'))


def analise_correspondencia_multipla_e_grafico(variaveis_ativas, variaveis_suplementares=None, n_components=2, x_component=0, y_component=1):
    """
    Realiza a Análise de Correspondência Múltipla e gera um gráfico dos resultados.

    Args:
    variaveis_ativas (pd.DataFrame): DataFrame com variáveis ativas.
    variaveis_suplementares (pd.DataFrame): DataFrame com variáveis suplementares.
    x_component (int): Componente para o eixo X.
    y_component (int): Componente para o eixo Y.
    n_components (int): Número de dimensões para a análise.

    Returns:
    None: Exibe o gráfico.
    """
    if variaveis_suplementares is not None:
        data = pd.concat([variaveis_ativas, variaveis_suplementares], axis=1)
    else:
        data = variaveis_ativas.copy()
    data_encoded = pd.get_dummies(data)

    active_encoded_columns = pd.get_dummies(variaveis_ativas).columns

    mca = prince.MCA(
        n_components=n_components,
        n_iter=10,
        copy=True,
        check_input=True,
        engine='sklearn',
        random_state=42
    )
    mca.fit(data_encoded[active_encoded_columns])

    row_coords = mca.row_coordinates(data_encoded[active_encoded_columns])
    row_coords['Type'] = 'Row'
    row_coords['Label'] = variaveis_ativas.index.astype(str)

    column_coords = mca.column_coordinates(data_encoded[active_encoded_columns])
    column_coords['Type'] = 'Active Variable'
    column_coords['Label'] = column_coords.index

    if variaveis_suplementares is not None:
        supplementary_encoded_columns = pd.get_dummies(variaveis_suplementares).columns
        supplement_coords = mca.column_coordinates(data_encoded[supplementary_encoded_columns])
        supplement_coords['Type'] = 'Supplementary Variable'
        supplement_coords['Label'] = supplement_coords.index
        column_coords = pd.concat([column_coords, supplement_coords], axis=0)

    all_coords = pd.concat([row_coords, column_coords], axis=0, ignore_index=True)
    all_coords.columns = all_coords.columns.astype(str)

    chart = alt.Chart(all_coords).mark_text(size=12, font='Arial').encode(
        x=alt.X(str(x_component), title=f'Dimensão {x_component+1}'),
        y=alt.Y(str(y_component), title=f'Dimensão {y_component+1}'),
        text='Label',
        color='Type'
    ).properties(
        width=720,
        height=480
    )

    x_rule = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(color='black').encode(x='x')
    y_rule = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='black').encode(y='y')
    final_chart = (chart + x_rule + y_rule).interactive()
    final_chart.display()