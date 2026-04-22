import json
import random

used_variants = {}

def load_level(level_name, variant=None):
    with open(f"levels/{level_name}.json") as f:
        data = json.load(f)

    variants = data["variants"]
    total = len(variants)

    # init if not create
    if level_name not in used_variants:
        used_variants[level_name] = []

    # make it random the variant that not already used
    if variant is None:
        available = [i for i in range(total) if i not in used_variants[level_name]]

        if not available:
            # reset if used all variant already
            used_variants[level_name] = []
            available = list(range(total))

        variant = random.choice(available)
        used_variants[level_name].append(variant)

    return variants[variant], variant, data.get("time_limit", 15)