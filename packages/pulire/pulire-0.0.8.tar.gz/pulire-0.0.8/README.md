# Pulire

A lightweight DataFrame validation library for [Pandas](https://pandas.pydata.org/).

## Auto Formatting

```sh
poetry run black .
```

## Testing

Run the following command for unit tests:

```sh
poetry run pytest tests
```

## Schema

Pulire requires a `Schema` which describes all columns in a given `DataFrame`.

```py
from pulire import Schema, Column, validators, formatters

Schema([
    Column("temp", "Float64", [
        validators.minimum(-80),
        validators.maximum(65),
        formatters.decimals(1)
    ])
])
```

## Validate

Pulire automatically removes values which fail the validation. Let's use the `meteostat` library to get some data:

```py
from datetime import datetime
from meteostat import Hourly

df = Hourly("10637", datetime(2018, 1, 1), datetime(2018, 1, 1, 23, 59)).fetch()

print(df)
```

Now, we can get a valid copy of our Meteostat `DataFrame` by running our schema's `validate` method:

```py
df = myschema.validate(df)
```

### Lazy Validations

```py
try:
    schema.validate(df, lazy=True)
except ValueError as error:
    print(error.args[0])
```