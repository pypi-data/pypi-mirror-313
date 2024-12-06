def example(extract='m', estimate=False):
    import larch as lx

    lx.__version__

    d = lx.examples.MTC(format="dataset")
    d

    m = lx.Model(d, compute_engine="numba")

    from larch import PX, P, X

    m.utility_co[2] = P("ASC_SR2") + P("hhinc#Moto") * X("hhinc")
    m.utility_co[3] = P("ASC_SR3P") + P("hhinc#Moto") * X("hhinc")
    m.utility_co[4] = P("ASC_TRAN") + P("hhinc#Moto") * X("hhinc")
    m.utility_co[5] = P("ASC_BIKE") + P("hhinc#5") * X("hhinc")
    m.utility_co[6] = P("ASC_WALK") + P("hhinc#6") * X("hhinc")

    m.utility_ca = PX("tottime") + PX("totcost")

    m.availability_ca_var = "avail"
    m.choice_ca_var = "chose"

    m.title = "MTC Example 2, Motorized"

    m.choice_avail_summary()

    m.set_cap(20)

    assert m.compute_engine == "numba"
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    result = m.maximize_loglike(stderr=True)
    m.calculate_parameter_covariance()
    m.loglike()

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
