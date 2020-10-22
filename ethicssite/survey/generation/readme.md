# Generation

Here we use json/yaml to show the inner data structure each Python class represent.

## Concepts

### Scenerio

Each scenario is composed of n number of combinations. Using `Generator.get_scenario(n)` will return a randomly generated scneario that follows the default rules

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

```yaml
categories:
  age:
    0: "5"
    1: "8"
    2: "12"
    3: "18"
    4: "21"
    5: "23"
    6: "27"
    7: "32"
    8: "52"
    9: "61"
    10: "72"
```

The key should always be integer. However, the sqeuence of the number could be random or even incontineous. Integers allow us to use set operation efficiently eliminate bad combos, etc.

The category may have a special operator key instead of regular indexes. Currently implemented is `[range]`, which generates all the numbers between the first and second index of the following list.

## Rule

Rule is used to shape generation with custom rules (also referred to as bad combos in the json file). A rules object may looks like this:

```yaml
bad_combos:
  age:
    1:
      number of dependents:
        - 1
        - 2
        - 3
        - 4
        - 5
    2:
      income level:
        - 2
      number of dependents:
        - 1
        - 2
        - 3
        - 4
        - 5
    3:
      income level:
        - 2
      number of dependents:
        - 4
        - 5
    5:
      number of dependents:
        - 4
        - 5
    9:
      number of dependents:
        - 4
        - 5
    10:
      number of dependents:
        - 3
        - 4
        - 5
```

`bad_combos` **MUST** follow the same squeuence where catalogies listed.

> For instance, the root node of this rule is `age`, which means the first feature in `categories` must be `age`. The inner sequence should also do the same, if necessary.

## Steps

- After being initiated with the rules, the generator then can be called by using 'get_scenario()', one at the time
- Each combination is then generated separately. At each step, the Catgory object will return a value chosen only from the valid pool of values to choose from.
- Once all the options are generated, the generator once more checks them to ensure the number of duplicates. If the requirements are met, the scenario is returned.

## Demo

```bash
python3 cli.py rule/rule.yaml
```

it will generate `rule.json` at the directory
