def example(extract='m', estimate=False):
    import larch

    import larch

    larch.__version__

    d = larch.examples.MTC(format="dataset")
    d

    d = d.sel(caseid=d.femdum == 1)

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

    m.title = "MTC Example 17D, Segmented for females"

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
        "ASC_Bike": -1.0412780932548384,
        "ASC_SR2": -1.5539810652068256,
        "ASC_SR3+": -3.1854305680124058,
        "ASC_Transit": -0.46976829166153894,
        "ASC_Walk": 1.3688704069415694,
        "costbyincome": -0.043530473293242354,
        "hhinc#4": -0.008929802961855733,
        "hhinc#5": -0.03840955269802502,
        "hhinc#6": -0.005082499964774252,
        "motorized_ovtbydist": -0.08879718827392451,
        "motorized_time": -0.01913530894108756,
        "nonmotorized_time": -0.0712577146848601,
        "vehbywrk_Bike": -0.10343275503303231,
        "vehbywrk_SR": -0.6135515751452322,
        "vehbywrk_Transit": -1.1794317963027092,
        "vehbywrk_Walk": -0.917891133747879,
        "wkcbd_Bike": 1.0534091265461347,
        "wkcbd_SR2": 0.45194163205040755,
        "wkcbd_SR3+": 0.3685888989631644,
        "wkcbd_Transit": 1.3811852123386674,
        "wkcbd_Walk": -0.008517015595822975,
        "wkempden_Bike": 0.004039748186460425,
        "wkempden_SR2": 0.0029908432533657533,
        "wkempden_SR3+": 0.005134839725445598,
        "wkempden_Transit": 0.004565945257271104,
        "wkempden_Walk": 0.005465423507422594,
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
