import csv
from reserva import Reserva
from quarto import Quarto
from produto import Produto
from uteis import encontra

# Classe estática
# para abstrair a parte relacionada a manipulação de arquivo
class Arquivo:
    @classmethod
    def carrega_produtos(cls):
        # Espera-se que os dados estejam na ordem:
        # codigo, nome, preco
        dados = cls.__carrega_dados("produto.txt")
        produtos: list[Produto] = []
        for linha in dados:
            produtos.append(Produto(int(linha[0]), linha[1], float(linha[2])))
        return produtos

    @classmethod
    def salva_produtos(cls, produtos: list[Produto]):
        cabecalho = ["codigo","nome","preco"]
        dados = [[p.codigo,p.nome,p.preco] for p in produtos]
        cls.__salva_dados("produto.txt", cabecalho, dados)


    @classmethod
    def carrega_quartos(cls):
        # Espera-se que os dados estejam na ordem:
        # numero, categoria, diária, consumo
        dados = cls.__carrega_dados("quarto.txt")
        quartos: list[Quarto] = []
        for linha in dados:
            consumo = list(map(lambda codigo: int(codigo), linha[3][1:-1].split(",")))
            quartos.append(Quarto(int(linha[0]), linha[1], float(linha[2]), consumo))
        return quartos

    @classmethod
    def salva_quartos(cls, quartos: list[Quarto]):
        cabecalho = ["numero","categoria","diária","consumo"]
        dados = [[q.numero,q.categoria,q.diaria,q.consumo] for q in quartos]
        cls.__salva_dados("quarto.txt", cabecalho, dados)


    @classmethod
    def carrega_reservas(cls, quartos: list[Quarto]):
        # Espera-se que os dados estejam na ordem:
        # dia_inicio, dia_fim, cliente, quarto, status
        dados = cls.__carrega_dados("reserva.txt")
        reservas: list[Reserva] = []
        for linha in dados:
            n_quarto = int(linha[3])
            quarto = encontra(quartos, lambda quarto: quarto.numero == n_quarto)
            if not quarto:
                raise ValueError(f'Número do quarto {n_quarto} em reserva.txt não corresponde à nenhum quarto (())')
            reservas.append(Reserva(int(linha[0]), int(linha[1]), linha[2], quarto, linha[4]))
        return reservas

    @classmethod
    def salva_reservas(cls, reservas: list[Reserva]):
        cabecalho = ["dia_inicio","dia_fim","cliente","quarto","status"]
        dados = [[r.dia_inicio,r.dia_fim,r.cliente,r.quarto.numero,r.status] for r in reservas]
        cls.__salva_dados("reserva.txt", cabecalho, dados)


    @classmethod
    def __carrega_dados(cls, caminho_arquivo: str):
        with open(caminho_arquivo, "r") as arquivo:
            leitor_csv = csv.reader(arquivo)
            dados_brutos = list(leitor_csv)
            dados = dados_brutos[1::]
            return dados

    @classmethod
    def __salva_dados(cls, caminho_arquivo: str, cabecalho: list[str], dados: list[list]):
        with open(caminho_arquivo, "w") as arquivo:
            escritor_csv = csv.writer(arquivo)
            escritor_csv.writerow(cabecalho)
            escritor_csv.writerows(dados)
