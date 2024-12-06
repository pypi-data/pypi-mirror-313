def example(extract='m', estimate=False):
    import larch

    larch.__version__

    d = larch.examples.MTC(format="dataset")
    d

    m = larch.Model(d, compute_engine="numba")

    from larch import P, X

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
        +P("nonmotorized_time") * X("(altid> 4) * tottime")
        + P("motorized_time") * X("(altid <= 4) * ivtt")
        + (P("motorized_time") + (P("motorized_ovtbydist") / X("dist")))
        * X("(altid <= 4) * ovtt")
        + P("costbyinc") * X("totcost/hhinc")
    )

    m.availability_ca_var = "avail"
    m.choice_ca_var = "chose"

    m.title = "MTC Example 16, Cost by Income"

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
        "ASC_Bike": -1.6217774612007492,
        "ASC_SR2": -1.7297986582095874,
        "ASC_SR3+": -3.6562561506975255,
        "ASC_Transit": -0.6917042404795228,
        "ASC_Walk": 0.07521549340170937,
        "costbyinc": -0.05177365897066612,
        "hhinc#2,3": 3.691866127922073e-05,
        "hhinc#4": -0.005335573957018,
        "hhinc#5": -0.008671987053899464,
        "hhinc#6": -0.006017166395409271,
        "motorized_ovtbydist": -0.13272166895031992,
        "motorized_time": -0.0201578217327816,
        "nonmotorized_time": -0.045438649548417406,
        "vehbywrk_Bike": -0.7040646431527947,
        "vehbywrk_SR2": -0.38161738059345535,
        "vehbywrk_SR3+": -0.13880487622153995,
        "vehbywrk_Transit": -0.937505306213354,
        "vehbywrk_Walk": -0.72385335687274,
        "wkcbd_Bike": 0.4863239419169535,
        "wkcbd_SR2": 0.24714212608546096,
        "wkcbd_SR3+": 1.0943587942374322,
        "wkcbd_Transit": 1.3056155684640574,
        "wkcbd_Walk": 0.09724802958992065,
        "wkempden_Bike": 0.0019224683185795574,
        "wkempden_SR2": 0.0015964358018843575,
        "wkempden_SR3+": 0.0022037880176673103,
        "wkempden_Transit": 0.0031316557035939658,
        "wkempden_Walk": 0.002881429335761498,
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
