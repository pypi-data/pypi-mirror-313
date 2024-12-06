import os

import numpy as np
import polars as pl
import polars.testing as plt

from refidxdb.aria import Aria


def test_olivine_fabian():
    fabian = (
        pl.read_csv(
            os.path.dirname(__file__) + "/data/olivine_Z_Fabian_2001.ri",
            schema_overrides={"WAVN": pl.Float64, "N": pl.Float64, "K": pl.Float64},
            comment_prefix="#",
            separator="\t",
        )
        .with_columns(pl.col("WAVN").mul(1e2))
        .sort("WAVN")
    )
    fabian.columns = ["w", "n", "k"]

    # Test loading
    aria = Aria(
        "data_files/Minerals/Olivine/z_orientation_(Fabian_et_al._2001)/olivine_Z_Fabian_2001.ri",
        wavelength=False,
    )
    print(fabian, aria.nk)
    plt.assert_frame_equal(fabian, aria.nk)

    # Test interpolation
    groundtrouth = pl.DataFrame(
        {
            "w": np.arange(1, 10),
            "n": [
                0.105641000000000,
                2.468603409016394,
                2.468626565929566,
                2.468658287469288,
                2.468698850000000,
                2.468748850000000,
                2.468809098280098,
                2.468878274365274,
                2.468956009828010,
            ],
            "k": [
                0.000026000000000,
                0.000127804918033,
                0.000191710073710,
                0.000255592137592,
                0.000319576229508,
                0.000384330327869,
                0.000448302211302,
                0.000512184275184,
                0.000576438984439,
            ],
        }
    )
    interpolated = aria.interpolate(groundtrouth["w"])
    plt.assert_frame_equal(groundtrouth, interpolated)
    # with pl.Config(float_precision=15):
    #     print(interpolated["n"])
    #     print(interpolated["k"])
