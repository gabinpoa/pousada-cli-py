from enums import CategoriaQuarto
from produto import Produto

class Quarto:
    def __init__(self, numero: int, categoria: str, diaria: float, consumo: list[int] = []):
        self.__numero = numero
        self.__categoria = categoria
        self.__diaria = diaria
        self.__consumo = consumo

    @property
    def numero(self):
        return self.__numero
    @numero.setter
    def numero(self, numero):
        self.__numero = numero

    @property
    def categoria(self):
        return self.__categoria
    @categoria.setter
    def categoria(self, categoria: CategoriaQuarto):
        self.__categoria = categoria.value

    @property
    def diaria(self):
        return self.__diaria
    @diaria.setter
    def diaria(self, diaria):
        self.__diaria = diaria

    @property
    def consumo(self):
        return self.__consumo
    @consumo.setter
    def consumo(self, consumo: list[int]):
        self.__consumo = consumo

    def __str__(self) -> str:
        return f'Quarto {self.numero}:\n\tCategoria: {self.categoria}\n\tDiaria: R$ {self.diaria:.2f}'

    def adiciona_consumo(self, codigo_produto: int):
        self.consumo.append(codigo_produto)

    def lista_consumo(self, produtos: list[Produto]) -> list[Produto]:
        produtos_consumidos = []
        for codigo_produto in self.consumo:
            for produto in produtos:
                if codigo_produto == produto.codigo:
                    produtos_consumidos.append(produto)
        return produtos_consumidos

    def imprime_consumo(self, produtos: list[Produto]):
        produtos_consumidos = self.lista_consumo(produtos)
        for produto in produtos_consumidos:
            print(produto)

    def valor_total_consumo(self, produtos: list[Produto]) -> float:
        valor_total = 0.0
        produtos_consumidos = self.lista_consumo(produtos)
        for produto in produtos_consumidos:
            valor_total += produto.preco
        return valor_total

    def limpa_consumo(self):
        self.consumo = []
