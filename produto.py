class Produto:
    def __init__(self, codigo: int, nome: str, preco: float):
        self.__codigo = codigo
        self.__nome = nome
        self.__preco = preco

    @property
    def codigo(self):
        return self.__codigo
    @codigo.setter
    def codigo(self, codigo: int):
        self.__codigo = codigo

    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def preco(self):
        return self.__preco
    @preco.setter
    def preco(self, preco: float):
        self.__preco = preco

    def __str__(self) -> str:
        """Retorna str com nome e preço do produto"""
        return f'{self.nome}: R$ {self.preco:.2f}'
