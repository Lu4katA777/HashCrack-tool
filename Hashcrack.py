#!/usr/bin/env python3

import hashlib
import argparse
import sys
import time
from pathlib import Path
from colorama import Fore, init

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

# ===== MUTATIONS =====
def generate_mutations(word):
    variations = set()
    base = word.strip()

    variations.add(base)
    variations.add(base.lower())
    variations.add(base.upper())
    variations.add(base.capitalize())

    # case mix per letter
    for i in range(len(base)):
        variations.add(base[:i] + base[i].upper() + base[i+1:])
        variations.add(base[:i] + base[i].lower() + base[i+1:])

    nums = ["123","1234","12345","123456"]

    for v in list(variations):
        for n in nums:
            variations.add(v+n)

    # leet
    leet = base.replace("a","@").replace("i","1").replace("o","0")
    variations.add(leet+"123456")

    return variations


    variations.add(base)
    variations.add(base.lower())
    variations.add(base.upper())
    variations.add(base.capitalize())
    variations.add(base.swapcase())

    nums = ["123","1234","12345","123456","2024","2025","2026"]

    for v in list(variations):
        for n in nums:
            variations.add(v+n)

    # leet
    leet = base.replace("a","@").replace("i","1").replace("o","0")
    variations.add(leet)
    variations.add(leet+"123")
    variations.add(leet+"123456")

    # symbols
    variations.add(base+"!")
    variations.add(base+"@")

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
