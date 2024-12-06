from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm
import os


def recibos_pagamento() -> int:  # 9
    # Cria a pasta de destino dos recibos
    if not os.path.exists('Arquivos'):
        os.mkdir('Arquivos')
    tot_pags: int = 0

    escolha = ''
    while escolha not in ['1', '2']:
        escolha = input('-' * 30 + '\n'
                        '1: Separar por funcionário.\n'
                        '2: Separar por Lotação.\n'
                        'Escolha: ')

    files = [file for file in os.listdir() if '.pdf' in file]

    for arq in files:
        with open(arq, 'rb') as file:
            # Cria um objeto PdfFileReader para ler o conteúdo do arquivo PDF
            pdf_reader = PdfReader(file)
            tot_pags += len(pdf_reader.pages)
            if escolha == '1':  # Separa por funcionário
                # Itera sobre todas as páginas do PDF
                for pag in tqdm(pdf_reader.pages):
                    rows = pag.extract_text().split('\n')
                    # Acessa a linha que contém o nome do empregado.
                    nome = rows[11]
                    # Acessa a linha que contém a lotação do empregado.
                    lotacao = rows[9][:-5]
                    file_name = f'Arquivos\\{lotacao}-{nome}.pdf'.replace('/', '')
                    pdf_writer = PdfWriter()
                    # Adiciona a página atual ao objeto PdfWriter
                    pdf_writer.add_page(pag)

                    # Salva a página em um novo arquivo PDF
                    with open(file_name, 'wb') as output_file:
                        pdf_writer.write(output_file)

            elif escolha == '2':  # Separa por lotação
                for pag in tqdm(pdf_reader.pages):
                    rows = pag.extract_text().split('\n')
                    lotacao = rows[9][:-5]

                    file_name = f'Arquivos\\{lotacao}.pdf'.replace('/', '')
                    pdf_writer = PdfWriter()
                    # Verifica se já existe um arquivo para esta lotação.
                    if os.path.exists(file_name):
                        pdf_reader_temp = PdfReader(file_name)
                        # Copia todas as páginas do documento da lotação para o writer.
                        for page_num in range(len(pdf_reader_temp.pages)):
                            pdf_writer.add_page(pdf_reader_temp.pages[page_num])
                    # Adiciona a página atual
                    pdf_writer.add_page(pag)
                    # Salva o arquivo
                    with open(file_name, "wb") as output_pdf:
                        pdf_writer.write(output_pdf)
    return tot_pags
