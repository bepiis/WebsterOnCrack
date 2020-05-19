#!/usr/bin/env python
# coding=utf-8

import argparse as arg
import itertools
import math as m
import time

import tqdm
from random import choice


def arg_parse():
    parser = arg.ArgumentParser(description="A dictionary creation tool")
    parser.add_argument(
        "-l",
        "--list",
        nargs="*",
        type=str,
        help="input a list of keywords",
        required=True
    )

    parser.add_argument(
        "-max",
        "--max",
        type=int,
        dest="max",
        help="specify maximum password length (defaults to 8)"
    )

    parser.add_argument(
        "-min",
        "--min",
        type=int,
        dest="min",
        help="specify minimum password length (defaults to 6)"
    )

    parser.add_argument(
        "-w",
        "--write",
        dest="write",
        type=str,
        help="pass output to a file"
    )

    parser.add_argument(
        "-rc",
        "--random-case",
        dest="case",
        action='store_true',
        help="Add random capitals"
    )
    parser.set_defaults(
        case=False,
        min=6,
        max=8
    )

    return parser.parse_args()


def parse_args():
    args = arg_parse()
    root_list = args.list
    if args.write:
        calc_and_write(root_list, args.min, args.max, args.write, args.case)


def add_case(word_list):
    return [str(idx).capitalize() for idx in word_list]


def calc_and_write(lst, min_len, max_len, path, case_dup):
    with open(path, "w") as file:
        total = npr(len(lst), len(lst))
        start = time.time()
        with tqdm.tqdm(total=total, desc="[*]") as pbar:
            for j in reversed(range(len(lst))):
                for p in itertools.permutations(lst, j):
                    if min_len <= len(''.join(p)) <= max_len:
                        if case_dup:
                            file.write(str(''.join(rand_case(p)) + "\n"))
                        file.write(str(''.join(p) + "\n"))
                    pbar.update(1.56)
            pbar.close()
            file.close()
        elapsed = int(time.time() - start)
        t = "minutes"
        if elapsed < 60:
            t = "seconds:"
        print("[*] Yielded {} permutations in {} {}".format(int(total), elapsed, t))


def print_perms(gen):
    [print(line + "\n") for line in gen]


def rand_case(tup):
    return [choice((str.capitalize(idx[0]), str(idx)[0])) + idx[1:] for idx in tup]


def npr(n, r):
    s = 0
    while r > 0:
        s += m.factorial(n) / m.factorial(n - r)
        r -= 1
    return s

parse_args()
