#!/usr/bin/env python3
"""Calculate conservative workload limits to help prevent overload crashes."""

import argparse
import json
import math


K_MAX = 4096
B_MAX = 64
C_MAX = 2048
L_REF = 2048
A_0 = 500.0
A_0_GRAIN = 0.5


def get_buffer_window(current_scale: int) -> int:
    """Return the maximum amount of work kept in memory at once."""
    if current_scale <= 1:
        return 1
    ratio = (1 + math.log(L_REF)) / (1 + math.log(current_scale))
    return max(1, min(K_MAX, math.floor(K_MAX * ratio)))


def get_capacity_limit(current_scale: int) -> int:
    """Return the recommended maximum number of parallel tasks."""
    if current_scale <= 1:
        return B_MAX
    area_norm = math.sqrt(math.pi) / math.sqrt(math.log(current_scale) + A_0)
    return max(1, math.floor(B_MAX * area_norm))


def get_task_granularity(current_scale: int) -> int:
    """Return the recommended size for each small piece of work."""
    if current_scale <= 2:
        return C_MAX

    ln_scale = math.log(current_scale)
    alpha = (1.0 / ln_scale) + (A_0_GRAIN / (ln_scale**2))
    chunk = math.ceil(C_MAX * alpha)
    return max(1, min(C_MAX, chunk))


def get_recommendation(current_scale: int) -> dict[str, int]:
    """Return all three limits for a workload scale."""
    if (
        isinstance(current_scale, bool)
        or not isinstance(current_scale, int)
        or current_scale < 1
    ):
        raise ValueError("workload scale must be a whole number of 1 or greater")

    return {
        "buffer_window": get_buffer_window(current_scale),
        "parallel_tasks": get_capacity_limit(current_scale),
        "task_size": get_task_granularity(current_scale),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate safer work limits for a computer under load."
    )
    parser.add_argument(
        "scale",
        type=int,
        help="estimated workload size, as a whole number of 1 or greater",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the result in a format other programs can read",
    )
    args = parser.parse_args()
    try:
        recommendation = get_recommendation(args.scale)
    except (ValueError, OverflowError) as error:
        parser.error(str(error))

    if args.json:
        print(json.dumps(recommendation, indent=2))
        return

    print(f"Recommended limits for workload scale {args.scale}:")
    print(f"  Keep at most {recommendation['buffer_window']} items waiting")
    print(f"  Run at most {recommendation['parallel_tasks']} tasks at once")
    print(f"  Process work in groups of {recommendation['task_size']}")


if __name__ == "__main__":
    main()