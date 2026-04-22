# Task-1 (Git reset--Hands on)

## What is the difference between --soft, --mixed, and --hard?
--soft → moves HEAD/branch, keeps staging area and working directory unchanged
--mixed (default) → moves HEAD/branch, resets staging area, keeps working directory unchanged
--hard → moves HEAD/branch, resets staging area and overwrites working directory to match the target commit
## Which one is destructive and why?
--hard is destructive because it permanently discards uncommitted changes in both the staging area and working directory (overwrites files on disk).
## When would you use each one?
--soft → when you want to uncommit but keep changes staged (e.g. edit last commit, split commits)
--mixed → when you want to uncommit and unstage changes but keep the files modified in your working directory
--hard → when you want to completely throw away all uncommitted changes and go back to a clean state at a specific commit
## Should you ever use git reset on commits that are already pushed?
Almost never on shared branches — use git revert instead to avoid rewriting public history and breaking teammates' work.

# Task 2: (Git Revert — Hands-On)

## How is git revert different from git reset?
git revert creates a new commit that undoes changes while keeping history intact; git reset moves the branch pointer and can discard commits from history.
## Why is revert considered safer than reset for shared branches?
 Revert preserves public history so collaborators can pull safely without conflicts or lost work; reset rewrites history and requires force push that breaks others' branches.
## When would you use revert vs reset?
Use revert for already-pushed/shared commits to avoid breaking history; use reset for local-only commits you haven't pushed yet or on personal branches.

# Task 4: (Branching Strategies)

## 1) GitFlow
 
How it works: Long-lived main (prod) + develop; feature → develop, release → main, hotfix → main & develop.
Flow: main ← release ← develop ← feature ; hotfix → main + develop
Used: Enterprises with planned versioned releases.
Pros/Cons: Clear structure & stable releases; but heavy, slow, merge-conflict prone.

## 2) GitHub Flow

How it works: Single main; short feature branches → PR → merge to main → deploy.
Flow: main ← feature (PR)
Used: SaaS, CI/CD environments deploying continuously.
Pros/Cons: Simple & fast; but weak for complex release/version control.

## 3) Trunk-Based Development

How it works: Developers commit directly to main (trunk) or very short-lived branches; heavy CI + feature flags.
Flow: devs → main (daily merges)
Used: High-velocity teams (e.g., big tech CI-driven orgs).
Pros/Cons: Minimal merge pain & fast integration; requires strong discipline and automation.

## Which strategy would you use for a startup shipping fast?

Startup shipping fast: GitHub Flow or Trunk-Based (speed > structure).

## Which strategy would you use for a large team with scheduled releases?

Large team with scheduled releases: GitFlow (controlled release cycles).

## Which one does your favorite open-source project use? (check any repo on GitHub)

Open-source example: Kubernetes uses a trunk-based style with main + release branches.
