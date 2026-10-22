#!/usr/bin/env python3
"""Restore the complete V5 CJK serif from versioned binary parts."""
from pathlib import Path
import hashlib, os, tempfile
ROOT=Path(__file__).resolve().parents[1]
EXPECTED="19322be2ecf5dd2abd546db7a86cc83c286026cbd28593583bfcfd721e48c9fe"
TARGETS=["examples/creative-lab/refraction-system/fonts/RefractionSong.otf","examples/creative-lab/refraction-canvas/fonts/RefractionSong.otf","examples/creative-lab/refraction-canvas/ds/refraction/fonts/RefractionSong.otf"]
def main():
    parts=sorted((ROOT/"assets/fonts/native").glob("RefractionSong.otf.part[0-9][0-9][0-9]"))
    if len(parts)!=3: raise SystemExit("Expected three complete font parts; check your clone.")
    data=b"".join(p.read_bytes() for p in parts)
    if hashlib.sha256(data).hexdigest()!=EXPECTED: raise SystemExit("Font part checksum mismatch.")
    for name in TARGETS:
        p=ROOT/name
        if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==EXPECTED: continue
        p.parent.mkdir(parents=True,exist_ok=True)
        fd,temp=tempfile.mkstemp(prefix=".font-",suffix=".tmp",dir=p.parent)
        try:
            with os.fdopen(fd,"wb") as f: f.write(data)
            os.replace(temp,p)
        finally:
            if os.path.exists(temp): os.unlink(temp)
    print("Complete Noto Serif CJK SC font restored and SHA256 verified at all three V5 paths.")
if __name__=="__main__": main()
