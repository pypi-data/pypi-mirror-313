from getpass import getpass
import pyfiglet
from InquirerPy import inquirer
from termcolor import colored
import os
from mjolnir_arq.business.mjolnir_business import MjolnirBusiness


def check_folder_exists_os(folder_path):
    return os.path.isdir(folder_path)


def get_current_directory():
    return os.getcwd()


class MjolnirController:
    def __init__(self) -> None:
        self.mjolnir_business = MjolnirBusiness()

    def show_title(self):
        title = pyfiglet.figlet_format("MJOLNIR-ARQ")
        title = colored(title, "cyan")
        print(colored(".", "cyan") * 100)
        print(title)
        print(colored("mjolnir-arq: 0.0.40", "cyan"))
        print(colored("Python: 3.11", "cyan"))
        print(colored("Author: Marlon Andres Leon Leon", "cyan"))
        print(colored(".", "cyan") * 100)

    def menu(self):
        self.show_title()
        password = getpass("Contraseña: ")
        if not password == "soybatman":
            print("Contraseña invalida.")
            return
        print(colored("contraseña valida", "cyan"))
        options = [
            "Crear flujo base",
            "Crear flujo base completo",
            "Crear flujo de negocio",
            "Crear proyecto",
            "Salir",
        ]

        selected_option = inquirer.select(
            message="Seleccione una opción:",
            choices=options,
            default=options[0],
        ).execute()

        if selected_option == "Crear flujo base":
            self.mjolnir_business.create_flow_base()
        elif selected_option == "Crear flujo base completo":
            self.mjolnir_business.create_flow_base_complete()
        elif selected_option == "Crear flujo de negocio":
            print("Has seleccionado flujo de negocio.")
        elif selected_option == "Crear proyecto":
            self.mjolnir_business.create_project()
        elif selected_option == "Salir":
            print("Saliendo...")
