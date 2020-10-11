# Generation

Here we use json to show the inner data structure each Python class represent.

## Concepts

### Scenerio

@TODO

### Combo

Combo is a part of a scenerio. E.g.

```json
{
  "combo": {
    "age": "27",
    "health": "moderate health problems",
    "gender": "female",
    "income level": "low",
    "education level": "Graduate degree",
    "number of dependents": "4",
    "survival without jacket": "27%",
    "survival with jacket": "77%"
  }
}
```

However, it could be in partial mode where need to be expand to complete type. The number refer to the index of the catagories. The partial mode example:

```json
{
  "combo": {
    "age": 0,
    "health": 0,
    "gender": 0,
    "income level": 0,
    "education level": 0,
    "number of dependents": 0,
    "survival without jacket": 0,
    "survival with jacket": 0
  }
}
```

### Catagory

Catagories stores index of each options, it might look like this:

```json
{
  "age": {
    "0": "5",
    "1": "8",
    "2": "12",
    "3": "18",
    "4": "21",
    "5": "23",
    "6": "27",
    "7": "32",
    "8": "52",
    "9": "61",
    "10": "72"
  }
}
```

The key should always be integer. However, the sqeuence of the number could be random or even incontineous. Integers allow us to use set operation efficiently eliminate bad combos, etc.

## Rule

Rule is used to shape generation with custom rules

## Steps

<!--There is some issue with combo definition.-->

## Demo

```bash
python3 cli.py rule/rule.yaml
```

it will generate `rule.json` at the directory
