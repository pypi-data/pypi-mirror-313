def example(extract='m', estimate=False):
    import geopandas as gpd
    import pandas as pd

    import larch as lx

    lx.__version__

    from larch.examples import example_file

    taz_shape = gpd.read_file("zip://" + example_file("exampville_taz.zip"))

    emp = pd.read_csv(example_file("exampville_employment.csv.gz"), index_col="TAZ")

    emp.head()

    from larch.omx import OMX

    skims = OMX(example_file("exampville_skims.omx"), mode="r")
    skims

    hh = pd.read_csv(example_file("exampville_households.csv.gz"))

    hh.head()

    pp = pd.read_csv(example_file("exampville_persons.csv.gz"))

    pp.head()

    tour = pd.read_csv(example_file("exampville_tours.csv.gz"))

    tour.head()
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]

    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
