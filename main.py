from pousada import Pousada
from menu import Menu, MenuItem

if __name__ == "__main__":
    try:
        pousada = Pousada("Pousada do Mar", "51 99592-6116")
        pousada.carrega_dados()

        funcoes_menu = [
            MenuItem(1, "Consultar disponibilidade", Menu.dia_n_quarto(pousada.consulta_disponibilidade)),
            MenuItem(2, "Consultar reserva", Menu.str_dia_cliente_n_quarto_opcional(pousada.consulta_reserva)),
            MenuItem(3, "Realizar reserva", Menu.data_cliente_n_quarto(pousada.realiza_reserva)),
            MenuItem(4, "Cancelar reserva", Menu.cliente(pousada.cancela_reserva)),
            MenuItem(5, "Realizar check-in", Menu.cliente(pousada.realiza_checkin)),
            MenuItem(6, "Realizar check-out", Menu.cliente(pousada.realiza_checkout)),
            MenuItem(7, "Registra consumo", pousada.menu_registra_consumo),
            MenuItem(8, "Salvar", pousada.salva_dados)
        ]
        menu = Menu(funcoes_menu)
        menu.iniciar()
    except KeyboardInterrupt:
        print("\nSaindo do programa")
