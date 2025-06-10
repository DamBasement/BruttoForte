#!/usr/bin/env python3
"""
xpb_bruteforce.py – Scova le versioni “retro” di stack web
dai campi X-Powered-By e Server.

USAGE
  python3 xpb_bruteforce.py -f targets.txt          # da file
  python3 xpb_bruteforce.py -u https://a https://b  # da CLI

Flags extra
  --verbose   Stampa tutti gli header per ogni host
  -t 20       Imposta #thread (default 10)
"""

import argparse
import re
import sys
import urllib3
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# ——————————————————————————————————————————————————————————
# Disattiva l’allarme giallo sui cert self-signed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Firma → regex per estrarre la versione (o vuota se non serve)
SIGS = {
    "PHP":       re.compile(r"PHP/(\d+\.\d+\.\d+)", re.I),
    "ASP.NET":   re.compile(r"ASP\.NET/?(\d+\.\d+)?", re.I),
    ".NET CLR":  re.compile(r"\.NET CLR (\d+\.\d+\.\d+)", re.I),
    "Express":   re.compile(r"Express/?(\d+\.\d+\.\d+)?", re.I),
    "Jetty":     re.compile(r"Jetty/(\d+\.\d+\.\d+)", re.I),
    "IIS":        re.compile(r"Microsoft-IIS/(\d+\.\d+)", re.I),
    "ASP.NET":    re.compile(r"X-AspNet-Version: (\d+\.\d+\.\d+)", re.I),
    ".NET CLR":   re.compile(r"\.NET CLR (\d+\.\d+\.\d+)", re.I),
}

# ——————————————————————————————————————————————————————————
def fetch_header(url, timeout=5, verbose=False):
    """Ritorna stringa tipo 'PHP 5.6.40' o None"""
    try:
        r = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            verify=False,
        )
        if verbose:
            print(f"\n--- {url} headers ---")
            for k, v in r.headers.items():
                print(f"{k}: {v}")

        # Concateno X-Powered-By e Server, così becco più roba
        banner = "\n".join([f"{k}: {v}" for k, v in r.headers.items()])

        for tech, rx in SIGS.items():
            if (m := rx.search(banner)):
                version = m.group(1) or ""      # alcune firme non hanno num versione
                return f"{tech} {version}".strip()

    except requests.RequestException:
        pass
    return None


# ——————————————————————————————————————————————————————————
def parse_args():
    p = argparse.ArgumentParser(description="Bruteforce X-Powered-By & Server headers")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("-f", "--file", help="File con URL (uno per linea)")
    g.add_argument("-u", "--urls", nargs="+", help="URL singoli (spazio-separati)")
    p.add_argument("-t", "--threads", type=int, default=10, help="Thread pool size")
    p.add_argument("--verbose", action="store_true", help="Header full dump")
    return p.parse_args()


# ——————————————————————————————————————————————————————————
def main():
    args = parse_args()

    # — Target list
    if args.file:
        try:
            with open(args.file, encoding="utf-8") as fh:
                targets = [l.strip() for l in fh if l.strip()]
        except IOError as e:
            sys.exit(f"[x] Cannot read {args.file}: {e}")
    else:
        targets = args.urls or []

    if not targets:
        sys.exit("[x] No valid targets supplied.")

    # — Scan
    counter = Counter()
    details = defaultdict(list)

    print(f"[+] Scanning {len(targets)} target(s) with {args.threads} threads…")

    with ThreadPoolExecutor(max_workers=args.threads) as pool:
        futmap = {pool.submit(fetch_header, u, verbose=args.verbose): u for u in targets}
        for fut in as_completed(futmap):
            url = futmap[fut]
            sig = fut.result()
            if sig:
                counter[sig] += 1
                details[sig].append(url)
                print(f"    {url:40} -> {sig}")

    # — Report
    if not counter:
        sys.exit("\n[!] Nessuna firma trovata.")

    print("\n=== Top 5 stack retro ===")
    for sig, n in counter.most_common(5):
        first = details[sig][0]
        extra = " ..." if n > 1 else ""
        print(f"[{n} hit] {sig:<15}  <--  {first}{extra}")

    print("\nDone. Legacy never dies. 💀")


if __name__ == "__main__":
    main()