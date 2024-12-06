def example(extract='m', estimate=False):
    import larch

    larch.__version__

    d = larch.examples.MTC(format="dataset")
    d

    d = d.sel(caseid=d.femdum == 0)

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

    m.title = "MTC Example 17C, Segmented for males"

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
        "ASC_Bike": -1.928007825476385,
        "ASC_SR2": -1.912455790177904,
        "ASC_SR3+": -3.5514203840398006,
        "ASC_Transit": -0.8658094170164065,
        "ASC_Walk": -1.2203008866494844,
        "costbyincome": -0.06390233682221723,
        "hhinc#4": -0.0020804355665526397,
        "hhinc#5": -0.0013784543619515673,
        "hhinc#6": -0.00501951838450115,
        "motorized_ovtbydist": -0.18639734021256957,
        "motorized_time": -0.01951022691589421,
        "nonmotorized_time": -0.024446076816243063,
        "vehbywrk_Bike": -0.9930978890574966,
        "vehbywrk_SR": -0.20981196496890442,
        "vehbywrk_Transit": -0.8322463141471179,
        "vehbywrk_Walk": -0.6105805888289391,
        "wkcbd_Bike": 0.3204533731833982,
        "wkcbd_SR2": 0.027661592161988033,
        "wkcbd_SR3+": 1.423466120894847,
        "wkcbd_Transit": 1.196921606447681,
        "wkcbd_Walk": 0.22281387280820592,
        "wkempden_Bike": 0.0004958705725495997,
        "wkempden_SR2": 0.0009305263934769419,
        "wkempden_SR3+": 0.0005787415453590467,
        "wkempden_Transit": 0.002487830750207477,
        "wkempden_Walk": 0.0012923574145590863,
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
