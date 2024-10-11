from collections.abc import Callable

# Funcao para substituir list.index()
# Diferença: Quando item não é encontrado na lista, retorna -1 ao invés de levantar um erro
def indice[T](lista: list[T], funcao: Callable[[T], bool]) -> int:
    for i, item in enumerate(lista):
        if funcao(item) == True:
            return i
    return -1

def encontra[T](lista: list[T], funcao: Callable[[T], bool]) -> T | None:
    for item in lista:
        if funcao(item) == True:
            return item

def encontra_varios[T](lista: list[T], funcao: Callable[[T], bool]) -> list[T]:
    itens_correspondentes = []
    for item in lista:
        if funcao(item) == True:
            itens_correspondentes.append(item)
    return itens_correspondentes

