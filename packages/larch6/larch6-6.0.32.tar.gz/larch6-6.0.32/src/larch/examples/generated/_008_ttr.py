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
        + P("motorized_ivtt") * (X("(altid <= 4) * ivtt") + 2.5 * X("(altid <= 4) * ovtt"))
        + PX("totcost")
    )

    m.availability_ca_var = "avail"
    m.choice_ca_var = "chose"

    m.title = "MTC Example 8, TTR = 2.5"

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
    revealed_x = dict(zip(m.pnames, result.x))

    # TEST
    from pytest import approx

    expected_x = {
        "ASC_BIKE": -1.8019897052221918,
        "ASC_SR2": -2.3298554039662283,
        "ASC_SR3P": -3.756413794251253,
        "ASC_TRAN": -0.582221916159616,
        "ASC_WALK": 0.4380372173849091,
        "hhinc#2,3": -0.0015674849574736722,
        "hhinc#4": -0.005515844848425141,
        "hhinc#5": -0.012357167709979168,
        "hhinc#6": -0.009464085538793363,
        "motorized_ivtt": -0.02536879896953912,
        "nonmotorized_time": -0.06627353731450113,
        "totcost": -0.00486979028829524,
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
