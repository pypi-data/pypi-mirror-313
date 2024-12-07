import os
import shutil
from termcolor import colored


class DirectoryManager:

    def create_directory(self, dir_path: str) -> bool:

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(colored(f"SUCCESS: carpeta '{dir_path}' creada con éxito.", "cyan"))
            return True
        else:
            return False

    def list_contents(self, dir_path: str):

        if not os.path.exists(dir_path):
            print(f"La carpeta '{dir_path}' no existe.")
            return []

        contents = os.listdir(dir_path)
        return contents

    def delete_directory(self, dir_path: str):

        if not os.path.exists(dir_path):
            print(f"La carpeta '{dir_path}' no existe.")
            return

        shutil.rmtree(dir_path)
        print(f"Carpeta '{dir_path}' eliminada con éxito.")

    def directory_exists(self, dir_path: str):

        return os.path.exists(dir_path)

    def move_directory(self, dir_path: str, new_path):

        if not os.path.exists(dir_path):
            print(f"La carpeta '{dir_path}' no existe.")
            return

        shutil.move(dir_path, new_path)
        dir_path = new_path
        print(f"Carpeta movida a '{new_path}' con éxito.")
