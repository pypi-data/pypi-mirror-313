from .limpa_terminal import limpa_terminal
from .main_hub import main_hub
from .help_doc import help_doc


def info_hub() -> None:
    help_msg: str = '''
     0: Retornar  
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
        print('Escolha uma opção para abrir um arquivo do tipo e ler seu funcionamento.')
        print(help_msg)
        try:
            option = int(input('Escolha: '))
            limpa_terminal()
        except ValueError:
            pass
    if option not in options:
        info_hub()
    elif option != 0:
        help_doc(option)
        input('\nDigite enter para continuar')
        print('\n' * 50)
        main_hub()

