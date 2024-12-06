SEED_OFFSET = 1021
UPPER_SEED_LIMIT = 2**63 - 1
LOWER_SEED_LIMIT = -(2**63)


def generate_next_random_seed(prev_seed) -> int:
    """Generate next random seed based on previous seed.

    Cycle through the seed range, if the next seed exceeds the upper limit.
    """
    next_seed = prev_seed + SEED_OFFSET
    if next_seed > UPPER_SEED_LIMIT:
        overflow = next_seed - UPPER_SEED_LIMIT
        next_seed = LOWER_SEED_LIMIT + overflow
    return next_seed
