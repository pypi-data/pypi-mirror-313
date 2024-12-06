from PyPDF2 import PdfReader
import os


def nfs_fortaleza() -> int:  # 32
    tot_pags: int = 0

    files = [file for file in os.listdir() if '.pdf' in file.lower()]
    for file in files:
        with open(file, 'rb') as file_b:
            pdf = PdfReader(file_b).pages[0]
            rows = pdf.extract_text().split('\n')
            tot_pags += len(PdfReader(file_b).pages)

        if rows[0] == 'Número da':
            # Modelo 1
            num_nf = ''.join(i for i in rows[1].split()[0] if i.isnumeric())
            for row in rows:
                if 'Complemento:' in row:
                    nome = row[12:].strip()
                    break
        elif rows[0] == 'Dados do Prestador de Serviços':
            # modelo 2
            primeiro = True
            for i, row in enumerate(rows):
                if row == 'NFS-e':
                    num_nf = rows[i + 1]
                if row == 'Razão Social/Nome':
                    if primeiro:
                        primeiro = False
                    else:
                        nome = rows[i + 1]
                        break
        else:
            continue
        os.rename(file, f'NF {num_nf} - {nome}.pdf')
    return tot_pags
