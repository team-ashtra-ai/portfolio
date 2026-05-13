#!/usr/bin/env python3

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout.strip(), file=sys.stderr)
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        raise SystemExit(result.returncode)
    return result.stdout.strip()


def default_message() -> str:
    now = dt.datetime.now().astimezone()
    return now.strftime("Portfolio update %Y-%m-%d %H:%M:%S %Z")


def current_branch() -> str:
    return run_git("rev-parse", "--abbrev-ref", "HEAD")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stage all changes, create an allow-empty commit, rebase from origin, and push.",
    )
    parser.add_argument(
        "-m",
        "--message",
        help="Commit message. Defaults to a day/time based message.",
    )
    parser.add_argument(
        "--skip-pull",
        action="store_true",
        help="Skip pulling with rebase before pushing.",
    )
    parser.add_argument(
        "--remote",
        default="origin",
        help="Remote to push to. Defaults to origin.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    message = args.message or default_message()
    branch = current_branch()

    print(f"Repository: {REPO_ROOT}")
    print(f"Branch: {branch}")
    print(f"Commit message: {message}")

    run_git("add", "-A")
    run_git("commit", "--allow-empty", "-m", message)

    if not args.skip_pull:
        run_git("pull", "--rebase", "--autostash", args.remote, branch)

    run_git("push", args.remote, branch)
    print("Push completed.")


if __name__ == "__main__":
    main()
