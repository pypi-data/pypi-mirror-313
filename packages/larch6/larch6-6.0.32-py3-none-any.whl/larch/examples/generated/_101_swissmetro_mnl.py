def example(extract='m', estimate=False):
    import larch as lx

    m = lx.Model()

    m.title = "swissmetro example 01 (simple logit)"

    m.availability_co_vars = {
        1: "TRAIN_AV * (SP!=0)",
        2: "SM_AV",
        3: "CAR_AV * (SP!=0)",
    }

    m.choice_co_code = "CHOICE"

    from larch import P, X

    m.utility_co[1] = P("ASC_TRAIN")
    m.utility_co[2] = 0
    m.utility_co[3] = P("ASC_CAR")
    m.utility_co[1] += X("TRAIN_TT") * P("B_TIME")
    m.utility_co[2] += X("SM_TT") * P("B_TIME")
    m.utility_co[3] += X("CAR_TT") * P("B_TIME")
    m.utility_co[1] += X("TRAIN_CO*(GA==0)") * P("B_COST")
    m.utility_co[2] += X("SM_CO*(GA==0)") * P("B_COST")
    m.utility_co[3] += X("CAR_CO") * P("B_COST")

    m.ordering = [
        (
            "ASCs",
            "ASC.*",
        ),
        (
            "LOS",
            "B_.*",
        ),
    ]

    import pandas as pd

    raw_data = pd.read_csv(lx.example_file("swissmetro.csv.gz")).rename_axis(index="CASEID")
    raw_data.head()

    keep = raw_data.eval("PURPOSE in (1,3) and CHOICE != 0")
    selected_data = raw_data[keep]

    ds = lx.Dataset.construct.from_idco(selected_data, alts={1: "Train", 2: "SM", 3: "Car"})

    ds

    m.datatree = ds
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    m.set_cap(15)
    result = m.maximize_loglike(method="SLSQP")

    m.calculate_parameter_covariance();

    m.parameter_summary()
    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
