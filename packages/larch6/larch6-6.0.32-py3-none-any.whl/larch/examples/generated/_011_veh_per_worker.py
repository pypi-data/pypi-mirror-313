def example(extract='m', estimate=False):
    import larch

    larch.__version__

    d = larch.examples.MTC(format="dataset")
    d

    m = larch.Model(d, compute_engine="numba")

    from larch import PX, P, X

    for a in [2, 3]:
        m.utility_co[a] = +P("hhinc#2,3") * X("hhinc") + P(f"vehbywrk#{a}") * X("vehbywrk")

    for a in [4, 5, 6]:
        m.utility_co[a] = +P(f"hhinc#{a}") * X("hhinc") + P(f"vehbywrk#{a}") * X("vehbywrk")

    d.dc.alts_mapping

    for a, name in d.dc.alts_mapping.items():
        if a == 1:
            continue
        m.utility_co[a] += P("ASC_" + name)

    m.utility_ca = (
        +PX("totcost")
        + P("motorized_time") * X("(altid <= 4) * tottime")
        + P("nonmotorized_time") * X("(altid > 4) * tottime")
        + P("motorized_ovtbydist") * X("(altid <= 4) * ovtt/dist")
    )

    m.availability_ca_var = "avail"
    m.choice_ca_var = "chose"

    m.title = "MTC Example 11, Vehicle by Worker"

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
        "ASC_Bike": -1.8312948675848564,
        "ASC_SR2": -1.5938047044131862,
        "ASC_SR3+": -3.1403150395708557,
        "ASC_Transit": 0.9264355074748487,
        "ASC_Walk": -0.23791815713833725,
        "hhinc#2,3": -0.0016737691797456366,
        "hhinc#4": -0.005978922878394666,
        "hhinc#5": -0.011599742186799886,
        "hhinc#6": -0.007958683075229829,
        "motorized_ovtbydist": -0.18138343284593078,
        "motorized_time": -0.038408722097899604,
        "nonmotorized_time": -0.047008767061813846,
        "totcost": -0.004229789226989649,
        "vehbywrk#2": -0.43307980337078766,
        "vehbywrk#3": -0.26653390681741285,
        "vehbywrk#4": -0.9899350231601534,
        "vehbywrk#5": -0.6728100342263964,
        "vehbywrk#6": -0.6283434464699432,
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
