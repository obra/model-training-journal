#!/usr/bin/env python3
"""Record an explicit completed editorial review, tied to exact public bytes."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from validate import ROOT, ValidationError, digest, private_terms, validate


def terms_digest(terms: list[str]) -> str:
    return hashlib.sha256(json.dumps(sorted(terms), separators=(",", ":")).encode()).hexdigest()


def verify_receipt(path: Path, hashes: dict[str, str], terms: list[str], root: Path = ROOT) -> dict:
    if root.resolve() in path.resolve().parents:
        raise ValidationError("Review receipts must stay outside public Git history")
    receipt = json.loads(path.read_text())
    if receipt.get("schema") != 1 or receipt.get("repository") != "obra/model-training-journal":
        raise ValidationError("Wrong review receipt schema or target")
    if receipt.get("files") != hashes or receipt.get("candidate_sha256") != digest(hashes):
        raise ValidationError("Review receipt is stale: public candidate changed; review again")
    if receipt.get("private_terms_sha256") != terms_digest(terms):
        raise ValidationError("Private review terms changed; review again")
    if receipt.get("checks") != {"privacy": True, "factual_accuracy": True, "licensing": True, "rendered_pages": True}:
        raise ValidationError("Review receipt is missing required editorial assertions")
    if not isinstance(receipt.get("note"), str) or len(receipt["note"].strip()) < 20:
        raise ValidationError("Review receipt needs a substantive review note")
    try:
        reviewed = datetime.fromisoformat(receipt["reviewed_utc"])
        now = datetime.now(timezone.utc)
        if reviewed.tzinfo is None or reviewed > now or (now - reviewed).total_seconds() > 86_400:
            raise ValueError("expired")
    except (KeyError, TypeError, ValueError) as exc:
        raise ValidationError("Review timestamp is invalid or older than 24 hours") from exc
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-terms-file", type=Path, required=True)
    parser.add_argument("--reviewed", action="store_true", help="Assert actual privacy, licensing, factual and rendered-page review is complete")
    parser.add_argument("--note", required=True, help="Brief description of evidence and review performed; kept local")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if not args.reviewed:
            raise ValidationError("No approval recorded: complete editorial review, then explicitly pass --reviewed")
        if ROOT.resolve() in args.output.resolve().parents:
            raise ValidationError("Store review receipts outside the public checkout")
        if len(args.note.strip()) < 20:
            raise ValidationError("Supply a substantive review note")
        terms = private_terms(args.private_terms_file)
        hashes = validate(terms=terms)
        receipt = {
            "schema": 1, "repository": "obra/model-training-journal",
            "reviewed_utc": datetime.now(timezone.utc).isoformat(),
            "candidate_sha256": digest(hashes), "files": hashes,
            "private_terms_sha256": terms_digest(terms),
            "checks": {"privacy": True, "factual_accuracy": True, "licensing": True, "rendered_pages": True},
            "note": args.note,
        }
        # Refuse accidental overwrite of a receipt from another reviewed candidate.
        with args.output.open("x") as stream:
            json.dump(receipt, stream, indent=2)
            stream.write("\n")
    except (ValidationError, OSError, SyntaxError) as exc:
        parser.exit(1, f"Review stopped: {exc}\n")
    print(f"Recorded completed review for {len(hashes)} files; SHA256 {digest(hashes)}")


if __name__ == "__main__":
    main()
