def example(extract='m', estimate=False):
    import pandas as pd

    import larch as lx
    from larch.util.namespaces import Namespace

    spec_content = """expression,DA,SR,Walk,Bike,Transit
    AUTO_TIME,InVehTime,InVehTime,,,
    AUTO_COST,Cost,,,,
    AUTO_COST*0.5,,Cost,,,
    1,,ASC_SR,ASC_Walk,ASC_Bike,ASC_Transit
    log(INCOME),,LogIncome_SR,LogIncome_Walk,LogIncome_Bike,LogIncome_Transit
    WALK_TIME,,,NonMotorTime,,
    BIKE_TIME,,,,NonMotorTime,
    TRANSIT_IVTT,,,,,InVehTime
    TRANSIT_OVTT,,,,,OutVehTime
    TRANSIT_FARE,,,,,Cost
    """

    from io import StringIO

    spec = pd.read_csv(StringIO(spec_content)).set_index("expression")
    spec

    hh, pp, tour, skims = lx.example(200, ["hh", "pp", "tour", "skims"])

    Mode = Namespace(
        DA=1,
        SR=2,
        Walk=3,
        Bike=4,
        Transit=5,
    )

    # tour_dataset = lx.Dataset.construct.from_idco(tour.set_index('TOURID'), alts=Mode)

    tour_dataset = tour.set_index("TOURID")
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
        root_node_name="tour",
    )

    spec.columns

    dt.set_altnames(spec.columns)

    dt.alts_name_to_id()

    import larch.model.from_spec

    m = lx.Model.from_spec(spec, dt)

    m.choice_co_code = "TOURMODE"

    m.should_preload_data()
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    m.maximize_loglike()

    dt.n_cases

    m.logsums()

    m.pvals = {"Cost": -0.1, "InVehTime": -0.2, "ASC_Bike": 2.0}

    m.pf


    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
