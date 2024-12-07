<!-- ![](.github/refidxdb-logo.png) -->

<p align="center">
  <img src="https://github.com/arunoruto/RefIdxDB/blob/main/.github/logo.png?raw=true" alt="RefIdxDB-Logo"/>
</p>

# RefIdxDB

Python interface for various refractive index databases

I was tired to download files from here and there, parse them each manually and locally.
Hence, I copied most of my parsing code into this project, so it can be developed further.

> [!note]
> If your source is not implemented, feel free to open an issue!
> You can also try to implement it yourself.
> You can take `refidx` and `aria` as a reference on what needs to be implemented.

## Installation

`refidxdb` can be downloaded from PiPy.org:

```sh
pip install refidxdb
```

After the `pip` command, the `refidxdb` command should be available.

## CLI

The main purpose of the CLI is to download and cache the databases locally and interact with it.
The data will be downloaded to `$HOME/.cache/refidxdb` under a folder corresponding to the class name.
Please use `refidxdb --help` to explore the functionality.

Example:

```console
$ # Download all databases
$ # equivalent to refidxdb db --download aria,refidx
$ refidxdb db --download all
Downloading the database for RefIdx from https://github.com/polyanskiy/refractiveindex.info-database/releases/download/v2024-08-14/rii-database-2024-08-14.zip to /home/mar/.cache/refidxdb/RefIdx
Downloading the database for Aria from https://eodg.atm.ox.ac.uk/ARIA/data_files/ARIA.zip to /home/mar/.cache/refidxdb/Aria
All databases downlaoded!
Bye :)

$ # Replace table with plot to diplay a graph of the data in the terminal
$ refidxdb show --db aria --data "data_files/Minerals/Olivine/z_orientation_(Fabian_et_al._2001)/olivine_Z_Fabian_2001.ri" --display table --bounds 2.5,15.5
shape: (2_748, 3)
┌───────────┬──────────┬──────────┐
│ w         ┆ n        ┆ k        │
│ ---       ┆ ---      ┆ ---      │
│ f64       ┆ f64      ┆ f64      │
╞═══════════╪══════════╪══════════╡
│ 2.500617  ┆ 1.619696 ┆ 0.000053 │
│ 2.501381  ┆ 1.619685 ┆ 0.000053 │
│ 2.502144  ┆ 1.619674 ┆ 0.000053 │
│ 2.502909  ┆ 1.619663 ┆ 0.000053 │
│ 2.503674  ┆ 1.619652 ┆ 0.000053 │
│ …         ┆ …        ┆ …        │
│ 15.369648 ┆ 1.42662  ┆ 0.036282 │
│ 15.398545 ┆ 1.419686 ┆ 0.036761 │
│ 15.427528 ┆ 1.412672 ┆ 0.037256 │
│ 15.456643 ┆ 1.405576 ┆ 0.037768 │
│ 15.485869 ┆ 1.398394 ┆ 0.038299 │
└───────────┴──────────┴──────────┘

$ # Explore the databases using streamlit
$ refidxdb explore
/home/user/Projects/refidxdb/refidxdb

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.42.42.212:8501
```

## API

`RefIdxDB`: is the main blueprint class from which all the specific parser classes need to inherit.
This yields a unified API, i.e., all the instances have the same methods available.

`path`: is the path leading to the wanted file relative to the database.
This value can be usually copied from the URL.

`data`: represents the raw data obtained from the file found under `path`.

`nk`: are the parsed real and imaginary parts of the refractive index.
The main column is always the wavelength, i.e., wave numbers will always be transformed into wavelengths.

`interpolate`: you rarely want to use the tables as is, therefore an interpolation method is implemented
to calculate `n` and `k` for a target wavelength.

> [!warning]
> Only wavelengths are currently supported, since they are my main use-case.
> If you have a proposal on how to add wave number support, please submit an issue/PR.

## Supported DBs

### [refractiveindex.info](https://refractiveindex.info/)

`refractiveindex.info` mainly differentiates between raw data with wavelengths in micrometers,
or polynomial functions which hold for a certain range. The raw data is contained in `YAML` files,
with each data type being referenced.

Currently, supported data types are:

- `tabulated_nk`
- `tabulated_n`
- `tabulated_k`
- `formula 1`
- `formula 2`
- `formula 3`

### [ARIA - Aerosol Refractive Index Archive](https://eodg.atm.ox.ac.uk/ARIA/)

Aria consists of `ri` files, which are whitespace separated values.
The header is prefixed by a hashtag `#`. The `FORMAT` value gives information about the column labels.
Both wavelengths `WAVL` and wave numbers `WAVN` will be read correctly and transformed into wavelengths
with no SI prefix (meters [m]). The default scales for wavelengths and wave numbers are 1e-6 (micrometers)
and 1e2 (centimeters^-1).

## Similar projects

RefIdxDB is, to the best of my knowledge,
the only project that tries to unify multiple databases under one API.
Nevertheless, there are projects that have tried to achieve the same for a single database:

- [refractiveindex](https://pypi.org/project/refractiveindex/)
- [PyTMM](https://github.com/kitchenknif/PyTMM) - the API is implemented in
  [refractiveindex.py](https://github.com/kitchenknif/PyTMM/blob/master/PyTMM/refractiveIndex.py)
- [PyOptik](https://github.com/MartinPdeS/PyOptik)
