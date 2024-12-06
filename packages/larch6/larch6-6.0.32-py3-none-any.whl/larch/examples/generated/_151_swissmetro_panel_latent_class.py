def example(extract='m', estimate=False):
    import numpy as np
    import pandas as pd
    from pytest import approx

    import larch as lx
    from larch import P, X

    raw = pd.read_csv(lx.example_file("swissmetro.csv.gz"))
    raw["SM_COST"] = raw["SM_CO"] * (raw["GA"] == 0)
    raw["TRAIN_COST"] = raw.eval("TRAIN_CO * (GA == 0)")
    raw["TRAIN_COST_SCALED"] = raw["TRAIN_COST"] / 100
    raw["TRAIN_TT_SCALED"] = raw["TRAIN_TT"] / 100

    raw["SM_COST_SCALED"] = raw.eval("SM_COST / 100")
    raw["SM_TT_SCALED"] = raw["SM_TT"] / 100

    raw["CAR_CO_SCALED"] = raw["CAR_CO"] / 100
    raw["CAR_TT_SCALED"] = raw["CAR_TT"] / 100
    raw["CAR_AV_SP"] = raw.eval("CAR_AV * (SP!=0)")
    raw["TRAIN_AV_SP"] = raw.eval("TRAIN_AV * (SP!=0)")

    raw["keep"] = raw.eval("PURPOSE in (1,3) and CHOICE != 0")

    raw

    data = lx.Dataset.construct.from_idco(raw).dc.query_cases("keep")

    availability_co_vars = {
        1: "TRAIN_AV_SP",
        2: "SM_AV",
        3: "CAR_AV_SP",
    }

    m1 = lx.Model(title="Model1")
    m1.availability_co_vars = availability_co_vars
    m1.choice_co_code = "CHOICE"
    m1.utility_co[1] = P("ASC_TRAIN") + X("TRAIN_COST_SCALED") * P("B_COST")
    m1.utility_co[2] = X("SM_COST_SCALED") * P("B_COST")
    m1.utility_co[3] = P("ASC_CAR") + X("CAR_CO_SCALED") * P("B_COST")

    m2 = lx.Model(title="Model2")
    m2.availability_co_vars = availability_co_vars
    m2.choice_co_code = "CHOICE"
    m2.utility_co[1] = (
        P("ASC_TRAIN")
        + X("TRAIN_TT_SCALED") * P("B_TIME")
        + X("TRAIN_COST_SCALED") * P("B_COST")
    )
    m2.utility_co[2] = X("SM_TT_SCALED") * P("B_TIME") + X("SM_COST_SCALED") * P("B_COST")
    m2.utility_co[3] = (
        P("ASC_CAR") + X("CAR_TT_SCALED") * P("B_TIME") + X("CAR_CO_SCALED") * P("B_COST")
    )

    m3 = lx.Model(title="Model3")
    m3.availability_co_vars = availability_co_vars
    m3.choice_co_code = "CHOICE"
    m3.utility_co[1] = X("TRAIN_COST_SCALED") * P("Z_COST")
    m3.utility_co[2] = X("SM_COST_SCALED") * P("Z_COST")
    m3.utility_co[3] = X("CAR_CO_SCALED") * P("Z_COST")

    mk = lx.Model()
    mk.utility_co[102] = P("W_OTHER")
    mk.utility_co[103] = P("W_COST")

    b = lx.LatentClass(
        mk,
        {101: m1, 102: m2, 103: m3},
        datatree=data.dc.set_altids([1, 2, 3]),
        groupid="ID",
    )

    b.lock_value(Z_COST=-10000)  # set the lexicographic parameter

    b.set_cap(25)
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    result = b.maximize_loglike(method="slsqp")

    b.calculate_parameter_covariance();

    b.parameter_summary()
    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
