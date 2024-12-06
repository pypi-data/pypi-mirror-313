def example(extract='m', estimate=False):
    import numpy as np
    import pandas as pd

    import larch as lx
    from larch import P, X

    hh, pp, tour, skims, emp = lx.example(200, ["hh", "pp", "tour", "skims", "emp"])

    hh["INCOME_GRP"] = pd.qcut(hh.INCOME, 3)

    co = lx.Dataset.construct(
        tour.set_index("TOURID"),
        caseid="TOURID",
        alts=skims.TAZ_ID,
    )
    co

    emp.info()

    tree = lx.DataTree(
        base=co,
        hh=hh.set_index("HHID"),
        person=pp.set_index("PERSONID"),
        emp=emp,
        skims=lx.Dataset.construct.from_omx(skims),
        relationships=(
            "base.TAZ_ID @ emp.TAZ",
            "base.HHID @ hh.HHID",
            "base.PERSONID @ person.PERSONID",
            "hh.HOMETAZ @ skims.otaz",
            "base.TAZ_ID @ skims.dtaz",
        ),
    ).digitize_relationships()

    m = lx.Model(datatree=tree)
    m.title = "Exampville Tour Destination Choice v2"

    m.quantity_ca = (
        +P.EmpRetail_HighInc * X("RETAIL_EMP * (INCOME>50000)")
        + P.EmpNonRetail_HighInc * X("NONRETAIL_EMP") * X("INCOME>50000")
        + P.EmpRetail_LowInc * X("RETAIL_EMP") * X("INCOME<=50000")
        + P.EmpNonRetail_LowInc * X("NONRETAIL_EMP") * X("INCOME<=50000")
    )

    m.quantity_scale = P.Theta

    m.utility_ca = +P.distance * X.AUTO_DIST

    m.choice_co_code = "base.DTAZ"

    m.plock(EmpRetail_HighInc=0, EmpRetail_LowInc=0)

    mj = m.copy()

    m.compute_engine = "numba"
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    result = m.maximize_loglike(stderr=True)

    resultj = mj.maximize_loglike(stderr=True)

    resultj

    m.histogram_on_idca_variable("AUTO_DIST")

    m.histogram_on_idca_variable("RETAIL_EMP")

    m.histogram_on_idca_variable("AUTO_DIST", bins=40, span=(0, 10))

    m.histogram_on_idca_variable(
        "AUTO_DIST",
        x_label="Distance (miles)",
        bins=26,
        span=(0, 13),
        filter_co="INCOME<10000",
    )

    tour_plus = tour.join(hh.set_index("HHID")[["HOMETAZ", "INCOME"]], on="HHID")
    tour_plus["LOW_INCOME"] = tour_plus.INCOME < 50_000
    tour_agg = (
        tour_plus.groupby(["HOMETAZ", "DTAZ", "LOW_INCOME"])
        .size()
        .unstack("DTAZ")
        .fillna(0)
    )

    # j = tour_agg.reset_index(drop=True)
    # lx.DataArray(j.values, dims=("index", "DTAZ"), coords={"index": j.index, "DTAZ": j.columns})

    agg_dataset = lx.Dataset.construct.from_idco(
        tour_agg.index.to_frame().reset_index(drop=True)
    )
    j = tour_agg.reset_index(drop=True)
    agg_dataset = agg_dataset.assign(
        destinations=lx.DataArray(
            j.values,
            dims=("index", "DTAZ"),
            coords={"index": j.index, "DTAZ": j.columns},
        )
    )
    agg_dataset.dc.ALTID = "DTAZ"
    agg_dataset

    agg_tree = lx.DataTree(
        base=agg_dataset,
        emp=emp,
        skims=lx.Dataset.construct.from_omx(skims),
        relationships=(
            "base.DTAZ @ emp.TAZ",
            "base.HOMETAZ @ skims.otaz",
            "base.DTAZ @ skims.dtaz",
        ),
    )

    mg = lx.Model(datatree=agg_tree, compute_engine="numba")
    mg.title = "Exampville Semi-Aggregate Destination Choice"

    mg.quantity_ca = (
        +P.EmpRetail_HighInc * X("RETAIL_EMP * (1-LOW_INCOME)")
        + P.EmpNonRetail_HighInc * X("NONRETAIL_EMP") * X("(1-LOW_INCOME)")
        + P.EmpRetail_LowInc * X("RETAIL_EMP") * X("LOW_INCOME")
        + P.EmpNonRetail_LowInc * X("NONRETAIL_EMP") * X("LOW_INCOME")
    )

    mg.quantity_scale = P.Theta

    mg.utility_ca = +P.distance * X.AUTO_DIST

    mg.choice_ca_var = "base.destinations"

    mg.plock(EmpRetail_HighInc=0, EmpRetail_LowInc=0)

    result = mg.maximize_loglike(stderr=True)
    result
    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
