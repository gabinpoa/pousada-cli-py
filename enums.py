from enum import Enum

class StatusReserva(Enum):
    ATIVA = 'A'
    CANCELADA = 'C'
    CHECK_IN = 'I'
    CHECK_OUT = 'O'

class CategoriaQuarto(Enum):
    STANDARD = 'S'
    MASTER = 'M'
    PREMIUM = 'P'