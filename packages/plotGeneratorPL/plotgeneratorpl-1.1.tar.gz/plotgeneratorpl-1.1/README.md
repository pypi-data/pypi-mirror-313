# Image Processor

## Overview

The **Image Processor Tool** is an interactive script designed to provide users with functionalities to:

1. Generate FTIR (Fourier-transform infrared spectroscopy) plots.
2. Use ImageJ for image processing, such as color changes and intensity readings.
3. Exit the program when finished.

The tool guides users through each step and provides an easy way to interactively work with image files and FTIR data.

## Features

- **Generate FTIR Plot**: Users can input FTIR data to generate a plot for visualization purposes.
- **ImageJ Integration**: Perform image processing, including color adjustments, intensity analysis, and other modifications.

## Setup and Installation

To use this tool, follow these simple steps to set up the environment.

### Install the Package

To install the tool and all required dependencies, use the following command:

```sh
pip install plotGeneratorPL
```

### Running the Tool

You have two options to run the package:

1. **In Terminal**:
    - After installing, you can execute the tool directly from the terminal by running:

      ```sh
      plotGeneratorPL
      ```

      This will provide you with an interactive interface to use the available features.

2. **In a Python Notebook**:
    - You can also import and use the main functionality within a Python notebook:

      ```python
      from plotGeneratorPL import main
      main.main()
      ```

### How to Use

1. **Interact with the Program**:
    - When prompted, you will see the following options:
      ```
      1. Generate FTIR Plot
      2. Use ImageJ for image processing
      3. Exit the program
      ```
    - Enter the corresponding number to select the desired function.

2. **Follow the Prompts**: The program will guide you through the process of providing data or selecting image files as needed.

### Example Usage

After running the tool, you may be prompted as follows:

```plaintext
Welcome to the Image Processor!

Options:
1. Generate FTIR Plot
2. Use ImageJ
3. Exit
Enter the number of the function you want to use:

