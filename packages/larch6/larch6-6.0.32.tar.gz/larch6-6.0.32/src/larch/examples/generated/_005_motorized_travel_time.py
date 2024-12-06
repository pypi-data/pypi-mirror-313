def example(extract='m', estimate=False):
    import larch

    larch.__version__

    d = larch.examples.MTC(format="dataset")
    d

    m = larch.Model(d, compute_engine="numba")

    from larch import PX, P, X

    m.utility_co[2] = P("ASC_SR2") + P("hhinc#2,3") * X("hhinc")
    m.utility_co[3] = P("ASC_SR3P") + P("hhinc#2,3") * X("hhinc")
    m.utility_co[4] = P("ASC_TRAN") + P("hhinc#4") * X("hhinc")
    m.utility_co[5] = P("ASC_BIKE") + P("hhinc#5") * X("hhinc")
    m.utility_co[6] = P("ASC_WALK") + P("hhinc#6") * X("hhinc")

    m.utility_ca = +(
        P("motorized_time") * X("(altid <= 4) * tottime")
        + P("nonmotorized_time") * X("(altid >4) * tottime")
        + PX("totcost")
    )

    m.availability_ca_var = "avail"
    m.choice_ca_var = "chose"

    m.title = "MTC Example 5, Motorized Travel Times"

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
            "motorized_time",
            "nonmotorized_time",
        ),
        (
            "Income",
            "hhinc.*",
        ),
        (
            "ASCs",
            "ASC.*",
        ),
    )

    m.parameter_summary()

    m.estimation_statistics()

    # TEST
    revealed_x = dict(zip(m.pnames, result.x))

    # TEST
    from pytest import approx

    expected_x = {
        "ASC_BIKE": -1.840892643878567,
        "ASC_SR2": -2.2622448341521775,
        "ASC_SR3P": -3.6771306979421228,
        "ASC_TRAN": -0.852957222474832,
        "ASC_WALK": 0.4685149210255025,
        "hhinc#2,3": -0.0015329803832402177,
        "hhinc#4": -0.005431498351689336,
        "hhinc#5": -0.012539862511200987,
        "hhinc#6": -0.009455692802202887,
        "motorized_time": -0.04307376568436681,
        "nonmotorized_time": -0.06856560413388568,
        "totcost": -0.0050037305794018135,
    }
    for k in expected_x:
        assert revealed_x[k] == approx(
            expected_x[k], 2e-2
        ), f"{k}, {revealed_x[k]/expected_x[k]}"
    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
