# HashCrackBG 🔐

Educational hash cracking tool made in Bulgaria 🇧🇬  
Built for learning, lab testing and fun.

⚠️ This project is for **educational purposes only**.  
Do NOT use it for illegal activities.

---

## Features

- Hash generator (MD5, SHA1, SHA256 etc.)
- Wordlist cracking
- Smart mutations:
  - case variations
  - numbers (123456, 2025 etc.)
  - symbols (! @ #)
  - leet (@ 1 0)
- Speed display (hashes/sec)
- Progress stats
- Auto‑save found passwords → `found.txt`
- Color hacker‑style terminal UI

---

## Installation

Clone the repo:

```bash
git clone https://github.com/YOUR_USERNAME/HashCrackBG.git
cd HashCrackBG
```

Install dependency:

```bash
pip3 install colorama
```

---

## Usage

### Generate hash

```bash
python3 HashCrackBG.py generate -t password123 -a md5
```

### Crack hash

```bash
python3 HashCrackBG.py crack -hsh HASH -w wordlist.txt -a md5
```

Example:

```bash
python3 HashCrackBG.py crack -hsh 249184d5a8efb213886762d1cc915253 -w wordlist.txt
```

---

## Wordlist

Put base words inside:

```
wordlist.txt
```

Example:

```
admin
root
password
linux
```

The tool will generate smart variations automatically.

---

## Output

If a password is found:

```
FOUND: admiN123456
Base: admin
Speed: 52000/s
```

Also saved to:

```
found.txt
```

---

## Legal Notice

This tool is made for:
- cybersecurity learning
- CTF practice
- lab environments

The author is not responsible for misuse.
