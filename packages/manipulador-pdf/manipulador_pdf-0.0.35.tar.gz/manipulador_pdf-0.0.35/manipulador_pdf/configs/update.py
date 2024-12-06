import importlib.metadata
import subprocess
import requests
import socket
import sys
import os


def check_update():

    if tem_conexao():
        print('Verificando atualizações...')
        pacote = "manipulador_pdf"
        # Obtém a versão da biblioteca instalada
        versao_instalada = importlib.metadata.version(pacote)
        print(f"Versão atual do pacote: {versao_instalada}")

        # Obtém a versão mais recente disponível no PyPI
        versao_mais_recente = get_last_version(pacote)

        # Compara as versões
        if versao_instalada != versao_mais_recente:
            print('Há uma nova versão da ferramenta, digite 1 para baixar, 0 para continuar nesta versão.')
            resp = input()
            if resp == '1':
                update()
    else:
        print('Sem conexão para verificar atualizações...')



def tem_conexao() -> bool:
    try:
        socket.create_connection(('8.8.8.8', 53), timeout=5)
        return True
    except Exception:
        return False


def get_last_version(pacote):
    """
    Obtém a versão mais recente do pacote disponível no PyPI usando a API JSON do PyPI.
    """
    try:
        # Faz uma requisição GET à API do PyPI
        response = requests.get(f"https://pypi.org/pypi/{pacote}/json")
        response.raise_for_status()  # Levanta um erro se a requisição falhar
        data = response.json()
        return data["info"]["version"]
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar a versão mais recente: {e}")
        return None


def update():
    download_new_version()
    self_destruct()


def download_new_version():

    url_exe = 'https://github.com/LuizGusQueiroz/manipulador_pdf/raw/master/manip.exe'
    # Faz o download do arquivo
    response = requests.get(url_exe)

    # Verifica se o download foi bem-sucedido
    if response.status_code == 200:
        # Salva o arquivo no mesmo diretório onde o script está sendo executado
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'manip.exe')

        # Escreve o conteúdo no arquivo local
        with open(file_path, 'wb') as f:
            f.write(response.content)


def self_destruct():
    # Comando que agendará a exclusão do próprio arquivo
    delete_command = 'del "main.exe"'
    # Comando para renomear o arquivo manip.exe para manip.exe
    rename_command = 'rename manip.exe manip.exe'
    # Cria um arquivo em lote temporário para excluir o executável após um pequeno atraso
    with open("temp_delete.bat", "w") as bat_file:
        bat_file.write(f'ping localhost -n 3 > nul\n')  # Espera alguns segundos
        bat_file.write(f'{delete_command}\n')  # Comando para excluir o executável atual
        bat_file.write(f'timeout /T 0.5 > nul\n')  # Espera 0.5 segundos
        bat_file.write(f'{rename_command}\n')  # Comando para renomear manip.exe para manip.exe
        bat_file.write(f'del "%~f0"\n')  # Exclui o arquivo .bat após o uso
    # Executa o arquivo .bat que vai fazer a exclusão e renomeação
    subprocess.Popen("temp_delete.bat", shell=True)
