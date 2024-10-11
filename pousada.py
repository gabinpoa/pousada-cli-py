from quarto import Quarto
from reserva import Reserva, Status, StatusReserva
from produto import Produto
from arquivo import Arquivo
from uteis import encontra, encontra_varios

class Pousada:
    def __init__(self, nome: str, contato: str, reservas: list[Reserva] = [], quartos: list[Quarto] = [], produtos: list[Produto] = []):
        self.__nome = nome
        self.__contato = contato
        self.__reservas = reservas
        self.__quartos = quartos
        self.__produtos = produtos

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
    def quartos(self, lista_quartos: list[Quarto]):
        self.__quartos = lista_quartos

    @property
    def reservas(self):
        return self.__reservas
    @reservas.setter
    def reservas(self, lista_reservas: list[Reserva]):
        self.__reservas = lista_reservas

    @property
    def produtos(self):
        return self.__produtos
    @produtos.setter
    def produtos(self, lista_produtos: list[Produto]):
        self.__produtos = lista_produtos

    def __dia_disponivel_quarto(self, dia_buscado: int, n_quarto: int) -> bool:
        for reserva in self.reservas:
            if reserva.quarto.numero == n_quarto and dia_buscado in range(reserva.dia_inicio, reserva.dia_fim + 1):
                return False
        return True

    def __dias_disponiveis_quarto(self, dia_inicio_: int, dia_fim_: int, n_quarto: int) -> bool:
        for reserva in self.reservas:
            if reserva.quarto == n_quarto and not (dia_fim_ < reserva.dia_inicio or dia_inicio_ > reserva.dia_fim):
                return False
        return True

    def __cliente_disponivel(self, cliente: str) -> bool:
        for reserva in self.reservas:
            if reserva.cliente == cliente and reserva.status in (StatusReserva.ATIVA, StatusReserva.CHECK_OUT):
                return False
        return True

    def __encontra_reserva_por_cliente(self, status_reserva: Status):
        cliente = input("Insira o nome do hóspede: ")

        reserva = encontra(self.reservas, lambda reserva : reserva.cliente == cliente and reserva.status == status_reserva)
        if not reserva:
            raise ValueError("Nenhuma reserva ativa no nome de {}.".format(cliente))
        return reserva

    def carrega_dados(self):
        self.produtos = Arquivo.carrega_produtos()
        self.quartos = Arquivo.carrega_quartos()
        self.reservas = Arquivo.carrega_reservas(self.quartos)

    def salva_dados(self):
        # Remove as reservas canceladas ou com checkout realizado
        # e salva dados das reservas, quartos e produtos em seus respectivos arquivos
        self.reservas = list(filter(lambda reserva : reserva.status not in (StatusReserva.CHECK_OUT, StatusReserva.CANCELADA), self.reservas))
        Arquivo.salva_produtos(self.produtos)
        Arquivo.salva_quartos(self.quartos)
        Arquivo.salva_reservas(self.reservas)

    def consulta_disponibilidade(self):
        quarto_a_buscar = int(input("Insira o número do quarto: "))
        dia_a_buscar = int(input("Insira o dia para consultar: "))

        disponivel = self.__dia_disponivel_quarto(dia_a_buscar, quarto_a_buscar)
        if disponivel:
            print("DISPONÍVEL. Quarto {} está disponível para o dia {}.".format(quarto_a_buscar, dia_a_buscar))
            print(quarto_a_buscar)
        else:
            print("INDISPONÍVEL. Quarto {} NÃO está disponível para o dia {}.".format(quarto_a_buscar, dia_a_buscar))

    def consulta_reserva(self):
        nome_cliente = input("Insira o nome do hóspede ou ENTER para pular:  ")
        numero_quarto = input("Insira o número do quarto ou ENTER para pular: ")
        dia_buscado = input("Insira o dia da reserva ou ENTER para pular: ")

        def funcao_busca(reserva: Reserva) -> bool:
            condicao_de_busca = reserva.status == StatusReserva.ATIVA
            if len(nome_cliente) > 0:
                condicao_de_busca = condicao_de_busca and nome_cliente == reserva.cliente 
            if len(numero_quarto) > 0:
                condicao_de_busca = condicao_de_busca and numero_quarto == reserva.quarto 
            if len(dia_buscado) > 0:
                condicao_de_busca = condicao_de_busca and dia_buscado == reserva.dia_inicio 
            if len(dia_buscado) == 0 and len(numero_quarto) == 0 and len(nome_cliente) == 0:
                condicao_de_busca = False
            return condicao_de_busca

        reservas_correspondentes = encontra_varios(self.reservas, funcao_busca)
        if len(reservas_correspondentes) == 0:
            raise ValueError("Nenhuma reserva ativa encontrada com os parametros informados.")

        for reserva in reservas_correspondentes:
            print("Data de início: {}\nData de fim: {}".format(reserva.dia_inicio, reserva.dia_fim))
            print("Nome do cliente: {}".format(reserva.cliente))

            print(reserva.quarto)

            print("Produtos consumidos:")
            for produto in reserva.quarto.lista_consumo(self.produtos):
                print("\t{}".format(produto))
            
    def realiza_reserva(self):
        dia_inicio = int(input("Insira o dia de início da reserva: "))
        dia_fim = int(input("Insira o dia de fim da reserva: "))
        n_quarto = int(input("Insira o número do quarto: "))
        cliente = input("Insira o nome do hóspede: ")
        
        quarto_disponivel = self.__dias_disponiveis_quarto(dia_inicio, dia_fim, n_quarto)
        cliente_disponivel = self.__cliente_disponivel(cliente)

        if not quarto_disponivel:
            raise ValueError("INDISPONÍVEL. Quarto {} NÃO está disponível para a os dias informados.".format(n_quarto))

        elif not cliente_disponivel:
            raise ValueError("'{}' já possui uma reserva em andamento.".format(cliente))

        else:
            quarto_reservado = encontra(self.quartos, lambda quarto : quarto.numero == n_quarto)
            if not quarto_reservado:
                raise ValueError(f'Quarto de número {n_quarto} não existe')

            self.reservas.append(Reserva(dia_inicio, dia_fim, cliente, quarto_reservado))
            print("Reserva do quarto {} entre os dias {} e {} efetuada com sucesso.".format(n_quarto, dia_inicio, dia_fim))
        
    def cancela_reserva(self):
        reserva = self.__encontra_reserva_por_cliente(StatusReserva.ATIVA)
        reserva.cancela()
        print("Reserva cancelada.")

    def realiza_checkin(self):
        reserva = self.__encontra_reserva_por_cliente(StatusReserva.CHECK_IN)
        quantidade_dias = reserva.quantidade_dias()
        valor_total_diarias = reserva.total_diarias()

        print("Dia de início: {}\nDia de fim: {}".format(reserva.dia_inicio, reserva.dia_fim))
        print("Quantidade de dias reservados: {}".format(quantidade_dias))
        print("Valor total das diárias: R$ {:.2f}".format(valor_total_diarias))
        print(reserva.quarto)
        reserva.checkin()

    def realiza_checkout(self):
        reserva = self.__encontra_reserva_por_cliente(StatusReserva.ATIVA)
        quantidade_dias = reserva.quantidade_dias()
        valor_total_diarias = reserva.total_diarias()
        valor_total_consumo = reserva.quarto.valor_total_consumo(self.produtos)
        valor_final = valor_total_consumo + valor_total_diarias

        print("Data de início: {}\nData de fim: {}".format(reserva.dia_inicio, reserva.dia_fim))
        print("Dias reservados: {}".format(quantidade_dias))
        print("Valor total das diárias: R$ {:.2f}".format(valor_total_diarias))
        print(reserva.quarto)
        reserva.quarto.imprime_consumo(self.produtos)
        print("Valor total dos produtos consumidos: R$ {:.2f}".format(valor_total_consumo))
        print("Valor final: R$ {:.2f}".format(valor_final))

        reserva.checkout()

    def registra_consumo(self):
        reserva = self.__encontra_reserva_por_cliente(StatusReserva.ATIVA)

        print("Produtos disponíveis: ")
        for produto in self.produtos:
            print("\t{} - {}".format(produto.codigo, produto))

        produto_selecionado = int(input("Insira o código associado ao produto que deseja: "))
        if not encontra(self.produtos, lambda produto: produto.codigo == produto_selecionado):
            raise ValueError("Código inserido '{}' não corresponde a nenhum produto.".format(produto_selecionado))

        reserva.quarto.adiciona_consumo(produto_selecionado)

