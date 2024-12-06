from .limpa_terminal import limpa_terminal
from .process_option import process_option


def main_hub():

    main_msg: str = '''
     1: Documentos de Admissão 
     2: Documentos de Rescisão 
     3: Boletos BMP 
     4: Boletos de Cobrança 
     5: Fichas de Registro 
     6: Folha de Pagamento, Férias e Rescisão 
     7: Guias FGTS 
     8: Listagem de Conferência 
     9: Recibos de Pagamento 
    10: Recibos FOLK 
    11: Relatório de Serviços Administrativos 
    12: Resumo Geral Mês/Período 
    31: NFs Curitiba
    32: NFs Fortaleza
    33: NFs Salvador
    34: NFs Sorocaba
    '''

    options = list(range(100))

    option: int = -1

    while option not in options:
        print('Digite uma opção de documento para separar.')
        print(main_msg)
        try:
            option = int(input('Escolha: '))
            limpa_terminal()
        except ValueError:
            pass
    process_option(option)
