# pgwidget

pgwidget is a Python library for easy creation of GUI widgets in pygame environment.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pgwidget.

```bash
pip install pgwidget
```

## Usage

```python
import pgwidget.pgwidget_core as pgw

buttons=pgw.PgWidget()
button1=pgw.Button([800,100],[80,20],"Submit")
buttons.elements.append(button1)

pgwidgets=[buttons]
pgw.main_program_loop(pgwidgets,None)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Currently implemented

* Checkbox
* Radio button
* Button (image)
* Button (classical)
* Table (spreadsheet)
