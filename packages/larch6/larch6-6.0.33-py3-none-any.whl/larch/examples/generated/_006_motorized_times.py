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
        +P("nonmotorized_time") * X("(altid>4) * tottime")
        + P("motorized_ovtt") * X("(altid <= 4) * ovtt")
        + P("motorized_ivtt") * X("(altid <= 4) * ivtt")
        + PX("totcost")
    )

    m.availability_ca_var = "avail"
    m.choice_ca_var = "chose"

    m.title = "MTC Example 6, Motorized Times"

    m.choice_avail_summary()

    m.set_cap(20)

    assert m.compute_engine == "numba"
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    result = m.maximize_loglike(stderr=True, method="bhhh")
    m.calculate_parameter_covariance()
    m.loglike()

    m.parameter_summary()

    m.ordering = (
        (
            "LOS",
            "totcost",
            "nonmotorized_time",
            "motorized_ivtt",
            "motorized_ovtt",
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
        "ASC_BIKE": -1.719093452086421,
        "ASC_SR2": -2.4299943985819956,
        "ASC_SR3P": -3.8834310483961114,
        "ASC_TRAN": -0.4898195783250097,
        "ASC_WALK": 0.4091981983094832,
        "hhinc#2,3": -0.0015835444926238225,
        "hhinc#4": -0.005692708506297093,
        "hhinc#5": -0.01221964685106249,
        "hhinc#6": -0.009303042887650576,
        "motorized_ivtt": -0.002540641825564394,
        "motorized_ovtt": -0.07594330410291915,
        "nonmotorized_time": -0.06319642667912634,
        "totcost": -0.0047982963933021535,
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
