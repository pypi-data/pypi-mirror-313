def example(extract='m', estimate=False):
    # TEST
    import larch

    import larch

    larch.__version__

    d = larch.examples.MTC(format="dataset")
    d

    d = d.sel(caseid=d.numveh <= 1)

    m = larch.Model(d, compute_engine="numba")

    from larch import P, X

    for a in [4, 5, 6]:
        m.utility_co[a] += X("hhinc") * P(f"hhinc#{a}")

    for i in d["alt_names"][1:3]:
        name = str(i.values)
        a = int(i.altid)
        m.utility_co[a] += (
            +X("vehbywrk") * P("vehbywrk_SR")
            + X("wkccbd+wknccbd") * P("wkcbd_" + name)
            + X("wkempden") * P("wkempden_" + name)
            + P("ASC_" + name)
        )

    for i in d["alt_names"][3:]:
        name = str(i.values)
        a = int(i.altid)
        m.utility_co[a] += (
            +X("vehbywrk") * P("vehbywrk_" + name)
            + X("wkccbd+wknccbd") * P("wkcbd_" + name)
            + X("wkempden") * P("wkempden_" + name)
            + P("ASC_" + name)
        )

    m.utility_ca = (
        +X("totcost/hhinc") * P("costbyincome")
        + X("tottime * (altid <= 4)") * P("motorized_time")
        + X("tottime * (altid >= 5)") * P("nonmotorized_time")
        + X("ovtt/dist * (altid <= 4)") * P("motorized_ovtbydist")
    )

    m.availability_ca_var = "avail"
    m.choice_ca_var = "chose"

    m.title = "MTC Example 17A, Segmented for 1 or fewer cars"

    m.choice_avail_summary()

    m.set_cap(25)

    assert m.compute_engine == "numba"
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    result = m.maximize_loglike(stderr=True, options={"maxiter": 1000, "ftol": 1e-10})
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
            "Zonal",
            "wkcbd.*",
            "wkempden.*",
        ),
        (
            "Household",
            "hhinc.*",
            "vehbywrk.*",
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
        "ASC_Bike": 0.9742143708899291,
        "ASC_SR2": 0.5953670936985695,
        "ASC_SR3+": -0.7824827134037493,
        "ASC_Transit": 2.2585074587816134,
        "ASC_Walk": 2.9039591287055986,
        "costbyincome": -0.02264018916095553,
        "hhinc#4": -0.006444094209484317,
        "hhinc#5": -0.011725009048022181,
        "hhinc#6": -0.01198956540981421,
        "motorized_ovtbydist": -0.11308926104452616,
        "motorized_time": -0.021067655041764506,
        "nonmotorized_time": -0.04394234551517281,
        "vehbywrk_Bike": -2.644433522672152,
        "vehbywrk_SR": -3.0157086560458417,
        "vehbywrk_Transit": -3.9631693279363467,
        "vehbywrk_Walk": -3.3398299003269862,
        "wkcbd_Bike": 0.371887416799123,
        "wkcbd_SR2": 0.37071617423118847,
        "wkcbd_SR3+": 0.22893265840284804,
        "wkcbd_Transit": 1.1056371095671524,
        "wkcbd_Walk": 0.030612758978009455,
        "wkempden_Bike": 0.001542900697956932,
        "wkempden_SR2": 0.00204432338331191,
        "wkempden_SR3+": 0.0035300285386588638,
        "wkempden_Transit": 0.00316015805069698,
        "wkempden_Walk": 0.0037858816800672803,
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
