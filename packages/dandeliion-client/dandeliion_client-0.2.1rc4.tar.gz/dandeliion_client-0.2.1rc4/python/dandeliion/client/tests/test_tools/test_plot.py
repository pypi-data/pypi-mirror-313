import client.tools.plotting as plot
import numpy as np
import unittest

from unittest.mock import patch


class PlotTest(unittest.TestCase):
    def setUp(self):
        self.data_two = [
            {
                'type': 'Line',
                'x': [1, 3, 5],
                'y': [2, 4, 6]
            },
            {
                'x': [7, 9, 11],
                'y': [8, 10, 12]
            }
        ]
        self.data_one = [
            {
                'x': [7, 9, 11],
                'y': [8, 10, 12]
            }
        ]

    @patch('client.tools.plotting.go')
    def test_make_plot(self, mock_go):
        '''Test make_plot returns html plot with two lines'''
        result = plot.make_plot(
            self.data_two,
            output=plot.default_html_output
        )

        mock_go.Figure.assert_called_once_with(
            data=[
                mock_go.Line(x=[1, 3, 5], y=[2, 4, 6]),
                mock_go.Scatter(x=[7, 9, 11], y=[8, 10, 12])
            ],
            layout={
                'yaxis_tickformat': '~g'
            }
        )

        mock_go.Figure.return_value.to_html.assert_called_once_with(
            include_mathjax=False,
            include_plotlyjs=False,
            full_html=False
        )
        self.assertEqual(result, mock_go.Figure.return_value.to_html.return_value)

    @patch('client.tools.plotting.go')
    def test_make_plot_logged(self, mock_go):
        '''Test make_plot returns one log plot'''
        result = plot.make_plot(
            self.data_one,
            layout={'log_y': True},
            output=plot.default_html_output
        )

        mock_go.Figure.assert_called_once_with(
            data=[
                mock_go.Scatter(x=[7, 9, 11], y=[8, 10, 12])
            ],
            layout={
                'yaxis_tickformat': '~g',
                'log_y': True
            }
        )
        self.assertEqual(result, mock_go.Figure.return_value.to_html.return_value)

    @patch('client.tools.plotting.go')
    def test_make_plot_show(self, mock_go):
        '''Test make_plot can show'''
        plot.make_plot(
            self.data_one
        )
        mock_go.Figure.return_value.show.assert_called_once()

    @patch('client.tools.plotting.go')
    def test_make_plot_png(self, mock_go):
        '''Test make_plot to png'''
        result = plot.make_plot(
            self.data_one,
            output={'format': 'png'}
        )
        mock_go.Figure.return_value.to_image.assert_called_once_with(
            format='png'
        )
        self.assertEqual(result, mock_go.Figure.return_value.to_image.return_value)

    @patch('client.tools.plotting.make_plot')
    @patch('client.tools.plotting.np.loadtxt')
    def test_plot_dat_file(self, mock_loadtxt, mock_plot):
        '''Test plot_dat_file reads in and plots a file'''
        # fake value for mocks to return
        mock_loadtxt.return_value = np.array([[1, 2], [3, 4], [5, 6]])
        result = plot.plot_dat_file('input/file/path.dat', layout={'a': 'layout'})

        # assert make_plot_div return value comes back
        self.assertEqual(result, mock_plot.return_value)

        # assert np.loadtxt callled correctly
        mock_loadtxt.assert_called_once_with('input/file/path.dat', skiprows=1)

        # assert correct data passed to make_plot
        mock_plot.assert_called_once_with(
            [{
                'x': [1, 3, 5],
                'y': [2, 4, 6]
            }],
            layout={'a': 'layout'}
        )

    @patch('client.tools.plotting.logger.warning')
    def test_plot_dat_file_bad_path(self, mock_warning):
        '''Test plot_dat_file when a bad path is used'''
        expected = '<span>Simulation output file not found</span>'
        result = plot.plot_dat_file('bad_file_path.dat')

        # ensure a warning is raised
        mock_warning.assert_called_once()
        self.assertEqual(result, expected)
