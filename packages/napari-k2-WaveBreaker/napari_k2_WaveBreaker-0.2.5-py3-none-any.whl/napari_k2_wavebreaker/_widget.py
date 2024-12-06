"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING
from qtpy.QtWidgets import QWidget, QFileDialog
from qtpy.QtGui import QPixmap
import qtpy.QtCore
from qtpy import uic
from multiprocessing import Pool, set_start_method, get_start_method
from functools import partial
import cv2
import platform

from skimage.morphology import disk
from skimage.color import rgb2gray

from napari.qt.threading import WorkerBase, WorkerBaseSignals
from napari.utils.notifications import show_info
from napari.utils.colormaps import DirectLabelColormap
from napari import Viewer, run

if TYPE_CHECKING:
    import napari

import warnings


from napari_plugin_engine import napari_hook_implementation

try:
    from .autocorrelation import *
    from .ClickLabel import ClickLabel
    from .crosscorrelation import *
    from .functions import *
except ImportError:
    from autocorrelation import *
    from ClickLabel import ClickLabel
    from crosscorrelation import *
    from functions import *

from scipy.ndimage import gaussian_filter
from pathvalidate import sanitize_filename

class ArrayShapeIncompatible(Exception):
    """Raised when the input value is too small"""
    pass

class NoOutputPath(Exception):
    """Raised when the output path is not defined"""
    pass

class NoGridsToAnalyze(Exception):
    """Raised when there are no grids to analyze"""
    pass

class AnalysisAttemptOnEmptyImage(Exception):
    """Raised when the image is empty"""
    pass

class resolutionError(Exception):
    """Raised when the resolution is zero"""
    pass

class GridSplitError(Exception):
    """Raised when the grid split is not possible"""
    pass


# Define the main widget window for the plugin
class AutocorrelationTool(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()

        if platform.system() == "Darwin":
            set_start_method('spawn', force=True)

        self.viewer = napari_viewer
        self.UI_FILE = abspath(__file__, 'static/form.ui')  # path to .ui file
        uic.loadUi(self.UI_FILE, self)

        # Updates comboboxes when a layer is added, removed or updated
        self.updatelayer()
        self.viewer.layers.events.removed.connect(self.updatelayer)
        self.viewer.layers.events.inserted.connect(self.updatelayer)
        self.viewer.layers.events.changed.connect(self.updatelayer)

        self.thread = None
        self.outputPath = None
        self.inputarray = None
        self.maskedarray = None
        self.maskedarray_c = None
        self.outputPath = None
        self.threshmask = None
        self.restrictdeg = [-90, 90]
        self.doCross = False

        self.label_19.setVisible(False)
        self.comboBox_layer_1.setVisible(False)
        self.radioButton_1.setVisible(False)
        self.radioButton_2.setVisible(False)
        self.radioButton_1.toggled.connect(self.corToggle)

        self.label_A.clicked.connect(self.corImgA)
        self.label_C.clicked.connect(self.corImgC)
        self.genThresh.clicked.connect(self.visualizeThresh)

        self.comboBox_mode.currentIndexChanged.connect(self.changeLock_zone)
        self.comboBox_gridsplit.currentIndexChanged.connect(self.changeLock_grid)

        self.angleSlider.valueChanged.connect(self.updateslidervalue)
        self.analyze.clicked.connect(self.Autocorrelate)
        self.pushButton_File.clicked.connect(self.filedialog)

    def corImgA(self):
        self.radioButton_1.click()
        self.label_A.setPixmap(QPixmap(abspath(__file__, 'static/auto_T.png')))
        self.label_C.setPixmap(QPixmap(abspath(__file__, 'static/cross_F.png')))


    def corImgC(self):
        self.radioButton_2.click()
        self.label_A.setPixmap(QPixmap(abspath(__file__, 'static/auto_F.png')))
        self.label_C.setPixmap(QPixmap(abspath(__file__, 'static/cross_T.png')))

    # Toggle between autocorrelation and cross-correlation
    def corToggle(self):
        if self.radioButton_1.isChecked():
            self.label_19.setVisible(False)
            self.comboBox_layer_1.setVisible(False)
            self.doCross = False

        else:
            self.label_19.setVisible(True)
            self.comboBox_layer_1.setVisible(True)
            self.doCross = True

    def updateslidervalue(self):
        self.sliderLabel.setText(str(self.angleSlider.value()))

    # File dialogue for output images and csv
    def filedialog(self):
        self.outputPath = QFileDialog.getExistingDirectory(self, 'Select output path')

    # Locks restricted angle parameters when full search is enabled
    def changeLock_zone(self):
        if self.comboBox_mode.currentText() == "Full search":
            self.spinBox_zoneMid.setEnabled(False)
            self.angleSlider.setEnabled(False)
            self.restrictdeg = [-90, 90]

        else:
            self.spinBox_zoneMid.setEnabled(True)
            self.angleSlider.setEnabled(True)
            self.restrictdeg = [self.spinBox_zoneMid.value() - self.angleSlider.value(),
                                self.spinBox_zoneMid.value() + self.angleSlider.value()]

    # Locks grid split option when None is selected
    def changeLock_grid(self):
        if self.comboBox_gridsplit.currentText() == "None":
            self.spinBox_gridLeft.setEnabled(False)
            self.spinBox_gridRight.setEnabled(False)
            self.checkBox_restrictGrid.setEnabled(False)

        else:
            self.spinBox_gridLeft.setEnabled(True)
            self.spinBox_gridRight.setEnabled(True)
            self.checkBox_restrictGrid.setEnabled(True)

    # Updates comboboxes
    def updatelayer(self):
        one = self.comboBox_layer.currentText()
        two = self.comboBox_layer_1.currentText()


        self.comboBox_layer.clear()
        self.comboBox_layer_1.clear()

        for i in self.viewer.layers:
            self.comboBox_layer.addItem(str(i))
            self.comboBox_layer_1.addItem(str(i))

        if one in self.viewer.layers:
            self.comboBox_layer.setCurrentText(one)
        if two in self.viewer.layers:
            self.comboBox_layer_1.setCurrentText(two)

    def threshold(self, input):
        blurredz = gaussian_filter(input, sigma=3)
        pixelsize = self.doubleSpinBox_pixel.value() / 2

        ### MANUAL THRESHOLDING ###
        thresh = (self.threshSlider.value() / 1000) * np.max(blurredz)
        print(thresh)
        blurredz[blurredz <= thresh] = 0
        blurredz[blurredz != 0] = 1


        kernel = disk(pixelsize)


        mask = cv2.morphologyEx(blurredz, cv2.MORPH_CLOSE, kernel)

        def biggestobject(mask):
            # Find biggest object in mask
            labels = measure.label(mask)
            props = measure.regionprops(labels)
            areas = [prop.area for prop in props]
            biggest = np.argmax(areas)
            biggestmask = labels == (biggest + 1)
            return biggestmask

        # Segment biggest object in image
        mask = biggestobject(mask)



        return mask

    def applythresh(self, array, arrayc, mask):

        array[mask == 0] = np.nan

        if self.doCross and (arrayc is not None):
            arrayc[mask == 0] = np.nan

        return array, arrayc


    def readfile(self):
        ### Read selected layer
        inputarray = self.viewer.layers[self.comboBox_layer.currentText()].data
        ### Set to greyscale if needed
        try:
            inputarray = rgb2gray(inputarray)
        except Exception:
            pass

        self.inputarray = np.array(inputarray, dtype="float32")

        if self.doCross:
            inputarray = self.viewer.layers[self.comboBox_layer_1.currentText()].data
            ### Set to greyscale if needed
            try:
                inputarray = rgb2gray(inputarray)
            except Exception:
                pass

            self.inputarray_c = np.array(inputarray, dtype='float32')

    def visualizeThresh(self):
        if (str(self.comboBox_layer.currentText()) + "_mask") in self.viewer.layers:
            self.viewer.layers.remove(str(self.comboBox_layer.currentText()) + "_mask")
        self.readfile()
        mask = self.threshold(self.inputarray)
        self.viewer.add_labels(mask.astype(int),
                                name=str(self.viewer.layers[self.comboBox_layer.currentText()]) + "_mask",
                                colormap=DirectLabelColormap(color_dict= {None: [0, 0, 0, 0], 1: [0, 1, 1, 1]}),
                                opacity= 0.30)
        self.viewer.layers[str(self.viewer.layers[self.comboBox_layer.currentText()]) + "_mask"].brush_size = 100

    def createshapelayer(self):
        self.viewer.add_shapes(shape_type="rectangle", edge_width=5, edge_color='#05d9b9', face_color='#05e69f',
                               opacity=0.4, name=str(self.viewer.layers[self.comboBox_layer.currentText()]) + "_ROI")

    def updateprogress(self, progress):
        print(progress)
        if progress[0]:
            self.progressBar.setValue(100)
        else:
            self.progressBar.setValue(int(self.progressBar.value() + (1 / int(progress[1])) * 100))

    def Autocorrelate(self):
        self.readfile()

        #Checkpoints before analysis
        if self.doCross and np.shape(self.inputarray) != np.shape(self.inputarray_c):
            raise ArrayShapeIncompatible("Selected layers should have the same shape")
        elif (self.outputPath is None) and (self.checkBox_outCSV.isChecked() or self.checkBox_outImg.isChecked()):
            raise NoOutputPath("No output path selected")
        else:
            if (str(self.comboBox_layer.currentText()) + "_mask") in self.viewer.layers:
                maskedarray, maskedarrayc = self.applythresh(self.inputarray,
                                                             self.inputarray_c if self.doCross else None,
                                                             self.viewer.layers[self.comboBox_layer.currentText() + "_mask"].data)
            else:
                mask = self.threshold(self.inputarray)
                maskedarray, maskedarrayc = self.applythresh(self.inputarray,
                                                             self.inputarray_c if self.doCross else None,
                                                             mask)

                show_info("No mask layer available - Mask generated from current threshold value")

            self.changeLock_zone()
            self.thread = MyWorker()
            self.thread.updateparameters(currentlayer=self.comboBox_layer.currentText(),
                                         maskedarray=maskedarray,
                                         maskedarray_c=(maskedarrayc if self.doCross else None),
                                         mode=self.comboBox_mode.currentText(),
                                         gridsplitmode=self.comboBox_gridsplit.currentText(),
                                         gridsplitleft=self.spinBox_gridLeft.value(),
                                         gridsplitright=self.spinBox_gridRight.value(),
                                         gridsplitrestrict=self.checkBox_restrictGrid.isChecked(),
                                         autocormode=self.comboBox_AutocorMethod.currentText(),
                                         pixelsize=self.doubleSpinBox_pixel.value(),
                                         outimg=self.checkBox_outImg.isChecked(),
                                         outcsv=self.checkBox_outCSV.isChecked(),
                                         path=self.outputPath,
                                         restrictdeg=self.restrictdeg)

        self.progressBar.setValue(0)
        self.thread.start()

        self.thread.progress.connect(self.updateprogress)


class MyWorkerSignals(WorkerBaseSignals):
    progress = qtpy.QtCore.Signal(object)

class MyWorker(WorkerBase):
    # progress = qtpy.QtCore.Signal(object)

    def __init__(self):
        super().__init__(SignalsClass=MyWorkerSignals)
        self.currentlayer = None
        self.path = None
        self.outcsv = None
        self.outimg = None
        self.pixelsize = None
        self.autocormode = None
        self.gridsplitright = None
        self.gridsplitleft = None
        self.gridsplitmode = None
        self.gridsplitrestrict = None
        self.analysismode = None
        self.maskedarray = None
        self.restrictdeg = None

    def updateparameters(self,
                         currentlayer,
                         maskedarray,
                         maskedarray_c,
                         mode,
                         gridsplitmode,
                         gridsplitleft,
                         gridsplitright,
                         gridsplitrestrict,
                         autocormode,
                         pixelsize,
                         outimg,
                         outcsv,
                         path,
                         restrictdeg):

        self.currentlayer = currentlayer
        self.maskedarray = maskedarray
        self.maskedarray_c = maskedarray_c
        self.analysismode = mode
        self.gridsplitmode = gridsplitmode
        self.gridsplitleft = gridsplitleft
        self.gridsplitright = gridsplitright
        self.autocormode = autocormode
        self.pixelsize = pixelsize
        self.outimg = outimg
        self.outcsv = outcsv
        self.path = path
        self.restrictdeg = restrictdeg
        self.gridsplitrestrict = gridsplitrestrict

    def run(self):
        print("ok")
        print(self.outcsv)
        if self.pixelsize == 0:
            raise resolutionError("Resolution cannot be zero")

        gridsplitmode = self.gridsplitmode
        # gridsplitmode = "Auto"

        gridsplitval = [self.gridsplitleft, self.gridsplitright]
        gridsplitrestrict = self.gridsplitrestrict
        # gridsplitval = [200,200]

        cleangrids = []

        # if self.maskedarray is all np.nan then raise exception
        if np.isnan(self.maskedarray).all():
            raise AnalysisAttemptOnEmptyImage("Analysis attempted on empty image. Make sure the mask layer is not empty")


        if self.maskedarray_c is None:
            grids = gridsplit(self.maskedarray, gridsplitmode, gridsplitval, gridsplitrestrict)
            for index, grid in enumerate(grids):
                if not np.isnan(grid).all():
                    cleangrids.append(grid)

            indexgrids = []

            for index, grid in enumerate(cleangrids):
                indexgrids.append([index, grid])

            with Pool(4) as self.pool:
                output = []
                for _ in self.pool.imap_unordered(partial(cycledegreesAuto,
                                                          pxpermicron=self.pixelsize,
                                                          filename=self.currentlayer,
                                                          outputimg=self.outimg,
                                                          restrictdeg=self.restrictdeg,
                                                          outputpath=self.path), indexgrids):
                    output.append(_)
                    self.progress.emit([False, len(indexgrids)])
                    # print(self.progressBar.value())
                    # self.progressBar.setValue(self.progressBar.value() + 1)

                self.pool.close()
                self.pool.join()
                print("analysis finished")
                self.progress.emit([True, len(indexgrids)])
                df = pd.concat(output)

                if self.outcsv:
                    df2 = pd.DataFrame({"total grids": [len(indexgrids)]})
                    new = pd.concat([df, df2], axis=1)
                    new.to_csv(self.path + "/" + self.currentlayer + ".csv", sep=";")



        else:
            grids_a = gridsplit(self.maskedarray, gridsplitmode, gridsplitval, gridsplitrestrict)
            grids_c = gridsplit(self.maskedarray_c, gridsplitmode, gridsplitval, gridsplitrestrict)
            for index, grid in enumerate(grids_a):
                if not np.isnan(grid).all():
                    cleangrids.append([grids_a[index],grids_c[index]])

            indexgrids = []

            for index, grid in enumerate(cleangrids):
                indexgrids.append([index, grid])

            with Pool(4) as self.pool:
                output = []
                for _ in self.pool.imap_unordered(partial(cycledegreesCross,
                                                          pxpermicron=self.pixelsize,
                                                          filename=self.currentlayer,
                                                          outputimg=self.outimg,
                                                          restrictdeg=self.restrictdeg,
                                                          outputpath=self.path), indexgrids):
                    output.append(_)
                    self.progress.emit([False, len(indexgrids)])
                    # print(self.progressBar.value())
                    # self.progressBar.setValue(self.progressBar.value() + 1)

                self.pool.close()
                self.pool.join()
                print("Analysis Complete")
                self.progress.emit([True, len(indexgrids)])
                df = pd.concat(output)

                if self.outcsv:
                    df2 = pd.DataFrame({"total grids": [len(indexgrids)]})
                    new = pd.concat([df, df2], axis=1)
                    new.to_csv(self.path + "/" + sanitize_filename(self.currentlayer + ".csv"), sep=";")

    def stop(self):
        self.terminate()
        self.pool.stop()



@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # if platform.system() == "Darwin":
    #     set_start_method('spawn')
    return AutocorrelationTool


if __name__ == '__main__':
    viewer = Viewer()

    Autocorrelation_widget = AutocorrelationTool(viewer)  # Create instance from our class
    viewer.window.add_dock_widget(Autocorrelation_widget, area='right')  # Add our gui instance to napari viewer

    def updatelayer(event):
        Autocorrelation_widget.updatelayer()


    run()