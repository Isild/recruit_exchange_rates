INITIAL_DATA = {
    'exchange_rates': [
        {
            "eur": 0.916332,
            "usd": 1,
            "jpy": 132.102,
            "gbp": 0.804457,
            "date": "2023-04-09 23:59:59"
        },
        {
            "eur": 0.909546,
            "usd": 1,
            "jpy": 132.155,
            "gbp": 0.805088,
            "date": "2023-04-08 23:59:17"
        },
        {
            "eur": 0.9094,
            "usd": 1,
            "jpy": 132.155,
            "gbp": 0.805088,
            "date": "2023-04-07 23:59:51"
        },
        {
            "eur": 0.915766,
            "usd": 1,
            "jpy": 131.679,
            "gbp": 0.803988,
            "date": "2023-04-06 23:59:59"
        },
        {
            "eur": 0.91717,
            "usd": 1,
            "jpy": 130.938,
            "gbp": 0.802397,
            "date": "2023-04-05 23:59:59"
        },
        {
            "eur": 0.91259,
            "usd": 1,
            "jpy": 131.438,
            "gbp": 0.800044,
            "date": "2023-04-04 23:59:58"
        }
    ]
}


def initialize_table(target, connection, **kw):
    tablename = str(target)
    if tablename in INITIAL_DATA and len(INITIAL_DATA[tablename]) > 0:
        connection.execute(target.insert(), INITIAL_DATA[tablename])
