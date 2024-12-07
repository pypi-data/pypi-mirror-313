# resposta_solicitacao_cobranca.py


from dataclasses import dataclass, asdict
from typing import Any, Dict

from bancointer.pix.models.pix import Pix
from bancointer.pix.models.calendario import Calendario
from bancointer.pix.models.devedor_recebedor_cobranca import DevedorRecebedorCobranca
from bancointer.pix.models.id_loc_payload import IdentificadorLocalizacaoPayload
from bancointer.pix.models.info_adicional_cobranca_imediata import (
    InfoAdicionalCobrancaImediata,
)
from bancointer.pix.models.status_cobranca_imediata import StatusCobrancaImediata
from bancointer.pix.models.valor_cobranca import ValorCobranca


@dataclass
class RespostaSolicitacaoCobrancaImediata(object):
    status: StatusCobrancaImediata
    valor: ValorCobranca
    calendario: Calendario
    txid: str
    revisao: int
    chave: str
    devedor: DevedorRecebedorCobranca = None
    loc: IdentificadorLocalizacaoPayload = None
    location: str = None
    pixCopiaECola: str = None
    solicitacaoPagador: str = None
    infoAdicionais: [InfoAdicionalCobrancaImediata] = None
    pix: [Pix] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
