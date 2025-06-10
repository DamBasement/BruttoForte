# BruttoForte

“There are two kinds of servers: those already hacked and those still leaking X-Powered-By.”
— some jaded pentester

# 🕵️‍♂️ CheckerBruttoForte  
_A tiny banner-grabber that digs through **X-Powered-By** and **Server** headers to spot “vintage” web stacks (aka low-hanging fruit)._  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/status-hack_in_progress-ff69b4)

---

## TL;DR
1. **Feed** it a list of internal URLs.  
2. **It fires** multithreaded HTTP/HTTPS requests.  
3. **Extracts** banners like `PHP/5.6.40`, `Microsoft-IIS/8.5`, `.NET CLR 3.5.30729`, `Express/4.17.3` …  
4. **Prints** the Top-5 most common versions (old stuff instantly pops).  
5. **Profit** – pick the rustiest target and move on to shell-exploiting.

---

## Why bother?
- _Legacy never dies_ – ancient stacks survive every Patch Tuesday.  
- Lightning-fast fingerprinting **before** you unleash loud tools (Nikto, Nessus, Burp Intruder…).  
- Perfect for a **coffee-break recon**: scans dozens of hosts in seconds.

---

## Requirements
```bash
pip install -r requirements.txt   # only: requests

# 1 – create targets.txt
cat > targets.txt <<EOF
https://intranet.lan
http://legacy.portal
https://hub.leonardo.com
EOF

# 2 – basic run (10 threads)
python3 xpb_bruteforce.py -f targets.txt

# 3 – verbose run + more threads
python3 xpb_bruteforce.py -f targets.txt -t 30 --verbose

[+] Scanning 3 target(s) with 30 threads…
    https://hub.leonardo.com         -> IIS 8.5
    https://intranet.lan            -> PHP 5.6.40
    http://legacy.portal            -> ASP.NET 4.0.30319

=== Top 5 retro stacks ===
[2 hit] IIS 8.5           <--  https://hub.leonardo.com ...
[1 hit] PHP 5.6.40        <--  https://intranet.lan

Done. Legacy never dies. 💀

## TODO
CSV / JSON output for CI pipelines.
Load regex signatures from YAML.
“Noisy” mode with directory brute (/phpinfo.php, /server-status, …).
Award badge if it finds PHP 5.x in 2025. BELIEVE ME, I DID IT. 😜

## Legal stuff
Run it only on systems you are explicitly authorised to test.
Nikita assumes zero liability for misuse or any Oh-sht* moments.

## License
MIT – fork, tweak, share, and pwn (your own boxes).
