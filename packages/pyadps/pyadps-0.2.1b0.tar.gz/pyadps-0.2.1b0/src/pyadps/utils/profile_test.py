import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib.widgets import Button, Slider, TextBox
from pyadps.utils import readrdi as rd

from .plotgen import plotmask, plotvar


class PlotEnds:
    def __init__(self, pressure, delta=10):
        self.dep = pressure / 980

        self.n = np.size(self.dep)
        self.delta = delta
        self.nmin = 0
        self.nmax = self.nmin + self.delta
        self.mmax = 0
        self.mmin = self.mmax - self.delta

        self.x = np.arange(0, self.n)

        self.start_ens = 0
        self.end_ens = 0

        self.fig, self.axs = plt.subplots(1, 2, figsize=(12, 8))
        self.fig.set_facecolor("darkgrey")
        plt.subplots_adjust(bottom=0.28, right=0.72)

        self.ax_end = self.fig.add_axes(rect=(0.25, 0.08, 0.47, 0.03))
        self.ax_start = self.fig.add_axes(rect=(0.25, 0.15, 0.47, 0.03))
        self.ax_button = self.fig.add_axes(rect=(0.81, 0.05, 0.15, 0.075))
        # self.ax_depmaxbutton = self.fig.add_axes(rect=(0.68, 0.13, 0.04, 0.02))
        # self.ax_depminbutton = self.fig.add_axes(rect=(0.25, 0.13, 0.04, 0.02))
        # self.ax_recmaxbutton = self.fig.add_axes(rect=(0.68, 0.06, 0.04, 0.02))
        # self.ax_recminbutton = self.fig.add_axes(rect=(0.25, 0.06, 0.04, 0.02))

        # Plot
        self.axs[0].scatter(self.x, self.dep, color="k")
        self.axs[1].scatter(self.x, self.dep, color="k")

        # Figure Labels
        for i in range(2):
            self.axs[i].set_xlabel("Ensemble")
        self.axs[0].set_xlim([self.nmin - 1, self.nmax])
        self.axs[1].set_xlim([self.n - self.delta, self.n])
        self.axs[0].set_ylabel("Depth (m)")
        self.fig.suptitle("Trim Ends")

        # Display statistics
        self.axs[0].text(0.82, 0.60, "Statistics", transform=plt.gcf().transFigure)
        self.max = np.round(np.max(self.dep), decimals=2)
        self.min = np.round(np.min(self.dep), decimals=2)
        self.median = np.round(np.median(self.dep), decimals=2)
        self.mean = np.round(np.mean(self.dep), decimals=2)
        self.t1 = self.axs[0].text(
            0.75,
            0.50,
            f"Dep. Max = {self.max} \nDep. Min = {self.min} \nDep. Median = {self.median}",
            transform=plt.gcf().transFigure,
        )

        self.sl_start = Slider(
            ax=self.ax_start,
            label="Dep. Ensemble",
            valmin=self.nmin,
            valmax=self.nmax,
            valinit=0,
            valfmt="%i",
            valstep=1,
        )

        self.sl_end = Slider(
            ax=self.ax_end,
            label="Rec. Ensemble",
            valmin=self.mmin,
            valmax=self.mmax,
            valinit=0,
            valfmt="%i",
            valstep=1,
        )

        self.sl_start.on_changed(self.update1)
        self.sl_end.on_changed(self.update2)
        self.button = Button(self.ax_button, "Save & Exit")
        # self.depminbutton = Button(self.ax_depminbutton, "<<")
        # self.depmaxbutton = Button(self.ax_depmaxbutton, ">>")
        # self.recminbutton = Button(self.ax_recminbutton, "<<")
        # self.recmaxbutton = Button(self.ax_recmaxbutton, ">>")

        self.button.on_clicked(self.exitwin)

    def update1(self, value):
        self.axs[0].scatter(self.x, self.dep, color="k")
        self.axs[0].scatter(self.x[0:value], self.dep[0:value], color="r")
        self.start_ens = value

    def update2(self, value):
        self.axs[1].scatter(self.x, self.dep, color="k")
        if value < 0:
            self.axs[1].scatter(
                self.x[self.n + value : self.n],
                self.dep[self.n + value : self.n],
                color="r",
            )
        self.end_ens = value

    def show(self):
        plt.show()

    def exitwin(self, event):
        plt.close()


def trim_ends(vlobj, mask, method="Manual"):
    transducer_depth = vlobj.vleader["Depth of Transducer"]
    # pressure = vlobj.vleader["Pressure"]
    if method == "Manual":
        out = PlotEnds(transducer_depth, delta=20)
        out.show()
        if out.start_ens > 0:
            mask[:, 0 : out.start_ens] = 1

        if out.end_ens < 0:
            mask[:, out.end_ens :] = 1

    return mask


def side_lobe_beam_angle(flobj, vlobj, mask, orientation='default', water_column_depth=0, extra_cells=2):
    beam_angle = int(flobj.system_configuration()["Beam Angle"])
    cell_size = flobj.field()["Depth Cell Len"]
    bin1dist = flobj.field()["Bin 1 Dist"]
    cells = flobj.field()["Cells"]
    ensembles = flobj.ensembles
    transducer_depth = vlobj.vleader["Depth of Transducer"]

    if orientation.lower() == "default":
        orientation = flobj.system_configuration()['Beam Direction']

    if orientation.lower() == "up":
        sgn = -1
        water_column_depth = 0
    else:
        sgn = 1

    beam_angle = np.deg2rad(beam_angle)
    depth = transducer_depth / 10
    valid_depth = (water_column_depth - sgn*depth) * np.cos(beam_angle) + sgn*bin1dist / 100
    valid_cells = np.trunc(valid_depth * 100 / cell_size) - extra_cells

    for i in range(ensembles):
        c = int(valid_cells[i])
        if cells > c:
            mask[c:, i] = 1

    return mask


def side_lobe_rssi_bump(echo, mask):
    pass


def manual_cut_bins(mask, min_cell, max_cell, min_ensemble, max_ensemble):
    """
    Apply manual bin cutting by selecting a specific range of cells and ensembles.

    Parameters:
        mask (numpy array): The mask array to modify.
        min_cell (int): The minimum cell index to mask.
        max_cell (int): The maximum cell index to mask.
        min_ensemble (int): The minimum ensemble index to mask.
        max_ensemble (int): The maximum ensemble index to mask.

    Returns:
        numpy array: The updated mask with selected areas masked.
    """
    # Ensure the indices are within valid range
    min_cell = max(0, min_cell)
    max_cell = min(mask.shape[0], max_cell)
    min_ensemble = max(0, min_ensemble)
    max_ensemble = min(mask.shape[1], max_ensemble)

    # Apply mask on the selected range
    mask[min_cell:max_cell, min_ensemble:max_ensemble] = 1

    return mask
