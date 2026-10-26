#!/usr/bin/env python3
"""Publish one reviewed static journal update using the Mac's existing Git login."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from review import verify_receipt
from validate import ROOT, ValidationError, allowed_path, private_terms, scan_text, validate

ORIGIN = "git@github.com:obra/model-training-journal.git"
PUBLIC_NAME = "Journal automation"
PUBLIC_EMAIL = "journal@users.noreply.github.com"


def git(*args: str, root: Path = ROOT, raw: bool = False, env: dict | None = None):
    result = subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, env=env)
    return result.stdout if raw else result.stdout.decode().strip()


def verify_origin(root: Path = ROOT) -> None:
    if git("remote", "get-url", "--all", "origin", root=root).splitlines() != [ORIGIN]:
        raise ValidationError("Origin does not exactly match the authorized SSH repository")
    if git("remote", "get-url", "--push", "--all", "origin", root=root).splitlines() != [ORIGIN]:
        raise ValidationError("Push origin does not exactly match the authorized repository")


def git_preflight(root: Path = ROOT) -> list[str]:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise ValidationError("Run from the dedicated journal Git checkout")
    if git("branch", "--show-current", root=root) != "main":
        raise ValidationError("Publication requires the main branch")
    verify_origin(root)
    staged = git("diff", "--cached", "--name-only", "-z", root=root, raw=True)
    if staged:
        raise ValidationError("Index already has staged changes; inspect and unstage them before publication")
    tracked = [name for name in git("ls-files", "-z", root=root, raw=True).decode().split("\0") if name]
    if any(not allowed_path(name) for name in tracked):
        raise ValidationError("Git contains files outside the public allowlist; inspect manually")
    return tracked


def verify_staged(hashes: dict[str, str], terms: list[str], root: Path = ROOT) -> None:
    staged_hashes = {}
    entries = git("ls-files", "--stage", "-z", root=root, raw=True).decode().split("\0")
    for entry in filter(None, entries):
        metadata, name = entry.split("\t", 1)
        mode, oid, stage = metadata.split()
        if not allowed_path(name) or mode not in {"100644", "100755"} or stage != "0":
            raise ValidationError("Index contains an unexpected path, symlink, submodule or merge conflict")
        data = git("cat-file", "blob", oid, root=root, raw=True)
        try:
            scan_text(data.decode("utf-8"), name, terms)
        except UnicodeDecodeError as exc:
            raise ValidationError("Index contains a non-text blob") from exc
        staged_hashes[name] = hashlib.sha256(data).hexdigest()
    if staged_hashes != hashes:
        raise ValidationError("Staged Git bytes differ from the reviewed candidate")


def verify_committed(commit: str, hashes: dict[str, str], terms: list[str], root: Path = ROOT, base: str | None = None) -> None:
    if base is not None and git("rev-list", "--parents", "-n", "1", commit, root=root).split() != [commit, base]:
        raise ValidationError("Commit history changed during publication; nothing was pushed")
    committed_hashes = {}
    entries = git("ls-tree", "-r", "--full-tree", "-z", commit, root=root, raw=True).decode().split("\0")
    for entry in filter(None, entries):
        metadata, name = entry.split("\t", 1)
        mode, kind, oid = metadata.split()
        if not allowed_path(name) or mode not in {"100644", "100755"} or kind != "blob":
            raise ValidationError("Commit contains an unexpected path, symlink or submodule")
        data = git("cat-file", "blob", oid, root=root, raw=True)
        try:
            scan_text(data.decode("utf-8"), name, terms)
        except UnicodeDecodeError as exc:
            raise ValidationError("Commit contains a non-text blob") from exc
        committed_hashes[name] = hashlib.sha256(data).hexdigest()
    if committed_hashes != hashes:
        raise ValidationError("Committed bytes differ from the reviewed candidate; nothing was pushed")
    scan_text(git("show", "-s", "--format=%B", commit, root=root), "committed message", terms)
    identity = git("show", "-s", "--format=%an%x00%ae%x00%cn%x00%ce", commit, root=root).split("\0")
    if identity != [PUBLIC_NAME, PUBLIC_EMAIL, PUBLIC_NAME, PUBLIC_EMAIL]:
        raise ValidationError("Commit identity differs from the public automation identity; nothing was pushed")


def commit_environment() -> dict:
    env = os.environ.copy()
    env.update(GIT_AUTHOR_NAME=PUBLIC_NAME, GIT_AUTHOR_EMAIL=PUBLIC_EMAIL,
               GIT_COMMITTER_NAME=PUBLIC_NAME, GIT_COMMITTER_EMAIL=PUBLIC_EMAIL)
    env.pop("GIT_AUTHOR_DATE", None)
    env.pop("GIT_COMMITTER_DATE", None)
    return env


def publish(review_path: Path, terms_path: Path, message: str, root: Path = ROOT) -> str:
    terms = private_terms(terms_path, root)
    scan_text(message, "commit message", terms)
    if len(message.strip()) < 8 or "\n" in message:
        raise ValidationError("Use a concise, nonempty single-line public commit message")
    # Validate untrusted candidate files before executing the repository builder.
    from validate import candidate
    candidate_hashes = candidate(root, terms)
    verify_receipt(review_path, candidate_hashes, terms, root)
    tracked = git_preflight(root)
    subprocess.run([sys.executable, str(root / "scripts" / "build.py")], cwd=root, check=True)
    hashes = validate(root, terms)
    verify_receipt(review_path, hashes, terms, root)
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=root, check=True)
    # Fetch only after local privacy and review gates have passed. No pull,
    # merge, reset, rebase, credential refresh or remote setting change occurs.
    git("fetch", "--no-tags", "origin", "refs/heads/main:refs/remotes/origin/main", root=root)
    base = git("rev-parse", "refs/remotes/origin/main", root=root)
    if git("rev-parse", "HEAD", root=root) != base:
        raise ValidationError("Local HEAD differs from origin/main; inspect history and reconcile manually")
    # A changed file between checks must not silently enter the commit.
    if validate(root, terms) != hashes:
        raise ValidationError("Candidate changed during validation; review again")
    paths = sorted(set(hashes) | set(tracked))
    git("add", "--", *paths, root=root)
    verify_staged(hashes, terms, root)
    if not git("diff", "--cached", "--name-only", root=root):
        return "No content changes; nothing was committed or pushed."
    git("commit", "-m", message, root=root, env=commit_environment())
    commit = git("rev-parse", "HEAD", root=root)
    verify_committed(commit, hashes, terms, root, base=base)
    verify_origin(root)
    git("-c", "push.followTags=false", "push", "origin", f"{commit}:refs/heads/main", root=root)
    return f"Pushed reviewed commit {commit}. Verify the Pages deployment and live post URLs before reporting publication complete."


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-terms-file", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--message", required=True)
    args = parser.parse_args()
    try:
        print(publish(args.review, args.private_terms_file, args.message))
    except (ValidationError, OSError, SyntaxError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        # Git's stderr can contain credential-bearing URLs on misconfigured
        # machines; avoid copying its raw output into a public automation log.
        if isinstance(exc, subprocess.CalledProcessError):
            parser.exit(1, f"Publication stopped: a local build, test or Git command failed (exit {exc.returncode}). Inspect its local state before retrying.\n")
        parser.exit(1, f"Publication stopped: {exc}\n")


if __name__ == "__main__":
    main()
