import matplotlib.pyplot as plt
from sas.sascalc.calculator import sas_gen as sg
from sas.sascalc.calculator import geni
from sas.qtgui.Plotting.Slicers import SectorSlicer as ss
import sas.qtgui.Plotting.PlotterData as pltd
import sas.qtgui.Plotting.PlotUtilities as pu
from scipy.spatial.transform import Rotation
import copy
from numpy.typing import NDArray

import sasdata.dataloader.data_info as di
import sasdata.dataloader.loader as ld
import numpy as np
import timeit, time, matplotlib
import matplotlib.colors as colors
import os

class Model:
    _model: sg.GenSAS
    _xvals = None
    _yvals = None
    qmax_x = None
    npts_x = None
    data = None,
    is_avg = False

    data_to_plot = None

    def __init__(self) -> None:
        pass

    def MagSLD2Model(self, data: sg.MagSLD):
        self._model = sg.GenSAS()
        self._model.set_sld_data(data)
        self._model.params["Up_theta"] = 90
        print("model created")

    def LoadFile(self, filepath: str):
        MagSLDData = None
        ext = filepath[-3:].lower()
        match ext:

            case "omf":
                omfloader = sg.OMFReader()
                MagSLDData = omfloader.read(filepath)
                print('\nloaded OMF file at "{0}"'.format(filepath))

            case "vtk":
                vtkloader = sg.VTKReader()
                MagSLDData = vtkloader.read(filepath)

            case "pdb":
                pdbloader = sg.PDBReader()
                MagSLDData = pdbloader.read(filepath)

            case "sld":
                sldloader = sg.SLDReader()
                MagSLDData = sldloader.read(filepath)

            case _:
                raise ValueError("Invalid file extension: " + ext)
        self.MagSLD2Model(MagSLDData)

    def computeI(
        self, QxMax=0.3, bins=30, rotation=Rotation.from_rotvec([0, 0, 0]), cross_section = [0,1], background=0.05, update=None
    ):
        """Carry out the compuation of I(qx, qy) in a new thread

        Gen compute complete function

        This function separates the range of q or (qx,qy) into chunks and then
        calculates each chunk with calls to the model.  Adapted from sasview
        source.

        :param input: input list [qx_data, qy_data, i_out]
        :type input: list
        """
        self._model.params["background"] = background
        self._model.params["Up_frac_in"], self._model.params["Up_frac_out"] = cross_section
        self._model.set_rotations(xyz_to_UVW=rotation)
        self.genXYData(QxMax=QxMax, bins=bins)

        input = [0, 1]
        input[0] = self.data.qx_data
        input[1] = self.data.qy_data
        timer = timeit.default_timer
        update_rate = 1.0  # seconds between updates
        next_update = timer() + update_rate if update is not None else np.inf
        nq = len(input[0])
        chunk_size = 256
        out = []
        for ind in range(0, nq, chunk_size):
            t = timer()
            if t > next_update:
                update(time=t, percentage=100 * ind / nq)
                time.sleep(0.01)
                next_update = t + update_rate

            inputi = [
                input[0][ind : ind + chunk_size],
                input[1][ind : ind + chunk_size],
            ]
            outi = self._model.runXY(inputi)

            out.append(outi)
        else:
            out = np.hstack(out)
            self.data_to_plot = out
            self.data.data = out
            if not self.is_avg:
                print("Gen computation completed.")
        return

    def genXYData(self, QxMax, bins):
        """Create the 2D data range for qx,qy

        Copied from previous version
        Create 2D data by default
        Adapted from Sasview source code

        .. warning:: This data is never plotted.
        """

        self.qmax_x = QxMax
        self.npts_x = bins
        self.data = pltd.Data2D()
        self.data.is_data = False
        # Default values
        self.data.detector.append(di.Detector())
        index = len(self.data.detector) - 1
        self.data.detector[index].distance = 8000  # mm
        self.data.source.wavelength = 6  # A
        self.data.detector[index].pixel_size.x = 5  # mm
        self.data.detector[index].pixel_size.y = 5  # mm
        self.data.detector[index].beam_center.x = self.qmax_x
        self.data.detector[index].beam_center.y = self.qmax_x
        self.data.detector[index]
        xmax = self.qmax_x
        xmin = -xmax
        ymax = self.qmax_x
        ymin = -ymax
        qstep = self.npts_x
        x = np.linspace(start=xmin, stop=xmax, num=qstep, endpoint=True)
        y = np.linspace(start=ymin, stop=ymax, num=qstep, endpoint=True)
        # use data info instead
        new_x = np.tile(x, (len(y), 1))
        new_y = np.tile(y, (len(x), 1))
        new_y = new_y.swapaxes(0, 1)
        # all data require now in 1d array
        qx_data = new_x.flatten()
        qy_data = new_y.flatten()
        q_data = np.sqrt(qx_data * qx_data + qy_data * qy_data)
        # set all True (standing for unmasked) as default
        mask = np.ones(len(qx_data), dtype=bool)
        self.data.source = di.Source()
        self.data.data = np.ones(len(mask))
        self.data.err_data = np.ones(len(mask))
        self.data.qx_data = qx_data
        self.data.qy_data = qy_data
        self.data.q_data = q_data
        self.data.mask = mask
        # store x and y bin centers in q space
        self.data.x_bins = x
        self.data.y_bins = y
        # max and min taking account of the bin sizes
        self.data.xmin = xmin
        self.data.xmax = xmax
        self.data.ymin = ymin
        self.data.ymax = ymax

    def plot(self):
        """Plots data and scales it logarithmically.  Largely adapted from Sasview source code.
        """
        x_coords = model.data.qx_data  # Length n
        y_coords = model.data.qy_data  # Length n
        intensities = model.data_to_plot  # Length n^2 (3x3)
        output = copy.deepcopy(intensities)
        try:
            if model.data.zmin <= 0 and len(output[output > 0]) > 0:
                zmin_temp = model.data.zmin
                output[output > 0] = np.log10(output[output > 0])
            elif model.data.zmin <= 0:
                zmin_temp = model.data.zmin
                output[output > 0] = np.zeros(len(output))
                output[output <= 0] = -32
            else:
                zmin_temp = model.data.zmin
                output[output > 0] = np.log10(output[output > 0])
        except:
            # Too many problems in 2D plot with scale
            print("issue with log")
            output[output > 0] = np.log10(output[output > 0])
            pass
        grid_intensity = np.reshape(output, (self.npts_x, self.npts_x))
        plt.imshow(
            grid_intensity,
            origin="lower",
            extent=(min(x_coords), max(x_coords), min(y_coords), max(y_coords)),
            cmap="jet",
            interpolation="nearest",
            vmin=output.min(),
            vmax=output.max(),
        )
        plt.colorbar(label="Intensity")  # Add a color bar
        plt.xlabel("X Coordinates")
        plt.ylabel("Y Coordinates")
        plt.title("Heatmap of Intensities")
        plt.show()
        print("graph shown")

    def save(self, filepath: str):
        """
        Generic file save routine called by SaveData1D and SaveData2D
        Adapted from Sasview Source

        :param data: Data 1D or Data2D object the data will be taken from
        :param wildcard_dict: Dictionary in format {"Display Text": ".ext"}
        """
        wildcard_dict = {"IGOR/DAT 2D file in Q_map": ".dat", "NXcanSAS files": ".h5"}

        # Ensure wildcard_dict is a dictionary
        if wildcard_dict is None or not isinstance(wildcard_dict, dict):
            wildcard_dict = {}
        # Construct wildcard string based on dictionary passed in
        wildcards = ""
        for wildcard in list(wildcard_dict.keys()):
            wildcards += f"{wildcard} (*{wildcard_dict[wildcard]});;"
        wildcards += "All files (*.*)"

        caption = "Save As"
        filter = wildcards
        parent = None
        # Query user for filename.
        filename = filepath

        # User cancelled or did not enter a filename
        if not filename:
            return

        # Check for selected file format
        ext = filepath[-3:].lower()
        for wildcard in list(wildcard_dict.keys()):
            if wildcard in ext:
                # Specify save format, while allowing free-form file extensions
                file_format = wildcard_dict[wildcard]
                # Append selected extension if no extension typed into box by user
                # Do not append if any extension typed to allow freeform extensions
                if len(filename.split(".")) == 1:
                    filename += wildcard_dict[wildcard]
                break
        else:
            # Set file_format to None if 'All files (*.*)' selected
            file_format = None

        # Instantiate a loader
        loader = ld.Loader()
        try:
            loader.save(filename, self.data, file_format)
            print("file saved")
        except (KeyError, ValueError):
            # If the base loader is unable to save the file, fallback to text file.
            format_based_on_data = "IGOR" if isinstance(self.data, di.Data2D) else "ASCII"
            print(
                f"Unknown file type specified when saving {filename}. Saving in {format_based_on_data} format."
            )
            self.onTXTSave(self.data, filename)

    def onTXTSave(self, data, path):
        """
        Save file as formatted txt
        coppied from Sasview source.
        """
        reader = None
        append_format = len(path.split(".")) == 1
        if isinstance(data, di.Data1D):
            from sasdata.dataloader.readers.ascii_reader import Reader as ASCIIReader
            path += ".txt" if append_format else ""
            reader = ASCIIReader()
        elif isinstance(data, di.Data2D):
            from sasdata.dataloader.readers.red2d_reader import Reader as Red2DReader
            path += ".dat" if append_format else ""
            reader = Red2DReader()
        if reader:
            reader.write(path, data)
        else:
            print(f"Data must be of type Data1D or Data2D, {type(data)} given.")

    def rotationAvg(
        
        
        self,
        thetaMin=1,
        thetaMax=89,
        dtheta=2,
        phiMin=0,
        phiMax=360,
        dphi=8,
        omegaMin=0,
        omegaMax=90,
        domega=15,
        bins=30,
        QxMax=0.3,
        cross_section = [0,1]
    ):
        # calculate total number of rotations for each axis
        numTheta = (thetaMax - thetaMin) / dtheta
        numPhi = (phiMax - phiMin) / dphi
        numOmega = (omegaMax - omegaMin) / domega
        timeCheck = 1
        self.is_avg = True
        sqr = bins ** 2
        # initialize array for summed scattering
        netScatteringData = np.zeros((sqr))
        startTime = time.time()

        for theta in np.arange(start=thetaMin, stop=thetaMax+1, step=dtheta):
            for phi in np.arange(start=phiMin, stop=phiMax+1, step=dphi):
                for omega in np.arange(start=omegaMin, stop=omegaMax+1, step=domega):
                    r=Rotation.from_euler('xzx',[omega, theta, phi], degrees=True)
                    self.computeI(bins=bins, rotation=r, QxMax=QxMax, cross_section=cross_section)
                    netScatteringData += self.data.data

                    # print estimated computation time
                    if timeCheck:
                        timeCheck=0
                        print('estimated time to completion (hrs): '+((time.time() - startTime)*numTheta*numPhi*numOmega/60/60).__str__())
        self.data.data = np.divide(netScatteringData, (numTheta*numPhi*numOmega))
        print("Avg computation completed in {0} hrs.".format(((time.time() - startTime)*numTheta*numPhi*numOmega/60/60)))
        self.data_to_plot = self.data.data
        self.is_avg=False





# # model._xvals = xs
# # model._yvals= ys
# # print(model.data_to_plot)

# x_coords = model.data.qx_data  # Length n
# y_coords = model.data.qy_data  # Length n
# intensities = model.data_to_plot  # Length n^2 (3x3)
# print(intensities.__len__())
# # print(y_coords)
# intensities.min()
# # Create a heatmap
# grid_x, grid_y = np.meshgrid((x_coords), (y_coords))
# # grid_intensity = np.zeros_like(grid_x, dtype=float)

# # Fill the grid with intensities
# # intensities[intensities < 0.05] = intensities.min()
# output = copy.deepcopy(intensities)
# try:
#     if model.data.zmin <= 0 and len(output[output > 0]) > 0:
#         zmin_temp = model.data.zmin
#         output[output > 0] = np.log10(output[output > 0])
#     elif model.data.zmin <= 0:
#         zmin_temp = model.data.zmin
#         output[output > 0] = np.zeros(len(output))
#         output[output <= 0] = -32
#     else:
#         zmin_temp = model.data.zmin
#         output[output > 0] = np.log10(output[output > 0])
# except:
#     # Too many problems in 2D plot with scale
#     print("issue with log")
#     output[output > 0] = np.log10(output[output > 0])
#     pass

# print(output.min())
# grid_intensity = np.reshape(output, (30, 30))
# plt.imshow(
#     grid_intensity,
#     origin="lower",
#     extent=(min(x_coords), max(x_coords), min(y_coords), max(y_coords)),
#     cmap="jet",
#     interpolation="nearest",
#     vmin=output.min(),
#     vmax=output.max(),
# )
# # fig = plt.figure(figsize=(22,11))
# # ax1 = fig.add_subplot(121)
# # ax1.pcolormesh(x_coords, y_coords, intensities, edgecolors='w',cmap="plasma")


# # result = IntensityCalc(model)

# # sas.qtgui.Plotting.Slicers.SectorSlicer module

# # LoadFile(os.path.join(".\REM1.5MTestParams_C1_L1SLD0.9_R3.25e-09_SFB0.04.omf"))
