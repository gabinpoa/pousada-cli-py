from pousada import Pousada
from menu import Menu, MenuItem

if __name__ == "__main__":
    try:
        pousada = Pousada("Pousada do Mar", "51 99592-6116")
        pousada.carrega_dados()

        funcoes_menu = [MenuItem(1, "Consultar disponibilidade", pousada.consulta_disponibilidade)]
        funcoes_menu.append(MenuItem(2, "Consultar reserva", pousada.consulta_reserva))
        funcoes_menu.append(MenuItem(3, "Realizar reserva", pousada.realiza_reserva))
        funcoes_menu.append(MenuItem(4, "Cancelar reserva", pousada.cancela_reserva))
        funcoes_menu.append(MenuItem(5, "Realizar check-in", pousada.realiza_checkin))
        funcoes_menu.append(MenuItem(6, "Realizar check-out", pousada.realiza_checkout))
        funcoes_menu.append(MenuItem(7, "Registra consumo", pousada.registra_consumo))
        funcoes_menu.append(MenuItem(8, "Salvar", pousada.salva_dados))

        menu = Menu(funcoes_menu)
        menu.iniciar()
    except KeyboardInterrupt:
        print("\nSaindo do programa")
