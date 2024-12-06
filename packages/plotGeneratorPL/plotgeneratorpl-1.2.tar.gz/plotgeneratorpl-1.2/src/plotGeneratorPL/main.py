#!/usr/bin/env python
# coding: utf-8
# Necessary Packages3
from .utils import get_user_input
from . import plot_FTIR
from . import imageJ_tool


def main():
    while True:
        print("Welcome to the Image Processer!")

        # Ask the user which function they want to use
        print("\nOptions:\n1. Generate FTIR Plot")
        print("2. Use ImageJ")
        print("3. Exit.")

        choice = get_user_input("Enter the number of function to use: ", int)

        if choice == 1:          # FTIR PLOT Function
            plot_FTIR.user_input_FTIR()
        elif choice == 2:        # Image J function
            imageJ_tool.image_processing()
        elif choice == 3:
            break


if __name__ == "__main__":
    main()
