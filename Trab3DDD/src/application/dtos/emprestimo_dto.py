from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class EmprestimoDTO:
    """
    DTO para transferência de dados de Emprestimo
    """
    id: Optional[str] = None
    livro_id: str = ""
    usuario_id: str = ""
    data_emprestimo: Optional[datetime] = None
    data_devolucao_prevista: Optional[datetime] = None
    data_devolucao_real: Optional[datetime] = None
    multa: float = 0.0
    esta_em_atraso: bool = False
    dias_atraso: int = 0