from typing import Literal
from produto import Produto

class CategoriaQuarto:
    STANDARD = 'S'
    MASTER   = 'M'
    PREMIUM  = 'P'

type Categoria = Literal['S', 'M', 'P']

class Quarto:
    def __init__(self, numero: int, categoria: str | Categoria, diaria: float, consumo: list[int] = []):
        self.__numero = numero
        self.__categoria = categoria
        self.__diaria = diaria
        self.__consumo = consumo

    @property
    def numero(self):
        return self.__numero
    @numero.setter
    def numero(self, numero: int):
        self.__numero = numero

    @property
    def categoria(self) -> str | Categoria:
        return self.__categoria
    @categoria.setter
    def categoria(self, categoria: Categoria):
        self.__categoria = categoria

    @property
    def diaria(self):
        return self.__diaria
    @diaria.setter
    def diaria(self, diaria: float):
        self.__diaria = diaria

    @property
    def consumo(self):
        return self.__consumo
    @consumo.setter
    def consumo(self, consumo: list[int]):
        self.__consumo = consumo

    def __str__(self) -> str:
        """Retorna str com dados do quarto"""
        return f'Quarto {self.numero}:\n\tCategoria: {self.categoria}\n\tDiaria: R$ {self.diaria:.2f}'

    def adiciona_consumo(self, codigo_produto: int):
        """Adiciona código do produto recebido por parametro a lista de consumo"""
        self.consumo.append(codigo_produto)

    def lista_consumo(self, produtos: list[Produto]) -> list[Produto]:
        """
        Recebe lista de produtos da pousada por parametro.
        Retorna lista de produtos com código armazenado na lista de consumo.
        """
        produtos_consumidos = []
        for codigo_produto in self.consumo:
            for produto in produtos:
                if codigo_produto == produto.codigo:
                    produtos_consumidos.append(produto)
        return produtos_consumidos

    def imprime_consumo(self, produtos: list[Produto]):
        """
        Recebe lista de produtos da pousada por parametro e passa para método lista_consumo.
        Imprime cada produto retornado por lista_consumo.
        """
        produtos_consumidos = self.lista_consumo(produtos)
        for produto in produtos_consumidos:
            print(produto)

    def valor_total_consumo(self, produtos: list[Produto]) -> float:
        """
        Recebe lista de produtos da pousada por parametro e passa para método lista_consumo.
        Soma o preço de cada produto retornado por lista_consumo.
        Retorna o total da soma.
        """
        valor_total = 0.0
        produtos_consumidos = self.lista_consumo(produtos)
        for produto in produtos_consumidos:
            valor_total += produto.preco
        return valor_total

    def limpa_consumo(self):
        """Esvazia a lista de consumo"""
        self.consumo = []
