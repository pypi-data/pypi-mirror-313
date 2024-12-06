from .salva_relatorio import salva_relatorio
from ..functions.boletos_bmp import boletos_bmp
from ..functions.boletos_cobranca import boletos_cobranca
from ..functions.documentos_admissao import documentos_admissao
from ..functions.documentos_rescisao import documentos_rescisao
from ..functions.fichas_de_registro import fichas_de_registro
from ..functions.folha_rescisao_ferias import folha_rescisao_ferias
from ..functions.guias_fgts import guias_fgts
from ..functions.listagem_conferencia import listagem_conferencia
from ..functions.nfs_curitiba import nfs_curitiba
from ..functions.nfs_fortaleza import nfs_fortaleza
from ..functions.nfs_salvador import nfs_salvador
from ..functions.nfs_sorocaba import nfs_sorocaba
from ..functions.recibos_folk import recibos_folk
from ..functions.recibos_pagamento import recibos_pagamento
from ..functions.rel_servicos_adm import rel_servicos_adm
from ..functions.resumo_geral_mes_periodo import resumo_geral_mes_periodo

from datetime import datetime
import time


def process_option(option: int) -> None:
    """
    Processa a opção do usuário.
    """
    data = datetime.now().strftime("%d/%m/%Y")
    st = time.time()

    # if option == 0:
    #     info_hub()
    if   option == 1:
        n_pags = documentos_admissao()
        values = [[data, 'Documentos de Admissão', n_pags, time.time()-st]]
    elif option == 2:
        n_pags = documentos_rescisao()
        values = [[data, 'Documentos de Rescisão', n_pags, time.time()-st]]
    elif option == 3:
        n_pags = boletos_bmp()
        values = [[data, 'Boletos BMP', n_pags, time.time()-st]]
    elif option == 4:
        n_pags = boletos_cobranca()
        values = [[data, 'Boletos de Cobrança', n_pags, time.time()-st]]
    elif option == 5:
        n_pags = fichas_de_registro()
        values = [[data, 'Fichas de Registro', n_pags, time.time()-st]]
    elif option == 6:
        n_pags = folha_rescisao_ferias()
        values = [[data, 'Folha de Pagamento, Férias e Rescisão', n_pags, time.time()-st]]
    elif option == 7:
        n_pags = guias_fgts()
        values = [[data, 'Guias FGTS', n_pags, time.time()-st]]
    elif option == 8:
        n_pags = listagem_conferencia()
        values = [[data, 'Listagem de Conferência', n_pags, time.time()-st]]
    elif option == 9:
        n_pags = recibos_pagamento()
        values = [[data, 'Recibos de Pagamento', n_pags, time.time()-st]]
    elif option == 10:
        n_pags = recibos_folk()
        values = [[data, 'Recibos FOLK', n_pags, time.time()-st]]
    elif option == 11:
        n_pags = rel_servicos_adm()
        values = [[data, 'Relatório de Serviços Administrativos', n_pags, time.time()-st]]
    elif option == 12:
        n_pags = resumo_geral_mes_periodo()
        values = [[data, 'Resumo Geral Mês/Período', n_pags, time.time()-st]]
    elif option == 31:
        n_pags = nfs_curitiba()
        values = [[data, 'NFs Curitiba', n_pags, time.time()-st]]
    elif option == 32:
        n_pags = nfs_fortaleza()
        values = [[data, 'NFs Fortaleza', n_pags, time.time()-st]]
    elif option == 33:
        n_pags = nfs_salvador()
        values = [[data, 'NFs Salvador', n_pags, time.time()-st]]
    elif option == 34:
        n_pags = nfs_sorocaba()
        values = [[data, 'NFs Sorocaba', n_pags, time.time()-st]]

    if option != 0:
        salva_relatorio(values)

