from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm
import os


def folha_rescisao_ferias() -> int:  # 6
    # Cria a pasta de destino dos recibos
    if not os.path.exists('Arquivos'):
        os.mkdir('Arquivos')
    tot_pags: int = 0

    for arq in [file for file in os.listdir() if '.pdf' in file]:
        with open(arq, 'rb') as file:
            # Cria um objeto PdfFileReader para ler o conteúdo do arquivo PDF
            pdf_reader = PdfReader(file)
            pdf_writer = PdfWriter()
            lotacao = ''
            tot_pags += len(pdf_reader.pages)
            for page_pdf in tqdm(pdf_reader.pages):
                page = page_pdf.extract_text().split('\n')
                tipo = ' '.join(page[0].split()[:3])
                # Verifica o tipo de arquivo
                if tipo == 'Folha de Pagamento':
                    lotacao_nova = page[6]
                elif tipo == 'Listagem de Férias':
                    lotacao_nova = page[5]
                elif tipo == 'Listagem de Rescisão':
                    lotacao_nova = page[5]
                else:
                    print(tipo)
                    continue
                # Verifica se já há umas pasta para o tipo
                if not os.path.exists(f'Arquivos/{tipo}'):
                    os.mkdir(f'Arquivos/{tipo}')
                # Verifica se está na página de resumo ou se a lotacao for a mesma, se sim,
                # junta as páginas, caso contrário, salva o arquivo atual e cria um pdf novo.
                if 'Total Geral ' in lotacao_nova or lotacao_nova != lotacao:
                    if pdf_writer.pages:
                        with open(f'Arquivos/{tipo}/{lotacao.replace('/', '')}.pdf', 'wb') as output_file:
                            pdf_writer.write(output_file)
                        pdf_writer = PdfWriter()
                    lotacao = lotacao_nova
                    pdf_writer.add_page(page_pdf)
                else:
                    pdf_writer.add_page(page_pdf)
    return tot_pags
