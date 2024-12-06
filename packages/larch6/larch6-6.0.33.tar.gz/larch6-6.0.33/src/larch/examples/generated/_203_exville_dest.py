def example(extract='m', estimate=False):
    import numpy as np
    import pandas as pd

    import larch as lx
    from larch import P, X

    hh, pp, tour, skims, emp = lx.example(200, ["hh", "pp", "tour", "skims", "emp"])

    hh["INCOME_GRP"] = pd.qcut(hh.INCOME, 3)

    logsums_file = lx.example(202, output_file="logsums.zarr")
    logsums = lx.DataArray.from_zarr("logsums.zarr")

    ca = lx.Dataset.construct(
        {"logsum": logsums},
        caseid="TOURID",
        alts=skims.TAZ_ID,
    )
    ca

    emp.info()

    tree = lx.DataTree(
        base=ca,
        tour=tour.rename_axis(index="TOUR_ID"),
        hh=hh.set_index("HHID"),
        person=pp.set_index("PERSONID"),
        emp=emp,
        skims=lx.Dataset.construct.from_omx(skims),
        relationships=(
            "base.TAZ_ID @ emp.TAZ",
            "base.TOURID -> tour.TOUR_ID",
            "tour.HHID @ hh.HHID",
            "tour.PERSONID @ person.PERSONID",
            "hh.HOMETAZ @ skims.otaz",
            "base.TAZ_ID @ skims.dtaz",
        ),
    )

    m = lx.Model(datatree=tree)
    m.title = "Exampville Work Tour Destination Choice v1"

    m.quantity_ca = (
        +P.EmpRetail_HighInc * X("RETAIL_EMP * (INCOME>50000)")
        + P.EmpNonRetail_HighInc * X("NONRETAIL_EMP") * X("INCOME>50000")
        + P.EmpRetail_LowInc * X("RETAIL_EMP") * X("INCOME<=50000")
        + P.EmpNonRetail_LowInc * X("NONRETAIL_EMP") * X("INCOME<=50000")
    )

    m.quantity_scale = P.Theta

    m.utility_ca = +P.logsum * X.logsum + P.distance * X.AUTO_DIST

    m.choice_co_code = "tour.DTAZ"

    m.plock(EmpRetail_HighInc=0, EmpRetail_LowInc=0)

    mj = m.copy()

    m.compute_engine = "numba"

    m.loglike()

    m.d_loglike()

    mj.d_loglike()
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    result = m.maximize_loglike(stderr=True)

    resultj = mj.maximize_loglike(stderr=True)

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

    report = lx.Reporter(title=m.title)

    report << "# Parameter Summary" << m.parameter_summary()

    report << "# Parameter Summary" << m.parameter_summary()

    report << "# Estimation Statistics" << m.estimation_statistics()

    report << "# Utility Functions" << m.utility_functions()

    figure = m.histogram_on_idca_variable(
        "AUTO_DIST",
        bins=30,
        span=(0, 15),
        x_label="Distance (miles)",
    )
    report << "# Visualization"
    report << figure

    report.save(
        "exampville_dest_choice.html",
        overwrite=True,
        metadata=m.dumps(),
    )
    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
