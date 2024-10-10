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
        self.__arquivo_reservas = Arquivo(Produto)
        self.__arquivo_quartos = Arquivo(Quarto)
        self.__arquivo_produtos = Arquivo(Reserva)

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
            self.__produtos = lista_quartos

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
            self.__produtos = lista_reservas

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

    def __coleta_data_e_quarto_usuario(self) -> tuple[data, Quarto]:
        data_hoje = data.today()

        dia = input("(Deixe em branco para {}) DIA: ".format(data_hoje.day))
        mes = input("(Deixe em branco para {}) MÊS: ".format(data_hoje.month))
        ano = input("(Deixe em branco para {}) ANO: ".format(data_hoje.year))
        n_quarto = input("N° QUARTO:")
        for input_usuario in (ano,mes,dia,n_quarto):
            if not input_usuario.isdigit():
                raise TypeError("Inputs de dia, mês, ano e número do quarto devem ser inteiros")

        if dia == "": dia = data_hoje.day
        else: dia = int(dia)

        if mes == "": mes = data_hoje.month
        else: mes = int(mes)

        if ano == "": ano = data_hoje.year
        else: ano = int(ano)

        n_quarto = int(n_quarto)

        quarto_a_buscar = encontra(self.quartos, lambda quarto : n_quarto == quarto.numero)
        if not quarto_a_buscar:
            raise ValueError("Nenhum quarto com número {} foi encontrado".format(n_quarto))

        data_a_buscar = data.frombrformat("{}/{}/{}".format(dia, mes, ano))
        return data_a_buscar, quarto_a_buscar

    def __cliente_disponivel(self, cliente: str) -> bool:
        for reserva in self.reservas:
            if reserva.cliente == cliente and (reserva.status == StatusReserva.ATIVA or reserva.status == StatusReserva.CHECK_IN):
                return False
        return True

    def __cria_funcao_busca_reseva(self, nome_cliente: str, numero_quarto: str, data_buscada: str):
        if len(nome_cliente) > 0:
            return lambda reserva : nome_cliente == reserva.cliente and reserva.status == StatusReserva.ATIVA
        elif len(numero_quarto) > 0:
            return lambda reserva : numero_quarto == reserva.quarto and reserva.status == StatusReserva.ATIVA
        elif len(data_buscada) > 0:
            return lambda reserva : data_buscada == reserva.dia_inicio and reserva.status == StatusReserva.ATIVA
        else:
            raise ValueError("Todos os parametros de busca foram deixados vazios.")

    def __encontra_varias_reservas(self, funcao_busca: Callable[[Reserva], bool]):
        reservas = encontra_varios(self.reservas, funcao_busca)
        if len(reservas) == 0:
            raise ValueError("Nenhuma reserva encontrada com os parametros informados.")
        return reservas

    def carrega_dados(self):
        self.produtos = self.__arquivo_produtos.carrega_dados()
        self.quartos = self.__arquivo_quartos.carrega_dados()
        self.reservas = self.__arquivo_reservas.carrega_dados()

    def salva_dados(self):
        """Remove as reservas canceladas ou com checkout realizado
            e salva dados das reservas, quartos e produtos em seus respectivos arquivos"""
        self.reservas = list(filter(lambda reserva : reserva.status not in (StatusReserva.CHECK_OUT, StatusReserva.CANCELADA), self.reservas))
        self.__arquivo_produtos.salva_dados(self.produtos)
        self.__arquivo_quartos.salva_dados(self.quartos)
        self.__arquivo_reservas.salva_dados(self.reservas)

    def consulta_disponibilidade(self):
        data_a_buscar, quarto_a_buscar = self.__coleta_data_e_quarto_usuario()

        disponivel = self.__data_disponivel_quarto(data_a_buscar, quarto_a_buscar.numero)
        if disponivel:
            print("DISPONÍVEL. Quarto {} está disponível para a data {}.".format(quarto_a_buscar, data_a_buscar))
            print(quarto_a_buscar)
        else:
            print("INDISPONÍVEL. Quarto {} NÃO está disponível para a data {}.".format(quarto_a_buscar, data_a_buscar))

    def consulta_reserva(self):
        nome_cliente = input("Insira o nome do hóspede para buscar reserva: ")
        numero_quarto = input("Insira o número do quarto para buscar reserva: ")
        data_buscada = input("Insira a data da reserva: `dd/mm/aaaa` ")
        def funcao_busca(reserva: Reserva) -> bool:
            condicao_de_busca = reserva.status == StatusReserva.ATIVA
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
        for reserva in reservas_correspondentes:
            print("Data de início: {}\nData de fim: {}".format(reserva.dia_inicio, reserva.dia_fim))
            print("Nome do cliente: {}".format(reserva.cliente))
            quarto_reserva = reserva.obj_quarto(self.quartos)
            print(quarto_reserva)
            print("Produtos consumidos:")
            for produto in quarto_reserva.lista_consumo(self.produtos):
                print("\t\t{}".format(produto))
            
    def realiza_reserva(self):
        input_data_inicio = input("Insira a data de início da reserva: `dd/mm/aaaa` ")
        input_data_fim = input("Insira a data de fim da reserva: `dd/mm/aaaa` ")
        numero_quarto = int(input("Insira o número do quarto: "))
        nome_cliente = input("Insira o nome do hóspede: ")
        
        data_inicio = data.frombrformat(input_data_inicio)
        data_fim = data.frombrformat(input_data_fim)
        
        quarto_disponivel = self.__datas_disponiveis_quarto(data_inicio, data_fim, numero_quarto)
        cliente_disponivel = self.__cliente_disponivel(nome_cliente)
        if not quarto_disponivel:
            raise ValueError("INDISPONÍVEL. Quarto {} NÃO está disponível para a data informada.".format(numero_quarto))
        elif not cliente_disponivel:
            raise ValueError("'{}' já possui uma reserva em andamento.".format(nome_cliente))
        else:
            self.reservas.append(Reserva(input_data_inicio, input_data_fim, nome_cliente, numero_quarto))
            print("Reserva do quarto {} entre os dias {} e {} efetuada com sucesso.".format(numero_quarto, data_inicio, data_fim))
        
    def cancela_reserva(self):
        nome_cliente = input("Insira o nome do hóspede: ")
        reserva = encontra(self.reservas, lambda reserva : reserva.cliente == nome_cliente and reserva.status == StatusReserva.ATIVA)
        if not reserva:
            raise ValueError("Nenhuma reserva ativa no nome de {}.".format(nome_cliente))
        reserva.cancela()
        print("Reserva cancelada.")

    def realiza_checkin(self):
        nome_cliente = input("Insira o nome do hóspede: ")
        reserva = encontra(self.reservas, lambda reserva : reserva.cliente == nome_cliente and reserva.status == StatusReserva.CHECK_IN)
        if not reserva:
            raise ValueError("Nenhuma reserva para check-in no nome de {}.".format(nome_cliente))

        quantidade_dias, valor_total_diarias, quarto = reserva.infos(self.quartos)

        print("Data de início: {}\nData de fim: {}".format(reserva.dia_inicio, reserva.dia_fim))
        print("Dias reservados: {}".format(quantidade_dias))
        print("Valor total das diárias: R$ {:.2f}".format(valor_total_diarias))
        print(quarto)

        reserva.checkin()

    def realiza_checkout(self):
        nome_cliente = input("Insira o nome do hóspede: ")
        reserva = encontra(self.reservas, lambda reserva : reserva.cliente == nome_cliente and reserva.status == StatusReserva.ATIVA)
        if not reserva:
            raise ValueError("Nenhuma reserva ativa no nome de {}.".format(nome_cliente))

        quantidade_dias, valor_total_diarias, quarto = reserva.infos(self.quartos)
        valor_total_consumo = quarto.valor_total_consumo(self.produtos)
        valor_final = valor_total_consumo + valor_total_diarias

        print("Data de início: {}\nData de fim: {}".format(reserva.dia_inicio, reserva.dia_fim))
        print("Dias reservados: {}".format(quantidade_dias))
        print("Valor total das diárias: R$ {:.2f}".format(valor_total_diarias))
        print(quarto)
        quarto.imprime_consumo(self.produtos)
        print("Valor total dos produtos consumidos: R$ {:.2f}".format(valor_total_consumo))
        print("Valor final: R$ {:.2f}".format(valor_final))

        reserva.checkout()
        quarto.limpa_consumo()

    def registra_consumo(self):
        nome_cliente = input("Insira o nome do hóspede: ")
        reserva = encontra(self.reservas, lambda reserva : reserva.cliente == nome_cliente and reserva.status == StatusReserva.ATIVA)
        if not reserva:
            raise ValueError("Nenhuma reserva ativa no nome de {}.".format(nome_cliente))

        print("Produtos disponíveis: ")
        for produto in self.produtos:
            print("\t{} - {}".format(produto.codigo, produto))

        produto_selecionado = int(input("Insira o código associado ao produto que deseja: "))
        if not encontra(self.produtos, lambda produto: produto.codigo == produto_selecionado):
            raise ValueError("Código inserido '{}' não corresponde a nenhum produto.".format(produto_selecionado))

        quarto = reserva.obj_quarto(self.quartos)
        quarto.adiciona_consumo(produto_selecionado)


