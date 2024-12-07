import requests
import pyreadstat
import tempfile
import os


def download_and_load_sav_file(public_url):

    """
    Baixa um arquivo .sav do OneDrive e carrega os dados em um DataFrame.

    Args:
    public_url (str): URL pública direta do arquivo no OneDrive com o parâmetro de download.

    Returns:
    DataFrame: DataFrame carregado a partir do arquivo .sav ou None se houver um erro.
    """
    # Criar um diretório temporário
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Nome do arquivo
        file_name = 'downloaded_file.sav'
        downloaded_file_path = os.path.join(tmpdirname, file_name)

        try:
            # Baixar o arquivo do OneDrive
            response = requests.get(public_url)
            response.raise_for_status()  # Levanta um erro para códigos de status de resposta ruins

            # Salvar o arquivo no diretório temporário
            with open(downloaded_file_path, 'wb') as file:
                file.write(response.content)
            print("Arquivo baixado com sucesso.")

            # Carregar o DataFrame
            df, meta = pyreadstat.read_sav(downloaded_file_path)
            print("DataFrame carregado com sucesso.")
            return df, meta

        except requests.RequestException as req_err:
            print("Erro ao baixar o arquivo:", req_err)
        except pyreadstat.ReadstatError as read_err:
            print("Erro ao carregar o arquivo:", read_err)
        except Exception as e:
            print("Erro inesperado:", e)

    return None
