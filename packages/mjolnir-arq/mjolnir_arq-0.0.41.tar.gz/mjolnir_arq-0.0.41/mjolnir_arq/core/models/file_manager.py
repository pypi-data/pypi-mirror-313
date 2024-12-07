import os

from termcolor import colored


class FileManager:

    def create_file(self, file_path: str, content=""):

        with open(file_path, "w") as file:
            file.write(content)
        print(colored(f"SUCCESS: archivo '{file_path}' creado con éxito.", "cyan"))

    def read_file(self, file_path: str):

        if not os.path.exists(file_path):
            print(f"El archivo '{file_path}' no existe.")
            return None

        with open(file_path, "r") as file:
            content = file.read()
        return content

    def update_file(self, file_path: str, new_content):

        if not os.path.exists(file_path):
            print(f"El archivo '{file_path}' no existe.")
            return

        with open(file_path, "w") as file:
            file.write(new_content)
        print(f"Archivo '{file_path}' actualizado con éxito.")

    def append_to_file(self, file_path: str, additional_content):

        if not os.path.exists(file_path):
            print(f"El archivo '{file_path}' no existe.")
            return

        with open(file_path, "a") as file:
            file.write(additional_content)
        print(f"Contenido agregado al archivo '{file_path}' con éxito.")

    def delete_file(self, file_path: str):

        if not os.path.exists(file_path):
            print(f"El archivo '{file_path}' no existe.")
            return

        os.remove(file_path)
        print(f"Archivo '{file_path}' eliminado con éxito.")

    def file_exists(self, file_path: str):
        return os.path.exists(file_path)

    def add_line_to_file(self, filename, comment, new_line):

        with open(filename, "r") as file:
            lines = file.readlines()

        insert_index = None
        for i, line in enumerate(lines):
            if comment in line:
                insert_index = i
                break

        if insert_index is not None and new_line not in lines:
            lines.insert(insert_index + 1, new_line + "\n")

        with open(filename, "w") as file:
            file.writelines(lines)

        print(colored(f"SUCCESS: archivo '{filename}' actualizado con éxito.", "cyan"))
