import re

import polars as pl

from .refidxdb import RefIdxDB


class Aria(RefIdxDB):
    @property
    def url(self) -> str:
        return "https://eodg.atm.ox.ac.uk/ARIA/data_files/ARIA.zip"

    @property
    def data(self):
        if self._data is not None:
            return self._data

        if self._path is None:
            raise Exception("Path is not set, cannot retrieve any data!")
        if self._path.startswith("/"):
            absolute_path = self._path
        else:
            absolute_path = f"{self.cache_dir}/{self._path}"
        with open(absolute_path, "r", encoding="cp1252") as f:
            data = f.readlines()
            header = [h for h in data if h.startswith("#")]
            header = [h for h in header if not h.startswith("##")]
            header = [h.split("=") for h in header]
            header = {h[0][1:].strip(): h[1].strip() for h in header}
            # print(header)
            data = [d.strip() for d in data if not d.startswith("#")]
            data = re.sub(r"[ \t]{1,}", " ", "\n".join(data))

        self._data = pl.read_csv(
            data.encode(),
            # new_columns=header["FORMAT"].split(" "),
            schema_overrides={h: pl.Float64 for h in header["FORMAT"].split(" ")},
            comment_prefix="#",
            separator=" ",
        )

        return self._data

    @property
    def nk(self):
        if self.data is None:
            raise Exception("Data could not have been loaded")
        if self._nk is not None:
            return self._nk
        # Using a small trick
        # micro is 10^-6 and 1/centi is 10^2,
        # but we will use 10^-2, since the value needs to be inverted
        local_scale = 1e-6 if "WAVL" in self.data.columns else 1e-2
        if self._wavelength:
            w = (
                self.data["WAVL"]
                if ("WAVL" in self.data.columns)
                else 1 / (self.data["WAVN"])
            ) * local_scale
        else:
            w = (
                self.data["WAVN"]
                if ("WAVN" in self.data.columns)
                else 1 / (self.data["WAVL"])
            ) / local_scale
        nk = {
            "w": w,
            "n": self.data["N"] if ("N" in self.data.columns) else None,
            "k": self.data["K"] if ("K" in self.data.columns) else None,
        }

        self._nk = pl.DataFrame(nk).sort("w")
        return self._nk
