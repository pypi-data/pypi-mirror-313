import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os
import sys
from .utils import (get_user_input, get_directory, get_filename, get_file_path)

__all__ = [
    "plot_FTIR",
    "modify_inputs",
    "is_first_column_xaxis",
    "get_valid_smooth_level",
    "user_input_FTIR"
    ]


def plot_FTIR(title: str, dataPath: str, smoothLevel: int):
    """
    Plots an FTIR graph based on the provided data and parameters.
    Args:
        title (str): The title of the figure.
        dataPath (str): The full path to the Excel file with the FTIR data
        smoothLevel (int): The level of smoothing to apply to the dataset.
                           It determines the step size for reducing the
                           dataset (e.g., every nth row).
    Returns:
        tuple: A tuple containing the matplotlib Figure and Axes objects.
    """
    df = pd.read_excel(dataPath)
    # Smooth the dataset
    df = df.iloc[::smoothLevel, :]
    numberofPlots = df.shape[1] - 1
    # Get the names for labels
    labels = df.columns.tolist()
    # Generate a colormap with a unique color for each plot
    colors = cm.viridis(np.linspace(0, 1, numberofPlots))

    fig, axs = plt.subplots(numberofPlots, 1, figsize=(10, 12), sharex=True,
                            gridspec_kw={'hspace': 0})
    for i in range(numberofPlots):
        axs[i].plot(df['xaxis'], df[labels[i+1]], label=labels[i+1], lw=2,
                    color=colors[i])
        axs[i].tick_params(axis='x', which='both', bottom=False, top=False,
                           labelbottom=False)
        axs[i].set_xlabel('Wavenumber (cm⁻¹)', fontsize=14)

    for ax in axs:
        ax.grid(False)
        ax.legend(loc='upper right')
        ax.tick_params(left=False, labelleft=False)

    axs[-1].tick_params(axis='x', which='both', bottom=True, top=False,
                        labelbottom=True)
    axs[-1].set_xticks(np.arange(df['xaxis'].min(), df['xaxis'].max() + 1,
                                 500))
    fig.text(0.02, 0.5, 'Absorbance', va='center', rotation='vertical',
             fontsize=14)
    fig.suptitle(title, fontsize=16, y=0.9)
    plt.subplots_adjust(hspace=0)
    plt.tight_layout(rect=[0.04, 0.03, 1, 0.92])
    return fig, axs


def is_first_column_xaxis(dataPath: str):
    """
    Checks if the first column in the Excel file is labeled 'xaxis'.
    Args:
        dataPath (str): The full path to the Excel file.
    Returns:
        bool: True if the first column is labeled 'xaxis', False otherwise.
    """
    try:
        df = pd.read_excel(dataPath, nrows=1)
        return df.columns[0] == 'xaxis'
    except Exception:
        return False


def modify_inputs(dataPath: str, smoothLevel: int, title: str):
    """
    Allows the user to modify specific inputs (dataPath, smoothLevel, or title)
    Returns the potentially updated inputs.
    Args:
        dataPath (str): The current path to the Excel data file.
        smoothLevel (int): The current smoothing level applied to the data.
        title (str): The current title of the figure.
    Returns:
        tuple: A tuple containing the updated values of dataPath, smoothLevel,
        and title.
    """
    while True:
        print("\nWhich input would you like to modify?")
        print("1. Filepath")
        print("2. Smooth Level")
        print("3. Title")
        print("4. Keep all inputs and continue")

        choice = input("Enter the number of your choice: ").strip()

        if choice == "1":
            dataPath = get_file_path("Enter the new full path to the data file"
                                     " (Excel format): ")
        elif choice == "2":
            smoothLevel = get_valid_smooth_level(dataPath)
        elif choice == "3":
            title = get_user_input("Enter the new title of the figure: ")
        elif choice == "4":
            print("Keeping all inputs as is.")
            break
        else:
            print("Invalid choice. Please enter a valid number.")
            continue

        modify_again = input("Do you want to modify another input? (yes/no): ")
        modify_again = modify_again.strip().lower()
        if modify_again != "yes":
            break

    return dataPath, smoothLevel, title


def get_valid_smooth_level(dataPath: str):
    """
    Prompts the user to input a smoothing level and validates it
    against the number of rows in the dataset.

    Args:
        dataPath (str): The path to the Excel data file.

    Returns:
        int: A valid smoothing level.
    """
    # Read the Excel file to get the number of rows
    try:
        df = pd.read_excel(dataPath)
        num_rows = df.shape[0]  # Total number of rows in the dataset
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        sys.exit(1)

    while True:
        try:
            # Prompt the user for the smoothing level
            inputw = f"Enter the smoothing level (0 to {num_rows}): "
            smoothLevel = int(input(inputw).strip())
            if 0 <= smoothLevel <= num_rows:
                return smoothLevel
            else:
                print(f"Invalid input! Integer between 0 and {num_rows}.")
        except ValueError:
            print("Invalid input! Please enter an integer.")


def user_input_FTIR(dataPath: str = None, smoothLevel: int = None,
                    title: str = None):
    """
    Collects user input for generating an FTIR plot, allows modifications,
    and handles saving the figure.
    Args:
        dataPath (str, optional): The path to the Excel data file. If None,
        user will be prompted for input.
        smoothLevel (int, optional): The smoothing level for the data. If None,
        user will be prompted for input.
        title (str, optional): The title for the figure. If None, user will be
        prompted for input.
    """
    print("\nYou chose to generate an FTIR plot.")
    print("Please ensure your Excel data is organized as follows:")
    print(" 1. Sample names should be in the first row.")
    print(" 2. The first column must be labeled 'xaxis'.")
    print(" 3. Data for each sample should be in the corresponding columns.")

    # Initial input collection if not provided
    if not dataPath:
        prompt_sentence = "Enter full path to the data file (Excel format):"
        dataPath = get_file_path(prompt_sentence)
    if not smoothLevel:
        smoothLevel = get_valid_smooth_level(dataPath)
    if not title:
        title = get_user_input("Enter the title of the figure: ")

    while True:
        if is_first_column_xaxis(dataPath):
            fig, axs = plot_FTIR(title, dataPath, smoothLevel)
            print("Close the figure to continue.")
            plt.show()
        else:
            print("The first column is not labeled 'xaxis'. Exiting...")
            sys.exit()
        question = "Do you want to save the figure? (yes/no): "
        save_choice = input(question).strip().lower()

        if save_choice == "yes":
            filename = "Enter the name of the figure file (e.g., plot.png):"
            filename = get_filename(filename)
            saveDir = get_directory("Enter the directory to save the figure: ")
            savePath = os.path.join(saveDir, filename)
            fig.savefig(savePath)
            print(f"Figure saved to {savePath}")
            plt.close(fig)
            return

        elif save_choice == "no":
            modify_choice = "Modify the Path/Smooth/Title? (yes/no): "
            modify_choice = input(modify_choice).strip().lower()
            if modify_choice == "yes":
                plt.close(fig)
                dataPath, smoothLevel, title = modify_inputs(dataPath,
                                                             smoothLevel,
                                                             title)
                continue
            else:
                print("Exiting without saving or modifying.")
                plt.close(fig)
                return
        else:
            print("Invalid choice. Please type 'yes' or 'no'.")
