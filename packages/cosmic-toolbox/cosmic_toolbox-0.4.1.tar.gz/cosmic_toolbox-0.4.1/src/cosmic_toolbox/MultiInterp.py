"""
author: Tomasz Kacprzak
"""

import sys
import warnings

import numpy as np
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator, Rbf
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import BallTree, KNeighborsRegressor, RadiusNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler

from cosmic_toolbox.logger import get_logger

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("once", category=UserWarning)
LOGGER = get_logger(__file__)


class Rbft:
    def __init__(self, points, values, **kw_rbf):
        self.points = points
        self.values = values
        self.bounds = [np.min(points, axis=0), np.max(points, axis=0)]
        self.scaler = MinMaxScaler()
        self.scaler.fit(self.points)
        self.points = self.scaler.transform(self.points)
        self.interp = Rbf(*list(self.points.T), self.values, **kw_rbf)

    def __call__(self, points, **kw_rbf):
        values_pred = np.zeros(len(points))
        select = self._in_bounds(points)
        values_pred[~select] = -np.inf

        points = self.scaler.transform(points)
        values_pred[select] = self.interp(*list(points[select].T))
        return values_pred

    def _in_bounds(self, x):
        return np.all(x > self.bounds[0], axis=1) & np.all(x < self.bounds[1], axis=1)


def query_split(X, tree, k, n_proc):
    nx = X.shape[0]
    n_per_batch = int(np.ceil(nx / n_proc))
    LOGGER.info(
        "querying BallTree with a pool for n_grid={} "
        "n_proc={} n_per_batch={} n_neighbors={}".format(nx, n_proc, n_per_batch, k)
    )
    X_chunks = [X[(i * n_per_batch) : (i + 1) * n_per_batch, :] for i in range(n_proc)]
    from functools import partial
    from multiprocessing import Pool

    f = partial(query_batch, tree=tree, k=k, n_per_batch=100000)
    with Pool(n_proc) as pool:
        list_y = pool.map(f, X_chunks)

    distances = np.concatenate([list_y[i][0] for i in range(n_proc)])
    indices = np.concatenate([list_y[i][1] for i in range(n_proc)])
    return distances, indices


def query_batch(X, tree, k=100, n_per_batch=10000):
    nx = X.shape[0]
    n_batches = int(np.ceil(nx / n_per_batch))
    indices = np.zeros([nx, k], dtype=np.int)
    distances = np.zeros([nx, k])
    for i in range(n_batches):
        si, ei = i * n_per_batch, (i + 1) * n_per_batch
        Xq = X[si:ei, :]
        if len(Xq) > 0:
            dist, ind = tree.query(Xq, k=k)
            indices[si:ei, :] = ind
            distances[si:ei, :] = dist
            LOGGER.info("batch={:>6}/{:>6}".format(i, n_batches))

    return distances, indices


def predict_with_neighbours(y, ind, dist):
    yn = y[ind]
    wn = 1.0 / dist
    wn[wn == 0] = 1e10
    yi = np.average(yn, weights=wn, axis=1)

    return yi


def predict_knn_balltree(Xi, X, y, n_neighbors, tree):
    nx, nd = Xi.shape
    dist, ind = tree.query(Xi, k=n_neighbors)
    yi = predict_with_neighbours(y, ind, dist)
    return yi


def predict_knn_linear(Xi, X, y, n_neighbors, tree):
    nx, nd = Xi.shape
    dist, ind = tree.query(Xi, k=n_neighbors)
    X_nearest = X[ind, :]
    y_nearest = y[ind]
    yi = np.full(nx, -np.inf)
    n_nan = 0

    for i in range(nx):
        Xn = X_nearest[i, :]
        yn = y_nearest[i, :]
        interp = LinearNDInterpolator(Xn, yn)
        yi[i] = interp(Xi[i, :])
        if ~np.isfinite(yi[i]):
            n_nan += 1
        sys.stdout.write("\r{}/{} {}".format(i, nx, n_nan))

    return yi


class MultiInterp:
    def __init__(self, X, y, method="nn", **kw):
        self.X = X.copy()
        self.y = y.copy()
        self.bounds = [np.min(X, axis=0), np.max(X, axis=0)]
        self.scaler = MinMaxScaler()
        self.scaler.fit(self.X)
        self.X = self.scaler.transform(self.X)
        self.interp = None
        self.method = method
        self.kw = kw
        self.init_interp(**kw)

    def __call__(self, Xi, **kw):
        yi = np.zeros(len(Xi))
        select = self._in_bounds(Xi)
        yi[~select] = -np.inf

        Xi = self.scaler.transform(Xi.copy())

        if self.method.lower() == "rbf":
            yi[select] = self.interp(*list(Xi[select, :].T), **kw)

        elif self.method.lower() == "rbft":
            yi[select] = self.interp(Xi[select, :], **kw)

        elif self.method.lower() in ["knn_regression", "rnn_regression"]:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                yi[select] = self.interp.predict(Xi[select, :], **kw)

        elif self.method.lower() in ["nn", "linear"]:
            yi[select] = self.interp(Xi[select, :], **kw)

        elif self.method.lower() == "knn_linear":
            yi[select] = predict_knn_linear(
                Xi[select, :],
                self.X,
                self.y,
                self.n_neighbors,
                self.interp,
                **kw,
            )

        elif self.method.lower() == "random_forest":
            yi[select] = self.interp.predict(Xi[select, :], **kw)

        elif self.method.lower() == "knn_balltree":
            yi[select] = predict_knn_balltree(
                Xi[select, :],
                self.X,
                self.y,
                self.n_neighbors,
                self.interp,
                **kw,
            )

        else:
            raise Exception(f"unknown interp method {self.method}")

        return yi

    def _in_bounds(self, X):
        return np.all(X > self.bounds[0], axis=1) & np.all(X < self.bounds[1], axis=1)

    def init_interp(self, **kw):
        if self.method.lower() == "rbf":
            self.interp = Rbf(*list(self.X.T), self.y, **kw)

        elif self.method.lower() == "rbft":
            self.interp = Rbft(points=self.X, values=self.y, **kw)

        elif self.method.lower() == "knn":
            self.interp = KNeighborsRegressor(**kw)
            self.interp.fit(self.X, self.y)

        elif self.method.lower() == "knn_regression":
            self.interp = KNeighborsRegressor(**kw)
            self.interp.fit(self.X, self.y)

        elif self.method.lower() == "rnn_regression":
            kw.setdefault("radius", 0.1)
            self.interp = RadiusNeighborsRegressor(**kw)
            self.interp.fit(self.X, self.y)

        elif self.method.lower() == "nn":
            self.interp = NearestNDInterpolator(self.X, self.y, **kw)

        elif self.method.lower() == "linear":
            self.interp = LinearNDInterpolator(self.X, self.y, **kw)

        elif self.method.lower() == "knn_linear":
            # self.slice_linear_upsampling(n_repeat=1)
            n_neighbors = kw.pop("n_neighbors", self.X.shape[1] * 3)
            self.interp = BallTree(self.X, **kw)
            self.n_neighbors = n_neighbors

        elif self.method.lower() == "random_forest":
            self.interp = RandomForestRegressor(**kw)
            self.interp.fit(self.X, self.y)

        elif self.method.lower() == "knn_balltree":
            n_neighbors = kw.pop("n_neighbors", self.X.shape[1] * 3)
            self.interp = BallTree(self.X, **kw)
            self.n_neighbors = n_neighbors

        else:
            raise Exception(f"unknown interp method {self.method}")

    def precompute_grid_neighbors(self, Xn, n_neighbors=100, n_proc=1):
        assert self.method == "knn_balltree"

        Xn = self.scaler.transform(Xn.copy())
        dist, ind = query_split(tree=self.interp, X=Xn, k=n_neighbors, n_proc=n_proc)

        self.neighbors_ind = ind
        self.neighbors_dist = dist.astype(np.float32)
        self.neighbors_Xn = Xn.astype(np.float32)

    def interpolate_grid_neighbours(self, y, n_neighbors=None):
        assert len(y) == len(self.X)
        if n_neighbors is None:
            n_neighbors = self.n_neighbors

        nn = self.neighbors_ind.shape[1]
        if n_neighbors > nn:
            raise Exception("number of available neighbors {}".format(nn))
        yi = predict_with_neighbours(
            y,
            self.neighbors_ind[:, :n_neighbors],
            self.neighbors_dist[:, :n_neighbors],
        )

        return yi

    def slice_linear_upsampling(self, n_repeat=1, n_neighbors=1):
        for i in range(n_repeat):
            bt = BallTree(self.X)
            dist, ids = bt.query(self.X, k=n_neighbors + 1)
            list_Xn = [self.X]
            list_yn = [self.y]
            for j in range(1, n_neighbors + 1):
                Xn = (self.X + self.X[ids[:, j], :]) / 2.0
                yn = (self.y + self.y[ids[:, j]]) / 2.0
                list_Xn += [Xn]
                list_yn += [yn]

                # Xp = self.X[ids,:]
                # yp = self.y[ids]
                # Xn = Xp.mean(axis=1)
                # yn = yp.mean(axis=1)
            # Xc = np.concatenate([self.X, Xn], axis=0)
            # yc = np.concatenate([self.y, yn])
            Xn = np.concatenate(list_Xn, axis=0)
            yn = np.concatenate(list_yn, axis=0)
            self.X = Xn
            self.y = yn
            print(Xn.shape, yn.shape)
