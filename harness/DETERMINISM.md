# Determinism Contract

The rules that make Loop 1 reproducible. Every rule here is enforced by the
`harness` CLI — not by convention, not by memory.

## 1. One seed

- Each run takes one master seed (a string, e.g. `2026-10-02-nightly`).
- Every component derives its own integer seed from it:
  `sha256(master + ":" + component)`, first 4 bytes.
- Components: `maestro`, `playwright`, `flutter`, `backend`, `dart`.
- The same master seed on any machine gives the same derived seeds.
- Shards never share a random stream.

## 2. Frozen clock

- Loop 1 runs set `HARNESS_TEST_CLOCK` to an ISO-8601 instant.
- Date-dependent features (Daily Moments, reading plans, streaks) read this
  instead of the wall clock.
- Loop 2 does not freeze the clock — production is live.

## 3. Stubbed externals

- LLM calls, push notifications, and third-party APIs return canned fixtures
  in Loop 1. No live network calls to external services.
- A test that needs a live external service (e.g.
  `cerebras_client_live_test.go`) is quarantined or stubbed before it enters
  the baseline. No exceptions.

## 4. Pinned tools

- Flutter/Dart, Node, Playwright browsers, Maestro, Go, Python, and container
  versions are pinned. The run manifest records what actually ran.

## 5. No sleeps, no silent retries

- Flows wait on conditions (element visible, text present), never fixed
  sleeps.
- A failed step fails the test. No automatic retries inside the run.
- Sharding is by stable hash of the test id — the same test always lands on
  the same shard.

## 6. Quarantine, not deletion

- A flaky test moves to `quarantine.yml` with a reason, an owner, and a date.
- Quarantined tests are skipped but always listed in the report as
  quarantined-skipped. Nothing disappears silently.

## 7. Manifest every run

- Each run writes `run-manifest.json`: schema version, loop, timestamp,
  master seed + derived seeds, clock value, test selection, repo SHAs, app
  version (Loop 2), environment, tool versions.
- The manifest plus the seed is sufficient to replay the run exactly.

## 8. What is NOT deterministic

- Loop 3 (exploratory agents) — non-deterministic by design.
- Loop 2's environment — production is live; only the *steps* are
  deterministic.
