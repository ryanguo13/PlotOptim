# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# import numpy as np
# import pandas as pd
# from analyzer import IntensityAnalyzer
#
# # Custom Canvas to render Matplotlib figures within the PyQt GUI
# class MplCanvas(FigureCanvas):
#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#         super().__init__(fig)
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         # Setup main window
#         self.setWindowTitle("Intensity Analyzer")
#         self.setGeometry(100, 100, 1200, 800)
#
#         # Initialize analyzer
#         self.analyzer = None
#
#         # Setup layout
#         layout = QVBoxLayout()
#
#         # Create buttons
#         self.load_button = QPushButton("Load Data", self)
#         self.load_button.clicked.connect(self.load_data)
#
#         self.process_button = QPushButton("Process Data", self)
#         self.process_button.clicked.connect(self.process_data)
#         self.process_button.setEnabled(False)
#
#         # Create Matplotlib figure
#         self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
#
#         # Add widgets to layout
#         layout.addWidget(self.load_button)
#         layout.addWidget(self.process_button)
#         layout.addWidget(self.canvas)
#
#         # Set central widget and layout
#         central_widget = QWidget(self)
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)
#
#     def load_data(self):
#         # Open file dialog for selecting the data file
#         file_path, _ = QFileDialog.getOpenFileName(self, "Open Data File", "", "Text Files (*.TXT)")
#         if file_path:
#             self.analyzer = IntensityAnalyzer(file_path)
#             self.analyzer.read_data()
#             self.analyzer.filter_data()
#             self.process_button.setEnabled(True)
#
#     def process_data(self):
#         # Process data and generate plot
#         if self.analyzer:
#             self.analyzer.detect_spikes()
#             self.analyzer.map_data()
#             self.display_plot()
#
#     def display_plot(self):
#         # Clear previous plots
#         self.canvas.axes.clear()
#
#         # Plot data
#         self.canvas.axes.plot(self.analyzer.mapped_data['Sputter_Time__s_'],
#                               self.analyzer.mapped_data['Intensity'], label='Intensity Mapped', color='blue')
#
#         self.canvas.axes.plot(self.analyzer.df['Sputter_Time__s_'],
#                               self.analyzer.df['Intensity'], label='Intensity', color='green')
#
#         # Highlight detected spike intervals
#         for start, end in self.analyzer.skip_intervals:
#             self.canvas.axes.axvspan(start, end, color='red', alpha=0.3)
#
#         # Set plot labels and legends
#         self.canvas.axes.set_title('Intensity with Detected Spikes')
#         self.canvas.axes.set_xlabel('Sputter Time (s)')
#         self.canvas.axes.set_ylabel('Intensity')
#         self.canvas.axes.legend()
#
#         # Refresh canvas to display the updated plot
#         self.canvas.draw()
#
# def main():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())
#
# if __name__ == "__main__":
#     main()

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QTextEdit
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from analyzer import *
import pandas as pd
import logging
from io import StringIO


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Intensity Analyzer")
        self.setGeometry(100, 100, 1200, 800)

        # Setup logging
        self.log_stream = StringIO()
        logging.basicConfig(stream=self.log_stream, level=logging.INFO)

        self.analyzer = None

        layout = QVBoxLayout()

        self.load_button = QPushButton("Load Data", self)
        self.load_button.clicked.connect(self.load_data)

        self.process_button = QPushButton("Process Data", self)
        self.process_button.clicked.connect(self.process_data)
        self.process_button.setEnabled(False)

        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)

        # Add log output console
        self.console = QTextEdit(self)
        self.console.setReadOnly(True)

        layout.addWidget(self.load_button)
        layout.addWidget(self.process_button)
        layout.addWidget(self.canvas)
        layout.addWidget(self.console)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_data(self):
        # Open file dialog for selecting multiple data files
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Open Data Files", "", "Text Files (*.TXT)")
        if file_paths:
            # Assuming you have a method to process multiple files
            for file_path in file_paths:
                logging.info(f"Loading data from: {file_path}")
                # Initialize analyzer for each file
                self.analyzer = IntensityAnalyzer(file_path)
                self.analyzer.read_data()
                self.analyzer.filter_data()

            self.process_button.setEnabled(True)

    def process_data(self):
        if self.analyzer:
            # Assuming you have code to process data
            logging.info("Processing data...")
            self.analyzer.detect_spikes()
            self.analyzer.map_data()
            self.display_plot()
            self.update_console()

    def display_plot(self):
    # Clear previous plots
            self.canvas.axes.clear()

            # Plot data
            self.canvas.axes.plot(self.analyzer.mapped_data['Sputter_Time__s_'],
                                  self.analyzer.mapped_data['Intensity'], label='Intensity Mapped', color='blue')

            self.canvas.axes.plot(self.analyzer.df['Sputter_Time__s_'],
                                  self.analyzer.df['Intensity'], label='Intensity', color='green')

            # Highlight detected spike intervals
            for start, end in self.analyzer.skip_intervals:
                self.canvas.axes.axvspan(start, end, color='red', alpha=0.3)

            # Set plot labels and legends
            self.canvas.axes.set_title('Intensity with Detected Spikes')
            self.canvas.axes.set_xlabel('Sputter Time (s)')
            self.canvas.axes.set_ylabel('Intensity')
            self.canvas.axes.legend()

            # Refresh canvas to display the updated plot
            self.canvas.draw()

    def update_console(self):
        # Display logs in the console
        self.console.setPlainText(self.log_stream.getvalue())


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
