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
        print("0 - Sair")
        for item in self.__itens:
            print(f'{item.codigo} - {item.nome}')

    def __seleciona_item(self) -> bool:
        """Retorna booleano para indicar se o programa deve continuar"""
        codigo = int(input("Qual ação você quer realizar? "))
        if codigo == 0:
            self.__limpar()
            print("Saindo do programa")
            return False

        indice_item = indice(self.__itens, lambda item : item.codigo == codigo)
        if indice_item == -1:
            self.__limpar()
            print("!    Selecione uma opção existente   !")
            return self.__seleciona_item()
        else:
            self.__indice_selecionado = indice_item
            return True

    def __acionar_item(self):
        self.__limpar()
        print(f'Selecionado: {self.__itens[self.__indice_selecionado].nome}')
        self.__itens[self.__indice_selecionado].funcao()

    def iniciar(self):
        while True:
            self.__mostrar_itens()
            if self.__seleciona_item() == True:
                try:
                    self.__acionar_item()
                except ValueError as e:
                    print(e)
                finally:
                    print("\n")
            else:
                break

    @classmethod
    def cliente(cls, funcao: Callable[[str], None]):
        cliente = input("Nome do hóspede: ")
        return lambda : funcao(cliente)

    @classmethod
    def dia_n_quarto(cls, funcao: Callable[[int, int], None]):
        n_quarto = int(input("Número do quarto: "))
        dia = int(input("Dia: "))
        return lambda : funcao(dia, n_quarto)

    @classmethod
    def data_cliente_n_quarto(cls, funcao: Callable[[tuple[int, int], str, int], None]):
        data = int(input("Dia de início: ")), int(input("Dia de fim: "))
        cliente = input("Nome do hóspede: ")
        n_quarto = int(input("Número do quarto: "))
        return lambda : funcao(data, cliente, n_quarto)

    @classmethod
    def str_dia_cliente_n_quarto_opcional(cls, funcao: Callable[[str, str, str], None]):
        dia = input("Dia (ENTER para pular): ")
        cliente = input("Nome do hóspede (ENTER para pular):  ")
        n_quarto = input("Número do quarto (ENTER para pular): ")
        return lambda : funcao(dia, cliente, n_quarto)
