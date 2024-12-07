# SPDX-FileCopyrightText: 2022 - 2023 Peter Urban, Ghent University
# SPDX-FileCopyrightText: 2022 Peter Urban, GEOMAR Helmholtz Centre for Ocean Research Kiel
#
# SPDX-License-Identifier: MPL-2.0

import numpy as np

from numba import njit

from .functions import gridfunctions as gf
from .forwardgridder import ForwardGridder

from collections.abc import MutableMapping

import warnings


@njit
def static_get_target_pos(image, min_val=np.nan):

    x_sum = 0
    y_sum = 0
    z_sum = 0
    x_weight = 0
    y_weight = 0
    z_weight = 0

    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            for z in range(image.shape[2]):
                if not np.isfinite(image[x][y][z]):
                    continue

                if image[x][y][z] < min_val:
                    continue

                x_sum += image[x][y][z] * x
                y_sum += image[x][y][z] * y
                z_sum += image[x][y][z] * z
                x_weight += image[x][y][z]
                y_weight += image[x][y][z]
                z_weight += image[x][y][z]

    return x_sum / x_weight, y_sum / y_weight, z_sum / z_weight


class EchoGrid:
    def __init__(self, imagesums, imagenums, gridder):
        self.ImageSums = imagesums.copy()
        self.ImageNums = imagenums.copy()
        self.ImageAvg = np.empty(imagenums.shape, dtype=np.float64)
        self.ImageAvg.fill(np.nan)

        self.ImageAvg[imagenums > 0] = (
            imagesums[imagenums > 0] / imagenums[imagenums > 0]
        )

        self.TotalValue = np.nansum(self.ImageAvg) * (
            gridder.xres * gridder.yres * gridder.zres
        )

        self.ZDiff = gridder.get_extent_z()[1] - gridder.get_extent_z()[0]

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            self.TotalValueLayer = (
                np.nansum(np.nanmean(self.ImageAvg, axis=2))
                * gridder.xres
                * gridder.yres
                * self.ZDiff
            )

        # self.Gridder = gridder
        self.ExtentX = gridder.get_extent_x()
        self.ExtentY = gridder.get_extent_y()
        self.ExtentZ = gridder.get_extent_z()
        self.ResX = gridder.xres
        self.ResY = gridder.yres
        self.ResZ = gridder.zres
        self.MinX = gridder.xmin
        self.MaxX = gridder.xmax
        self.MinY = gridder.ymin
        self.MaxY = gridder.ymax
        self.MinZ = gridder.zmin
        self.MaxZ = gridder.zmax

    def get_target_pos(self, min_val=np.nan):
        xi, yi, zi = static_get_target_pos(self.ImageAvg, min_val)

        return (
            xi * self.ResX + self.MinX,
            yi * self.ResY + self.MinY,
            zi * self.ResZ + self.MinZ,
        )

    def getTotalvalue(self, min_val):
        if not np.isfinite(min_val):
            return self.TotalValue

        return np.nansum(self.ImageAvg[self.ImageAvg >= min_val]) * (
            self.ResX * self.ResY * self.ResZ
        )

    def getTotalvalueLayer(self, min_val):
        if not np.isfinite(min_val):
            return self.TotalValueLayer

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            layerAvg = np.nanmean(self.ImageAvg, axis=2)

        return (
            np.nansum(layerAvg[layerAvg >= min_val])
            * self.ResX
            * self.ResY
            * self.ZDiff
        )

    def getGridder(self):
        return ForwardGridder(
            self.ResX,
            self.ResY,
            self.ResZ,
            self.MinX,
            self.MaxX,
            self.MinY,
            self.MaxY,
            self.MinZ,
            self.MaxZ,
        )

    def cutDepthLayer(self, layer_z, layer_size):

        gridder_old = self.getGridder()

        minZ = gridder_old.get_z_grd_value(
            layer_z - (layer_size - gridder_old.zres) / 2
        )
        maxZ = gridder_old.get_z_grd_value(
            layer_z + (layer_size - gridder_old.zres) / 2
        )

        gridder = ForwardGridder(
            self.ResX,
            self.ResY,
            self.ResZ,
            self.MinX,
            self.MaxX,
            self.MinY,
            self.MaxY,
            minZ,
            maxZ,
        )

        iz0 = gridder_old.get_z_index(minZ)
        iz1 = gridder_old.get_z_index(maxZ)

        imagesums = self.ImageSums[:, :, iz0: iz1 + 1]
        imagenums = self.ImageNums[:, :, iz0: iz1 + 1]

        return EchoGrid(imagesums, imagenums, gridder)

    def getDepthMeanImage(self, layer_z, layer_size):

        gridder_old = self.getGridder()

        minZ = gridder_old.get_z_grd_value(
            layer_z - (layer_size - gridder_old.zres) / 2
        )
        maxZ = gridder_old.get_z_grd_value(
            layer_z + (layer_size - gridder_old.zres) / 2
        )

        gridder = ForwardGridder(
            self.ResX,
            self.ResY,
            self.ResZ,
            self.MinX,
            self.MaxX,
            self.MinY,
            self.MaxY,
            minZ,
            maxZ,
        )

        iz0 = gridder_old.get_z_index(minZ)
        iz1 = gridder_old.get_z_index(maxZ)

        imagesums = self.ImageSums[:, :, iz0: iz1 + 1]
        imagenums = self.ImageNums[:, :, iz0: iz1 + 1]

        return imagesums, imagenums, gridder

    def getGridExtents(self):
        return self.ExtentX, self.ExtentY, self.ExtentZ

    def toString(self, TrueValue, methodName=None, minMethodNameSize=None):

        if methodName is None:
            prefix = "TotalValue"
        else:
            prefix = "Bubbles Grid"
            if minMethodNameSize:
                prefix += "[{:MMMs}]".replace(
                    "MMM", str(int(minMethodNameSize))
                ).format(methodName)
            else:
                prefix += "[{}]".format(methodName)

        string = prefix + ": {:15.2f}  | {:5.2f} %".format(
            round(self.TotalValue, 2), round(100 * (self.TotalValue / TrueValue - 1), 2)
        )
        return string

    def print(self, methodName, minMethodNameSize, TrueValue):
        print(self.toString(methodName, minMethodNameSize, TrueValue))

    def get_3DImage(self, toDb=True, minDbVal=-50):

        image = self.ImageAvg.copy()
        image[self.ImageNums == 0] = np.nan
        if toDb:
            image[image == 0] = 0.000000000000001
            image = 10 * np.log10(image)
            image[image < minDbVal] = minDbVal

        return image

    def plot(
        self,
        figure,
        targets_color=None,
        target_size=1,
        show_wci=True,
        show_echo=True,
        show_map=True,
        show_colorbar=True,
        toDb=True,
        minDbVal=-50,
        minDbReplace=None,
        xindex=None,
        yindex=None,
        zindex=None,
        zindeces=None,
        kwargs=None,
        colorbar_kwargs=None,
    ):

        figure.clear()

        nplots = sum([show_wci, show_echo, show_map])
        if kwargs is None:
            kwargs = {}
        if colorbar_kwargs is None:
            colorbar_kwargs = {}

        # gs = figure.add_gridspec(2, 2)
        #
        #
        # if nplots == 1:
        #     axes = [
        #         figure.add_subplot(gs[:, :])
        #     ]
        # elif nplots == 2:
        #     if show_wci:
        #         axes = [
        #             figure.add_subplot(gs[0, :]),
        #             figure.add_subplot(gs[1, :]),
        #         ]
        #     else:
        #         axes = [
        #             figure.add_subplot(gs[:, 0]),
        #             figure.add_subplot(gs[:, 1]),
        #         ]
        # elif nplots == 3:
        #     axes = [
        #         figure.add_subplot(gs[0, :]),
        #         figure.add_subplot(gs[1, 0]),
        #         figure.add_subplot(gs[1, 1])
        #     ]
        # else:
        #     axes = []
        if nplots == 1:
            axes = [figure.subplots(ncols=nplots)]
        else:
            axes = figure.subplots(ncols=nplots)

        axit = iter(axes)
        image_extent_x, image_extent_y, image_extent_z = self.getGridExtents()

        def getNanSum(imageLin, axis, divide=1):
            # image = np.nansum(imageLin,axis=axis)
            image = np.nanmean(imageLin, axis=axis)
            num = np.nansum(self.ImageNums, axis=axis)

            if divide != 1:
                image /= divide

            image[num == 0] = np.nan

            if toDb:
                image[image == 0] = 0.000000000000001
                image = 10 * np.log10(image)
                if minDbReplace is not None:
                    image[image < minDbVal] = minDbReplace
                else:
                    image[image < minDbVal] = minDbVal

            return image

        if show_wci:
            ax = next(axit)

            if xindex is None:
                image = getNanSum(self.ImageAvg.copy(), axis=0)
            else:
                image = self.ImageAvg[xindex, :, :]
                if toDb:
                    image[image == 0] = 0.000000000000001
                    image = 10 * np.log10(image)
                    if minDbReplace is not None:
                        image[image < minDbVal] = minDbReplace
                    else:
                        image[image < minDbVal] = minDbVal

            mapable = ax.imshow(
                image.transpose(),
                aspect="equal",
                extent=[
                    image_extent_y[0],
                    image_extent_y[1],
                    image_extent_z[1],
                    image_extent_z[0],
                ],
                **kwargs
            )

            if show_colorbar:
                figure.colorbar(mapable, ax=ax, **colorbar_kwargs)

            if targets_color:
                for targets, color in targets_color:
                    ax.scatter(targets.y, targets.z, c=color, s=target_size)

        if show_echo:
            ax = next(axit)

            if yindex is None:
                image = getNanSum(self.ImageAvg.copy(), axis=1)
            else:
                image = self.ImageAvg[:, yindex, :]
                if toDb:
                    image[image == 0] = 0.000000000000001
                    image = 10 * np.log10(image)
                    if minDbReplace is not None:
                        image[image < minDbVal] = minDbReplace
                    else:
                        image[image < minDbVal] = minDbVal

            mapable = ax.imshow(
                image.transpose(),
                aspect="equal",
                extent=[
                    image_extent_x[0],
                    image_extent_x[1],
                    image_extent_z[1],
                    image_extent_z[0],
                ],
                **kwargs
            )
            if targets_color:
                for targets, color in targets_color:
                    ax.scatter(targets.x, targets.z, c=color, s=target_size)

            if show_colorbar:
                figure.colorbar(mapable, ax=ax, **colorbar_kwargs)

        if show_map:
            ax = next(axit)

            if zindex is None and zindeces is None:
                image = getNanSum(self.ImageAvg.copy(), axis=2)
            elif zindex is None and zindeces is not None:
                image = getNanSum(
                    self.ImageAvg[:, :, zindeces[0]: zindeces[1] + 1], axis=2
                )  # ,divide=abs(zindeces[1]-zindeces[0]))

            else:
                image = self.ImageAvg[:, :, zindex]
                if toDb:
                    image[image == 0] = 0.000000000000001
                    image = 10 * np.log10(image)
                    if minDbReplace is not None:
                        image[image < minDbVal] = minDbReplace
                    else:
                        image[image < minDbVal] = minDbVal

            mapable = ax.imshow(
                image,
                aspect="equal",
                extent=[
                    image_extent_y[0],
                    image_extent_y[1],
                    image_extent_x[1],
                    image_extent_x[0],
                ],
                **kwargs
            )
            if targets_color:
                for targets, color in targets_color:
                    ax.scatter(targets.y, targets.x, c=color, s=target_size)

            if show_colorbar:
                figure.colorbar(mapable, ax=ax, **colorbar_kwargs)

        return figure, ax, image


class EchoGridDict(MutableMapping):
    def print(self, TrueValue):
        maxKeyLen = max([len(k) for k in self.keys()])
        for k in self.keys():
            self.store[k].print(TrueValue, k, maxKeyLen)

    def cutDepthLayer(self, layer_z, layer_size):
        scd = EchoGridDict()
        for k in self.keys():
            scd[k] = self[k].cutDepthLayer(layer_z, layer_size)

        z_extend = scd[k].ExtentZ
        true_layer_size_z = abs(z_extend[1] - z_extend[0])
        z_coordinates = scd[k].getGridder().get_z_coordinates()

        return scd, (z_extend, true_layer_size_z, z_coordinates)

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        if isinstance(value, EchoGrid):
            self.store[key] = value
        else:
            try:
                self.store[key] = EchoGrid(*value)
            except:
                try:
                    types = [type(v) for v in value]
                except:
                    types = [type(value)]

                raise RuntimeError(
                    "Cannot initialize EchoGrid using arguments of type:", *types
                )

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)


if __name__ == "__main__":

    imN = np.ones((10, 10, 10))
    imS = np.ones((10, 10, 10))
    gridder = gf.GRIDDER(1, 1, 1, 0, 1, 0, 1, 0, 1)
    sc = EchoGrid(imN, imS, gridder)

    scd = EchoGridDict()
    scd["test"] = sc
    scd["test2"] = imN, imS, gridder

    print(scd["test"].toString(999, "peter", 10))
    print(scd["test2"].toString(1010, "peter", 10))
    print(scd["test2"].toString(1020, "peter"))
    print(
        scd["test2"].toString(
            1030,
        )
    )

    print("---")
    scd.print(999)

    print("done")
