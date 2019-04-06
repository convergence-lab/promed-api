# PROMED API

Unofficial Python API of [ProMed](https://www.promedmail.org/).

# Cloning

```
git clone https://github.com/convergence-lab/promed-api
```

# Getting Started

```
pip install -r requirements.txt
```

# Running

## Usage
```
python search.py <FROM> <TO> --verbose --output <OUTPUT_FILE>
```


## Example usage:
```
python search.py 04/01/2019 04/02/2019 --verbose --output data.json
```

## File format

```
[
  {
    "id": id,
    "date": MM/DD/YYYY,
    "title": title of the alert,
    "html": raw html data of alert,
    "text": html tag removed text of alert
  },
  ...
]
```
