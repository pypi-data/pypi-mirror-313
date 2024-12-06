def example(extract='m', estimate=False):
    import pandas as pd

    import larch as lx
    from larch import P, X

    m = lx.example(1)
    m.title = "MTC Example 30 (Constrained Simple MNL)"
    m.compute_engine = "numba"

    m_explicit = m.copy()

    m_explicit.utility_ca = P.tottime * X.tottime + P.tottime * 3 * X.totcost
    m_explicit.remove_unused_parameters()
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    result_explicit = m_explicit.maximize_loglike(stderr=True)

    from larch.model.constraints import RatioBound

    m.pmaximum = {"totcost": 0, "tottime": 0}

    m.constraints = [
        RatioBound("totcost", "tottime", min_ratio=3.0, max_ratio=999.0, scale=100),
    ]

    result = m.maximize_loglike(stderr=True)

    result

    m.parameter_summary()

    m.ordering = (
        (
            "LOS",
            "totcost",
            "tottime",
        ),
        (
            "ASCs",
            "ASC.*",
        ),
        (
            "Income",
            "hhinc.*",
        ),
    )

    m.parameter_summary()
    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
