# pgwidget

pgwidget is a Python library for easy creation of GUI widgets in pygame environment (+web engine experimental).

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

In examples folder you can get several GUI elements.
## Examples of UIs possible to create with pgwidget
Project Forloop.ai
![obrazek](https://github.com/DovaX/pgwidget/assets/29150831/789131c7-8789-4e09-841c-79250c209dc2)
![obrazek](https://github.com/DovaX/pgwidget/assets/29150831/6d7a9239-a31f-44c6-b1d9-caa56a21f55e)
Older example
![alt text](https://github.com/dovax/pgwidget/blob/main/example1.png?raw=true)

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
