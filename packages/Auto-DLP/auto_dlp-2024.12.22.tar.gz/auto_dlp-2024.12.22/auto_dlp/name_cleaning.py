import re
import sys
from functools import cache

_n_whitespace_re = re.compile("\s+")

@cache
def regex_for_rule(config, rule):
    for value, repl in config.rule_macros.items():
        rule = rule.replace(value, repl)
    return re.compile(rule, flags=re.IGNORECASE)


def _verbose_clean_name(config, name):
    print(f"Name at start: {name}", file=sys.stderr)

    name = "".join(filter(lambda c: c not in "/!*&\":?#|.,", name))
    name = name.replace("\xc2\xa0", " ")
    print(f"Name after removing illegal chars: {name}", file=sys.stderr)

    for raw_rule in config.name_rules:
        rule = regex_for_rule(config, raw_rule)
        name = rule.sub("", name)
        print(f"Name after regex rule {raw_rule}: {name}", file=sys.stderr)


def clean_name(config, name: str, verbose=False):
    if verbose:
        print(f"Name at start: {name}", file=sys.stderr)

    if name in config.rename:
        if verbose:
            print(f"Name has been force renamed: {name} -> {config.rename[name]}", file=sys.stderr)
        return config.rename[name]

    og_name = name
    name = "".join(filter(lambda c: c not in "/!*&\":?#|.,", name))
    name = name.replace(" ", " ")

    if verbose:
        print(f"Name after removing illegal chars: {name}", file=sys.stderr)

    for rule in config.name_rules:
        rule: re.Pattern = regex_for_rule(config, rule)
        name = rule.sub("", name)
        if verbose:
            print(f"Name after regex rule {rule.pattern}: {name}", file=sys.stderr)

    name = _n_whitespace_re.sub(" ", name)
    name = name.strip()

    if name == "":
        if not verbose:
            clean_name(config, og_name, verbose=True)
        raise ValueError(f"Name is empty after cleaning: {og_name}")

    return name
