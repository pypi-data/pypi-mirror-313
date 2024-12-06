import os
import sys
import tempfile
import unittest
from unittest.mock import patch
import pandas as pd
import cv2
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                             'src')))
from plotGeneratorPL import main
from plotGeneratorPL.imageJ_tool import (color_change, batch_process_images,
                         divide_and_measure_intensity,
                         process_images_and_save_intensity,
                         image_processing)
from plotGeneratorPL.utils import (get_user_input, get_directory, get_filename,
                   get_file_path)
from plotGeneratorPL.plot_FTIR import (plot_FTIR, modify_inputs,
                       is_first_column_xaxis,
                       user_input_FTIR, get_valid_smooth_level)


class TestMainFunction(unittest.TestCase):

    @patch('builtins.print')  # Mock print to suppress output during testing
    @patch('plotGeneratorPL.main.get_user_input', side_effect=[1, 2, 3])
    @patch('plotGeneratorPL.plot_FTIR.user_input_FTIR')
    @patch('plotGeneratorPL.imageJ_tool.image_processing')
    def test_main(self, mock_image_processing, mock_user_input_FTIR,
                  mock_get_user_input, mock_print):

        main.main()
        self.assertEqual(mock_get_user_input.call_count, 3)
        mock_user_input_FTIR.assert_called_once()
        mock_image_processing.assert_called_once()

        # Verify print output contains the menu and welcome message
        mock_print.assert_any_call("Welcome to the Image Processer!")
        mock_print.assert_any_call("\nOptions:\n1. Generate FTIR Plot")
        mock_print.assert_any_call("2. Use ImageJ")
        mock_print.assert_any_call("3. Exit.")


class TestHelpFunctions(unittest.TestCase):

    def test_get_user_input(self):
        """
        Test get_user_input with different data types.
        """
        with patch('builtins.input', side_effect=["42", "invalid", "21"]):
            # Valid integer input
            self.assertEqual(get_user_input("Enter a number: ", int), 42)
            # Retry with valid input
            self.assertEqual(get_user_input("Enter a number: ", int), 21)

    def test_get_directory(self):
        """
        Test get_directory with valid and invalid directory inputs.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Valid directory
            with patch('builtins.input', side_effect=[temp_dir]):
                self.assertEqual(get_directory("Enter a valid directory: "),
                                 temp_dir)

            # Invalid directory followed by a valid directory
            with patch('builtins.input', side_effect=["/invalid/dir",
                                                      temp_dir]):
                self.assertEqual(get_directory("Enter a valid directory: "),
                                 temp_dir)

    def test_get_filename(self):
        """
        Test get_filename with valid and invalid filenames.
        """
        with patch('builtins.input', side_effect=["valid_name.txt",
                                                  "invalid:name.txt",
                                                  "correct_file.png"]):
            self.assertEqual(get_filename("Enter a valid filename: "),
                             "valid_name.txt")
            self.assertEqual(get_filename("Enter a valid filename: "),
                             "correct_file.png")

    def test_get_file_path(self):
        """
        Test get_file_path with valid and invalid file paths.
        """
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            valid_file_path = temp_file.name

        try:
            with patch('builtins.input', side_effect=[valid_file_path]):
                self.assertEqual(get_file_path("Enter a valid file path: "),
                                 valid_file_path)
            with patch('builtins.input', side_effect=["/invalid/path.txt",
                                                      valid_file_path]):
                self.assertEqual(get_file_path("Enter a valid file path: "),
                                 valid_file_path)
        finally:
            os.remove(valid_file_path)


class TestFTIRProcessing(unittest.TestCase):

    @patch('pandas.read_excel')
    @patch('matplotlib.pyplot.subplots')
    def test_plot_FTIR(self, mock_subplots, mock_read_excel):
        # Mock input data from StringIO
        excel_data = StringIO("""xaxis,data1,data2
        1,10,20
        2,15,25
        3,20,30
        """)
        mock_read_excel.return_value = pd.read_csv(excel_data)
        mock_fig = plt.figure()
        mock_axs = [plt.subplot() for _ in range(2)]
        mock_subplots.return_value = (mock_fig, mock_axs)
        fig, axs = plot_FTIR("Test Title", "/mock/path.xlsx", 1)
        mock_read_excel.assert_called_once_with("/mock/path.xlsx")
        self.assertEqual(len(axs), 2)  # One plot per data column
        mock_subplots.assert_called_once_with(2, 1, figsize=(10, 12),
                                              sharex=True,
                                              gridspec_kw={'hspace': 0})

    @patch('pandas.read_excel')
    @patch('builtins.input', side_effect=['-1', '500', '2'])
    def test_get_valid_smooth_level(self, mock_input, mock_read_excel):
        # Mock the Excel data with 100 rows
        excel_data = StringIO("""xaxis,data1,data2
        1,10,20
        2,15,25
        3,20,30
        """)
        df = pd.read_csv(excel_data)
        mock_read_excel.return_value = df
        data_path = "fake_path.xlsx"
        valid_smooth_level = get_valid_smooth_level(data_path)
        self.assertEqual(valid_smooth_level, 2)

    @patch("builtins.input", side_effect=[
        "1",  # Modify filepath
        "/new/path.xlsx",  # New filepath input
        "no",  # Do not modify again
        "4"   # Keep all inputs and continue
    ])
    @patch("plotGeneratorPL.plot_FTIR.get_file_path",
           return_value="/new/path.xlsx")
    @patch("plotGeneratorPL.plot_FTIR.get_valid_smooth_level",
           return_value=2)
    @patch("plotGeneratorPL.plot_FTIR.get_user_input",
           return_value="New Title")
    def test_modify_inputs(self, mock_get_user_input,
                           mock_get_valid_smooth_level,
                           mock_get_file_path, mock_input):
        dataPath = "/old/path.xlsx"
        smoothLevel = 1
        title = "Old Title"
        updated_dataPath, updated_smoothLevel, updated_title = modify_inputs(
            dataPath, smoothLevel, title)
        mock_get_file_path.assert_called_once_with(
            "Enter the new full path to the data file (Excel format): ")
        self.assertEqual(updated_dataPath, "/new/path.xlsx")
        self.assertEqual(updated_smoothLevel, 1)
        self.assertEqual(updated_title, "Old Title")

    @patch('pandas.read_excel')
    def test_first_column_is_xaxis(self, mock_read_excel):
        # Mock input data where the first column is 'xaxis'
        excel_data = StringIO("""xaxis,data1,data2
        1,10,20
        2,15,25
        """)
        mock_read_excel.return_value = pd.read_csv(excel_data)
        result = is_first_column_xaxis("/mock/path.xlsx")
        mock_read_excel.assert_called_once_with("/mock/path.xlsx", nrows=1)
        self.assertTrue(result)

    @patch('pandas.read_excel')
    def test_first_column_is_not_xaxis(self, mock_read_excel):
        # Mock input data where the first column is not 'xaxis'
        excel_data = StringIO("""wrong_column,data1,data2
        1,10,20
        2,15,25
        """)
        mock_read_excel.return_value = pd.read_csv(excel_data)
        result = is_first_column_xaxis("/mock/path.xlsx")
        mock_read_excel.assert_called_once_with("/mock/path.xlsx", nrows=1)
        self.assertFalse(result)

    @patch("plotGeneratorPL.plot_FTIR.get_file_path",
           return_value="test_data.xlsx")
    @patch("plotGeneratorPL.plot_FTIR.get_valid_smooth_level",
           side_effect=[1, "Test Title"])
    @patch("plotGeneratorPL.plot_FTIR.get_filename", return_value="plot.png")
    @patch("plotGeneratorPL.plot_FTIR.get_directory", return_value="/tmp")
    @patch("pandas.read_excel")
    @patch("matplotlib.pyplot.show")
    @patch("matplotlib.figure.Figure.savefig")
    @patch("builtins.input", side_effect=[
        "yes",
        "no",
        "no"  # Exit after one iteration
    ])
    def test_user_input_FTIR(self, mock_input, mock_savefig, mock_show,
                             mock_read_excel,
                             mock_get_directory, mock_get_filename,
                             mock_get_valid_smooth_level, mock_get_file_path):

        mock_read_excel.return_value = pd.DataFrame({
            'xaxis': [1000, 2000, 3000],
            'Sample1': [0.1, 0.2, 0.3],
            'Sample2': [0.4, 0.5, 0.6]
        })
        user_input_FTIR()


class TestImageProcessingFunctions(unittest.TestCase):

    @patch('os.listdir', return_value=['image1.tif', 'image2.tif'])
    @patch('cv2.imread', return_value=np.array([[100, 200], [150, 250]],
                                               dtype=np.uint8))
    @patch('cv2.imwrite')
    def test_batch_process_images(self, mock_imwrite, mock_imread,
                                  mock_listdir):
        batch_process_images('input_dir', 'output_dir', 'green', 150)
        self.assertEqual(mock_imwrite.call_count, 2)

    @patch('cv2.imread', return_value=np.array([[100, 200, 150],
                                                [150, 250, 100],
                                                [200, 100, 50]],
                                               dtype=np.uint8))
    def test_divide_and_measure_intensity(self, mock_imread):
        intensities = divide_and_measure_intensity('image_path.tif')
        expected_intensities = [150.0, 166.67, 116.67]
        for i in range(len(intensities)):
            self.assertAlmostEqual(intensities[i], expected_intensities[i],
                                   places=1)

    @patch('os.listdir', return_value=['image1.tif', 'image2.tif'])
    @patch('cv2.imread', return_value=np.array([[100, 200], [150, 250]],
                                               dtype=np.uint8))
    @patch('pandas.DataFrame.to_excel')
    def test_process_images_and_save_intensity(self, mock_to_excel,
                                               mock_imread, mock_listdir):
        process_images_and_save_intensity('input_dir', 'output_excel.xlsx')
        mock_to_excel.assert_called_once()

    @patch("cv2.imread")
    @patch("cv2.threshold")
    @patch("cv2.imwrite")
    def test_color_change(self, mock_imwrite, mock_threshold, mock_imread):
        # Mock the grayscale image
        mock_image = np.array([
            [100, 200, 150],
            [50, 255, 120],
            [30, 100, 180]
        ], dtype=np.uint8)
        mock_imread.return_value = mock_image

        # Mock the thresholding operation
        mock_threshold.return_value = (None, np.array([
            [0, 255, 0],
            [0, 255, 0],
            [0, 0, 255]
        ], dtype=np.uint8))
        input_path = "/mock/input.tif"
        output_path = "/mock/output.tif"
        color = "red"
        color_change(input_path, output_path, color)
        mock_imread.assert_called_once_with(input_path, cv2.IMREAD_GRAYSCALE)
        mock_threshold.assert_called_once_with(mock_image, 150, 255,
                                               cv2.THRESH_BINARY)
        mock_imwrite.assert_called_once()
        saved_image = mock_imwrite.call_args[0][1]
        self.assertEqual(saved_image.shape, (3, 3, 3))
        # Check if the bright areas are red
        self.assertTrue(np.array_equal(saved_image[0, 1], [0, 0, 255]))  # Red
        self.assertTrue(np.array_equal(saved_image[1, 1], [0, 0, 255]))  # Red
        self.assertTrue(np.array_equal(saved_image[2, 2], [0, 0, 255]))  # Red
        # Check if non-bright areas are black
        self.assertTrue(np.array_equal(saved_image[0, 0], [0, 0, 0]))  # Black


if __name__ == "__main__":
    unittest.main()
