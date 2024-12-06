def example(extract='m', estimate=False):
    import numpy as np

    import larch as lx
    from larch import P, X

    hh, pp, tour, skims = lx.example(200, ["hh", "pp", "tour", "skims"])

    from addicty import Dict

    Mode = Dict(
        DA=1,
        SR=2,
        Walk=3,
        Bike=4,
        Transit=5,
    ).freeze()

    tour_dataset = lx.Dataset.construct.from_idco(tour.set_index("TOURID"), alts=Mode)

    od_skims = lx.Dataset.construct.from_omx(skims)

    dt = lx.DataTree(
        tour=tour_dataset,
        hh=hh.set_index("HHID"),
        person=pp.set_index("PERSONID"),
        od=od_skims,
        do=od_skims,
        relationships=(
            "tours.HHID @ hh.HHID",
            "tours.PERSONID @ person.PERSONID",
            "hh.HOMETAZ @ od.otaz",
            "tours.DTAZ @ od.dtaz",
            "hh.HOMETAZ @ do.dtaz",
            "tours.DTAZ @ do.otaz",
        ),
    )

    dt_work = dt.query_cases("TOURPURP == 1")
    dt_work.n_cases

    dt_work_low_income = dt.query_cases("TOURPURP == 1 and INCOME < 30000")
    dt_work_low_income.n_cases

    m = lx.Model(datatree=dt_work)
    m.title = "Exampville Work Tour Mode Choice v1"

    m.utility_co[Mode.DA] = (
        +P.InVehTime * X.AUTO_TIME + P.Cost * X.AUTO_COST  # dollars per mile
    )

    m.utility_co[Mode.SR] = (
        +P.ASC_SR
        + P.InVehTime * X.AUTO_TIME
        + P.Cost * (X.AUTO_COST * 0.5)  # dollars per mile, half share
        + P("LogIncome:SR") * X("log(INCOME)")
    )

    m.utility_co[Mode.Walk] = (
        +P.ASC_Walk + P.NonMotorTime * X.WALK_TIME + P("LogIncome:Walk") * X("log(INCOME)")
    )

    m.utility_co[Mode.Bike] = (
        +P.ASC_Bike + P.NonMotorTime * X.BIKE_TIME + P("LogIncome:Bike") * X("log(INCOME)")
    )

    m.utility_co[Mode.Transit] = (
        +P.ASC_Transit
        + P.InVehTime * X.TRANSIT_IVTT
        + P.OutVehTime * X.TRANSIT_OVTT
        + P.Cost * X.TRANSIT_FARE
        + P("LogIncome:Transit") * X("log(INCOME)")
    )

    Car = m.graph.new_node(parameter="Mu:Car", children=[Mode.DA, Mode.SR], name="Car")
    NonMotor = m.graph.new_node(
        parameter="Mu:NonMotor", children=[Mode.Walk, Mode.Bike], name="NonMotor"
    )
    Motor = m.graph.new_node(
        parameter="Mu:Motor", children=[Car, Mode.Transit], name="Motor"
    )

    m.graph

    m.choice_co_code = "TOURMODE"

    m.availability_co_vars = {
        Mode.DA: "AGE >= 16",
        Mode.SR: 1,
        Mode.Walk: "WALK_TIME < 60",
        Mode.Bike: "BIKE_TIME < 60",
        Mode.Transit: "TRANSIT_FARE>0",
    }

    m.choice_avail_summary()

    m.compute_engine = "numba"

    # TEST
    # testing the JAX engine
    mj = m.copy()
    mj.compute_engine = "jax"
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    result = m.maximize_loglike(method="bhhh")

    m.calculate_parameter_covariance();

    m.parameter_summary()

    m.estimation_statistics()

    # TEST
    # testing the JAX engine
    mj.set_cap(20)

    # TEST
    # testing the JAX engine
    resultj = mj.maximize_loglike(stderr=False)

    report = lx.Reporter(title=m.title)

    report.append("# Parameter Summary")
    report.append(m.parameter_summary())
    report

    report << "# Estimation Statistics" << m.estimation_statistics()

    report << "# Utility Functions" << m.utility_functions()

    report.save(
        "exampville_mode_choice.html",
        overwrite=True,
        metadata=m.dumps(),
    )
    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
