import pandas as pd
from tabulate import tabulate

import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

from sklearn.cluster import KMeans
import numpy as np

from scipy.spatial.distance import pdist

from scipy import stats

import plotly.graph_objects as go

from sklearn.manifold import TSNE
import plotly.express as px

import seaborn as sns

from scipy.stats import chi2_contingency


def hierarchical_clustering_analysis(df, columns, method='average', metric='sqeuclidean'):
    """
    Realiza a análise de clusters hierárquicos com base nos parâmetros fornecidos.

    Parâmetros:
    df (DataFrame): DataFrame contendo os dados a serem analisados.
    columns (list): Lista de colunas a serem usadas na análise de clusters.
    method (str): Método de aglomeração a ser utilizado. Opções comuns incluem:
        - 'single': ligação simples (mínimo)
        - 'complete': ligação completa (máximo)
        - 'average'(Default): ligação média (usado para médias) 
        - 'ward': minimiza a variância dentro dos clusters (bom para clusters esféricos)
    metric (str): Métrica de distância a ser utilizada. Opções comuns incluem:
        - 'euclidean': distância euclidiana padrão
        - 'sqeuclidean'(Default): distância euclidiana quadrada
        - 'cityblock': distância de Manhattan (ou L1)
        - 'cosine': distância baseada em cosseno
        - 'correlation': distância baseada em correlação

    Retorno:
    str: Tabela formatada com os resultados da análise de clusters.

    A tabela contém as seguintes colunas:
    - Cluster 1: Índice do primeiro cluster que está sendo unido.
    - Cluster 2: Índice do segundo cluster que está sendo unido.
    - Coefficients: A distância entre os dois clusters que estão sendo unidos.
      Este valor representa a similaridade ou diferença entre os clusters unidos.
    - Number of Points in Cluster: O número de pontos (ou observações) no cluster resultante da união.
      Isso indica quantos dados estão contidos no novo cluster formado.
    """
    
    # Selecionar as colunas relevantes para a análise de cluster
    data_for_clustering = df[columns]

    # Realizar a análise de cluster com os parâmetros fornecidos
    Z = linkage(data_for_clustering, method=method, metric=metric)

    # Criar a tabela de aglomeração
    agglomeration_schedule = pd.DataFrame(Z, columns=['Cluster 1', 'Cluster 2', 'Coefficients', 'Number of Points\n in Cluster'])

    # Exibir a tabela utilizando a biblioteca tabulate, sem a primeira coluna
    formatted_schedule = tabulate(agglomeration_schedule[['Cluster 1', 'Cluster 2', 'Coefficients', 'Number of Points\n in Cluster']], 
                    headers=['Cluster 1', 'Cluster 2', 'Distance\n (Coefficients)', 'Number of Points\n in Cluster'], 
                    tablefmt='fancy_grid')
    
    print(formatted_schedule)
    
    

def plot_dendrogram(df, columns, method='average', metric='sqeuclidean'):
    """
    Gera e exibe um dendrograma baseado na análise de clusters hierárquicos.

    Parâmetros:
    df (DataFrame): DataFrame contendo os dados a serem analisados.
    columns (list): Lista de colunas a serem usadas na análise de clusters.
    method (str): Método de aglomeração a ser utilizado. Opções comuns incluem:
        - 'single': ligação simples (mínimo)
        - 'complete': ligação completa (máximo)
        - 'average'(Default): ligação média (usado para médias)
        - 'ward': minimiza a variância dentro dos clusters (bom para clusters esféricos)
    metric (str): Métrica de distância a ser utilizada. Opções comuns incluem:
        - 'euclidean': distância euclidiana padrão
        - 'sqeuclidean'(Default): distância euclidiana quadrada
        - 'cityblock': distância de Manhattan (ou L1)
        - 'cosine': distância baseada em cosseno
        - 'correlation': distância baseada em correlação
        - 'hamming': distância de Hamming (para dados binários)

    Retorno:
    None: A função gera e exibe um dendrograma, sem retorno.

    O dendrograma mostra as seguintes informações:
    - As profissões na lista são os rótulos das folhas (leaf labels).
    - A orientação do dendrograma é horizontal, com as folhas à direita.
    - As distâncias entre clusters são representadas na escala da métrica especificada.
    """
    
    # Selecionar as colunas relevantes para a análise de cluster
    data_for_clustering = df[columns]

    # Realizar a análise de cluster com os parâmetros fornecidos
    Z = linkage(data_for_clustering, method=method, metric=metric)

    # Criar o dendrograma
    plt.figure(figsize=(10, 7))
    dendrogram(Z, labels=df['profissão'].tolist(), leaf_rotation=0, leaf_font_size=10, orientation='right')
    plt.title(f'Dendrograma da Análise de Cluster\nMétodo: {method.capitalize()}, Métrica: {metric.capitalize()}')
    plt.xlabel('Profissões')
    plt.ylabel(f'Distância ({metric.capitalize()})')
    plt.show()
    

def cluster_membership_analysis(df, columns, method='average', metric='sqeuclidean', num_clusters=[3, 4]):
    """
    Realiza uma análise de clusters hierárquicos e retorna uma tabela que identifica a qual cluster cada caso pertence 
    para diferentes soluções de cluster.

    Parâmetros:
    ----------
    df : pandas.DataFrame
        DataFrame contendo os dados a serem analisados. As linhas representam os casos (ex.: profissões) e as colunas 
        representam as variáveis (ex.: z_prestigio, z_suicídio).
        
    columns : list
        Lista de strings contendo os nomes das colunas do DataFrame que serão utilizadas na análise de clusters.
        Essas colunas devem conter os dados quantitativos padronizados que serão usados para calcular as distâncias 
        entre os casos.

    method : str, opcional, default='complete'
        Método de aglomeração a ser utilizado na análise de clusters. Os métodos comuns incluem:
        - 'single': ligação simples, que une os clusters com a menor distância mínima entre elementos.
        - 'complete': ligação completa, que une os clusters com a maior distância máxima entre elementos.
        - 'average'(Default): ligação média, que une os clusters com base na média das distâncias entre todos os pares de elementos.
        - 'ward': minimiza a variância total dentro dos clusters ao combiná-los, adequado para clusters esféricos.

    metric : str, opcional, default='euclidean'
        Métrica de distância a ser utilizada para calcular as distâncias entre os casos. Métricas comuns incluem:
        - 'euclidean': distância euclidiana padrão.
        - 'sqeuclidean'(Default): distância euclidiana ao quadrado.
        - 'cityblock': distância de Manhattan, também conhecida como L1.
        - 'cosine': distância baseada no cosseno do ângulo entre dois vetores.
        - 'correlation': distância baseada na correlação entre vetores.
        - 'hamming': distância de Hamming, utilizada para dados binários.

    num_clusters : list, opcional, default=[3, 4]
        Lista contendo os números de clusters desejados para a análise. Cada valor na lista representa uma solução 
        de cluster que será calculada e reportada na tabela final. Ex.: [3, 4] calculará soluções de cluster para 3 
        e 4 clusters.

    Retorno:
    --------
    str
        Uma string formatada representando a tabela de "Cluster Membership", onde cada caso (ex.: profissão) é associado 
        ao cluster correspondente para diferentes soluções de cluster. A tabela inclui:
        - Case: Nome ou identificação do caso analisado (ex.: nome da profissão).
        - Colunas de Clusters: Cada coluna corresponde a uma solução de cluster diferente (ex.: 3 clusters, 4 clusters),
          mostrando a qual grupo o caso pertence em cada solução.
        
    Exemplos de Uso:
    ----------------
    >>> formatted_membership = cluster_membership_analysis(df, 
                                                           columns=['z_prestigio', 'z_suicídio', 'z_rendimento', 'z_educação'], 
                                                           method='complete', 
                                                           metric='euclidean',
                                                           num_clusters=[3, 4])
    >>> print(formatted_membership)

    Esta função é útil em contextos onde é necessário identificar e comparar a alocação de casos em diferentes soluções de 
    cluster, auxiliando na identificação de grupos homogêneos dentro dos dados.
    """
    
    # Selecionar as colunas relevantes para a análise de cluster
    data_for_clustering = df[columns]

    # Realizar a análise de cluster com os parâmetros fornecidos
    Z = linkage(data_for_clustering, method=method, metric=metric)

    # Adicionar colunas para os clusters
    for n_clusters in num_clusters:
        df[f'{n_clusters} Clusters'] = fcluster(Z, n_clusters, criterion='maxclust')

    # Organizar os resultados para a tabela de "Cluster Membership"
    cluster_membership = df[['profissão'] + [f'{n_clusters} Clusters' for n_clusters in num_clusters]]

    # Formatando a tabela usando tabulate
    formatted_membership = tabulate(cluster_membership, headers=['Case'] + [f'{n_clusters} Clusters' for n_clusters in num_clusters], 
                                     showindex=True, tablefmt='fancy_grid')

    print(formatted_membership)



def kmeans_cluster_analysis(df, columns, n_clusters=3, random_state=42, max_iter=10):
    """
    Realiza a análise de clusters usando K-Means e gera as tabelas e gráficos necessários.

    Parâmetros:
    df (DataFrame): DataFrame contendo os dados a serem analisados.
    columns (list): Lista de colunas a serem usadas na análise de clusters.
    n_clusters (int): Número de clusters a ser usado no K-Means.
    random_state (int): Semente aleatória para reprodução dos resultados.
    max_iter (int): Número máximo de iterações para o K-Means.

    Retorno:
    None: A função gera tabelas e gráficos, sem retorno.
    """
    data_for_clustering = df[columns]

    # Configuração do K-Means com uma iteração inicial
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=1, max_iter=1, init='k-means++')
    
    # Executar o K-Means e capturar os centros iniciais
    kmeans.fit(data_for_clustering)
    centers_history = [kmeans.cluster_centers_]
    
    # Obtenha as contagens de cada cluster inicial
    initial_labels = kmeans.labels_
    initial_cluster_counts = np.bincount(initial_labels)
    initial_cluster_percentages = initial_cluster_counts / len(initial_labels) * 100

    for i in range(1, max_iter):
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=1, max_iter=1, init=centers_history[-1])
        kmeans.fit(data_for_clustering)
        centers_history.append(kmeans.cluster_centers_)
        if np.allclose(centers_history[-1], centers_history[-2]):
            break  # Convergência alcançada
    
    # Obtenha as contagens de cada cluster final
    final_labels = kmeans.labels_
    final_cluster_counts = np.bincount(final_labels)
    final_cluster_percentages = final_cluster_counts / len(final_labels) * 100

    # Histórico de Iterações
    centers_history_array = np.array(centers_history)
    changes_in_centers = np.abs(np.diff(centers_history_array, axis=0)).max(axis=2)
    max_change = np.max(changes_in_centers)

    print("Iteration History")
    iteration_history_table = []
    for iter_num, changes in enumerate(changes_in_centers):
        iteration_history_table.append([f"{iter_num + 1}"] + [f"{change:.3f}" for change in changes])
    print(tabulate(iteration_history_table, headers=['Iteration'] + [f'Cluster {i+1}' for i in range(n_clusters)], tablefmt='fancy_grid'))
    
    print("\na. Convergence achieved due to no or small change in cluster centers.")
    print(f"The maximum absolute coordinate change for any center is {max_change:.3f}.")
    print(f"The current iteration is {len(centers_history)}.")
    # Usando pdist para calcular todas as distâncias entre os centros iniciais
    min_initial_center_distance = np.min(pdist(centers_history[0]))
    print("The minimum distance between initial centers is {:.3f}.".format(min_initial_center_distance))

    # Centros dos Clusters Iniciais
    initial_centers = centers_history[0]
    print("\nInitial Cluster Centers")
    initial_centers_table = pd.DataFrame(initial_centers.T, index=columns, columns=[f'Cluster {i+1}' for i in range(n_clusters)])
    print(tabulate(initial_centers_table, headers='keys', tablefmt='fancy_grid'))

    # Exibindo as contagens e porcentagens dos clusters iniciais
    initial_counts_table = pd.DataFrame({
        "Cluster": [f"Cluster {i+1}" for i in range(n_clusters)],
        "n": initial_cluster_counts,
        "%": initial_cluster_percentages
    })
    print("\nInitial Cluster Counts and Percentages")
    print(tabulate(initial_counts_table, headers='keys', tablefmt='fancy_grid'))

    # Centros dos Clusters Finais
    final_centers = centers_history[-1]
    print("\nFinal Cluster Centers")
    final_centers_table = pd.DataFrame(final_centers.T, index=columns, columns=[f'Cluster {i+1}' for i in range(n_clusters)])
    print(tabulate(final_centers_table, headers='keys', tablefmt='fancy_grid'))

    # Exibindo as contagens e porcentagens dos clusters finais
    final_counts_table = pd.DataFrame({
        "Cluster": [f"Cluster {i+1}" for i in range(n_clusters)],
        "n": final_cluster_counts,
        "%": final_cluster_percentages
    })
    print("\nFinal Cluster Counts and Percentages")
    print(tabulate(final_counts_table, headers='keys', tablefmt='fancy_grid'))

    # Distâncias entre os Centros Finais dos Clusters
    distances = np.zeros((n_clusters, n_clusters))
    for i in range(n_clusters):
        for j in range(i+1, n_clusters):
            distances[i, j] = np.linalg.norm(final_centers[i] - final_centers[j])
            distances[j, i] = distances[i, j]
    
    print("\nDistances between Final Cluster Centers")
    distances_table = pd.DataFrame(distances, columns=[f'Cluster {i+1}' for i in range(n_clusters)], index=[f'Cluster {i+1}' for i in range(n_clusters)])
    formatted_table = distances_table.map(lambda x: f'{x:.3f}' if x != 0 else '')
    print(tabulate(formatted_table, headers='keys', tablefmt='fancy_grid', showindex=True))

    # Gráficos dos Centros dos Clusters Iniciais e Finais
    fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

    ind = np.arange(n_clusters)  # Posições no eixo x
    width = 0.15  # Largura das barras

    # Plotar os centros iniciais
    for i, column in enumerate(columns):
        axes[0].bar(ind + i*width, initial_centers[:, i], width, label=f'{column}')
    axes[0].set_title('Initial Cluster Centers')
    axes[0].set_xticks(ind + width*(len(columns)-1)/2)
    axes[0].set_xticklabels([f'Cluster {i+1}' for i in range(n_clusters)])
    axes[0].legend()

    # Plotar os centros finais
    for i, column in enumerate(columns):
        axes[1].bar(ind + i*width, final_centers[:, i], width, label=f'{column}')
    axes[1].set_title('Final Cluster Centers')
    axes[1].set_xticks(ind + width*(len(columns)-1)/2)
    axes[1].set_xticklabels([f'Cluster {i+1}' for i in range(n_clusters)])
    axes[1].legend()

    plt.show()
    
    
def perform_kmeans(df, columns, n_clusters=3, random_state=42):
    """
    Executa KMeans e adiciona a coluna de rótulos de clusters ao DataFrame.

    Parâmetros:
    df (DataFrame): DataFrame contendo os dados.
    columns (list): Lista de colunas a serem usadas no KMeans.
    n_clusters (int): Número de clusters para o KMeans.
    random_state (int): Semente aleatória para reprodução dos resultados.

    Retorno:
    df (DataFrame): DataFrame com rótulos de clusters adicionados.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    df['Cluster'] = kmeans.fit_predict(df[columns])
    
    return df
    
def perform_kmeans_anova(df, columns, n_clusters=3):
    """
    Realiza a ANOVA para cada coluna em relação aos clusters e gera a tabela com todos os parâmetros.

    Parâmetros:
    df (DataFrame): DataFrame contendo os dados e os rótulos de clusters.
    columns (list): Lista de colunas para as quais a ANOVA será realizada.

    Retorno:
    DataFrame: Resultados da ANOVA com Sum of Squares, df, Mean Square, F-value e p-value.
    """
        
    df = perform_kmeans(df, columns, n_clusters)
    
    anova_results = []

    for col in columns:
        # Grupos divididos por cluster
        groups = [df[df['Cluster'] == cluster][col] for cluster in df['Cluster'].unique()]

        # Realizar ANOVA unidirecional
        f_value, p_value = stats.f_oneway(*groups)

        # Calcular os parâmetros da ANOVA manualmente
        ss_between = sum(len(group) * (group.mean() - df[col].mean())**2 for group in groups)
        ss_within = sum(((group - group.mean())**2).sum() for group in groups)
        df_between = len(groups) - 1
        df_within = df.shape[0] - len(groups)
        ms_between = ss_between / df_between
        ms_within = ss_within / df_within

        # Adicionar resultados à tabela
        anova_results.append([col, ss_between, df_between, ms_between, ss_within, df_within, ms_within, f_value, p_value])

    # Converter os resultados para um DataFrame
    anova_df = pd.DataFrame(anova_results, columns=['Variable', 'Sum of Squares\n(Between)', 'df\n(Between)',
                                                    'Mean Square\n(Between)', 'Sum of Squares\n(Within)', 'df\n(Within)',
                                                    'Mean Square\n(Within)', 'F-value', 'p-value'])
    
    # Exibir os resultados da ANOVA em formato de tabela
    print("ANOVA")
    print(tabulate(anova_df, headers='keys', tablefmt='fancy_grid', floatfmt=".3f", showindex=False))



def plot_elbow_method_plotly(X, max_clusters=10):
    """Gera o gráfico do Método Elbow com WSS, AIC e BIC utilizando Plotly."""
    def calculate_aic_bic(kmeans, X):
        """Calcula AIC e BIC para o modelo KMeans."""
        m = kmeans.n_clusters  # número de clusters
        n, d = X.shape  # nº observações / nº de variáveis

        # Within-Cluster Sum of Squares (WSS)
        wss = kmeans.inertia_

        # Log-verossimilhança aproximada   
        ll = -wss / 2

        # Número de parâmetros (centroides + variância)
        k = m * d + 1

        # AIC
        aic = 2 * k - 2 * ll

        # BIC
        bic = k * np.log(n) - 2 * ll

        return aic, bic

    wss = []
    aic = []
    bic = []

    for k in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        
        # WSS (Within-Cluster Sum of Squares)
        wss.append(kmeans.inertia_)
        
        # Calcular AIC e BIC usando a função corrigida
        aic_k, bic_k = calculate_aic_bic(kmeans, X)
        aic.append(aic_k)
        bic.append(bic_k)
    
    clusters = list(range(2, max_clusters + 1))

    # Criar a figura usando Plotly
    fig = go.Figure()

    # Adicionar a curva WSS
    fig.add_trace(go.Scatter(x=clusters, y=wss, mode='lines+markers', name='WSS', line=dict(color='black')))

    # Adicionar a curva AIC
    fig.add_trace(go.Scatter(x=clusters, y=aic, mode='lines+markers', name='AIC', line=dict(dash='dash', color='red')))

    # Adicionar a curva BIC
    fig.add_trace(go.Scatter(x=clusters, y=bic, mode='lines+markers', name='BIC', line=dict(dash='dot', color='blue')))

    # Marcar o menor valor de BIC
    min_bic_index = np.argmin(bic)
    min_bic_cluster = clusters[min_bic_index]
    fig.add_trace(go.Scatter(x=[min_bic_cluster], y=[bic[min_bic_index]], mode='markers', name='Menor BIC',
                             marker=dict(color='red', size=10, symbol='x')))

    # Layout do gráfico, incluindo escala do eixo X de 1 em 1
    fig.update_layout(
        title='Método Elbow com AIC e BIC',
        xaxis_title='Número de Clusters',
        yaxis_title='Métricas',
        legend_title='Métricas',
        width=800,
        height=600,
        hovermode='x',
        xaxis=dict(
            dtick=1  # Define a escala principal de 1 em 1 no eixo X
        )
    )

    # Exibir o gráfico interativo
    fig.show()
    



def plot_tsne_clusters_interactive(X, n_clusters=3, perplexity=30, random_state=42, hover_col=None, width=800, height=600):
    """
    Gera e plota um gráfico t-SNE dos clusters interativamente usando Plotly.
    
    Parâmetros:
    - X: DataFrame ou array com os dados.
    - n_clusters: Número de clusters a serem utilizados no KMeans.
    - perplexity: Parâmetro do t-SNE.
    - random_state: Semente para reprodução.
    - hover_col: Coluna opcional para exibir ao passar o mouse (ex: df_z['profissão']).
    - width: Largura da figura (em pixels).
    - height: Altura da figura (em pixels).
    """
    
    # Verificar o número de amostras e ajustar perplexity, se necessário
    n_samples = X.shape[0]
    if perplexity >= n_samples:
        perplexity = max(5, n_samples // 2)  # Ajustar perplexity para ser menor que o número de amostras
    
    # Aplicar KMeans aos dados
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    clusters = kmeans.fit_predict(X)
    
    # Aplicar t-SNE para reduzir a dimensionalidade a 2D
    tsne = TSNE(n_components=2, perplexity=perplexity, random_state=random_state)
    X_tsne = tsne.fit_transform(X)
    
    # Criar um DataFrame com as coordenadas t-SNE e os clusters
    df_tsne = pd.DataFrame(X_tsne, columns=['Dim1', 'Dim2'])
    df_tsne['Cluster'] = clusters
    
    # Adicionar hover_col (ex: 'profissão') ao DataFrame se fornecida
    hover_data = None
    if hover_col is not None:
        df_tsne['hover_info'] = hover_col
        hover_data = ['hover_info']
    
    # Criar gráfico interativo usando Plotly
    fig = px.scatter(df_tsne, x='Dim1', y='Dim2', color=df_tsne['Cluster'].astype(str),
                     title=f't-SNE dos Clusters)',
                     labels={'color': 'Cluster'}, 
                     hover_data=hover_data)
    
    # Ajustar o tamanho da figura
    fig.update_layout(width=width, height=height)
    
    # Exibir gráfico
    fig.show()
    

def plot_pairgrid_with_clusters(df, n_clusters=3):
    """
    Gera um gráfico do tipo PairGrid com KDE e scatterplot para os dados e clusters fornecidos.
    
    Parâmetros:
    - df: DataFrame com as colunas de interesse para os clusters.
    - n_clusters: Número de clusters a serem utilizados no KMeans.
    """
    
    # Copiar o DataFrame para evitar alterações no original
    X = df.copy(deep=True)
    
    # Aplicar o algoritmo KMeans para identificar os clusters
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    X['Cluster'] = kmeans.fit_predict(X)
    
    # Configurar o PairGrid com os clusters e cores
    g = sns.PairGrid(X, hue="Cluster", palette='tab10')
    
    # Gráficos na diagonal: KDE (Densidade)
    g.map_diag(sns.kdeplot)
    
    # Gráficos acima da diagonal: Scatterplot
    g.map_upper(sns.scatterplot)
    
    # Gráficos abaixo da diagonal: KDE
    g.map_lower(sns.kdeplot)
    
    # Adicionar legenda ao gráfico
    g.add_legend()
    
    # Mostrar o gráfico
    plt.show()
    

def cluster_variation_analysis(df, columns, n_clusters, cluster_col, test_col):
    """
    Realiza a análise de variação dos clusters segundo uma coluna de interesse,
    criando uma tabela de contigência que inclui contagens observadas, contagens esperadas,
    percentuais e resíduos ajustados.

    Parâmetros:
    df (DataFrame): DataFrame contendo os dados a serem analisados.
    cluster_col (str): Nome da coluna que contém os clusters.
    test_col (str): Nome da coluna de interesse (ex.: Sexo, Idade) a ser testada.

    Retorno:
    None: A função exibe a tabela de contigência.
    """
    df = perform_kmeans(df, columns, n_clusters)
    
    # Criar tabela de contingência
    contingency_table = pd.crosstab(df[test_col], df[cluster_col])
    
    # Executar o teste do qui-quadrado
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    
    # Converter as tabelas para numpy arrays para evitar problemas de indexação
    contingency_array = contingency_table.to_numpy()
    expected_array = np.array(expected)
    
    # Calcular os resíduos ajustados
    residuals = (contingency_array - expected_array) / np.sqrt(expected_array * (1 - np.sum(contingency_array, axis=1, keepdims=True) / np.sum(contingency_array)) * (1 - np.sum(contingency_array, axis=0) / np.sum(contingency_array)))

    # Formatar os resultados na estrutura desejada
    results = []

    test_groups = contingency_table.index.tolist()
    clusters = contingency_table.columns.tolist()
    total_count = np.sum(contingency_array)

    for group in test_groups:
        group_index = contingency_table.index.get_loc(group)
        observed_counts = contingency_array[group_index]
        expected_counts = expected_array[group_index]
        residual_values = residuals[group_index]
        total_group_count = np.sum(observed_counts)
        
        results.append([group, 'Count'] + list(observed_counts) + [total_group_count])
        results.append([None, 'Expected Count'] + list(np.round(expected_counts, 1)) + [total_group_count])
        results.append([None, '% within Group'] + list(np.round(observed_counts / total_group_count * 100, 1)) + [100.0])
        results.append([None, 'Adjusted Residual'] + list(np.round(residual_values, 1)) + [''])

    # Adicionando a linha de totais
    total_per_cluster = contingency_table.sum(axis=0).values
    results.append(['Total', 'Count'] + list(total_per_cluster) + [total_count])
    results.append([None, 'Expected Count'] + list(np.round(expected.sum(axis=0), 1)) + [total_count])
    results.append([None, '% within Group'] + list(np.round(total_per_cluster / total_count * 100, 1)) + [100.0])

    # Exibir os resultados formatados
    headers = [test_col, ''] + [f'Cluster {i+1}' for i in range(len(clusters))] + ['Total']
    print(tabulate(results, headers=headers, tablefmt="grid"))

    # Exibir o teste de qui-quadrado
    print(f"\nChi-Square Test: χ² = {chi2:.3f}, df = {dof}, p-value = {p:.3f}")
    
    
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, StratifiedKFold
from tabulate import tabulate
from scipy.stats import fisher_exact
import statsmodels.api as sm
import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning

class DecisionTreeNode:
    def __init__(self, data, target, features, depth=0, max_depth=3,
                 min_parent_node_size=300, min_child_node_size=150,
                 node_id=1):
        self.data = data
        self.target = target
        self.features = features
        self.depth = depth
        self.max_depth = max_depth
        self.min_parent_node_size = min_parent_node_size
        self.min_child_node_size = min_child_node_size
        self.is_leaf = False
        self.children = []
        self.split_feature = None
        self.split_value = None
        self.class_counts = data[target].value_counts().to_dict()
        self.majority_class = data[target].mode()[0]
        self.node_id = node_id

    def predict(self, x):
        if self.is_leaf:
            return self.majority_class
        else:
            feature_value = x.get(self.split_feature, None)
            if feature_value is None:
                return self.majority_class
            if isinstance(self.split_value, tuple):
                if feature_value in self.split_value:
                    return self.children[0].predict(x)
                else:
                    return self.children[1].predict(x)
            else:
                if feature_value <= self.split_value:
                    return self.children[0].predict(x)
                else:
                    return self.children[1].predict(x)

    def add_edges(self, graph):
        if self.is_leaf:
            node_label = (f"Node {self.node_id}\n"
                          f"n: {len(self.data)}\n"
                          f"Counts:\n{self.class_counts}\n"
                          f"Pred.: {self.majority_class}")
            node_color = 'lightgreen'
        else:
            node_label = (f"Node {self.node_id}\n"
                          f"n: {len(self.data)}\n"
                          f"Counts:\n{self.class_counts}")
            node_color = 'lightblue'
        graph.add_node(self.node_id, label=node_label, color=node_color)

        if self.children:
            for i, child in enumerate(self.children):
                if isinstance(self.split_value, tuple):
                    if i == 0:
                        edge_label = f"{self.split_feature} in {self.split_value}"
                    else:
                        edge_label = f"{self.split_feature} not in {self.split_value}"
                else:
                    if i == 0:
                        edge_label = f"{self.split_feature} ≤ {self.split_value}"
                    else:
                        edge_label = f"{self.split_feature} > {self.split_value}"
                child.add_edges(graph)
                graph.add_edge(self.node_id, child.node_id, label=edge_label)

class CHAIDNode(DecisionTreeNode):
    def __init__(self, data, target, features, depth=0, max_depth=3,
                 min_parent_node_size=300, min_child_node_size=150,
                 alpha_merge=0.05, alpha_split=0.05, node_id=1):
        super().__init__(data, target, features, depth, max_depth,
                         min_parent_node_size, min_child_node_size, node_id)
        self.alpha_merge = alpha_merge
        self.alpha_split = alpha_split
        self.p_value = None
        self.chi2 = None  # Armazenar o valor do qui-quadrado
        self._build_tree()

    def _build_tree(self):
        if (self.depth >= self.max_depth or
            len(self.data) < self.min_parent_node_size):
            self.is_leaf = True
            return

        best_feature, best_groups, best_p_value, best_chi2 = self._find_best_split()

        if best_feature is None or best_p_value > self.alpha_split:
            self.is_leaf = True
            return

        # Garantir o tamanho mínimo dos nós filhos
        valid_split = all(len(group) >= self.min_child_node_size for group in best_groups.values())
        if not valid_split:
            self.is_leaf = True
            return

        self.split_feature = best_feature
        self.p_value = best_p_value
        self.chi2 = best_chi2  # Armazenar o valor do qui-quadrado
        self.split_value = list(best_groups.keys())

        for group_value, group_data in best_groups.items():
            child_node = CHAIDNode(
                data=group_data,
                target=self.target,
                features=[f for f in self.features if f != best_feature],
                depth=self.depth + 1,
                max_depth=self.max_depth,
                min_parent_node_size=self.min_parent_node_size,
                min_child_node_size=self.min_child_node_size,
                alpha_merge=self.alpha_merge,
                alpha_split=self.alpha_split,
                node_id=self.node_id * 10 + len(self.children) + 1
            )
            self.children.append(child_node)

    def _find_best_split(self):
        best_p_value = 1.0
        best_feature = None
        best_groups = None
        best_chi2 = None  # Armazenar o melhor valor de qui-quadrado

        for feature in self.features:
            # CHAID EXAUSTIVO: Avaliar todas as possíveis divisões
            groups = self.data.groupby(feature)
            categories = list(groups.groups.keys())
            all_groupings = self._all_possible_groupings(categories)

            for grouping in all_groupings:
                merged_groups = self._merge_groups(groups, grouping)
                if len(merged_groups) < 2:
                    continue  # Precisa de pelo menos dois grupos para dividir

                observed = []
                for group in merged_groups.values():
                    counts = group[self.target].value_counts()
                    observed.append(counts.reindex(self.data[self.target].unique(), fill_value=0).values)

                chi2, p_value, _, _ = chi2_contingency(observed)

                if p_value < best_p_value:
                    best_p_value = p_value
                    best_feature = feature
                    best_groups = merged_groups
                    best_chi2 = chi2

        return best_feature, best_groups, best_p_value, best_chi2

    def _all_possible_groupings(self, categories):
        # Gerar todos os agrupamentos possíveis não vazios de categorias
        groupings = []
        n = len(categories)
        for i in range(1, n // 2 + 1):
            for combo in combinations(categories, i):
                group1 = list(combo)
                group2 = [cat for cat in categories if cat not in combo]
                if group1 and group2:
                    groupings.append([group1, group2])
        return groupings

    def _merge_groups(self, groups, grouping):
        merged_groups = {}
        for group_keys in grouping:
            group_data = pd.concat([groups.get_group(k) for k in group_keys])
            merged_groups[tuple(group_keys)] = group_data
        return merged_groups

    def add_edges(self, graph):
        if self.is_leaf:
            node_label = (f"Nó {self.node_id}\n"
                          f"n: {len(self.data)}\n"
                          f"Contagens:\n{self.class_counts}\n"
                          f"Pred.: {self.majority_class}")
            node_color = 'lightgreen'
        else:
            node_label = (f"Nó {self.node_id}\n"
                          f"n: {len(self.data)}\n"
                          f"Contagens:\n{self.class_counts}\n"
                          f"χ²: {self.chi2:.2f}\n"
                          f"P-valor: {self.p_value:.4f}")
            node_color = 'lightblue'
        graph.add_node(self.node_id, label=node_label, color=node_color)

        if self.children:
            for i, child in enumerate(self.children):
                group_value = self.split_value[i]
                if isinstance(group_value, tuple):
                    edge_label = f"{self.split_feature} in {group_value}"
                else:
                    edge_label = f"{self.split_feature} = {group_value}"
                child.add_edges(graph)
                graph.add_edge(self.node_id, child.node_id, label=edge_label)
                
    def predict(self, x):
        if self.is_leaf:
            return self.majority_class
        else:
            feature_value = x.get(self.split_feature, None)
            if feature_value is None:
                return self.majority_class
            for idx, group_value in enumerate(self.split_value):
                if isinstance(group_value, tuple):
                    if feature_value in group_value:
                        return self.children[idx].predict(x)
                else:
                    if feature_value == group_value:
                        return self.children[idx].predict(x)
            return self.majority_class  # Caso não encontre correspondência

class CARTNode(DecisionTreeNode):
    def __init__(self, data, target, features, depth=0, max_depth=3,
                 min_parent_node_size=10500, min_child_node_size=2500,
                 min_impurity_decrease=0.0, node_id=1):
        super().__init__(data, target, features, depth, max_depth,
                         min_parent_node_size, min_child_node_size, node_id)
        self.min_impurity_decrease = min_impurity_decrease
        self.gini = self._calculate_gini(data[target])
        self.impurity_decrease = 0  # Para importância de variáveis
        self._build_tree()

    def _build_tree(self):
        if (self.depth >= self.max_depth or
            len(self.data) < self.min_parent_node_size or
            self.gini == 0):
            self.is_leaf = True
            return

        best_feature, best_value, best_impurity, impurity_decrease = self._find_best_split()

        if best_feature is None or impurity_decrease < self.min_impurity_decrease:
            self.is_leaf = True
            return

        # Dividir os dados
        if isinstance(best_value, tuple):
            left_mask = self.data[best_feature].isin(best_value)
            right_mask = ~left_mask
        else:
            left_mask = self.data[best_feature] <= best_value
            right_mask = self.data[best_feature] > best_value

        left_indices = self.data[left_mask].index
        right_indices = self.data[right_mask].index

        # Verificar tamanhos mínimos dos nós filhos
        if (len(left_indices) < self.min_child_node_size or
            len(right_indices) < self.min_child_node_size):
            self.is_leaf = True
            return

        self.split_feature = best_feature
        self.split_value = best_value
        self.impurity_decrease = impurity_decrease

        left_node = CARTNode(
            data=self.data.loc[left_indices],
            target=self.target,
            features=self.features,
            depth=self.depth + 1,
            max_depth=self.max_depth,
            min_parent_node_size=self.min_parent_node_size,
            min_child_node_size=self.min_child_node_size,
            min_impurity_decrease=self.min_impurity_decrease,
            node_id=self.node_id * 2
        )

        right_node = CARTNode(
            data=self.data.loc[right_indices],
            target=self.target,
            features=self.features,
            depth=self.depth + 1,
            max_depth=self.max_depth,
            min_parent_node_size=self.min_parent_node_size,
            min_child_node_size=self.min_child_node_size,
            min_impurity_decrease=self.min_impurity_decrease,
            node_id=self.node_id * 2 + 1
        )

        self.children = [left_node, right_node]

    def _find_best_split(self):
        best_impurity = float('inf')
        best_feature = None
        best_value = None
        best_impurity_decrease = 0

        current_impurity = self.gini

        for feature in self.features:
            unique_values = self.data[feature].dropna().unique()
            if self.data[feature].dtype.kind in 'bifc':  # Variáveis Numéricas
                sorted_values = np.unique(self.data[feature].dropna())
                if len(sorted_values) <= 1:
                    continue
                # Usar quantis para reduzir pontos de divisão
                percentiles = np.percentile(sorted_values, [25, 50, 75])
                potential_split_points = np.unique(percentiles)

                for value in potential_split_points:
                    left_mask = self.data[feature] <= value
                    right_mask = self.data[feature] > value

                    left_data = self.data[left_mask][self.target]
                    right_data = self.data[right_mask][self.target]

                    if len(left_data) < self.min_child_node_size or len(right_data) < self.min_child_node_size:
                        continue

                    impurity = ((len(left_data) * self._calculate_gini(left_data) +
                                 len(right_data) * self._calculate_gini(right_data)) /
                                len(self.data))

                    impurity_decrease = current_impurity - impurity

                    if impurity < best_impurity:
                        best_impurity = impurity
                        best_feature = feature
                        best_value = value
                        best_impurity_decrease = impurity_decrease

            else:  # Variáveis Categóricas
                categories = unique_values
                if len(categories) <= 1:
                    continue
                # Ordenar categorias com base na taxa de resposta
                category_order = self.data.groupby(feature)[self.target].mean().sort_values().index
                for i in range(1, len(categories)):
                    left_categories = category_order[:i]
                    left_mask = self.data[feature].isin(left_categories)
                    right_mask = ~left_mask

                    left_data = self.data[left_mask][self.target]
                    right_data = self.data[right_mask][self.target]

                    if len(left_data) < self.min_child_node_size or len(right_data) < self.min_child_node_size:
                        continue

                    impurity = ((len(left_data) * self._calculate_gini(left_data) +
                                 len(right_data) * self._calculate_gini(right_data)) /
                                len(self.data))

                    impurity_decrease = current_impurity - impurity

                    if impurity < best_impurity:
                        best_impurity = impurity
                        best_feature = feature
                        best_value = tuple(left_categories)
                        best_impurity_decrease = impurity_decrease

        return best_feature, best_value, best_impurity, best_impurity_decrease

    def _calculate_gini(self, y):
        class_counts = y.value_counts()
        n = len(y)
        impurity = 1.0 - sum((count / n) ** 2 for count in class_counts)
        return impurity

    def predict(self, x):
        if self.is_leaf:
            return self.majority_class
        else:
            feature_value = x.get(self.split_feature, None)
            if feature_value is None:
                # Estratégia para valores faltantes: retornar a classe majoritária do nó atual
                return self.majority_class
            if isinstance(self.split_value, tuple):
                if feature_value in self.split_value:
                    return self.children[0].predict(x)
                else:
                    return self.children[1].predict(x)
            else:
                if feature_value <= self.split_value:
                    return self.children[0].predict(x)
                else:
                    return self.children[1].predict(x)

    def add_edges(self, graph):
        if self.is_leaf:
            node_label = (f"Nó {self.node_id}\n"
                          f"n: {len(self.data)}\n"
                          f"Contagens:\n{self.class_counts}\n"
                          f"Pred.: {self.majority_class}")
            node_color = 'lightgreen'
        else:
            node_label = (f"Nó {self.node_id}\n"
                          f"n: {len(self.data)}\n"
                          f"Contagens:\n{self.class_counts}\n"
                          f"Gini: {self.gini:.2f}\n"
                          f"ΔImpurity: {self.impurity_decrease:.4f}")
            node_color = 'lightblue'
        graph.add_node(self.node_id, label=node_label, color=node_color)

        if self.children:
            left_child, right_child = self.children
            if isinstance(self.split_value, tuple):
                left_edge_label = f"{self.split_feature} in {self.split_value}"
                right_edge_label = f"{self.split_feature} not in {self.split_value}"
            else:
                left_edge_label = f"{self.split_feature} ≤ {self.split_value:.2f}"
                right_edge_label = f"{self.split_feature} > {self.split_value:.2f}"

            left_child.add_edges(graph)
            right_child.add_edges(graph)
            graph.add_edge(self.node_id, left_child.node_id, label=left_edge_label)
            graph.add_edge(self.node_id, right_child.node_id, label=right_edge_label)


# Funções comuns
def visualize_tree(model):
    graph = nx.DiGraph()
    model.add_edges(graph)

    pos = hierarchy_pos(graph, model.node_id)
    labels = nx.get_node_attributes(graph, 'label')
    edge_labels = nx.get_edge_attributes(graph, 'label')
    node_colors = [graph.nodes[node]['color'] for node in graph.nodes()]

    plt.figure(figsize=(14, 10))
    nx.draw(graph, pos, with_labels=False, node_size=2500, node_color=node_colors, arrows=False)
    nx.draw_networkx_labels(graph, pos, labels, font_size=8)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=7)
    plt.title('Decision Tree CHAID' if isinstance(model, CHAIDNode) else 'Decision Tree CART')
    plt.axis('off')
    plt.show()


def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):

    def _hierarchy_pos(G, root, pos, parent=None, leftmost=0, width=1.,
                       vert_gap=0.2, vert_loc=0, xcenter=0.5):

        neighbors = list(G.neighbors(root))
        if parent and parent in neighbors:
            neighbors.remove(parent)
        if len(neighbors) != 0:
            dx = width / len(neighbors)
            nextx = xcenter - width / 2 - dx / 2
            for neighbor in neighbors:
                nextx += dx
                pos = _hierarchy_pos(G, neighbor, pos, root, width=dx,
                                     vert_gap=vert_gap, vert_loc=vert_loc - vert_gap,
                                     xcenter=nextx)
        pos[root] = (xcenter, vert_loc)
        return pos

    return _hierarchy_pos(G, root, {}, width=width, vert_gap=vert_gap,
                          vert_loc=vert_loc, xcenter=xcenter)


def predict(model, X):
    return X.apply(model.predict, axis=1)

def calculate_variable_importance(model):
    importance_dict = {}

    def traverse(node):
        if not node.is_leaf and node.split_feature is not None:
            if isinstance(node, CHAIDNode):
                # Importância baseada no qui-quadrado
                importance = node.chi2
            elif isinstance(node, CARTNode):
                # Importância baseada na diminuição de impureza
                weight = len(node.data) / len(model.data)
                importance = node.impurity_decrease * weight
            else:
                importance = 0

            importance_dict[node.split_feature] = importance_dict.get(node.split_feature, 0) + importance

            for child in node.children:
                traverse(child)

    traverse(model)

    # Converter para DataFrame
    importance_df = pd.DataFrame(list(importance_dict.items()), columns=['Variable', 'Importance'])

    # Normalizar a importância
    max_importance = importance_df['Importance'].max()
    importance_df['Normalized Importance (%)'] = (importance_df['Importance'] / max_importance) * 100

    # Ordenar por importância
    importance_df = importance_df.sort_values(by='Importance', ascending=False).reset_index(drop=True)

    # Exibir a importância das variáveis usando tabulate
    print("Variables Importance:")
    print(tabulate(importance_df, headers='keys', tablefmt='github', showindex=False))

# Funções específicas para CHAID
def fit_chaid(data, target, features, max_depth=3,
              min_parent_node_size=300, min_child_node_size=150,
              alpha_merge=0.05, alpha_split=0.05):
    return CHAIDNode(
        data=data,
        target=target,
        features=features,
        depth=0,
        max_depth=max_depth,
        min_parent_node_size=min_parent_node_size,
        min_child_node_size=min_child_node_size,
        alpha_merge=alpha_merge,
        alpha_split=alpha_split,
        node_id=1
    )


# Funções específicas para CART
def fit_cart(data, target, features, max_depth=3,
             min_parent_node_size=10500, min_child_node_size=2500,
             min_impurity_decrease=0.0):
    return CARTNode(
        data=data,
        target=target,
        features=features,
        depth=0,
        max_depth=max_depth,
        min_parent_node_size=min_parent_node_size,
        min_child_node_size=min_child_node_size,
        min_impurity_decrease=min_impurity_decrease,
        node_id=1
    )
    
    
# Funções para gerar relatórios e análises
def generate_classification_report(model, data, features, target):
    # Gerar predições
    predictions = predict(model, data[features])

    # Criar matriz de confusão
    confusion = pd.crosstab(data[target], predictions, rownames=['Observado'], colnames=['Previsto'], margins=True)

    # Obter rótulos das classes
    observed_classes = confusion.index[:-1]  # Excluir linha 'All'
    predicted_classes = confusion.columns[:-1]  # Excluir coluna 'All'

    # Calcular porcentagem correta por classe
    percent_correct = {}
    for cls in observed_classes:
        correct = confusion.at[cls, cls] if cls in confusion.columns else 0
        total = confusion.at[cls, 'All']
        percent = (correct / total) * 100 if total > 0 else 0
        percent_correct[cls] = percent

    # Calcular porcentagem correta geral
    total_correct = sum(confusion.at[cls, cls] for cls in observed_classes if cls in confusion.columns)
    total_samples = confusion.at['All', 'All']
    overall_percent_correct = (total_correct / total_samples) * 100 if total_samples > 0 else 0

    # Preparar porcentagem geral por classe prevista
    overall_predicted_percent = {}
    for cls in predicted_classes:
        total_predicted = confusion.at['All', cls]
        overall_percent = (total_predicted / total_samples) * 100 if total_samples > 0 else 0
        overall_predicted_percent[cls] = overall_percent

    # Construir o relatório
    report_data = []
    for cls in observed_classes:
        row = {'Observado': cls}
        for pred_cls in predicted_classes:
            count = confusion.at[cls, pred_cls] if pred_cls in confusion.columns else 0
            row[pred_cls] = count
        row['Percentual Correto'] = f"{percent_correct[cls]:.1f}%"
        report_data.append(row)

    # Criar DataFrame
    report_df = pd.DataFrame(report_data)

    # Criar a linha de porcentagem geral
    overall_row = {'Observado': 'Geral'}
    for cls in predicted_classes:
        overall_row[cls] = f"{overall_predicted_percent[cls]:.1f}%"
    overall_row['Percentual Correto'] = f"{overall_percent_correct:.1f}%"

    # Adicionar a linha geral ao DataFrame
    report_df = pd.concat([report_df, pd.DataFrame([overall_row])], ignore_index=True)

    # Definir cabeçalhos
    headers = report_df.columns.tolist()

    # Usar tabulate para formatar a tabela
    report_str = tabulate(report_df, headers=headers, tablefmt='github', showindex=False)

    # Informações adicionais
    growing_method = "CHAID" if isinstance(model, CHAIDNode) else "CART"
    dependent_variable = target

    # Exibir o relatório de classificação
    print("Classificações estimadas pelo modelo")
    print(report_str)
    print(f"\nMétodo de Crescimento: {growing_method}")
    print(f"Variável Dependente: {dependent_variable}")

def generate_risk_table(model, data, features, target, n_splits=5):
    if isinstance(model, CHAIDNode):
        kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    else:
        kf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

    # Risco de Resubstituição
    predictions = predict(model, data[features])
    incorrect = (predictions != data[target]).sum()
    total = len(data)
    resubstitution_error_rate = incorrect / total
    resub_std_error = np.sqrt((resubstitution_error_rate * (1 - resubstitution_error_rate)) / total)

    # Risco de Validação Cruzada
    error_rates = []

    for train_index, test_index in kf.split(data[features], data[target]):
        train_data = data.iloc[train_index]
        test_data = data.iloc[test_index]

        if isinstance(model, CHAIDNode):
            cv_model = fit_chaid(
                data=train_data,
                target=target,
                features=features,
                max_depth=model.max_depth,
                min_parent_node_size=model.min_parent_node_size,
                min_child_node_size=model.min_child_node_size,
                alpha_merge=model.alpha_merge,
                alpha_split=model.alpha_split
            )
        else:
            cv_model = fit_cart(
                data=train_data,
                target=target,
                features=features,
                max_depth=model.max_depth,
                min_parent_node_size=model.min_parent_node_size,
                min_child_node_size=model.min_child_node_size,
                min_impurity_decrease=model.min_impurity_decrease
            )

        cv_predictions = predict(cv_model, test_data[features])

        cv_incorrect = (cv_predictions != test_data[target]).sum()
        cv_total = len(test_data)
        cv_error_rate = cv_incorrect / cv_total
        error_rates.append(cv_error_rate)

    # Média da taxa de erro de validação cruzada
    cv_error_rate_mean = np.mean(error_rates)

    # Erro padrão para a taxa de erro de validação cruzada
    cv_std_error = np.std(error_rates, ddof=1) / np.sqrt(n_splits)

    # Criar a tabela de risco
    risk_data = [
        ['Resubstituição', f"{resubstitution_error_rate:.3f}", f"{resub_std_error:.3f}"],
        ['Validação Cruzada', f"{cv_error_rate_mean:.3f}", f"{cv_std_error:.3f}"]
    ]

    # Definir cabeçalhos
    headers = ['Método', 'Estimativa', 'Erro Padrão']

    # Usar tabulate para formatar a tabela
    risk_table_str = tabulate(risk_data, headers=headers, tablefmt='github')

    # Exibir a tabela de risco
    print("Risco")
    print(risk_table_str)

def assign_nodes(model, data):
    node_assignments = pd.Series(index=data.index, dtype=int)

    def traverse(node, indices):
        # Caso base: se o nó é folha ou não tem split_feature, atribuir node_id
        if node.is_leaf or node.split_feature is None or not node.children:
            node_assignments.loc[indices] = node.node_id
            return

        # Verificar se o nó tem dois filhos e split_value não é uma lista (CART)
        if len(node.children) == 2 and not isinstance(node.split_value, list):
            # Nó CART com divisão binária
            if isinstance(node.split_value, (tuple, list)):
                # Divisão categórica
                left_mask = data.loc[indices, node.split_feature].isin(node.split_value)
                right_mask = ~left_mask
            else:
                # Divisão numérica
                left_mask = data.loc[indices, node.split_feature] <= node.split_value
                right_mask = data.loc[indices, node.split_feature] > node.split_value

            left_indices = indices[left_mask]
            right_indices = indices[right_mask]

            traverse(node.children[0], left_indices)
            traverse(node.children[1], right_indices)
        else:
            # Nó CHAID ou divisão múltipla
            for idx, child in enumerate(node.children):
                group_value = node.split_value[idx]
                if isinstance(group_value, (tuple, list)):
                    mask = data.loc[indices, node.split_feature].isin(group_value)
                else:
                    mask = data.loc[indices, node.split_feature] == group_value
                child_indices = indices[mask]
                if not child_indices.empty:
                    traverse(child, child_indices)

    traverse(model, data.index)
    return node_assignments


def compare_node_variable(model, data, node_id, variable):
    import pandas as pd
    import numpy as np
    from scipy.stats import chi2_contingency, norm
    import statsmodels.api as sm

    # Passo 1: Atribuir cada observação a um nó usando a função corrigida
    node_assignments = assign_nodes(model, data)

    # Verificar se o node_id existe
    if node_id not in node_assignments.values:
        print(f"Nó {node_id} não existe ou não possui observações.")
        return

    # Passo 2: Criar uma variável binária indicando se cada observação está no nó especificado
    data = data.copy()
    data['node_group'] = np.where(node_assignments == node_id, f'1. nó {node_id}', '0. outros nós')

    # Verificar se ambos os grupos têm observações
    group_counts = data['node_group'].value_counts()
    if len(group_counts) < 2:
        print("Não é possível realizar a comparação: Ambos os grupos de nós devem ter observações.")
        return

    # Passo 3: Criar uma tabela de contingência
    contingency_table = pd.crosstab(data['node_group'], data[variable], margins=False)

    # Verificar se a tabela de contingência é adequada
    if contingency_table.shape[0] < 2 or contingency_table.shape[1] < 2:
        print("Não é possível realizar a comparação: A tabela de contingência deve ter pelo menos duas linhas e duas colunas.")
        print("Verifique se o ID do nó e a variável estão corretos e se os dados têm categorias suficientes.")
        return

    # Passo 4: Realizar o teste do qui-quadrado para obter contagens esperadas e resíduos ajustados
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    # Passo 5: Calcular porcentagens e resíduos ajustados
    observed = contingency_table.values
    expected = expected

    # Cálculos para resíduos ajustados
    total_count = observed.sum()
    row_totals = observed.sum(axis=1).reshape(-1, 1)
    col_totals = observed.sum(axis=0)
    expected = np.where(expected == 0, 1e-10, expected)  # Evitar divisão por zero

    adjusted_residuals = (observed - expected) / np.sqrt(expected * (1 - row_totals / total_count) * (1 - col_totals / total_count))

    # Preparar DataFrames
    observed_df = contingency_table.reset_index()
    expected_df = pd.DataFrame(expected, columns=contingency_table.columns)
    expected_df.insert(0, 'node_group', observed_df['node_group'])

    residuals_df = pd.DataFrame(adjusted_residuals, columns=contingency_table.columns)
    residuals_df.insert(0, 'node_group', observed_df['node_group'])
    residuals_df = residuals_df.round(2)

    # Calcular percentagens dentro do grupo do nó
    observed_df['Total'] = observed_df.iloc[:, 1:].sum(axis=1)
    total_count = observed_df['Total'].sum()

    for index, row in observed_df.iterrows():
        for col in contingency_table.columns:
            observed_df.at[index, f'% dentro do grupo {col}'] = (row[col] / row['Total'] * 100)
            observed_df.at[index, f'% do Total {col}'] = (row[col] / total_count * 100)

    # Build the comparison table
    comparison_rows = []

    for idx, row in observed_df.iterrows():
        node_group = row['node_group']

        # Observed Counts
        group_data = {'Label': node_group}
        for col in contingency_table.columns:
            group_data[col] = int(row[col])
        group_data['Total'] = int(row['Total'])
        comparison_rows.append(group_data)

        # Expected Counts
        expected_row = expected_df.loc[expected_df['node_group'] == node_group]
        group_data = {'Label': 'Contagem Esperada'}
        for col in contingency_table.columns:
            group_data[col] = round(expected_row[col].values[0], 1)
        group_data['Total'] = round(expected_row.iloc[:, 1:].sum(axis=1).values[0], 1)
        comparison_rows.append(group_data)

        # % within node group
        group_data = {'Label': '% dentro do grupo'}
        for col in contingency_table.columns:
            percent = row[f'% dentro do grupo {col}']
            group_data[col] = f"{percent:.1f}%"
        group_data['Total'] = '100.0%'
        comparison_rows.append(group_data)

        # % of Total
        group_data = {'Label': '% do Total'}
        for col in contingency_table.columns:
            percent = row[f'% do Total {col}']
            group_data[col] = f"{percent:.1f}%"
        group_data['Total'] = f"{(row['Total'] / total_count * 100):.1f}%"
        comparison_rows.append(group_data)

        # Adjusted Residuals
        residuals_row = residuals_df.loc[residuals_df['node_group'] == node_group]
        group_data = {'Label': 'Resíduo Ajustado'}
        for col in contingency_table.columns:
            residual = residuals_row[col].values[0]
            group_data[col] = residual
        group_data['Total'] = ''
        comparison_rows.append(group_data)

    # Total row
    total_counts = data[variable].value_counts().reindex(contingency_table.columns, fill_value=0)
    total_row = {'Label': 'Total'}
    for col in contingency_table.columns:
        total_row[col] = total_counts[col]
    total_row['Total'] = total_counts.sum()
    comparison_rows.append(total_row)

    # % of Total for the total row
    group_data = {'Label': '% do Total'}
    for col in contingency_table.columns:
        percent = (total_counts[col] / total_count * 100)
        group_data[col] = f"{percent:.1f}%"
    group_data['Total'] = '100.0%'
    comparison_rows.append(group_data)

    # Create the final DataFrame
    comparison_df = pd.DataFrame(comparison_rows).fillna('')
    comparison_df = comparison_df.rename(columns={'Total': 'Total'})

    # Ensure 'Label' is the first column
    cols = ['Label'] + [col for col in comparison_df.columns if col != 'Label']
    comparison_df = comparison_df[cols]

    # Format the table using tabulate
    comparison_str = tabulate(comparison_df, headers='keys', tablefmt='github', showindex=False)

    # Display the comparison table
    print(f"Comparação do nó {node_id} com os restantes na variável '{variable}'")
    print(comparison_str)

    # Calculate odds ratio and relative risks if the contingency table is 2x2
    if contingency_table.shape == (2, 2):
        # Use statsmodels to calculate odds ratio and confidence intervals
        table_values = contingency_table.values
        table_sm = sm.stats.Table2x2(table_values)
        oddsratio = table_sm.oddsratio
        ci_lower_or, ci_upper_or = table_sm.oddsratio_confint()
        p_value_or = table_sm.oddsratio_pvalue()

        # Prepare risk data
        risk_data = []

        # For each category of the variable
        for col in contingency_table.columns:
            # Extract counts
            a = contingency_table.at[f'1. nó {node_id}', col]
            b = contingency_table.loc[f'1. nó {node_id}'].sum() - a
            c = contingency_table.at['0. outros nós', col]
            d = contingency_table.loc['0. outros nós'].sum() - c

            # Risk in node
            risk_node = a / (a + b) if (a + b) > 0 else 0
            # Risk in other nodes
            risk_others = c / (c + d) if (c + d) > 0 else 0
            # Relative Risk
            rr = risk_node / risk_others if risk_others > 0 else np.inf

            # Confidence interval for relative risk
            se_log_rr = np.sqrt((1 / a) - (1 / (a + b)) + (1 / c) - (1 / (c + d))) if a > 0 and c > 0 else 0
            z = norm.ppf(0.975)  # 95% confidence
            log_rr = np.log(rr) if rr > 0 else 0
            ci_lower_rr = np.exp(log_rr - z * se_log_rr)
            ci_upper_rr = np.exp(log_rr + z * se_log_rr)

            # Add to risk data
            risk_data.append([
                f"Para {variable} = {col}",
                f"{rr:.3f}",
                f"{ci_lower_rr:.3f}",
                f"{ci_upper_rr:.3f}"
            ])

        # Add Odds Ratio to risk data
        risk_data.insert(0, [
            f"Razão de Chances para {variable} (1. nó {node_id} / 0. outros nós)",
            f"{oddsratio:.3f}",
            f"{ci_lower_or:.3f}",
            f"{ci_upper_or:.3f}"
        ])

        # Create DataFrame for risk table
        risk_df = pd.DataFrame(risk_data, columns=['', 'Valor', 'IC 95% Inferior', 'IC 95% Superior'])

        # Format the risk table
        risk_table_str = tabulate(risk_df, headers='keys', tablefmt='github', showindex=False)

        # Display the risk table
        print("\nEstimativa de Risco")
        print(risk_table_str)
        print(f"Número de Casos Válidos: {len(data)}")
    else:
        print("\nCálculo da razão de chances e riscos relativos não realizado porque a tabela de contingência não é 2x2.")
        
def generate_gain_table(model, target_class):
    gain_data = []
    total_data_size = len(model.data)
    total_target_count = model.data[model.target].value_counts().get(target_class, 0)
    overall_target_rate = (total_target_count / total_data_size) * 100 if total_data_size > 0 else 0

    def traverse(node):
        if node.is_leaf:
            node_id = node.node_id
            N = len(node.data)
            percent = (N / total_data_size) * 100 if total_data_size > 0 else 0

            # Número de casos da classe alvo no nó
            target_counts = node.class_counts.get(target_class, 0)
            target_percent = (target_counts / N) * 100 if N > 0 else 0

            # Índice
            index = (target_percent / overall_target_rate * 100) if overall_target_rate > 0 else 0

            gain_data.append([
                node_id,
                N,
                f"{percent:.2f}%",
                target_counts,
                f"{target_percent:.2f}%",
                f"{index:.2f}%"
            ])
        else:
            for child in node.children:
                traverse(child)

    traverse(model)

    # Ordenar os dados pelo Índice em ordem decrescente
    gain_data.sort(key=lambda x: float(x[5].strip('%')), reverse=True)

    # Calcular totais
    total_N = sum(row[1] for row in gain_data)
    total_percent = sum(float(row[2].strip('%')) for row in gain_data)
    total_gain = sum(row[3] for row in gain_data)
    total_response_percent = (total_gain / total_N) * 100 if total_N > 0 else 0
    total_index = (total_response_percent / overall_target_rate * 100) if overall_target_rate > 0 else 0

    # Adicionar linha de totais
    gain_data.append([
        'Total',
        total_N,
        f"{total_percent:.2f}%",
        total_gain,
        f"{total_response_percent:.2f}%",
        f"{total_index:.2f}%"
    ])

    # Definir cabeçalhos
    headers = ['Node', 'N', 'Percent', f'Gain ({target_class})', 'Response Percent', 'Index']

    # Usar tabulate para formatar a tabela
    gain_table_str = tabulate(gain_data, headers=headers, tablefmt='github')

    # Exibir a tabela de ganhos
    print(f"Tabela de Ganhos por Nó: Proporção da Classe {target_class}")
    print(gain_table_str)

# Função para gerar o resumo de lucro formatado
def generate_profit_summary(model, revenue_per_class, expense_per_class):
    profit_data = []
    total_data_size = len(model.data)

    def traverse(node):
        if node.is_leaf:
            node_id = node.node_id
            N = len(node.data)
            percent = (N / total_data_size) * 100 if total_data_size > 0 else 0

            # Contagem de classes no nó
            class_counts = node.class_counts

            # Cálculo do lucro total no nó
            total_revenue = sum(class_counts.get(cls, 0) * revenue_per_class.get(cls, 0) for cls in revenue_per_class)
            total_expense = sum(class_counts.get(cls, 0) * expense_per_class.get(cls, 0) for cls in expense_per_class)
            total_profit = total_revenue - total_expense

            # ROI
            roi = (total_profit / total_expense) * 100 if total_expense != 0 else 0

            profit_data.append([
                node_id,
                N,
                f"{percent:.2f}%",
                f"{total_profit:,.2f}",
                f"{roi:.2f}%"
            ])
        else:
            for child in node.children:
                traverse(child)

    traverse(model)

    # Ordenar por 'ROI' em ordem decrescente
    profit_data.sort(key=lambda x: float(x[4].strip('%')), reverse=True)

    # Definir cabeçalhos
    headers = ['Node', 'N', 'Percent', 'Profit', 'ROI']

    # Usar tabulate para formatar a tabela
    profit_table_str = tabulate(profit_data, headers=headers, tablefmt='github')

    # Exibir a tabela de resumo de lucro
    print("Resumo de Lucro por Nó")
    print(profit_table_str)
    

# Função para gerar a tabela de probabilidades prevista formatada
def generate_predicted_probability_table(model, target_class):
    probability_data = []
    total_data_size = len(model.data)
    
    def traverse(node):
        if node.is_leaf:
            node_id = node.node_id
            N = len(node.data)
            percent = (N / total_data_size) * 100 if total_data_size > 0 else 0

            # Calculate the predicted probability for the target class
            class_counts = node.class_counts
            total_counts = sum(class_counts.values())
            probability = (class_counts.get(target_class, 0) / total_counts) if total_counts > 0 else 0.0

            probability_data.append([
                node_id,
                f"{probability:.4f}",
                N,
                f"{percent:.2f}%"
            ])
        else:
            for child in node.children:
                traverse(child)

    traverse(model)

    # Sort the data by probability in descending order
    probability_data.sort(key=lambda x: float(x[1]), reverse=True)

    # Define headers
    headers = ['Node', 'Probability', 'Frequency', 'Percent']

    # Use tabulate to format the table
    probability_table_str = tabulate(probability_data, headers=headers, tablefmt='github')

    # Display the predicted probability table
    print(f"Predicted Probability Table for Class {target_class}")
    print(probability_table_str)

def calculate_prevalence_ratios(model, data, node_id, variables):
    import pandas as pd
    import numpy as np
    import statsmodels.api as sm
    import warnings
    from statsmodels.tools.sm_exceptions import ConvergenceWarning
    from tabulate import tabulate

    # Atribuir IDs de nós aos dados
    node_assignments = assign_nodes(model, data)
    
    # Verificar se o node_id existe
    if node_id not in node_assignments.values:
        print(f"Nó {node_id} não existe ou não possui observações.")
        return
    
    # Criar variável binária para indicação de pertencimento ao nó
    data = data.copy()
    data['node_assignment'] = np.where(node_assignments == node_id, 1, 0)
    
    results = []
    for var in variables:
        # Preparar os dados
        df = data[['node_assignment', var]].dropna()
        if df.empty:
            print(f"\nNão há dados suficientes para a variável '{var}'.")
            continue
        y = df['node_assignment']
        X = df[[var]]
        
        # Se a variável for categórica, criar dummies
        if X[var].dtype.name == 'category' or X[var].dtype == 'object':
            X = pd.get_dummies(X[var], drop_first=True)
        else:
            # Se for numérica, usaremos como está
            X = X.astype(float)
        
        # Adicionar termo constante
        X = sm.add_constant(X)
        
        try:
            # Ajustar o modelo de regressão de Poisson com erros padrão robustos
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                warnings.simplefilter("ignore", category=ConvergenceWarning)
                poisson_model = sm.GLM(y, X, family=sm.families.Poisson())
                result = poisson_model.fit(cov_type='HC0')
            
            # Verificar se houve convergência
            if not result.converged:
                print(f"Modelo não convergiu para a variável '{var}'.")
                continue
            
            # Extrair o Rácio de Prevalência, intervalos de confiança e p-valores
            for i in range(1, len(result.params)):  # Ignorar o termo constante
                param = result.params.iloc[i]
                conf_int = result.conf_int().iloc[i]
                p_value = result.pvalues.iloc[i]
                
                # Exponenciar os coeficientes e intervalos de confiança
                pr = np.exp(param)
                ci_lower = np.exp(conf_int[0])
                ci_upper = np.exp(conf_int[1])
                significance = '<0.01' if p_value < 0.01 else f"{p_value:.3f}"
                if p_value >= 0.05:
                    significance += " (n.s)"
                variable_name = X.columns[i]
                results.append({
                    'Variável': variable_name,
                    'Value': pr,
                    'Lower': ci_lower,
                    'Upper': ci_upper,
                    'Asymptotic Significance': significance
                })
        except Exception as e:
            print(f"Não foi possível ajustar o modelo para a variável '{var}': {e}")
    
    # Criar DataFrame com os resultados
    results_df = pd.DataFrame(results)
    
    if not results_df.empty:
        # Arredondar as colunas numéricas
        results_df[['Value', 'Lower', 'Upper']] = results_df[['Value', 'Lower', 'Upper']].round(3)
        # Exibir a tabela
        print("\nRácio de Prevalência")
        print(tabulate(results_df,headers=['Variables', 'Value', ' 95% CI Lower', ' 95% CI Upper', 'Asymptotic Significance'], 
                       tablefmt='github', showindex=False))
    else:
        print("Não foi possível calcular o Rácio de Prevalência para as variáveis fornecidas.")