import csv

class Arquivo:
    def __init__(self, classe):
        self.__classe = classe
        self.__caminho = classe.__qualname__.lower() + ".txt"
        self.__lista_dados = []
        self.__cabecalho = []
        self.__args_init_classe_nome_tipo_dict: dict[str, type] = classe.__init__.__annotations__

    def __coleta_dados_arquivo(self):
        with open(self.__caminho, "r") as arquivo:
            leitor_csv = csv.reader(arquivo)
            lista_dados_brutos = list(leitor_csv)
            self.__cabecalho = lista_dados_brutos[0]
            for nome_coluna in self.__cabecalho:
                if nome_coluna not in self.__args_init_classe_nome_tipo_dict.keys():
                    print("Erro: coluna com nome {} não corresponde a nenhum atributo da classe {}".format(nome_coluna, self.__classe.__qualname__))
                    return None
            self.__lista_dados = lista_dados_brutos[1::]

    def __converte_valor_para_tipo_argumento(self, valor: str, tipo_argumento: type):
        if tipo_argumento == int:
            return int(valor)
        elif tipo_argumento == float:
            return float(valor)
        elif tipo_argumento == list[str]:
            return valor[1:-1].split(",")
        elif tipo_argumento == list[int]:
            return list(map(lambda x: int(x), valor[1:-1].split(",")))
        elif tipo_argumento == list[float]:
            return list(map(lambda x: float(x), valor[1:-1].split(",")))
        else:
            return valor

    def __cria_objs_com_dados_arquivo(self) -> list:
        lista_instancias_classe = []
        for linha in self.__lista_dados:
            args_init_classe = []
            for nome_arg in self.__args_init_classe_nome_tipo_dict:
                indice_col = self.__cabecalho.index(nome_arg)
                tipo_arg = self.__args_init_classe_nome_tipo_dict[nome_arg]
                valor = self.__converte_valor_para_tipo_argumento(linha[indice_col], tipo_arg)
                args_init_classe.append(valor)
            lista_instancias_classe.append(self.__classe(*args_init_classe))
        return lista_instancias_classe

    def __coleta_dados_objetos(self, objs_para_salvar: list):
        self.__lista_dados = []
        self.__cabecalho = [nome_atr for nome_atr in self.__classe.__dict__ if not nome_atr.startswith("__")]
        for objeto in objs_para_salvar:
            dados_objeto = []
            for nome_atr, valor in objeto.__dict__.items():
                if not nome_atr.startswith("__"):
                    if type(valor) == list:
                        dados_objeto.append("[{}]".format(",".join(valor)))
                    else:
                        dados_objeto.append(valor)
            self.__lista_dados.append(dados_objeto)

    def salva_dados(self, objs_para_salvar: list):
        self.__coleta_dados_objetos(objs_para_salvar)
        with open(self.__caminho, "w") as arquivo:
            escritor_csv = csv.writer(arquivo)
            escritor_csv.writerow(self.__cabecalho)
            escritor_csv.writerows(self.__lista_dados)

    def carrega_dados(self):
        self.__coleta_dados_arquivo()
        return self.__cria_objs_com_dados_arquivo()

