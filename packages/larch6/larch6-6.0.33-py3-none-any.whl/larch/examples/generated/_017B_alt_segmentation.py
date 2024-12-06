def example(extract='m', estimate=False):
    import larch

    larch.__version__

    d = larch.examples.MTC(format="dataset")
    d

    d = d.sel(caseid=d.numveh >= 2)

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

    m.title = "MTC Example 17B, Segmented for 2 or more cars"

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

    revealed_x

    # TEST
    from pytest import approx

    expected_x = {
        "ASC_Bike": -3.131353684453019,
        "ASC_SR2": -1.982918109708732,
        "ASC_SR3+": -3.7260108180838087,
        "ASC_Transit": -2.156692021346743,
        "ASC_Walk": -1.5835989189276731,
        "costbyincome": -0.0978607170004987,
        "hhinc#4": 0.0003613865368074286,
        "hhinc#5": -0.002650844116790726,
        "hhinc#6": 0.0009101590517897486,
        "motorized_ovtbydist": -0.1937603871636971,
        "motorized_time": -0.018754569843429904,
        "nonmotorized_time": -0.045210350568177106,
        "vehbywrk_Bike": -0.21719450776227095,
        "vehbywrk_SR": -0.23823848663321495,
        "vehbywrk_Transit": -0.23619743325813528,
        "vehbywrk_Walk": -0.07998140457786423,
        "wkcbd_Bike": 0.5651962301019509,
        "wkcbd_SR2": 0.16357641468531287,
        "wkcbd_SR3+": 1.3328985605250347,
        "wkcbd_Transit": 1.2613977817336346,
        "wkcbd_Walk": 0.21594406473797045,
        "wkempden_Bike": 0.0014358656965858384,
        "wkempden_SR2": 0.0010739771398805848,
        "wkempden_SR3+": 0.0013450278303126933,
        "wkempden_Transit": 0.0028932086005130325,
        "wkempden_Walk": -0.0010607308832536778,
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
