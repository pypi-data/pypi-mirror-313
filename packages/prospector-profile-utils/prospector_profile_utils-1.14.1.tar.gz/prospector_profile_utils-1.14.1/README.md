# Prospector profile utils

It contains some utility Prospector profiles.

## Usage

```bash
pip install prospector-profile-utils
```

Then, in your `.prospector.yaml` file, you can use the profiles like this:

```yaml
inherits:
  - utils:base
  - utils:fix
  - utils:c2cwsgiutils
  - utils:no-design-checks
  - utils:unsafe
```

It probide also an alternate base witch activate less strict checks:

```yaml
inherits:
  - utils:base-less-strict
```

## Contributing

Install the pre-commit hooks:

```bash
pip install pre-commit
pre-commit install --allow-missing-config
```
