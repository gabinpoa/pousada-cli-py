from collections.abc import Callable

def indice[T](lista: list[T], funcao_busca: Callable[[T], bool]) -> int:
    """
    Retorna o indice do primeiro item da lista que, passado como parametro a funcao_busca, retornar True.
    Se nenhum item retornar True passado como parametro a funcao_busca, retorna -1.
    funcao_busca: Uma função que recebe um item da lista como parametro.
    Ex: objetivo encontrar o indice da str 'bob' em uma lista com nomes
    >>> lista_nomes = ['ana', 'jorge', 'bob']
    >>> def nome_e_bob(nome: str) -> bool
    >>>    if nome == 'bob':
    >>>        return True
    >>>    else:
    >>>        return False
    >>> indice(lista_nomes, nome_e_bob)
    2
    """
    for i, item in enumerate(lista):
        if funcao_busca(item) == True:
            return i
    return -1

def encontra[T](lista: list[T], funcao_busca: Callable[[T], bool]) -> T | None:
    """
    Retorna o primeiro item da lista que, passado como parametro a funcao_busca, retornar True.
    Se nenhum item retornar True passado como parametro a funcao_busca, não retorna nada.
    funcao_busca: Uma função que recebe um item da lista como parametro.
    Ex: objetivo encontrar o nome que começa com 'b' em uma lista com nomes
    >>> lista_nomes = ['ana', 'jorge', 'bob']
    >>> def nome_comeca_com_b(nome: str) -> bool
    >>>    if nome.startswith('b'):
    >>>        return True
    >>>    else:
    >>>        return False
    >>> encontra(lista_nomes, nome_comeca_com_b)
    'bob'
    """
    for item in lista:
        if funcao_busca(item) == True:
            return item

def encontra_varios[T](lista: list[T], funcao_busca: Callable[[T], bool]) -> list[T]:
    """
    Retorna uma lista com os itens da lista que, passados como parametro a funcao_busca, retornarem True.
    Retorna uma lista vazia se nenhum item retornar True passado como parametro a funcao_busca.
    funcao_busca: Uma função que recebe um item da lista como parametro.
    Ex: objetivo encontrar os nomes que não começam com 'b' em uma lista com nomes
    >>> lista_nomes = ['ana', 'jorge', 'bob']
    >>> def nome_nao_comeca_com_b(nome: str) -> bool
    >>>    if nome.startswith('b'):
    >>>        return True
    >>>    else:
    >>>        return False
    >>> encontra_varios(lista_nomes, nome_nao_comeca_com_b)
    ['ana', 'jorge']
    """
    itens_correspondentes = []
    for item in lista:
        if funcao_busca(item) == True:
            itens_correspondentes.append(item)
    return itens_correspondentes

