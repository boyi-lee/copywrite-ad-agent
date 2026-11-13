# Release identity and rollback

This file keeps its historical `candidate-` filename for compatibility with existing checks and references; its content describes the current installed Skill and future release process.

## Current state

The active Skill is the directory installed at `/Users/boyi/.codex/skills/copywrite-ad-agent/`. This canonical directory is present in the installed Skill catalog. Its current tree has no verified release tag, so describe it as the **installed, unversioned snapshot**; do not describe it as an uninstalled candidate.

Other dated copies under the workspace or backup paths are historical artifacts. They are not the active source and must not be merged selectively into the installed tree. Verify a candidate as a complete tree before any future release.

## Before a release

1. Record a version and source revision for the candidate.
2. Preserve a complete, dated snapshot of the currently installed tree and its file manifest.
3. Run the verification commands in `README.md`, the applicable governance audit, and required independent Standards and Spec Reviews.
4. Install the complete reviewed tree in one operation. Do not mix files from different revisions.
5. Verify the installed tree against the reviewed candidate and run the same checks again.

## Rollback

If post-install verification fails, restore the preserved complete snapshot to the canonical path and rerun the same checks. Keep old workflow records readable; never relabel prior runs as newly verified. Do not restore generated `.DS_Store`, `__pycache__`, or bytecode files.

## Limits

A passing local check establishes only the checks it actually runs. It does not establish semantic truth of claims, reviewer identity, ad performance, platform approval, or publication status. No release is complete until the installed tree and the verification evidence are recorded together.
