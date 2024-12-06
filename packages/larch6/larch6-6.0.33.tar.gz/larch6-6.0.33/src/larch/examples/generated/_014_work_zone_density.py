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
        m.utility_co[a] += (
            +P("ASC_" + name)
            + P("vehbywrk_" + name) * X("vehbywrk")
            + P("wkempden_" + name) * X("wkempden")
        )

    m.utility_ca = (
        +PX("totcost")
        + P("motorized_time") * X("(altid <= 4) * tottime")
        + P("nonmotorized_time") * X("(altid > 4) * tottime")
        + P("motorized_ovtbydist") * X("(altid <= 4) * ovtt/dist")
    )

    m.availability_ca_var = "avail"
    m.choice_ca_var = "chose"

    m.title = "MTC Example 14, Work Zone Density"

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
        ("Ownership", "vehbywrk.*"),
        ("Zonal", "wkcbd.*"),
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
        "ASC_Bike": -1.597604389138021,
        "ASC_SR2": -1.604852502224575,
        "ASC_SR3+": -3.2123038625161646,
        "ASC_Transit": 0.4190578710080788,
        "ASC_Walk": -0.04100863602733044,
        "hhinc#2,3": -0.001774790620723634,
        "hhinc#4": -0.007075606155487522,
        "hhinc#5": -0.01118298552433892,
        "hhinc#6": -0.007903089907643455,
        "motorized_ovtbydist": -0.15748802513969926,
        "motorized_time": -0.029932168547457633,
        "nonmotorized_time": -0.04588150145362945,
        "totcost": -0.0028860643507599704,
        "vehbywrk_Bike": -0.7134510041177601,
        "vehbywrk_SR2": -0.40696239364371894,
        "vehbywrk_SR3+": -0.23731738368202027,
        "vehbywrk_Transit": -0.9946707857236002,
        "vehbywrk_Walk": -0.6812141773311737,
        "wkempden_Bike": 0.0010505639989477746,
        "wkempden_SR2": 0.0011364815897366538,
        "wkempden_SR3+": 0.0022153143196966783,
        "wkempden_Transit": 0.0026832716813030427,
        "wkempden_Walk": 0.0015105648018639885,
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
