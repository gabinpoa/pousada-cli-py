from collections.abc import Callable
from os import system, name as sysname
from uteis import indice

class MenuItem:
    def __init__(self, codigo: int, nome: str, funcao: Callable[[], None]):
        self.codigo = codigo
        self.nome = nome
        self.funcao = funcao

class Menu:
    def __init__(self, itens: list[MenuItem]):
        self.__itens = itens
        self.__indice_selecionado: int = -1

    def __limpar(self):
        if sysname == 'nt':
            system('cls')
        else:
            system('clear')

    def __mostrar_itens(self):
        for item in self.__itens:
            print(f'{item.codigo} - {item.nome}')

    ## Retorna booleano para indicar se o programa deve continuar
    def __seleciona_item(self) -> bool:
        codigo = int(input("Qual ação você quer realizar? "))
        indice_item = indice(self.__itens, lambda item : item.codigo == codigo)
        if codigo == -1:
            self.__limpar()
            print("!    Selecione uma opção existente   !")
            return self.__seleciona_item()
        elif codigo == 0:
            self.__limpar()
            print("Saindo do programa")
            return False
        else:
            self.__indice_selecionado = indice_item
            return True

    def __acionar_item(self):
        self.__limpar()
        print(f'Selecionado: {self.__itens[self.__indice_selecionado].nome}')
        self.__itens[self.__indice_selecionado].funcao()

    def iniciar(self):
        self.__mostrar_itens()
        while True:
            if self.__seleciona_item() == True:
                self.__acionar_item()
            else:
                break
