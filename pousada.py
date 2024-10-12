from collections.abc import Callable
from quarto import Quarto
from reserva import Reserva, StatusReserva
from produto import Produto
from arquivo import Arquivo
from uteis import encontra, encontra_varios
from data import data

class Pousada:
    def __init__(self, nome: str, contato: str, quartos: list[Quarto] = [], produtos: list[Produto] = []):
        self.__nome = nome
        self.__contato = contato
        self.__reservas: list[Reserva] = []
        self.__quartos = quartos
        self.__produtos = produtos
        self.__arquivo_reservas = Arquivo(Reserva)
        self.__arquivo_quartos = Arquivo(Quarto)
        self.__arquivo_produtos = Arquivo(Produto)

    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def contato(self):
        return self.__contato
    @contato.setter
    def contato(self, contato):
        self.__contato = contato

    @property
    def quartos(self):
        return self.__quartos
    @quartos.setter
    def quartos(self, lista_quartos):
        erro = False
        if not isinstance(lista_quartos, list):
            print("Erro: Tentativa de atribuir a 'Pousada.__reservas' elemento de tipo {}, esperava-se list[Quarto]".format(type(lista_quartos)))
            erro = True
        for quarto in lista_quartos:
            if not isinstance(quarto, Quarto):
                print("Erro: Tentativa de atribuir a 'Pousada.__quartos' list[{}], esperava-se list[Quarto]".format(type(quarto)))
                erro = True
        if not erro:
            self.__quartos = lista_quartos

    @property
    def reservas(self):
        return self.__reservas
    @reservas.setter
    def reservas(self, lista_reservas):
        erro = False
        if not isinstance(lista_reservas, list):
            print("Erro: Tentativa de atribuir a 'Pousada.__reservas' elemento de tipo {}, esperava-se list[Reserva]".format(type(lista_reservas)))
            erro = True
        for reserva in lista_reservas:
            if not isinstance(reserva, Reserva):
                print("Erro: Tentativa de atribuir a 'Pousada.__reservas' list[{}], esperava-se list[Reserva]".format(type(reserva)))
                erro = True
        if not erro:
            self.__reservas = lista_reservas

    @property
    def produtos(self):
        return self.__produtos
    @produtos.setter
    def produtos(self, lista_produtos):
        erro = False
        if not isinstance(lista_produtos, list):
            print("Erro: Tentativa de atribuir a 'Pousada.__produtos' elemento de tipo {}, esperava-se list[Produto]".format(type(lista_produtos)))
            erro = True
        for produto in lista_produtos:
            if not isinstance(produto, Produto):
                print("Erro: Tentativa de atribuir a 'Pousada.__produtos' list[{}], esperava-se list[Produto]".format(type(produto)))
                erro = True
        if not erro:
            self.__produtos = lista_produtos

    def __data_disponivel_quarto(self, data_buscada: data, quarto: int) -> bool:
        for reserva in self.reservas:
            data_inicio = data.frombrformat(reserva.dia_inicio)
            data_fim = data.frombrformat(reserva.dia_fim)
            if reserva.quarto == quarto and data_buscada >= data_inicio and data_buscada <= data_fim:
                return False
        return True

    def __datas_disponiveis_quarto(self, data_inicio_busca: data, data_fim_busca: data, quarto_busca: int) -> bool:
        for reserva in self.reservas:
            data_inicio = data.frombrformat(reserva.dia_inicio)
            data_fim = data.frombrformat(reserva.dia_fim)
            if reserva.quarto == quarto_busca and not (data_fim_busca < data_inicio or data_inicio_busca > data_fim):
                return False
        return True

    def __get_date_from_user(self):
        data_hoje = data.hoje()

        dia = input("Insira o dia (ENTER para {}): ".format(data_hoje.day, ))
        mes = input("Insira o mês (ENTER para {}): ".format(data_hoje.month, ))
        ano = input("Insira o ano (ENTER para {}): ".format(data_hoje.year, ))

        dia = data_hoje.day if dia == "" else int(dia)
        mes = data_hoje.month if mes == "" else int(mes)
        ano = data_hoje.year if ano == "" else int(ano)

        return data(ano, mes, dia)

    def __cliente_disponivel(self, cliente: str) -> bool:
        for reserva in self.reservas:
            if reserva.cliente == cliente and (reserva.status == StatusReserva.ATIVA.value or reserva.status == StatusReserva.CHECK_IN.value):
                return False
        return True

    def __encontra_varias_reservas(self, funcao_busca: Callable[[Reserva], bool]):
        reservas = encontra_varios(self.reservas, funcao_busca)
        return reservas

    def __get_nome_from_user(self):
        nome = input("Insira o nome do hóspede: ")
        if nome == "":
            raise ValueError("Nome do hóspede não pode estar vazio")
        return nome

    def carrega_dados(self):
        self.produtos = self.__arquivo_produtos.carrega_dados()
        self.quartos = self.__arquivo_quartos.carrega_dados()
        self.reservas = self.__arquivo_reservas.carrega_dados()

    def salva_dados(self):
        """Remove as reservas canceladas ou com checkout realizado
            e salva dados das reservas, quartos e produtos em seus respectivos arquivos"""
        self.reservas = list(filter(lambda r : r.status not in (StatusReserva.CHECK_OUT.value, StatusReserva.CANCELADA.value), self.reservas))
        self.__arquivo_produtos.salva_dados(self.produtos)
        self.__arquivo_quartos.salva_dados(self.quartos)
        self.__arquivo_reservas.salva_dados(self.reservas)

    def consulta_disponibilidade(self):
        data_a_buscar = self.__get_date_from_user()
        n_quarto = int(input("Número do quarto: "))

        quarto_a_buscar = encontra(self.quartos, lambda q : n_quarto == q.numero)
        if not quarto_a_buscar:
            raise ValueError("Nenhum quarto com número {} foi encontrado".format(n_quarto))

        disponivel = self.__data_disponivel_quarto(data_a_buscar, quarto_a_buscar.numero)
        if disponivel:
            print("DISPONÍVEL. Quarto {} está disponível para a data {}.\n".format(quarto_a_buscar.numero, data_a_buscar))
            print(quarto_a_buscar)
        else:
            print("INDISPONÍVEL. Quarto {} NÃO está disponível para a data {}.".format(quarto_a_buscar, data_a_buscar))

    def consulta_reserva(self):
        nome_cliente = input("Insira o nome do hóspede: ")
        numero_quarto = input("Insira o número do quarto: ")
        data_buscada = input("Insira a data da reserva: `dd/mm/aaaa` ")

        def funcao_busca(reserva: Reserva) -> bool:
            condicao_de_busca = reserva.status == StatusReserva.ATIVA.value
            if len(nome_cliente) > 0:
                condicao_de_busca = condicao_de_busca and nome_cliente == reserva.cliente 
            if len(numero_quarto) > 0:
                condicao_de_busca = condicao_de_busca and numero_quarto == reserva.quarto 
            if len(data_buscada) > 0:
                condicao_de_busca = condicao_de_busca and data_buscada == reserva.dia_inicio 
            if len(data_buscada) == 0 and len(numero_quarto) == 0 and len(nome_cliente) == 0:
                condicao_de_busca = False
            return condicao_de_busca

        reservas_correspondentes = self.__encontra_varias_reservas(funcao_busca)
        if len(reservas_correspondentes) == 0:
            print("Nenhuma reserva encontrada com os parametros informados.")

        for reserva in reservas_correspondentes:
            print("Data de início: {}\nData de fim: {}".format(reserva.dia_inicio, reserva.dia_fim))
            print("Nome do cliente: {}".format(reserva.cliente))
            quarto_reserva = reserva.obj_quarto(self.quartos)
            print(quarto_reserva)
            print("Produtos consumidos:")
            for produto in quarto_reserva.lista_consumo(self.produtos):
                print("\t\t{}".format(produto))
            
    def realiza_reserva(self):
        print("Data de início da reserva: ")
        data_inicio = self.__get_date_from_user()
        print("Data de fim da reserva: ")
        data_fim = self.__get_date_from_user()
        numero_quarto = int(input("Insira o número do quarto: "))
        nome_cliente = self.__get_nome_from_user()
        
        quarto_disponivel = self.__datas_disponiveis_quarto(data_inicio, data_fim, numero_quarto)
        if not quarto_disponivel:
            raise ValueError("INDISPONÍVEL. Quarto {} NÃO está disponível para a data informada.".format(numero_quarto))
        cliente_disponivel = self.__cliente_disponivel(nome_cliente)
        if not cliente_disponivel:
            raise ValueError("{} já possui uma reserva em andamento.".format(nome_cliente))

        self.reservas.append(Reserva(str(data_inicio), str(data_fim), nome_cliente, numero_quarto))
        print("\nReserva do quarto {} entre os dias {} e {} efetuada com sucesso.".format(numero_quarto, data_inicio, data_fim))
        
    def cancela_reserva(self):
        nome_cliente = self.__get_nome_from_user()
        reserva = encontra(self.reservas, lambda r : r.cliente == nome_cliente and r.status == StatusReserva.ATIVA.value)
        if not reserva:
            raise ValueError("Nenhuma reserva ativa no nome de {}.".format(nome_cliente))
        quarto = reserva.obj_quarto(self.quartos)
        reserva.cancela()
        quarto.limpa_consumo()
        print("Reserva cancelada")

    def realiza_checkin(self):
        nome_cliente = self.__get_nome_from_user()
        reserva = encontra(self.reservas, lambda r : r.cliente == nome_cliente and r.status == StatusReserva.CHECK_IN.value)
        if not reserva:
            raise ValueError("Nenhuma reserva para check-in no nome de {}.".format(nome_cliente))

        qnt_dias, valor_diarias, quarto = reserva.infos(self.quartos)

        print("Data de início: {}\nData de fim: {}".format(reserva.dia_inicio, reserva.dia_fim))
        print("Dias reservados: {}".format(qnt_dias))
        print("Valor total das diárias: R$ {:.2f}".format(valor_diarias))
        print(quarto)

        reserva.checkin()
        print("Check-in realizado")

    def realiza_checkout(self):
        nome_cliente = self.__get_nome_from_user()
        reserva = encontra(self.reservas, lambda r : r.cliente == nome_cliente and r.status == StatusReserva.ATIVA.value)
        if not reserva:
            raise ValueError("Nenhuma reserva ativa no nome de {}.".format(nome_cliente))

        qnt_dias, valor_diarias, quarto = reserva.infos(self.quartos)
        valor_consumo = quarto.valor_total_consumo(self.produtos)
        valor_final = valor_consumo + valor_diarias

        print("Data de início: {}\nData de fim: {}".format(reserva.dia_inicio, reserva.dia_fim))
        print("Dias reservados: {}".format(qnt_dias))
        print("Valor total das diárias: R$ {:.2f}".format(valor_diarias))
        print(quarto)
        quarto.imprime_consumo(self.produtos)
        print("Valor total dos produtos consumidos: R$ {:.2f}".format(valor_consumo))
        print("Valor final: R$ {:.2f}".format(valor_final))

        reserva.checkout()
        quarto.limpa_consumo()
        print("Check-out realizado")

    def registra_consumo(self):
        nome_cliente = self.__get_nome_from_user()
        reserva = encontra(self.reservas, lambda r : r.cliente == nome_cliente and r.status == StatusReserva.ATIVA.value)
        if not reserva:
            raise ValueError("Nenhuma reserva ativa no nome de {}.".format(nome_cliente))

        print("Produtos disponíveis: ")
        for produto in self.produtos:
            print("\t{} - {}".format(produto.codigo, produto))

        codigo_selecionado = int(input("Insira o código associado ao produto que deseja: "))
        produto_selecionado = encontra(self.produtos, lambda p: p.codigo == codigo_selecionado)
        if not produto_selecionado:
            raise ValueError("Código inserido '{}' não corresponde a nenhum produto.".format(produto_selecionado))

        quarto = reserva.obj_quarto(self.quartos)
        quarto.adiciona_consumo(codigo_selecionado)
        print("Novo consumo para reserva de {} registrado: {}".format(nome_cliente, produto_selecionado))


