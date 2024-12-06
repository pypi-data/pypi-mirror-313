def example(extract='m', estimate=False):
    import numpy as np
    from pytest import approx

    import larch as lx

    import larch as lx

    varnames = [
        "price",
        "time",
        "conven",
        "comfort",
        "meals",
        "petfr",
        "emipp",
        "nonsig1",
        "nonsig2",
        "nonsig3",
    ]
    d = lx.examples.ARTIFICIAL()
    m = lx.Model(d)
    m.utility_ca = sum(lx.PX(i) for i in varnames)
    m.choice_ca_var = "choice"
    randvars_normal = ["meals", "petfr", "emipp"]

    m.mixtures = [lx.mixtures.Normal(k, f"sd.{k}") for k in randvars_normal]

    m.n_draws = 300
    m.seed = 42
    m.common_draws = True
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    result = m.maximize_loglike(stderr=True)

    m2 = m.copy()
    m2.pvals = "init"
    m2.common_draws = False

    result2 = m2.maximize_loglike(stderr=True)

    m2.parameter_summary()

    from xlogit import MixedLogit

    df = d.to_dataframe().reset_index()
    varnames = [
        "price",
        "time",
        "conven",
        "comfort",
        "meals",
        "petfr",
        "emipp",
        "nonsig1",
        "nonsig2",
        "nonsig3",
    ]
    X = df[varnames].values
    y = df["choice"].values
    randvars = {"meals": "n", "petfr": "n", "emipp": "n"}
    alts = df["alt"]
    ids = df["id"]
    panels = None
    batch_size = 5000
    n_draws = 300

    np.random.seed(0)
    model = MixedLogit()
    model.fit(
        X,
        y,
        varnames,
        alts=alts,
        ids=ids,
        n_draws=n_draws,
        panels=panels,
        verbose=0,
        randvars=randvars,
        batch_size=batch_size,
    )

    model.summary()
    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
