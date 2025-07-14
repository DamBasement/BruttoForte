# BRUTTOFORTE — Banner Fingerprinting Tool

*A fast banner-grabber for vintage stacks and obvious misconfigs.*  
_There are two kinds of servers: those already hacked and those still leaking `X-Powered-By`._

---

## Overview

BRUTTOFORTE scans HTTP headers to spot legacy web stacks:  
- `X-Powered-By`, `Server`, `.NET CLR`, `PHP`, `IIS`, `Express`, etc.  
- Meant for fast recon before full-on exploitation.  
- Targets internal scopes and forgotten environments.

---

## Structure

```
bruttoforte/
├── CheckerBruttoForte.py   // Main script
├── targets.txt             // List of URLs to scan
├── requirements.txt
├── README.md
```

---

## Usage

Install requirements:

```bash
pip install -r requirements.txt
```

Run basic scan:

```bash
python3 CheckerBruttoForte.py -f targets.txt
```

Run with verbosity and more threads:

```bash
python3 CheckerBruttoForte.py -f targets.txt -t 30 --verbose
```

Example output:

```
[+] Scanning 3 target(s) with 30 threads…
    https://url.com       -> IIS 8.5
    https://url.lan       -> PHP 5.6.40
    http://url.portal     -> ASP.NET 4.0.30319

=== Top 5 retro stacks ===
[2 hit] IIS 8.5
[1 hit] PHP 5.6.40

Done. Legacy never dies.
```

---

## Why Use This

- Legacy stacks are still everywhere.
- It's fast and quiet.
- Perfect warm-up before noisy scanners.
- CI-friendly fingerprinting.

---

## Roadmap

- [ ] CSV / JSON output
- [ ] Regex signatures via YAML
- [ ] Noisy mode: `/phpinfo.php`, `/server-status`, etc.

---

## Legal

Use only on systems you have permission to test.  
We are not liable for misuse or negligence.

---

## License

MIT – clone, fork, repurpose.  
Exploit your own infrastructure. Always.
