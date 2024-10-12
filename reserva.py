from enums import StatusReserva
from uteis import encontra
from quarto import Quarto
from data import data

class Reserva:
    def __init__(self, dia_inicio: str, dia_fim: str, cliente: str, quarto: int, status: str = StatusReserva.CHECK_IN.value):
        self.__dia_inicio = dia_inicio
        self.__dia_fim = dia_fim
        self.__cliente = cliente
        self.__quarto = quarto
        self.__status = status

    @property
    def dia_inicio(self):
        return self.__dia_inicio
    @dia_inicio.setter
    def dia_inicio(self, dia_inicio):
        self.__dia_inicio = dia_inicio

    @property
    def dia_fim(self):
        return self.__dia_fim
    @dia_fim.setter
    def dia_fim(self, dia_fim):
        self.__dia_fim = dia_fim

    @property
    def cliente(self):
        return self.__cliente
    @cliente.setter
    def cliente(self, cliente):
        self.__cliente = cliente

    @property
    def quarto(self):
        return self.__quarto
    @quarto.setter
    def quarto(self, quarto):
        self.__quarto = quarto

    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self, status: StatusReserva):
        self.__status = status.value

    def infos(self, quartos: list[Quarto]) -> tuple[int, float, Quarto]:
        quarto = self.obj_quarto(quartos)
        quantidade_dias = data.frombrformat(self.dia_fim).toordinal() - data.frombrformat(self.dia_inicio).toordinal()
        valor_total_diarias = quantidade_dias * quarto.diaria
        return quantidade_dias, valor_total_diarias, quarto

    def obj_quarto(self, quartos: list[Quarto]) -> Quarto:
        quarto = encontra(quartos, lambda quarto : quarto.numero == self.quarto)
        if not quarto:
            raise ValueError("Número do quarto na reserva não corresponde a nenhum quarto.")
        return quarto

    def cancela(self):
        self.status = StatusReserva.CANCELADA

    def checkin(self):
        self.status = StatusReserva.ATIVA

    def checkout(self):
        self.status = StatusReserva.CHECK_OUT
