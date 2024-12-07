# -*- coding: utf-8 -*-
"""*widget_xy_chart* file.

*widget_xy_chart* file that contains ...

.. note:: LEnsE - Institut d'Optique - version 0.3.4

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""

import numpy as np
import sys

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from pyqtgraph import PlotWidget, mkPen, mkBrush
from lensepy.css import *

class XYChartWidget(QWidget):
    """
    Widget used to display data in a 2D chart - X and Y axis.
    Children of QWidget - QWidget can be put in another widget and / or window
    ---
    
    Attributes
    ----------
    title : str
        title of the chart
    plot_chart_widget : PlotWidget
        pyQtGraph Widget to display chart
    plot_chart : PlotWidget.plot
        plot object of the pyQtGraph widget
    plot_x_data : Numpy array
        value to display on X axis
    plot_y_data : Numpy array
        value to display on Y axis
    
    Methods
    -------
    set_data(x_axis, y_axis):
        Set the X and Y axis data to display on the chart.
    refresh_chart():
        Refresh the data of the chart.
    set_title(title):
        Set the title of the chart.
    set_information(infos):
        Set informations in the informations label of the chart.
    set_background(css_color):
        Modify the background color of the widget.
    """

    def __init__(self):
        """
        Initialisation of the time-dependent chart.
        """
        super().__init__()
        self.title = ''  # Title of the chart
        self.layout = QVBoxLayout()  # Main layout of the QWidget

        # Title label
        self.title_label = QLabel(self.title)
        style = "background-color: darkgray;"
        style += "font-weight:bold;"
        style += "color:white;"
        style += "font-size:20px;"
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(style)

        # Option label
        self.info_label = QLabel('')
        style = "background-color: lightgray;"
        style += "font-size:10px;"
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet(style)

        self.plot_chart_widget = PlotWidget()  # pyQtGraph widget
        # Create Numpy array for X and Y data
        self.plot_x_data = np.array([])
        self.plot_y_data = np.array([])
        self.x_label = ''
        self.y_label = ''

        # No data at initialization
        self.pen = mkPen(color=BLUE_IOGS, style=Qt.PenStyle.SolidLine, width=2.5)
        self.brush = mkBrush(ORANGE_IOGS)
        self.plot_chart = self.plot_chart_widget.plot([0], pen=self.pen)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.plot_chart_widget)
        self.layout.addWidget(self.info_label)
        self.setLayout(self.layout)

    def set_data(self, x_axis, y_axis, x_label: str = '', y_label: str = ''):
        """
        Set the X and Y axis data to display on the chart.

        Parameters
        ----------
        x_axis : Numpy array
            X-axis value to display.
        y_axis : Numpy array
            Y-axis value to display.
        """
        self.plot_x_data = x_axis
        self.plot_y_data = y_axis
        self.x_label = x_label
        self.y_label = y_label

    def refresh_chart(self, last: int = 0):
        """
        Refresh the data of the chart.
        """
        self.plot_chart_widget.removeItem(self.plot_chart)
        if last != 0:
            if len(self.plot_x_data) > last:
                x_plot = self.plot_x_data[-last:]
                y_plot = self.plot_y_data[-last:]
                self.plot_chart = self.plot_chart_widget.plot(x_plot, y_plot,
                                                              pen=self.pen, symbol='o', brush=self.brush)
            else:
                print('To do')
        else:
            self.plot_chart = self.plot_chart_widget.plot(self.plot_x_data,
                                                      self.plot_y_data,
                                                      pen=self.pen)
        x_axis = self.plot_chart_widget.getPlotItem().getAxis('bottom')
        x_size = len(self.plot_x_data)
        Te = self.plot_x_data[1]-self.plot_x_data[0]
        xTicks = [x_size/20*Te, x_size/100*Te]
        x_axis.setTickSpacing(xTicks[0], xTicks[1])
        # set x ticks (major and minor)
        self.plot_chart_widget.showGrid(x=True, y=True)
        styles = {"color": "black", "font-size": "18px"}
        if self.y_label != '':
            self.plot_chart_widget.setLabel("left", self.y_label, **styles)
        if self.x_label != '':
            self.plot_chart_widget.setLabel("bottom", self.x_label, **styles)

    def update_infos(self, value: bool = True):
        """
        Update mean and standard deviation data and display.

        :param value: True to display mean and standard deviation.
            False to display "acquisition in progress".
        """
        if value:
            mean_d = round(np.mean(self.plot_y_data), 2)
            stdev_d = round(np.std(self.plot_y_data), 2)
            self.set_information(f'Mean = {mean_d} / Standard Dev = {stdev_d}')
        else:
            self.set_information('Data Acquisition In Progress')

    def set_title(self, title: str):
        """
        Set the title of the chart.

        :param title: Title of the chart.
        """
        self.title = title
        self.title_label.setText(self.title)

    def set_information(self, infos: str):
        """
        Set informations in the informations label of the chart.
        (bottom)

        :param infos: Informations to display.
        """
        self.info_label.setText(infos)

    def set_background(self, css_color: str):
        """
        Modify the background color of the widget.

        :param css_color: Color in CSS style.
        """
        self.plot_chart_widget.setBackground(css_color)
        self.setStyleSheet("background:" + css_color + ";")

    def clear_graph(self):
        """
        Clear the main chart of the widget.
        """
        self.plot_chart_widget.clear()

    def display_last(self, number: int = 50):
        """Display the N last points.
        :param number: Number of points to display.
        """
        self.refresh_chart(last=number)



# -----------------------------------------------------------------------------------------------
# Only for testing
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("XY Chart")
        self.setGeometry(100, 100, 800, 600)

        self.centralWid = QWidget()
        self.layout = QVBoxLayout()

        self.chart_widget = XYChartWidget()
        self.chart_widget.set_title('My Super Chart')
        self.chart_widget.set_information('This is a test')
        self.layout.addWidget(self.chart_widget)

        x = np.linspace(0, 100, 101)
        y = np.random.randint(0, 100, 101, dtype=np.int8)

        self.chart_widget.set_background('white')

        self.chart_widget.set_data(x, y)
        self.chart_widget.refresh_chart()
        self.chart_widget.display_last(50)

        self.centralWid.setLayout(self.layout)
        self.setCentralWidget(self.centralWid)

# Launching as main for tests
from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyWindow()
    main.show()
    sys.exit(app.exec())
