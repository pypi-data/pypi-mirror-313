from typing import Optional

from pydantic import BaseModel, Field


class RpaProcesso(BaseModel):
    uuidProcesso: str = Field(..., alias="uuidProcesso")
    nomProcesso: str = Field(..., alias="nomProcesso")
    desProcesso: str = Field(..., alias="desProcesso")
    informacoes: Optional[str] = Field(None, alias="informacoes")
    prioridade: Optional[int] = Field(None, alias="prioridade")
    tempoMedio: Optional[int] = Field(None, alias="tempoMedio")
    ativo: bool = Field(..., alias="ativo")
    uuidRoboPreferencia: Optional[str] = Field(None, alias="uuidRoboPreferencia")
    uuidRoboPosFalha: Optional[str] = Field(None, alias="uuidRoboPosFalha")
    notificarFalha: bool = Field(..., alias="notificarFalha")
    gerarTarefaPosFalha: bool = Field(..., alias="gerarTarefaPosFalha")
    reenfileirarPosFalha: bool = Field(..., alias="reenfileirarPosFalha")
    campos: dict = Field(..., alias="campos")
    tipo: Optional[str] = Field(None, alias="tipo")
    deadline: int = Field(..., alias="deadline")
    urlDocumentacao: Optional[str] = Field(None, alias="urlDocumentacao")
    processamentoMax: int = Field(..., alias="processamentoMax")

    class Config:
        populate_by_name = True
