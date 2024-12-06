# Steuer-ID

> Validates the German Tax-ID (Steuerliche Identifikationsnummer, short: Steuer-ID) using Python.

Based on the [official ELSTER documentation](https://download.elster.de/download/schnittstellen/Pruefung_der_Steuer_und_Steueridentifikatsnummer.pdf) (chapter: 2).

> [!NOTE]
> This package validates solely the syntax and check digit of the provided input. It does not confirm, that the validated Steuer-ID was assigned to a person. Please contact the [Bundeszentralamt für Steuern](https://www.bzst.de/DE/Privatpersonen/SteuerlicheIdentifikationsnummer/steuerlicheidentifikationsnummer_node.html) in case you are unsure about your Steuer-ID.

## Usage

An example of how it can be used:

```python
from steuerid import SteuerIdValidator

validation_result = SteuerIdValidator.validate("02476291358")

print(validation_result) # (True, None) -> the provided input is a valid steuer id

validation_result = SteuerIdValidator.validate("x1234567890")
print(validation_result) # (False, OnlyDigitsAllowedException) -> invalid input, only digits are allowed
```

### Test-Steuer-IDs

Support for test Steuer-IDs (starting with `0`) is enabled by default. Test Steuer-IDs are typically invalid in production. It is recommended to disable them with the following environment variable:

```bash
STEUERID_PRODUCTION=true
```

## Development

For development first clone the repo. It is recommended to create a virtual env
and activate that virtual env. Inside the venv install the dependencies using
`poetry install` command.

### Testing

Execute `pytest` to run the unit tests.

```bash
pytest
```

## Credits

- [Numan Ijaz](NumanIjaz)
- [All Contributors](../../contributors)

## License

The MIT License (MIT). Please see [License File](LICENSE) for more information.
