def example(extract='m', estimate=False):
    import pandas as pd

    import larch as lx

    d = lx.examples.MTC(format="dataset")
    d

    m = lx.Model(d)

    from larch import PX, P, X

    m.utility_co[2] = P("ASC_SR2") + P("hhinc#2") * X("hhinc")
    m.utility_co[3] = P("ASC_SR3P") + P("hhinc#3") * X("hhinc")
    m.utility_co[4] = P("ASC_TRAN") + P("hhinc#4") * X("hhinc")
    m.utility_co[5] = P("ASC_BIKE") + P("hhinc#5") * X("hhinc")
    m.utility_co[6] = P("ASC_WALK") + P("hhinc#6") * X("hhinc")

    m.utility_ca = PX("tottime") + PX("totcost")

    m.availability_ca_var = "avail"
    m.choice_ca_var = "chose"

    m.title = "MTC Example 1 (Simple MNL)"

    m.choice_avail_summary()

    m.set_cap(20)
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    result = m.maximize_loglike(stderr=True)

    m.parameter_summary()

    m.ordering = (
        (
            "LOS",
            "totcost",
            "tottime",
        ),
        (
            "ASCs",
            "ASC.*",
        ),
        (
            "Income",
            "hhinc.*",
        ),
    )

    m.parameter_summary()

    m.estimation_statistics()
    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
