# socialdataanalysis

**Funções personalizadas para análise de dados nas ciências sociais, complementando o uso do SPSS.**

Este pacote oferece uma coleção de funções úteis para análise de dados, especialmente projetadas para complementar as capacidades do SPSS em pesquisas nas ciências sociais. As funções incluídas cobrem diversos aspectos da análise de associação, conforme descrito no livro [Análise de Dados Para Ciências Sociais: A Complementaridade do SPSS](https://silabo.pt/catalogo/informatica/aplicativos-estatisticos/livro/analise-de-dados-para-ciencias-sociais/).

## Recursos

- Pré-processamento de Dados
- Análise Exploratória de Dados
- Análise de Associação
- Análise Fatorial Exploratória
- Análise de Cluster

## Instalação

Você pode instalar o pacote diretamente do PyPI usando pip:

```bash
pip install socialdataanalysis
```

## Uso

Aqui está um exemplo de como usar este pacote em um script Python:

```python
from socialdataanalysis.exploratorydataanalysis import gerar_tabela_estatisticas_descritivas

# DataFrame exemplo
data = {
    'variable_1': [10, 20, 30, 40, 50],
    'variable_2': [15, 25, 35, 45, 55],
    'variable_3': [20, 30, 40, 50, 60]
}

df = pd.DataFrame(data)

# Exemplo de uso
gerar_tabela_estatisticas_descritivas(df=df, 
                                      variaveis=['variable_1', 'variable_2', 'variable_3'])

```

## Notebooks

Este pacote inclui notebooks de exemplo para demonstrar o uso das funções. Eles podem ser encontrados na pasta `notebooks` do pacote instalado.

## Contribuição

Se você deseja contribuir para este projeto, por favor, envie um pull request. Para problemas ou sugestões, utilize o issue tracker no GitHub.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Autor

Ricardo Coser Mergulhão - [ricardomergulhao@gmail.com](mailto:ricardomergulhao@gmail.com)
Maria Helena Pestana - [gageiropestana@gmail.com](mailto:gageiropestana@gmail.com)
Maria de Fátima Pina - [mariafatimadpina@gmail.com](mailto:mariafatimadpina@gmail.com)

## Agradecimentos

Agradecimentos especiais a todos os colaboradores e usuários deste pacote.
