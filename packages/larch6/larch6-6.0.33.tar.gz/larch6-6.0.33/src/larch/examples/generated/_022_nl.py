def example(extract='m', estimate=False):
    import larch as lx

    lx.__version__

    m = lx.example(17)
    m.compute_engine = "numba"

    motorized = m.graph.new_node(
        parameter="mu_motor", children=[1, 2, 3, 4], name="Motorized"
    )
    nonmotorized = m.graph.new_node(
        parameter="mu_nonmotor", children=[5, 6], name="Nonmotorized"
    )

    m.ordering = (
        (
            "CostbyInc",
            "costbyincome",
        ),
        (
            "TravelTime",
            ".*time.*",
            ".*dist.*",
        ),
        (
            "Household",
            "hhinc.*",
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

    m.graph

    mj = m.copy()
    mj.compute_engine = "jax"
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    result = m.maximize_loglike(method="bhhh")

    m.calculate_parameter_covariance()
    m.parameter_summary()

    resultj = mj.maximize_loglike(stderr=True)
    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
