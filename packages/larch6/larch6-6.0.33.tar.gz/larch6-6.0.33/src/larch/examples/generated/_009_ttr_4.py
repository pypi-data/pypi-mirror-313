def example(extract='m', estimate=False):
    import larch as lx

    lx.__version__

    d = lx.examples.MTC(format="dataset")
    d

    m = lx.Model(d, compute_engine="numba")

    from larch import PX, P, X

    m.utility_co[2] = P("ASC_SR2") + P("hhinc#2,3") * X("hhinc")
    m.utility_co[3] = P("ASC_SR3P") + P("hhinc#2,3") * X("hhinc")
    m.utility_co[4] = P("ASC_TRAN") + P("hhinc#4") * X("hhinc")
    m.utility_co[5] = P("ASC_BIKE") + P("hhinc#5") * X("hhinc")
    m.utility_co[6] = P("ASC_WALK") + P("hhinc#6") * X("hhinc")

    m.utility_ca = (
        +P("nonmotorized_time") * X("(altid>4) * tottime")
        + P("motorized_time") * (X("(altid <= 4) * ivtt") + 4 * X("(altid <= 4) * ovtt"))
        + PX("totcost")
    )

    m.availability_ca_var = "avail"
    m.choice_ca_var = "chose"

    m.title = "MTC Example 9, TTR = 4.0"

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
            ".*cost.*",
            ".*time.*",
            ".*ivtt.*",
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
    from pytest import approx

    revealed_x = dict(zip(m.pnames, result.x))
    expected_x = {
        "ASC_BIKE": -1.770293526149154,
        "ASC_SR2": -2.36434925168087,
        "ASC_SR3P": -3.7996202473241243,
        "ASC_TRAN": -0.5278848721558753,
        "ASC_WALK": 0.42911515571938,
        "hhinc#2,3": -0.0015697667050703,
        "hhinc#4": -0.005558458299255231,
        "hhinc#5": -0.01232547986107763,
        "hhinc#6": -0.009373810771427111,
        "motorized_time": -0.01726398858839431,
        "nonmotorized_time": -0.0652721175592692,
        "totcost": -0.004834718284259079,
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
