#!/usr/bin/env python3

import hashlib
import argparse
import sys
import time
from pathlib import Path
from colorama import Fore, init
import itertools

init(autoreset=True)

# ===== Banner =====
def banner():
    print(Fore.CYAN + r"""
██╗  ██╗ █████╗ ███████╗██╗  ██╗
██║  ██║██╔══██╗██╔════╝██║  ██║
███████║███████║███████╗███████║
██╔══██║██╔══██║╚════██║██╔══██║
██║  ██║██║  ██║███████║██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
HashCrack Lab Tool
""")

# ===== Warning =====
def warning_prompt():
    print(Fore.RED + "\n[!] Educational use only\n")
    if input("Continue? [y/n]: ").lower() != "y":
        sys.exit()

# ===== EXTRA GENERATORS =====

def interleave_numbers(word):
    results = set()
    nums = "1234567890"

    combo = ""
    for i, ch in enumerate(word):
        combo += ch
        if i < len(nums):
            combo += nums[i]
    results.add(combo)

    return results


def random_case_variants(word, limit=200):
    results = set()
    combos = itertools.product(*[(c.lower(), c.upper()) for c in word])

    for i, combo in enumerate(combos):
        if i > limit:
            break
        results.add("".join(combo))

    return results


def insert_symbol_number(word):
    results = set()
    symbols = ["#", "@", "!", "$"]

    for i in range(len(word)):
        for sym in symbols:
            for n in ["1","12","123","1234"]:
                results.add(word[:i] + sym + word[i:] + n)

    return results


# ===== MUTATIONS =====
def generate_mutations(word):
    variations = set()

    numbers = ["1","12","123","1234","885","000","133","12345"]
    symbols = ["#", "@", "!", "$"]

    # base forms
    base_forms = {
        word,
        word.lower(),
        word.upper(),
        word.capitalize(),
        word.swapcase(),
    }

    # mixed case variants
    mixed_variants = set()
    for combo in itertools.product(*[(c.lower(), c.upper()) for c in word]):
        mixed_variants.add("".join(combo))
        if len(mixed_variants) > 200:  # limit
            break

    base_forms.update(mixed_variants)

    for base in base_forms:
        variations.add(base)

        # numbers at end
        for n in numbers:
            variations.add(base + n)

        # symbol anywhere + numbers
        for sym in symbols:
            for i in range(1, len(base)):
                mid = base[:i] + sym + base[i:]
                variations.add(mid)

                for n in numbers:
                    variations.add(mid + n)

    # interleave
    nums = "1234567890"
    combo = ""
    for i, ch in enumerate(word):
        combo += ch
        if i < len(nums):
            combo += nums[i]
    variations.add(combo)

    return variations


# ===== HASH =====
def make_hash(text, algo):
    h = hashlib.new(algo)
    h.update(text.encode())
    return h.hexdigest()

# ===== CRACK =====
def crack_hash(target_hash, wordlist, algo):
    path = Path(wordlist)

    if not path.exists():
        print("Wordlist not found")
        sys.exit()

    print(Fore.CYAN + "\n[*] Cracking...\n")

    start = time.time()
    attempts = 0

    with open(path,"r",errors="ignore") as f:
        for word in f:
            word = word.strip()
            mutations = generate_mutations(word)

            for variant in mutations:
                attempts += 1

                if make_hash(variant, algo) == target_hash:
                    speed = int(attempts/(time.time()-start+0.001))

                    print(Fore.GREEN + f"\n[+] FOUND: {variant}")
                    print(Fore.YELLOW + f"[+] Base: {word}")
                    print(Fore.CYAN + f"[+] Attempts: {attempts}")
                    print(Fore.MAGENTA + f"[+] Speed: {speed}/s")

                    with open("found.txt","a") as out:
                        out.write(f"{variant} | {target_hash}\n")

                    print(Fore.GREEN + "[+] Saved to found.txt\n")
                    return

                if attempts % 5000 == 0:
                    speed = int(attempts/(time.time()-start+0.001))
                    print(Fore.MAGENTA + f"Checked: {attempts} | {speed}/s")

    print(Fore.RED + "\n[-] Hash not found")

# ===== GENERATE =====
def generate_hash(text, algo):
    print(Fore.GREEN + f"\nHash: {make_hash(text, algo)}\n")

# ===== CLI =====
def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    g = sub.add_parser("generate")
    g.add_argument("-t","--text", required=True)
    g.add_argument("-a","--algo", default="md5")

    c = sub.add_parser("crack")
    c.add_argument("-hsh","--hash", required=True)
    c.add_argument("-w","--wordlist", required=True)
    c.add_argument("-a","--algo", default="md5")

    args = parser.parse_args()
    banner()

    if args.cmd == "generate":
        warning_prompt()
        generate_hash(args.text, args.algo)

    elif args.cmd == "crack":
        warning_prompt()
        crack_hash(args.hash, args.wordlist, args.algo)

if __name__ == "__main__":
    main()
