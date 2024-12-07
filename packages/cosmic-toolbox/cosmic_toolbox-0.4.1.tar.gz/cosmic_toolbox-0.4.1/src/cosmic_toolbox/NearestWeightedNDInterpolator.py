"""
Convenience interface to N-D interpolation
.. versionadded:: 0.9
author: Tomasz Kacprzak
"""

import numpy as np
from scipy.interpolate.interpnd import NDInterpolatorBase
from sklearn.neighbors import BallTree
from sklearn.preprocessing import MinMaxScaler


class NearestWeightedNDInterpolator(NDInterpolatorBase):
    def __init__(self, x, y, k=None, tree_options={}):
        self.x = x
        self.y = y
        self.ndim = self.x.shape[1]
        if k is None:
            k = self.ndim + 1  # number of vertices of ndim dimensional simplex
        self.k = k
        self.scaler = MinMaxScaler()
        self.x = self.scaler.fit_transform(self.x)
        self.tree = BallTree(self.x, **tree_options)

        # from sklearn import neighbors
        # self.knn = neighbors.KNeighborsRegressor(n_neighbors=k,
        #                                          weights='distance')
        # self.knn.fit(self.x , self.y)

    def __call__(self, xi):
        assert len(xi.shape) == 2
        assert self.ndim == xi.shape[1]

        xi = self.scaler.transform(xi)
        # vi = self.knn.predict(xi)

        dist, i = self.tree.query(xi, self.k)
        vi = self.y[i].reshape((xi.shape[0], self.k))
        if self.k > 1:
            weight = 1.0 / dist
            weight[~np.isfinite(weight)] = 0
            weight = weight.reshape((xi.shape[0], self.k))
            vi = np.average(vi, weights=weight, axis=1)

        return vi


# class NearestWeightedNDInterpolator(NDInterpolatorBase):
#     """
#     NearestWeightedNDInterpolator(x, y)
#     NN interpolation in N dimensions with weighted interpolation.
#     Uses BallTree instead of cKDTree
#     .. versionadded:: 0.9
#     Methods
#     -------
#     __call__
#     Parameters
#     ----------
#     x : (Npoints, Ndims) ndarray of floats
#         Data point coordinates.
#     y : (Npoints,) ndarray of float or complex
#         Data values.
#     rescale : boolean, optional
#         Rescale points to unit cube before performing interpolation.
#         This is useful if some of the input dimensions have
#         incommensurable units and differ by many orders of magnitude.
#         .. versionadded:: 0.14.0
#     tree_options : dict, optional
#         Options passed to the underlying ``cKDTree``.
#         .. versionadded:: 0.17.0
#     Notes
#     -----
#     Uses ``scipy.spatial.cKDTree``
#     Examples
#     --------
#     We can interpolate values on a 2D plane:
#     >>> from scipy.interpolate import NearestNDInterpolator
#     >>> import matplotlib.pyplot as plt
#     >>> np.random.seed(0)
#     >>> x = np.random.random(10) - 0.5
#     >>> y = np.random.random(10) - 0.5
#     >>> z = np.hypot(x, y)
#     >>> X = np.linspace(min(x), max(x))
#     >>> Y = np.linspace(min(y), max(y))
#     >>> X, Y = np.meshgrid(X, Y)  # 2D grid for interpolation
#     >>> interp = NearestNDInterpolator(list(zip(x, y)), z)
#     >>> Z = interp(X, Y)
#     >>> plt.pcolormesh(X, Y, Z, shading='auto')
#     >>> plt.plot(x, y, "ok", label="input point")
#     >>> plt.legend()
#     >>> plt.colorbar()
#     >>> plt.axis("equal")
#     >>> plt.show()
#     See also
#     --------
#     griddata :
#         Interpolate unstructured D-D data.
#     LinearNDInterpolator :
#         Piecewise linear interpolant in N dimensions.
#     CloughTocher2DInterpolator :
#         Piecewise cubic, C1 smooth, curvature-minimizing interpolant in 2D.
#     """

#     def __init__(self, x, y, k=None, tree_options={}):
#         NDInterpolatorBase.__init__(self, x, y, rescale=True,
#                                     need_contiguous=False,
#                                     need_values=False)
#         ndim = self.points.shape[1]
#         if k==None:
#             k = ndim + 1 # number of vertices of ndim dimensional simplex
#         self.k = k
#         self.scaler = MinMaxScaler(copy=False)
#         self.scaler.fit_transform(self.points)
#         self.tree = BallTree(self.points, **tree_options)
#         self.values = np.asarray(y)

#     def __call__(self, *args):
#         """
#         Evaluate interpolator at given points.
#         Parameters
#         ----------
#         x1, x2, ... xn: array-like of float
#             Points where to interpolate data at.
#             x1, x2, ... xn can be array-like of float with broadcastable
#             shape or x1 can be array-like of float with shape ``(..., ndim)``
#         """

#         ndim = self.points.shape[1]
#         xi = _ndim_coords_from_arrays(args, ndim=ndim)
#         xi = self._check_call_shape(xi)
#         # xi = self._scale_x(xi)
#         orig_shape = xi.shape

#         if len(xi.shape) > 2:
#             xi = xi.reshape(-1, xi.shape[-1])
#         self.scaler.transform(xi)

#         dist, i = self.tree.query(xi, self.k)
#         weight = 1./dist
#         print(weight.shape)
#         weight[~np.isfinite(weight)] = 0
#         import ipdb; ipdb.set_trace()
#         try:
#             vi = np.average(self.values[i].squeeze(), weights=weight, axis=1)
#         except Exception as err:
#             print(err)
#             import ipdb; ipdb.set_trace()

#         return np.reshape(vi, orig_shape[:-1])
