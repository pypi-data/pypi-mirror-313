def example(extract='m', estimate=False):
    import larch as lx

    lx.__version__

    d = lx.examples.MTC(format="dataset")
    d

    m = lx.Model(d, compute_engine="numba")

    from larch import PX, P, X

    for a in [2, 3]:
        m.utility_co[a] = +P("hhinc#2,3") * X("hhinc") + P(f"numveh#{a}") * X("numveh")

    for a in [4, 5, 6]:
        m.utility_co[a] = +P(f"hhinc#{a}") * X("hhinc") + P(f"numveh#{a}") * X("numveh")

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

    m.title = "MTC Example 10, Autos per Household"

    m.choice_avail_summary()

    m.set_cap(20)

    # TEST
    assert m.compute_engine == "numba"
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    result = m.maximize_loglike(stderr=True, method="bhhh")

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
        ("Ownership", "numveh.*"),
        (
            "ASCs",
            "ASC.*",
        ),
    )

    m.parameter_summary()

    m.estimation_statistics()

    # TEST
    from pytest import approx

    assert result.loglike == approx(-3501.6427674451616)
    revealed_x = dict(zip(m.pnames, result.x))
    expected_x = {
        "ASC_Bike": -2.220318494507017,
        "ASC_SR2": -2.0539566005386884,
        "ASC_SR3+": -3.643068905518874,
        "ASC_Transit": 0.5738157734892145,
        "ASC_Walk": -0.4403348747865274,
        "hhinc#2,3": -0.001955401039169736,
        "hhinc#4": -0.0013233467107319043,
        "hhinc#5": -0.009513056978703192,
        "hhinc#6": -0.004156633998143166,
        "motorized_ovtbydist": -0.17850538190676227,
        "motorized_time": -0.03782098120360213,
        "nonmotorized_time": -0.047506740267090244,
        "numveh#2": -0.035252140629887845,
        "numveh#3": 0.07226723634772537,
        "numveh#4": -0.5544590047253285,
        "numveh#5": -0.22920682058782335,
        "numveh#6": -0.36557711952920985,
        "totcost": -0.004059016748597727,
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
