def example(extract='m', estimate=False):
    import larch

    larch.__version__

    d = larch.examples.MTC(format="dataset")
    d

    m = larch.Model(d, compute_engine="numba")

    from larch import PX, P, X

    m.utility_co[2] = P("ASC_SR2")
    m.utility_co[3] = P("ASC_SR3P")
    m.utility_co[4] = P("ASC_TRAN") + P("hhinc#4") * X("hhinc")
    m.utility_co[5] = P("ASC_BIKE") + P("hhinc#5") * X("hhinc")
    m.utility_co[6] = P("ASC_WALK") + P("hhinc#6") * X("hhinc")

    m.utility_ca = PX("tottime") + PX("totcost")

    m.availability_ca_var = "avail"
    m.choice_ca_var = "chose"

    m.title = "MTC Example 3, Zeroed Shared"

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

    # TEST
    revealed_x = dict(zip(m.pnames, result.x))

    # TEST
    from pytest import approx

    expected_x = {
        "ASC_BIKE": -2.3989187974851647,
        "ASC_SR2": -2.3041966926745103,
        "ASC_SR3P": -3.7034452031908507,
        "ASC_TRAN": -0.6966955353312382,
        "ASC_WALK": -0.2269314175275228,
        "hhinc#4": -0.00486415050538345,
        "hhinc#5": -0.012431555290989793,
        "hhinc#6": -0.009365241345664176,
        "totcost": -0.004912235245649822,
        "tottime": -0.05135135046958243,
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
