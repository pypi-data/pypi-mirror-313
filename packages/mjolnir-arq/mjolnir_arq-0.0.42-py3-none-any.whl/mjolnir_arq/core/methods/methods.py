import subprocess
from typing import List

def snake_to_pascal(snake_str):
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)

def convert_to_kebab_case(snake_str):
    return snake_str.replace('_', '-')


def execute_commands_in_directory(comandos: List[str], directorio_destino: str):
    try:
        for comando in comandos:
            resultado = subprocess.run(comando, shell=True, cwd=directorio_destino, check=True, text=True, capture_output=True)
            print(f"Salida del comando '{comando}':\n{resultado.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Ocurrió un error al ejecutar el comando '{e.cmd}': {e.stderr}")

