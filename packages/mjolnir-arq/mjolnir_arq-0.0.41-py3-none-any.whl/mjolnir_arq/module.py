
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from mjolnir_arq.controller.mjolnir_controller import MjolnirController

mjolnirController = MjolnirController()


def main():
    mjolnirController.menu()


if __name__ == "__main__":
    main()
