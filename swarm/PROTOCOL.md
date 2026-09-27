# Swarm Protocol — director / worker

Exercised later; the protocol and packet format exist NOW so any future multi-AI run plugs in without redesign. Pattern: scene-per-agent work packets (PDoomVideo's subagents), map-reduce frame rendering, merge + QC gate before ship.

## Roles

- **Director** (frontier-reasoning class): owns the brief, writes the storyboard, splits it into work packets, runs the merge + QC gate, ships or rejects. The ONLY role that talks to Steven.
- **Worker** (strong-code class): claims packets, delivers exactly the deliverables, never expands scope. A worker that is confused is killed and replaced — never pivoted mid-packet.

## Packet lifecycle

`open → claimed → done → verified`. The director moves packets; workers only move their own `claimed → done`.

1. Director writes packets per `work-packet.schema.json` into `swarm/packets/<brief>/<packet_id>.json` (status: `open`).
2. Worker claims: sets `status: claimed`, `worker_id`, `claimed_at`. One worker per packet — claiming is atomic (file rename / lock; second claimer backs off).
3. Worker delivers the packet's `deliverables` to the paths named, sets `status: done`.
4. Director (or QC worker) verifies against `acceptance_criteria`; pass → `verified`, fail → back to `open` with the failure note appended (max 2 retries, then director re-scopes).
5. When all packets are `verified`: **merge step** → **QC gate** (self-review loop on the merged cut) → ship.

## Map-reduce frame rendering

- Scene packets produce scene renders; frame packets partition a scene's frame range (`frame_start`/`frame_end`) across N workers.
- **Determinism requirement:** every frame is a pure function of its timestamp (taste law 16). Same `(kit_version, seed, timestamp)` → identical bytes, on any machine.
- Merge = concatenate/assemble in packet order by ffmpeg; no re-encoding of verified frames.
- A worker NEVER "improves" another packet's frames. Cross-packet consistency (palette, character) comes from the shared style pack, not from workers editing each other.

## Idempotency rules

- Re-running a packet with identical inputs produces **identical output**. Randomness is seeded; seeds live in the packet's `inputs`.
- Packets declare `kit_version`; a packet built under a different kit version is re-run, not patched.
- Budgets: each packet carries `budget_cap`; a worker that would exceed it stops and reports — it does not spend hoping for forgiveness.

## Failure handling

- Worker silent > 2× its `timeout_s`: director re-opens the packet.
- Two failed verifications: director re-scopes the packet (smaller, simpler) rather than retrying the same failing shape.
- Merge conflicts (overlapping frame ranges, mismatched fps): director's packet definitions are authoritative; regenerate the packet, don't hand-edit outputs.
