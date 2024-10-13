from typing import Literal
from quarto import Quarto

class StatusReserva:
    ATIVA = 'A'
    CANCELADA = 'C'
    CHECK_IN = 'I'
    CHECK_OUT = 'O'

type Status = Literal['A', 'C', 'I', 'O']

class Reserva:
    def __init__(self, dia_inicio: int, dia_fim: int, cliente: str, quarto: Quarto, status: str | Status = 'I'):
        self.__dia_inicio = dia_inicio
        self.__dia_fim = dia_fim
        self.__cliente = cliente
        self.__quarto = quarto
        self.__status = status

    @property
    def dia_inicio(self):
        return self.__dia_inicio
    @dia_inicio.setter
    def dia_inicio(self, dia_inicio: int):
        self.__dia_inicio = dia_inicio

    @property
    def dia_fim(self):
        return self.__dia_fim
    @dia_fim.setter
    def dia_fim(self, dia_fim: int):
        self.__dia_fim = dia_fim

    @property
    def cliente(self):
        return self.__cliente
    @cliente.setter
    def cliente(self, cliente: str):
        self.__cliente = cliente

    @property
    def quarto(self):
        return self.__quarto
    @quarto.setter
    def quarto(self, quarto: Quarto):
        self.__quarto = quarto

    @property
    def status(self) -> str | Status:
        return self.__status
    @status.setter
    def status(self, status: Status):
        self.__status = status

    def valor_diarias(self) -> float:
        """Retorna o valor total das diárias"""
        return self.quantidade_dias() * self.quarto.diaria

    def quantidade_dias(self) -> int:
        """Retorna a duração em dias da reserva"""
        return self.dia_fim - self.dia_inicio

    def cancela(self):
        """Muda status para cancelada e esvazia consumo"""
        self.status = 'C'
        self.quarto.limpa_consumo()

    def checkin(self):
        """Muda status para ativa"""
        self.status = 'A'

    def checkout(self):
        """Muda status para check-out e esvazia consumo"""
        self.status = 'O'
        self.quarto.limpa_consumo()
