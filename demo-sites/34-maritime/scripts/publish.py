#!/usr/bin/env python3
from __future__ import annotations
import argparse, datetime as dt, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REMOTE = "https://github.com/team-ashtra-ai/34.git"

def run(args):
    print("+", " ".join(args))
    return subprocess.check_call(args, cwd=ROOT)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--message")
    parser.add_argument("--remote", default=REMOTE)
    args = parser.parse_args()
    if not (ROOT / ".git").exists():
        run(["git", "init"])
        run(["git", "branch", "-M", "main"])
    remotes = subprocess.run(["git", "remote"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.split()
    if "origin" not in remotes:
        run(["git", "remote", "add", "origin", args.remote])
    else:
        run(["git", "remote", "set-url", "origin", args.remote])
    message = args.message or "update " + dt.datetime.now().strftime("%Y-%m-%d %H-%M")
    run(["git", "add", "-A"])
    run(["git", "commit", "--allow-empty", "-m", message])
    run(["git", "push", "-u", "origin", "main"])

if __name__ == "__main__":
    main()
