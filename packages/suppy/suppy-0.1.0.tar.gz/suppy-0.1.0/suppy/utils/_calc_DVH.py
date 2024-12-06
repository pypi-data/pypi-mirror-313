import numpy as np
import matplotlib.pyplot as plt


def calc_DVH(dose, idxs: list):
    """"""

    d_min = np.min(dose)
    d_max = np.max(dose)
    n = 1000
    dose_grid = np.linspace(0, 1.05 * d_max, n)
    dvh = []
    for struct in idxs:
        dvh.append((dose[struct, None] > dose_grid).sum(axis=0) / (struct.sum()))
    return dvh, dose_grid


if __name__ == "__main__":
    dose = np.linspace(0, 100, 10)
    idxs = [np.random.randint(0, 2, 10, dtype="bool") for i in range(10)]
    dvh, dose_grid = calc_DVH(dose, idxs)
    for el in dvh:
        plt.plot(dose_grid, el)
    print(dvh)
    print(dose_grid)
