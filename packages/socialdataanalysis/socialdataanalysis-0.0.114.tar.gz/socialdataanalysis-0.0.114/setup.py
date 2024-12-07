from setuptools import setup, find_packages
#import glob

# Listando todos os arquivos .ipynb na pasta notebooks
#notebooks_files = glob.glob('notebooks/*.ipynb')

setup(
    name='socialdataanalysis',
    version='0.0.114',  # Atualize o número da versão para refletir as mudanças
    packages=find_packages(),
    #include_package_data=True,
    #package_data={
    #    'socialdataanalysis': ['notebooks/*.ipynb'],
    #},
    #data_files=[
    #    ('share/socialdataanalysis', notebooks_files),
    #],
    include_package_data=True,  # Garantir que os dados do pacote sejam incluídos
    install_requires=[
        'altair',
        'factor-analyzer',
        'ipython',
        'pandas',
        'prince',
        'pyreadstat',
        'pingouin',
        'plotly',
        'networkx',
        'numpy',
        'requests',
        'statsmodels',
        'scipy',
        'scikit-learn',
        'seaborn',
        'sympy',
        'tabulate',
    ],
    author='Ricardo Mergulhão, Maria Helena Pestana, Maria de Fátima Pina',
    author_email='ricardomergulhao@gmail.com, gageiropestana@gmail.com, mariafatimadpina@gmail.com',
    description='Funções personalizadas para análise de dados nas ciências sociais.',
    long_description=open('README.md', encoding='utf-8').read(),  # Garantir compatibilidade com encoding UTF-8
    long_description_content_type='text/markdown',
    url='https://github.com/rcmergulhao/socialdataanalysis',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versão mínima do Python necessária
    project_urls={
        'Source': 'https://github.com/rcmergulhao/socialdataanalysis',
        'Documentation': 'https://github.com/rcmergulhao/socialdataanalysis#readme',
    },
)
