from io import StringIO

import numpy as np
import numpy.typing as npt
import polars as pl
import yaml

from .refidxdb import RefIdxDB


class RefIdx(RefIdxDB):
    """
    Handler for the refractiveindex.info database.
    Polyanskiy, M.N. Refractiveindex.info database of optical constants. Sci Data 11, 94 (2024).
    https://doi.org/10.1038/s41597-023-02898-2
    """

    @property
    def url(self) -> str:
        return "https://github.com/polyanskiy/refractiveindex.info-database/releases/download/v2024-08-14/rii-database-2024-08-14.zip"

    @property
    def data(self):
        if self._path is None:
            raise Exception("Path is not set, cannot retrieve any data!")

        if self._path.startswith("/"):
            absolute_path = self._path
        else:
            absolute_path = f"{self.cache_dir}/{self._path}"

        with open(absolute_path, "r") as f:
            data = yaml.safe_load(f)
            return data

    @property
    def nk(self):
        if self._nk is not None:
            return self._nk

        nk = pl.DataFrame(schema={"w": float, "n": float, "k": float})
        storage = []
        for i, data in enumerate(self.data["DATA"]):
            match data["type"]:
                case "tabulated nk":
                    storage.append(
                        pl.read_csv(
                            StringIO(data["data"]),
                            new_columns=["w", "n", "k"],
                            separator=" ",
                        )
                    )
                case "tabulated n":
                    storage.append(
                        pl.read_csv(
                            StringIO(data["data"]),
                            new_columns=["w", "n"],
                            separator=" ",
                        ).with_columns(k=pl.lit(None))
                    )
                case "tabulated k":
                    storage.append(
                        pl.read_csv(
                            StringIO(data["data"]),
                            new_columns=["w", "k"],
                            separator=" ",
                        )
                        .with_columns(n=pl.lit(None))
                        .select(["w", "n", "k"])
                    )
                case "formula 1":
                    storage.append(formula(1, data))
                case "formula 2":
                    storage.append(formula(2, data))
                case "formula 3":
                    storage.append(formula(3, data))
                case _:
                    raise Exception(f"Unsupported data type: {data['type']}")

        self._nk = (
            pl.concat([nk, *storage], how="vertical")
            .with_columns(pl.col("w").mul(self.scale))
            .sort("w")
        )
        return self._nk


def formula(number: int, data):
    """
    Get formula from the source paper.
    """
    w_range = [float(s) for s in data["wavelength_range"].split()]
    coefficients = np.array([float(s) for s in data["coefficients"].split()])
    match number:
        case 1:
            f = formula1(coefficients)
            print(f(2))
        case 2:
            f = formula2(coefficients)
        case 3:
            f = formula3(coefficients)
        case 4:
            raise Exception(f"Support incomming for formula {number}")
        case 5:
            raise Exception(f"Support incomming for formula {number}")
        case 6:
            raise Exception(f"Support incomming for formula {number}")
        case 7:
            raise Exception(f"Support incomming for formula {number}")
        case 8:
            raise Exception(f"Support incomming for formula {number}")
        case 9:
            raise Exception(f"Support incomming for formula {number}")
    w = np.linspace(w_range[0], w_range[1], 100)
    return pl.DataFrame({"w": w, "n": f(w)}).with_columns(k=pl.lit(None))


# other/semiconductor alloys/AlAs-GaAs/Perner-0.yml
def formula1(c: npt.NDArray):
    """
    Equation 1 in source paper.
    """
    c_mod = c
    c_mod[2::2] = c[2::2] ** 2
    return formula2(c_mod)


# Used by https://refractiveindex.info/?shelf=glass&book=OHARA-BAL&page=S-BAL2
def formula2(c: npt.NDArray):
    """
    Equation 2 in source paper.
    """
    return lambda x: np.sqrt(
        1 + c[0] + np.sum(c[1::2] / (1 - np.outer(1 / x**2, c[2::2])), axis=1)
    )


# Used by glass/ohara/BAL2
def formula3(c: npt.NDArray):
    """
    Equation 3 in source paper.
    """
    return lambda x: np.sqrt(
        c[0] + np.sum(c[1::2] * np.power.outer(x, c[2::2]), axis=1)
    )
