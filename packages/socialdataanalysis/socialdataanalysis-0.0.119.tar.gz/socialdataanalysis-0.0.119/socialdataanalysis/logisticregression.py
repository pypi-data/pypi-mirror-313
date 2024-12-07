import pandas as pd
import numpy as np
import statsmodels.api as sm
from tabulate import tabulate
from scipy import stats
from scipy.stats import norm
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score, auc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def analyze_glm_binomial(df, dependent_var, independent_vars):
    """
    Ajusta um modelo GLM binomial (logístico) a partir de um DataFrame, exibindo medidas de ajuste,
    testes do modelo e estimativas dos parâmetros.

    Parâmetros:
    - df: DataFrame com dados
    - dependent_var: Nome da variável dependente (binária, 0/1)
    - independent_vars: Lista de nomes de variáveis independentes

    A função valida a existência das variáveis, ajusta o modelo completo,
    realiza testes (Omnibus, LR de efeito), gera tabelas de ajuste e estimativas.
    """

    # Validação das variáveis
    all_vars = [dependent_var] + independent_vars
    for var in all_vars:
        if var not in df.columns:
            raise ValueError(f"A variável '{var}' não existe no DataFrame.")

    # Agrupar os dados pelas variáveis independentes e contar sucessos e fracassos
    grouped = df.groupby(independent_vars)[dependent_var].agg(['sum', 'count']).reset_index()
    grouped.columns = independent_vars + ['Success', 'Total']
    grouped['Failure'] = grouped['Total'] - grouped['Success']

    n_groups = len(grouped)
    n_total = df.shape[0]

    # Preparar as matrizes de design
    X_full = grouped[independent_vars]
    y = grouped[['Success', 'Failure']]
    X_full = sm.add_constant(X_full)

    # Ajustar o modelo completo
    model_full = sm.GLM(y, X_full, family=sm.families.Binomial())
    result_full = model_full.fit()
    deviance_full = result_full.deviance
    df_resid = result_full.df_resid
    df_model = result_full.df_model
    k = len(result_full.params)
    pearson_chi2 = np.sum(result_full.resid_pearson**2)
    log_likelihood_full = result_full.llf

    # Critérios de informação
    aic = -2 * log_likelihood_full + 2 * k
    bic = -2 * log_likelihood_full + k * np.log(n_total)
    AICc = aic + (2 * k * (k + 1)) / (n_total - k - 1)
    CAIC = aic + (np.log(n_total) + 1) * k

    # Estimação do parâmetro de escala (usando a deviance)
    scale = deviance_full / df_resid  # Método da Deviance

    # Ajuste dos erros padrão
    adjusted_bse = result_full.bse * np.sqrt(scale)

    # Recalcular Wald Chi-Quadrado e p-valores com os erros padrão ajustados
    wald_chi2 = (result_full.params / adjusted_bse) ** 2
    p_values = 1 - stats.chi2.cdf(wald_chi2, df=1)
    wald_chi2 = pd.Series(wald_chi2, index=result_full.params.index)
    p_values = pd.Series(p_values, index=result_full.params.index)

    # Testes tipo III (Likelihood Ratio) para cada parâmetro
    LR_stats = {}
    p_values_lr = {}
    for var in ['const'] + independent_vars:
        if var == 'const':
            # Modelo sem intercepto
            X_reduced = grouped[independent_vars]  # sem adicionar constante
        else:
            # Modelo sem a variável atual
            vars_reduced = [v for v in independent_vars if v != var]
            X_reduced = grouped[vars_reduced]
            X_reduced = sm.add_constant(X_reduced)

        model_reduced = sm.GLM(y, X_reduced, family=sm.families.Binomial())
        result_reduced = model_reduced.fit()
        deviance_reduced = result_reduced.deviance
        LR_stat = (deviance_reduced - deviance_full) / scale
        p_value_lr = 1 - stats.chi2.cdf(LR_stat, df=1)
        LR_stats[var] = LR_stat
        p_values_lr[var] = p_value_lr

    # Funções auxiliares de formatação
    def format_number(x):
        if isinstance(x, (int, float, np.float64, np.int64)):
            return f"{x:.3f}"
        else:
            return x

    def format_p_value(p):
        return "<0.001" if p < 0.001 else f"{p:.3f}"

    def create_goodness_of_fit_table():
        """
        Cria e exibe a tabela de "Goodness of Fit" com notas explicativas.
        """
        def add_superscript(text, superscripts):
            return f"{text}^{superscripts}"

        title = add_superscript('Goodness of Fit', 'a,b,c,d')
        log_likelihood_label = add_superscript('Log Likelihood', 'b,c')
        adjusted_log_likelihood_label = add_superscript('Adjusted Log Likelihood', 'd')

        # Usar escala fixa em 1 para Scaled Deviance (opcional)
        scale_fixed = 1
        scaled_deviance = df_resid * scale_fixed
        # Scaled Pearson: relação do Pearson Chi2 com a deviance
        scaled_pearson_chi2 = pearson_chi2 * (df_resid / deviance_full)

        adjusted_log_likelihood = -0.5 * scaled_deviance

        table = [
            ['Deviance', deviance_full, df_resid, deviance_full / df_resid],
            ['Scaled Deviance', scaled_deviance, df_resid, ''],
            ['Pearson Chi-Square', pearson_chi2, df_resid, pearson_chi2 / df_resid],
            ['Scaled Pearson Chi-Square', scaled_pearson_chi2, df_resid, ''],
            [log_likelihood_label, log_likelihood_full, '', ''],
            [adjusted_log_likelihood_label, adjusted_log_likelihood, '', ''],
            ["Akaike's Information Criterion (AIC)", aic, '', ''],
            ['Finite Sample Corrected AIC (AICc)', AICc, '', ''],
            ['Bayesian Information Criterion (BIC)', bic, '', ''],
            ['Consistent AIC (CAIC)', CAIC, '', '']
        ]
        headers = [title, 'Value', 'df', 'Value/df']

        formatted_table = []
        for row in table:
            formatted_row = [row[0]] + [format_number(x) for x in row[1:]]
            formatted_table.append(formatted_row)

        print(tabulate(formatted_table, headers=headers))

        footnotes = [
            "a. Information criteria are in smaller-is-better form.",
            "b. The full log likelihood function is displayed and used in computing information criteria.",
            "c. The log likelihood is based on a scale parameter fixed at 1.",
            "d. The adjusted log likelihood is based on the residual deviance and dispersion scaling."
        ]
        print('\n' + '\n'.join(footnotes))

    def create_omnibus_test_table():
        """
        Cria e exibe a tabela do teste Omnibus, comparando o modelo completo com o modelo nulo.
        """
        X_null = pd.DataFrame({'const': np.ones(grouped.shape[0])})
        model_null = sm.GLM(y, X_null, family=sm.families.Binomial())
        result_null = model_null.fit()
        deviance_null = result_null.deviance

        LR_stat_omnibus = (deviance_null - deviance_full) / scale
        p_value_omnibus = 1 - stats.chi2.cdf(LR_stat_omnibus, df=len(independent_vars))
        table = [
            [format_number(LR_stat_omnibus), len(independent_vars), format_p_value(p_value_omnibus)]
        ]
        headers = ['Likelihood Ratio Chi-Square', 'df', 'Sig.']
        print("Omnibus Tests of Model Coefficients")
        print(tabulate(table, headers=headers))

        footnotes = [
            "a. Compares the fitted model against the intercept-only model.",
            f"Dependent Variable: {dependent_var}",
            f"Model: (Intercept), {', '.join(independent_vars)}"
        ]
        print('\n' + '\n'.join(footnotes))

    def create_test_of_model_effects_table():
        """
        Cria e exibe a tabela com Testes Tipo III de Efeitos do Modelo (LR Tests).
        """
        df1 = 1
        df2 = df_resid

        table = []
        for var in ['const'] + independent_vars:
            source_name = '(Intercept)' if var == 'const' else var
            row = [
                source_name,
                format_number(LR_stats[var]),
                df1,
                format_p_value(p_values_lr[var]),
                format_number(LR_stats[var]),
                df1,
                format_number(df2),
                format_p_value(p_values_lr[var])
            ]
            table.append(row)

        headers = ['Source', 'Type III LR Chi-Square', 'df', 'Sig.', 'F', 'df1', 'df2', 'Sig.']
        print("Tests of Model Effects")
        print(tabulate(table, headers=headers))

        footnotes = [
            f"Dependent Variable: {dependent_var}",
            f"Model: (Intercept), {', '.join(independent_vars)}"
        ]
        print('\n' + ', '.join(footnotes))

    def create_parameter_estimates_table():
        """
        Cria e exibe a tabela de estimativas dos parâmetros, incluindo intervalos de confiança,
        razão de chances (Exp(B)) e testes de significância.
        """
        conf_int = result_full.conf_int()
        conf_int.columns = ['Lower', 'Upper']
        # Ajuste dos intervalos com os erros padrão escalonados
        conf_int['Lower'] = result_full.params - stats.norm.ppf(0.975) * adjusted_bse
        conf_int['Upper'] = result_full.params + stats.norm.ppf(0.975) * adjusted_bse

        exp_coef = np.exp(result_full.params)
        exp_conf_int_lower = np.exp(conf_int['Lower'])
        exp_conf_int_upper = np.exp(conf_int['Upper'])

        table = []
        for i in range(len(result_full.params)):
            param_name = result_full.params.index[i]
            row = [
                param_name if param_name != 'const' else '(Intercept)',
                format_number(result_full.params.iloc[i]),
                format_number(adjusted_bse.iloc[i]),
                format_number(conf_int.iloc[i]['Lower']),
                format_number(conf_int.iloc[i]['Upper']),
                format_number(wald_chi2[param_name]),
                1,
                format_p_value(p_values[param_name]),
                format_number(exp_coef.iloc[i]),
                format_number(exp_conf_int_lower.iloc[i]),
                format_number(exp_conf_int_upper.iloc[i])
            ]
            table.append(row)

        # Adicionar linha do parâmetro de escala
        table.append([
            '(Scale)',
            format_number(scale),
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            ''
        ])

        headers = [
            'Parameter', 'B', 'Std. Error',
            'Lower', 'Upper',
            'Wald Chi-Square', 'df', 'Sig.',
            'Exp(B)', 'Lower', 'Upper'
        ]
        print("Parameter Estimates (Adjusted for Deviance)")
        print(tabulate(table, headers=headers))

        footnotes = [
            f"Dependent Variable: {dependent_var}",
            f"Model: (Intercept), {', '.join(independent_vars)}",
            "a. Scale parameter estimated using the deviance."
        ]
        print('\n' + '\n'.join(footnotes))

    # Exibir resultados
    print(f"Número de observações: {n_total}")
    print(f"Número de grupos (combinações únicas): {n_groups}\n")
    create_goodness_of_fit_table()
    print()
    create_omnibus_test_table()
    print()
    create_test_of_model_effects_table()
    print()
    create_parameter_estimates_table()


def analyze_glm_binomial_plots(df, dependent_var, independent_vars):
    """
    Ajusta um modelo GLM binomial (logístico) e plota:
    - logit(p) versus a variável independente
    - Probabilidade prevista versus a variável independente

    Parâmetros:
    - df: DataFrame com dados
    - dependent_var: Nome da variável dependente (binária)
    - independent_vars: Lista de variáveis independentes (assume apenas uma, neste exemplo)

    Retorno:
    - Figura plotly com dois subplots.
    """

    # Validação
    all_vars = [dependent_var] + independent_vars
    for var in all_vars:
        if var not in df.columns:
            raise ValueError(f"A variável '{var}' não existe no DataFrame.")

    # Agrupar e montar o modelo
    grouped = df.groupby(independent_vars)[dependent_var].agg(['sum', 'count']).reset_index()
    grouped.columns = independent_vars + ['Success', 'Total']
    grouped['Failure'] = grouped['Total'] - grouped['Success']

    X_full = grouped[independent_vars]
    y = grouped[['Success', 'Failure']]
    X_full = sm.add_constant(X_full)

    model = sm.GLM(y, X_full, family=sm.families.Binomial())
    result = model.fit()

    intercept = result.params['const']
    coef = result.params[independent_vars[0]]
    equation = f"logit(p) = {intercept:.3f} + {coef:.5f} * {independent_vars[0]}"

    # Criar uma cópia explícita do DataFrame para evitar SettingWithCopyWarning
    df_copy = df.copy()

    # Adicionar colunas previstas ao DataFrame
    df_copy.loc[:, 'predicted_prob'] = result.predict(sm.add_constant(df_copy[independent_vars]))
    df_copy.loc[:, 'logit_p'] = np.log(df_copy['predicted_prob'] / (1 - df_copy['predicted_prob']))
    df_sorted = df_copy.sort_values(by=independent_vars[0])

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(f"Logit(p) vs {independent_vars[0]}", f"Predicted Probability vs {independent_vars[0]}")
    )

    # Logit(p)
    fig.add_trace(go.Scatter(
        x=df_sorted[independent_vars[0]],
        y=coef * df_sorted[independent_vars[0]] + intercept,
        mode='lines', name='Logit Regression Line', line=dict(color='orange')
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df_sorted[independent_vars[0]],
        y=df_sorted['logit_p'], mode='markers', name='logit(p)',
        marker=dict(color='red', size=3)
    ), row=1, col=1)
    
    # Probabilidade prevista
    fig.add_trace(go.Scatter(
        x=df_sorted[independent_vars[0]],
        y=df_sorted['predicted_prob'], mode='lines', name='Predicted Probability',
        line=dict(color='lightblue')
    ), row=1, col=2)

    fig.add_trace(go.Scatter(
        x=df_sorted[independent_vars[0]],
        y=df_sorted['predicted_prob'], mode='markers', name='Highlighted Points',
        marker=dict(color='blue', size=3)
    ), row=1, col=2)

    fig.update_layout(
        title_text="Logistic Regression Analysis (GLM Binomial)",
        width=1200,
        height=600,
        annotations=[
            dict(
                x=0.25,
                y=1.05,
                showarrow=False,
                text=equation,
                xref="paper",
                yref="paper",
                font=dict(size=12),
            )
        ],
        xaxis1_title=independent_vars[0],
        yaxis1_title="logit(p)",
        xaxis2_title=independent_vars[0],
        yaxis2_title="Predicted Probability",
    )

    fig.show()
    
    return df_copy


def classification_table(df, actual_col, predicted_prob_col, threshold=0.5):
    """
    Gera uma tabela de classificação a partir de um threshold para as probabilidades preditas.

    Parâmetros:
    - df: DataFrame com dados
    - actual_col: Nome da coluna com valores observados (0 ou 1)
    - predicted_prob_col: Nome da coluna com probabilidades previstas
    - threshold: ponto de corte

    Retorna:
    - Exibe a tabela de classificação formatada.
    """
    df = df.copy()
    df['predicted_class'] = np.where(df[predicted_prob_col] >= threshold, 1, 0)
    
    tn, fp, fn, tp = confusion_matrix(df[actual_col], df['predicted_class']).ravel()
    
    total = tn + fp + fn + tp
    total_nao = tn + fp
    total_sim = fn + tp
    total_previsto_nao = tn + fn
    total_previsto_sim = fp + tp

    especificidade = (tn / total_nao * 100) if total_nao != 0 else 0
    sensibilidade = (tp / total_sim * 100) if total_sim != 0 else 0
    precisao = (tp / total_previsto_sim * 100) if total_previsto_sim != 0 else 0

    table = [
        ["Real\\Previsão", "Previsto Não (0)", "Previsto Sim (1)", "Total"],
        ["Real Não (0)", tn, fp, total_nao],
        ["Real Sim (1)", fn, tp, total_sim],
        ["Total", total_previsto_nao, total_previsto_sim, total],
        ["", "", "", ""],
        ["Especificidade", f"{especificidade:.2f}%", ""],
        ["Sensibilidade", f"{sensibilidade:.2f}%", ""],
        ["Precisão", f"{precisao:.2f}%", ""],
    ]
    
    print(tabulate(table, headers="firstrow", tablefmt="grid"))


def auc_roc_table(df, actual_col, predicted_prob_col):
    """
    Gera uma tabela da AUC da curva ROC com IC 95%.

    Parâmetros:
    - df: DataFrame com dados
    - actual_col: Nome da coluna com valores observados (0 ou 1)
    - predicted_prob_col: Nome da coluna com probabilidades previstas

    Retorna:
    - Exibe a tabela formatada da AUC.
    """
    df = df.copy()
    auc_value = roc_auc_score(df[actual_col], df[predicted_prob_col])

    n1 = np.sum(df[actual_col] == 1)
    n2 = np.sum(df[actual_col] == 0)
    if n1 == 0 or n2 == 0:
        raise ValueError("Classes positivas e negativas não podem estar vazias.")

    # Fórmulas de Hanley & McNeil (1982)
    Q1 = auc_value / (2 - auc_value)
    Q2 = (2 * auc_value**2) / (1 + auc_value)
    auc_se = np.sqrt((auc_value * (1 - auc_value) + (n1 - 1)*(Q1 - auc_value**2) + (n2 - 1)*(Q2 - auc_value**2)) / (n1*n2))
    
    z = 1.96
    lower_bound = max(0, auc_value - z * auc_se)
    upper_bound = min(1, auc_value + z * auc_se)

    z_value = (auc_value - 0.5) / auc_se
    p_value = 2 * (1 - norm.cdf(abs(z_value)))

    table = [
        ["Área (AUC)", "Erro Padrão", "95% IC Inferior", "95% IC Superior", "Significância"],
        [f"{auc_value:.3f}", f"{auc_se:.4f}", f"{lower_bound:.3f}", f"{upper_bound:.3f}", f"{p_value:.3f}"]
    ]

    print(tabulate(table, headers="firstrow", tablefmt="grid"))
    print("a. Sob a suposição não-paramétrica\nb. Hipótese nula: área verdadeira = 0.5")


def plot_roc_curve_with_best_threshold(df, actual_col, predicted_prob_col, critical_col):
    """
    Plota a curva ROC, calcula o melhor threshold (Youden), exibe a AUC, e gera tabela com resultados.

    Parâmetros:
    - df: DataFrame com dados
    - actual_col: nome da coluna com valores observados
    - predicted_prob_col: nome da coluna com probabilidades previstas
    - critical_col: nome da coluna crítica associada ao threshold
    """
    df = df.copy()
    for col in [actual_col, predicted_prob_col, critical_col]:
        if col not in df.columns:
            raise ValueError(f"A coluna '{col}' não existe no DataFrame.")

    fpr, tpr, thresholds = roc_curve(df[actual_col], df[predicted_prob_col])
    roc_auc = auc(fpr, tpr)

    n1 = np.sum(df[actual_col] == 1)
    n2 = np.sum(df[actual_col] == 0)
    if n1 == 0 or n2 == 0:
        raise ValueError("Classes positivas e negativas não podem estar vazias.")

    youden_index = tpr - fpr
    best_idx = np.argmax(youden_index)
    best_threshold = thresholds[best_idx]
    best_fpr = fpr[best_idx]
    best_tpr = tpr[best_idx]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr,
        mode='lines', name=f'ROC Curve (AUC = {roc_auc:.3f})',
        line=dict(color='blue', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=[best_fpr], y=[best_tpr],
        mode='markers', name=f'Melhor Ponto (Threshold={best_threshold:.3f})',
        marker=dict(color='red', size=10)
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode='lines', name='Modelo Aleatório',
        line=dict(dash='dash', color='gray')
    ))

    fig.update_layout(
        title=f"Curva ROC (AUC = {roc_auc:.3f})",
        xaxis_title="1 - Especificidade (FPR)",
        yaxis_title="Sensibilidade (TPR)",
        width=600,
        height=600,
        showlegend=True
    )
    fig.show()

    best_critical_value = df.loc[df[predicted_prob_col] >= best_threshold, critical_col].min()

    table = [
        ["Melhor Threshold", f"{best_threshold:.3f}"],
        ["FPR no Melhor Ponto", f"{best_fpr:.3f}"],
        ["TPR no Melhor Ponto", f"{best_tpr:.3f}"],
        [f"Valor Crítico ({critical_col})", best_critical_value]
    ]
    print(tabulate(table, headers=["Descrição", "Valor"], tablefmt="grid"))
    
    # Exibir tabela de classificação para o melhor threshold
    classification_table(df, actual_col, predicted_prob_col, threshold=best_threshold)


def plot_odds_ratio_increments(df, dependent_var, independent_var, increment_steps=10, max_increment=100):
    """
    Gera um gráfico suave do efeito de incrementos na variável independente sobre o OR.

    Parâmetros:
    - df: DataFrame com dados
    - dependent_var: variável dependente (0/1)
    - independent_var: variável independente
    - increment_steps: passo dos incrementos
    - max_increment: incremento máximo
    """
    if dependent_var not in df.columns:
        raise ValueError(f"A variável dependente '{dependent_var}' não existe no DataFrame.")
    if independent_var not in df.columns:
        raise ValueError(f"A variável independente '{independent_var}' não existe no DataFrame.")

    grouped = df.groupby(independent_var)[dependent_var].agg(['sum', 'count']).reset_index()
    grouped.columns = [independent_var, 'Success', 'Total']
    grouped['Failure'] = grouped['Total'] - grouped['Success']

    X_full = grouped[[independent_var]]
    y = grouped[['Success', 'Failure']]
    X_full = sm.add_constant(X_full)

    model = sm.GLM(y, X_full, family=sm.families.Binomial())
    result = model.fit()

    intercept = result.params['const']
    coef = result.params[independent_var]

    increments = np.arange(0, max_increment + increment_steps, increment_steps)
    or_values = np.exp(coef * increments)
    increment_percentages = (or_values - 1) * 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=increments, y=or_values,
        mode='lines+markers', name='OR',
        line=dict(color='blue'), marker=dict(size=8)
    ))
    fig.update_layout(
        title=f"Efeito da variação em {independent_var} sobre o OR",
        xaxis_title=f"Incrementos em {independent_var} (u.m.)",
        yaxis_title="Odds Ratio (OR)",
        width=800, height=500
    )
    fig.show()

    table = [
        [round(inc, 3), round(or_val, 3), f"{round(perc, 1)}%"]
        for inc, or_val, perc in zip(increments, or_values, increment_percentages)
    ]
    print(tabulate(
        table,
        headers=[f"Incrementos em {independent_var} (u.m.)", "Odds Ratio (OR)", "Acréscimo (%)"],
        tablefmt="grid"
    ))


def calculate_independent_values_for_probabilities(df, dependent_var, independent_var, probabilities):
    """
    Dadas probabilidades desejadas, calcula quais valores da variável independente
    gerariam essas probabilidades no modelo logístico ajustado.

    Parâmetros:
    - df: DataFrame com dados
    - dependent_var: variável dependente (0/1)
    - independent_var: variável independente
    - probabilities: lista de probabilidades desejadas

    Retorna:
    - Exibe uma tabela com o valor do independente para cada p.
    """
    if dependent_var not in df.columns:
        raise ValueError(f"A variável dependente '{dependent_var}' não existe no DataFrame.")
    if independent_var not in df.columns:
        raise ValueError(f"A variável independente '{independent_var}' não existe no DataFrame.")

    grouped = df.groupby(independent_var)[dependent_var].agg(['sum', 'count']).reset_index()
    grouped.columns = [independent_var, 'Success', 'Total']
    grouped['Failure'] = grouped['Total'] - grouped['Success']

    X_full = grouped[[independent_var]]
    y = grouped[['Success', 'Failure']]
    X_full = sm.add_constant(X_full)

    model = sm.GLM(y, X_full, family=sm.families.Binomial())
    result = model.fit()

    intercept = result.params['const']
    coef = result.params[independent_var]

    def find_indep_value(p):
        return (np.log(p / (1 - p)) - intercept) / coef

    indep_values = [find_indep_value(p) for p in probabilities]

    table = [
        [f"{p:.3f}", f"{val:.3f}"] for p, val in zip(probabilities, indep_values)
    ]

    print(tabulate(
        table,
        headers=["Probabilidade (p)", f"Valor de {independent_var} (u.m.)"],
        tablefmt="grid"
    ))


def validate_logistic_model(df, dependent_var, independent_var, test_size=0.3, random_state=42):
    """
    Valida o modelo de regressão logística dividindo a amostra em treino e teste,
    estimando AUC na amostra de teste e exibindo uma tabela com IC e p-valor.

    Parâmetros:
    - df: DataFrame com dados
    - dependent_var: variável dependente (0/1)
    - independent_var: variável independente
    - test_size: proporção de teste (default=0.3)
    - random_state: semente para reprodutibilidade
    """
    if dependent_var not in df.columns:
        raise ValueError(f"A variável dependente '{dependent_var}' não existe no DataFrame.")
    if independent_var not in df.columns:
        raise ValueError(f"A variável independente '{independent_var}' não existe no DataFrame.")

    df = df.copy()
    np.random.seed(random_state)
    df['random'] = np.random.rand(len(df))

    train = df.loc[df['random'] > test_size].copy()
    test = df.loc[df['random'] <= test_size].copy()

    X_train = train[[independent_var]]
    y_train = train[dependent_var]
    X_train = sm.add_constant(X_train)

    X_test = test[[independent_var]]
    y_test = test[dependent_var]
    X_test = sm.add_constant(X_test)

    model = sm.Logit(y_train, X_train)
    result = model.fit(disp=False)

    test['Predicted_Prob'] = result.predict(X_test)

    auc = roc_auc_score(y_test, test['Predicted_Prob'])
    n1 = sum(y_test == 1)
    n2 = sum(y_test == 0)

    # Fórmula de Hanley & McNeil
    Q1 = auc / (2 - auc)
    Q2 = (2 * auc**2) / (1 + auc)
    auc_se = np.sqrt((auc * (1 - auc) + (n1 - 1)*(Q1 - auc**2) + (n2 - 1)*(Q2 - auc**2)) / (n1*n2))

    z = norm.ppf(0.975)
    lower_bound = auc - z * auc_se
    upper_bound = auc + z * auc_se
    if upper_bound > 1.0:
        upper_bound = 1.0

    z_score = (auc - 0.5) / auc_se
    p_value = 2 * (1 - norm.cdf(abs(z_score)))

    validation_table = [
        ["Área", f"{auc:.3f}", f"{auc_se:.3f}", f"{p_value:.3f}", f"{lower_bound:.3f}", f"{upper_bound:.3f}"]
    ]

    print(tabulate(
        validation_table,
        headers=["", "Area", "Std. Error", "Sig.", "Lower Bound (95%)", "Upper Bound (95%)"],
        tablefmt="grid",
        numalign="center"
    ))
    print("\na. Under the nonparametric assumption")
    print("b. Null hypothesis: true area = 0.5")
