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
        )

    m.utility_ca = (
        +PX("totcost")
        + P("motorized_time") * X("(altid <= 4) * tottime")
        + P("nonmotorized_time") * X("(altid > 4) * tottime")
        + P("motorized_ovtbydist") * X("(altid <= 4) * ovtt/dist")
    )

    m.availability_ca_var = "avail"
    m.choice_ca_var = "chose"

    m.title = "MTC Example 13, CBD"

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
        "ASC_Bike": -1.65086990936308,
        "ASC_SR2": -1.6343459309594404,
        "ASC_SR3+": -3.536895423106506,
        "ASC_Transit": -0.20182268467513967,
        "ASC_Walk": 0.08378500087016123,
        "hhinc#2,3": -0.0017353041895238406,
        "hhinc#4": -0.006149027560100709,
        "hhinc#5": -0.011116299683489442,
        "hhinc#6": -0.007835540009972525,
        "motorized_ovtbydist": -0.15011160599438625,
        "motorized_time": -0.028598343252833735,
        "nonmotorized_time": -0.04641360594486308,
        "totcost": -0.0032855739180273234,
        "vehbywrk_Bike": -0.6979736536562279,
        "vehbywrk_SR2": -0.4154516212033234,
        "vehbywrk_SR3+": -0.21205944593613626,
        "vehbywrk_Transit": -0.9109101165995294,
        "vehbywrk_Walk": -0.7194478370164099,
        "wkcbd_Bike": 0.3759603983833265,
        "wkcbd_SR2": 0.2558900818841308,
        "wkcbd_SR3+": 1.0573013291451367,
        "wkcbd_Transit": 1.3562157325427109,
        "wkcbd_Walk": 0.17467164791819956,
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
