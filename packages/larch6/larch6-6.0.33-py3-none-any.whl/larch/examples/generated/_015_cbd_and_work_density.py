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
            + P("wkcbd_" + name) * X("wkccbd + wknccbd")
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

    m.title = "MTC Example 15, CBD and Work Zone Density"

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
        (
            "Ownership",
            "vehbywrk.*",
        ),
        (
            "Zonal",
            "wkcbd.*",
            "wkempden.*",
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
        "ASC_Bike": -1.5151318657112478,
        "ASC_SR2": -1.639621785899234,
        "ASC_SR3+": -3.5498049001734238,
        "ASC_Transit": -0.47143923682534866,
        "ASC_Walk": 0.21026651839235272,
        "hhinc#2,3": -0.0017891356181531338,
        "hhinc#4": -0.007055215263878235,
        "hhinc#5": -0.010871925468591604,
        "hhinc#6": -0.008146028375074365,
        "motorized_ovtbydist": -0.1323506788859075,
        "motorized_time": -0.023127586918978607,
        "nonmotorized_time": -0.04674422574883194,
        "totcost": -0.0023594181967103688,
        "vehbywrk_Bike": -0.7148764842966541,
        "vehbywrk_SR2": -0.40107491197968403,
        "vehbywrk_SR3+": -0.18300198096457299,
        "vehbywrk_Transit": -0.929527581541754,
        "vehbywrk_Walk": -0.7274192267489848,
        "wkcbd_Bike": 0.46171020679060165,
        "wkcbd_SR2": 0.20374438316475474,
        "wkcbd_SR3+": 1.0180449637000595,
        "wkcbd_Transit": 1.2044875454394255,
        "wkcbd_Walk": 0.10842899827763496,
        "wkempden_Bike": 0.0008326068252564282,
        "wkempden_SR2": 0.0009948160919762453,
        "wkempden_SR3+": 0.001289870634851483,
        "wkempden_Transit": 0.002109547340455916,
        "wkempden_Walk": 0.0017929231441064044,
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
