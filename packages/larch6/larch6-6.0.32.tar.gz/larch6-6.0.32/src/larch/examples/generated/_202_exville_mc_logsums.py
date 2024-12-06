def example(extract='m', estimate=False):
    import numpy as np
    import xarray as xr
    from addicty import Dict

    import larch as lx

    hh, pp, tour, skims = lx.example(200, ["hh", "pp", "tour", "skims"])

    exampville_mode_choice_file = lx.example(
        201, output_file="exampville_mode_choice.html", estimate=True
    )
    m = lx.load_model(exampville_mode_choice_file)

    Mode = Dict(
        DA=1,
        SR=2,
        Walk=3,
        Bike=4,
        Transit=5,
    ).freeze()

    tour_dataset = lx.Dataset.construct.from_idco(tour.set_index("TOURID"), alts=Mode)
    od_skims = lx.Dataset.construct.from_omx(skims)

    dt = lx.DataTree(
        tour=tour_dataset.dc.query_cases("TOURPURP == 1"),
        hh=hh.set_index("HHID"),
        person=pp.set_index("PERSONID"),
        od=od_skims,
        do=od_skims,
        relationships=(
            "tours.HHID @ hh.HHID",
            "tours.PERSONID @ person.PERSONID",
            "hh.HOMETAZ @ od.otaz",
            "tours.DTAZ @ od.dtaz",
            "hh.HOMETAZ @ do.dtaz",
            "tours.DTAZ @ do.otaz",
        ),
    )

    logsums = lx.DataArray.zeros(
        dt.caseids(),
        skims.TAZ_ID,
        name="logsums",
    )

    for dtaz in logsums.TAZ_ID:
        m.datatree = dt.replace_datasets(
            tour=dt.root_dataset.assign(DTAZ=xr.full_like(dt._getitem("DTAZ"), dtaz)),
        )
        logsums.loc[dict(TAZ_ID=dtaz)] = m.logsums()

    logsums.to_zarr("logsums.zarr")

    lx.DataArray.from_zarr("logsums.zarr")
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
