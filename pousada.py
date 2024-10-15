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

    def __dia_disponivel_quarto(self, dia_buscado: int, quarto: Quarto) -> bool:
        """Retorna se quarto está disponível no dia_buscado"""
        for reserva in self.reservas:
            if reserva.quarto == quarto and dia_buscado in range(reserva.dia_inicio, reserva.dia_fim + 1):
                return False
        return True

    def __dias_disponiveis_quarto(self, dia_inicio: int, dia_fim: int, quarto: Quarto) -> bool:
        """Retorna se quarto está disponível em todos os dias entre e incluindo dia_inicio e dia_fim"""
        for reserva in self.reservas:
            if reserva.quarto == quarto and not (dia_fim < reserva.dia_inicio or dia_inicio > reserva.dia_fim):
                return False
        return True

    def __cliente_disponivel(self, cliente: str) -> bool:
        """Retorna se cliente não possui nenhuma reserva em andamento (ativa ou para check-in)"""
        for reserva in self.reservas:
            if reserva.cliente == cliente and reserva.status in (StatusReserva.ATIVA, StatusReserva.CHECK_IN):
                return False
        return True

    def __encontra_reserva(self, cliente: str, status: Status) -> Reserva:
        """Retorna reserva do cliente com status informado"""
        reserva = encontra(self.reservas, lambda r : r.cliente == cliente and r.status == status)
        if not reserva:
            raise ValueError("Nenhuma reserva com status {} no nome de {}.".format(status, cliente))
        return reserva

    def __encontra_quarto(self, numero: int) -> Quarto:
        quarto = encontra(self.quartos, lambda q : q.numero == numero)
        if not quarto:
            raise ValueError("Quarto com número inserido {} não existe".format(numero))
        return quarto

    def carrega_dados(self):
        self.produtos = Arquivo.carrega_produtos()
        self.quartos = Arquivo.carrega_quartos()
        self.reservas = Arquivo.carrega_reservas(self.quartos)

    def salva_dados(self):
        """
        Remove reservas canceladas ou com checkout realizado
        e salva dados de reservas, quartos e produtos em seus respectivos arquivos
        """
        self.reservas = list(filter(lambda r : r.status not in (StatusReserva.CHECK_OUT, StatusReserva.CANCELADA), self.reservas))
        Arquivo.salva_produtos(self.produtos)
        Arquivo.salva_quartos(self.quartos)
        Arquivo.salva_reservas(self.reservas)

    def consulta_disponibilidade(self, dia: int, n_quarto: int):
        """
        Recebe número do quarto e dia e imprime mensagem com dados de quarto.
        Se não estiver disponível, imprime que quarto não está indisponível.
        """
        quarto = self.__encontra_quarto(n_quarto)
        esta_disponivel = self.__dia_disponivel_quarto(dia, quarto)
        if esta_disponivel:
            print("Quarto {} está disponível para o dia {}.".format(quarto.numero, dia))
            print(quarto)
        else:
            print("INDISPONÍVEL. Quarto {} NÃO está disponível para o dia {}.".format(quarto.numero, dia))

    def consulta_reserva(self, dia: str, cliente: str, n_quarto: str):
        """
        Recebe dia, nome do cliente, número do quarto, todos opcionais.
        Imprime os dados de cada reserva ativa que corresponder aos parametros
        """
        def funcao_busca(reserva: Reserva) -> bool:
            """
            Verifica quais parametros foram inseridos pelo usuário
            e os adiciona à condição de busca de reservas ativas
            """
            cond_busca: bool = reserva.status == StatusReserva.ATIVA

            if cliente != "":
                cond_busca = cond_busca and cliente == reserva.cliente 
            if n_quarto != "":
                cond_busca = cond_busca and int(n_quarto) == reserva.quarto.numero
            if dia != "":
                cond_busca = cond_busca and int(dia) in range(reserva.dia_inicio, reserva.dia_fim + 1)

            if dia == "" and n_quarto == "" and cliente == "":
                cond_busca = False
            return cond_busca

        reservas = encontra_varios(self.reservas, funcao_busca)
        if len(reservas) == 0:
            raise ValueError("Nenhuma reserva ativa encontrada com os parametros informados.")
        
        for reserva in reservas:
            print("Data de início: {}\nData de fim: {}".format(reserva.dia_inicio, reserva.dia_fim))
            print("Nome do cliente: {}".format(reserva.cliente))
            print(reserva.quarto)
            print("Produtos consumidos:")
            for produto in reserva.quarto.lista_consumo(self.produtos):
                print("\t{}".format(produto))

    def realiza_reserva(self, data: tuple[int, int], cliente: str, n_quarto: int):
        """
        Recebe data[dia inicial, dia final], número do quarto e nome do cliente.
        Realiza reserva e imprime mensagem de sucesso.
        Se cliente não puder realizar reserva ou quarto estiver indisponível imprime mensagem informativa de erro.
        """
        dia_inicio, dia_fim = data
        quarto = self.__encontra_quarto(n_quarto)

        disponivel_quarto = self.__dias_disponiveis_quarto(dia_inicio, dia_fim, quarto)
        disponivel_cliente = self.__cliente_disponivel(cliente)
        
        if not disponivel_quarto:
            raise ValueError("INDISPONÍVEL. Quarto {} NÃO está disponível para a os dias informados.".format(quarto.numero))
        elif not disponivel_cliente:
            raise ValueError("'{}' já possui uma reserva em andamento.".format(cliente))
        
        self.reservas.append(Reserva(dia_inicio, dia_fim, cliente, quarto))
        print("Reserva do quarto {} entre os dias {} e {} efetuada com sucesso.".format(quarto.numero, dia_inicio, dia_fim))

    def cancela_reserva(self, cliente: str):
        """
        Recebe nome do cliente e encontra reserva ativa do cliente, esvazia consumo e
        muda status para cancelada. 
        """
        reserva = self.__encontra_reserva(cliente, StatusReserva.ATIVA)
        reserva.cancela()
        print("Reserva cancelada.")

    def realiza_checkin(self, cliente: str):
        """
        Recebe nome do cliente e encontra reserva para check-in do cliente,
        imprime seus dados e muda status para ativa. 
        """
        reserva = self.__encontra_reserva(cliente, StatusReserva.CHECK_IN)
        print("Dia de início: {}\nDia de fim: {}".format(reserva.dia_inicio, reserva.dia_fim))
        print("Quantidade de dias reservados: {}".format(reserva.quantidade_dias()))
        print("Valor total das diárias: R$ {:.2f}".format(reserva.valor_diarias()))
        print(reserva.quarto)
        reserva.checkin()

    def realiza_checkout(self, cliente: str):
        """
        Recebe nome do cliente e encontra reserva ativa do cliente, imprime seus dados e 
        valores finais, esvazia consumo e muda status para check-out. 
        """
        reserva = self.__encontra_reserva(cliente, StatusReserva.ATIVA)
        valor_diarias = reserva.valor_diarias()
        valor_consumo = reserva.quarto.valor_total_consumo(self.produtos)
        valor_final = valor_consumo + valor_diarias
        
        print("Data de início: {}\nData de fim: {}".format(reserva.dia_inicio, reserva.dia_fim))
        print("Dias reservados: {}".format(reserva.quantidade_dias()))
        print("Valor total das diárias: R$ {:.2f}".format(valor_diarias))
        print(reserva.quarto)
        reserva.quarto.imprime_consumo(self.produtos)
        print("Valor total dos produtos consumidos: R$ {:.2f}".format(valor_consumo))
        print("Valor final: R$ {:.2f}".format(valor_final))
        reserva.checkout()

    def registra_consumo(self, cliente: str, codigo_produto: int):
        reserva = self.__encontra_reserva(cliente, StatusReserva.ATIVA)
        reserva.quarto.adiciona_consumo(codigo_produto)

    def menu_registra_consumo(self):
        """
        Recebe nome do cliente por input.
        Imprime produtos disponíveis e recebe código do produto por input.
        Encontra produto com código recebido e adiciona seu código a lista de consumo
        da reserva ativa do cliente. 
        """
        cliente = input("Nome do hóspede: ")

        print("Produtos disponíveis: ")
        for produto in self.produtos:
            print("\t{} - {}".format(produto.codigo, produto))

        codigo_selecionado = int(input("Insira o código associado ao produto que deseja: "))
        if not encontra(self.produtos, lambda p: p.codigo == codigo_selecionado):
            raise ValueError("Código inserido '{}' não corresponde a nenhum produto.".format(codigo_selecionado))

        self.registra_consumo(cliente, codigo_selecionado)
