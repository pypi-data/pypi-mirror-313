def example(extract='m', estimate=False):
    import larch

    larch.__version__

    d = larch.examples.MTC(format="dataset")
    d

    m = larch.Model(d, compute_engine="numba")

    from larch import PX, P, X

    for a in [2, 3]:
        m.utility_co[a] = +P("hhinc#2,3") * X("hhinc")
    for a in [4, 5, 6]:
        m.utility_co[a] = +P(f"hhinc#{a}") * X("hhinc")

    d.dc.alts_mapping

    for a, name in d.dc.alts_mapping.items():
        if a == 1:
            continue
        m.utility_co[a] += P("ASC_" + name) + P("vehbyadlt_" + name) * X("numveh/numadlt")

    m.utility_ca = (
        +PX("totcost")
        + P("motorized_time") * X("(altid <= 4) * tottime")
        + P("nonmotorized_time") * X("(altid > 4) * tottime")
        + P("motorized_ovtbydist") * X("(altid <= 4) * ovtt/dist")
    )

    m.availability_ca_var = "avail"
    m.choice_ca_var = "chose"

    m.title = "MTC Example 12, Autos per Adult"

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
            ".*cost.*",
            ".*time.*",
            ".*dist.*",
        ),
        (
            "Income",
            "hhinc.*",
        ),
        ("Ownership", "vehbyadlt.*"),
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
    assert result["loglike"] == approx(-3490.3579715315, rel=1e-5), result["loglike"]

    expected_x = {
        "ASC_Bike": -1.9627758221667733,
        "ASC_SR2": -1.536865403172976,
        "ASC_SR3+": -3.0235322387181176,
        "ASC_Transit": 1.0496197735578745,
        "ASC_Walk": -0.21728572066754234,
        "hhinc#2,3": -0.0013240180758255255,
        "hhinc#4": -0.004616956633813837,
        "hhinc#5": -0.011663606663415026,
        "hhinc#6": -0.00764683683920611,
        "motorized_ovtbydist": -0.18489944106276082,
        "motorized_time": -0.03803405138642473,
        "nonmotorized_time": -0.046633097590087214,
        "totcost": -0.004179712660535923,
        "vehbyadlt_Bike": -0.6418346308251331,
        "vehbyadlt_SR2": -0.594456791391658,
        "vehbyadlt_SR3+": -0.447408231859455,
        "vehbyadlt_Transit": -1.4092358161539453,
        "vehbyadlt_Walk": -0.7935735138713005,
    }
    for k in expected_x:
        assert revealed_x[k] == approx(
            expected_x[k], 0.03
        ), f"{k}, {revealed_x[k]/expected_x[k]}"
    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
