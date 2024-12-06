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

    m.utility_ca = (
        +PX("totcost")
        + P("motorized_time") * X("(altid <= 4) * tottime")
        + P("nonmotorized_time") * X("(altid > 4) * tottime")
        + P("motorized_ovtbydist") * X("(altid <= 4) * ovtt/dist")
    )

    m.availability_ca_var = "avail"
    m.choice_ca_var = "chose"

    m.title = "MTC Example 7, Diminishing OVTT by Distance"

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
            ".*dist.*",
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
        "ASC_BIKE": -2.675340279013382,
        "ASC_SR2": -2.1871708718901455,
        "ASC_SR3P": -3.5170483581773535,
        "ASC_TRAN": -0.039611848334672385,
        "ASC_WALK": -1.0206078711851112,
        "hhinc#2,3": -0.001383608162986253,
        "hhinc#4": -0.007257729971526785,
        "hhinc#5": -0.01196363695212793,
        "hhinc#6": -0.008182417861122782,
        "motorized_ovtbydist": -0.18145744778558676,
        "motorized_time": -0.04156509908994426,
        "nonmotorized_time": -0.04755705411055601,
        "totcost": -0.004114472584806616,
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
