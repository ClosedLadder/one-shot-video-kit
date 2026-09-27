#!/usr/bin/env python3
"""seat_router.py — subscription-pool-aware model routing with circuit breakers.

Routes a prompt to the strongest healthy subscription seat. The core insight:
seats sharing a subscription pool are NOT real fallbacks for credit exhaustion,
so fallback hops POOLS, not just seats.

  Pools: claude-max (fable, opus, claude) | codex-pro (codex, codex-astra)
         | grok-sub (grok-seat) | astra (Astra, GPT-6 on the Air, async via bus)

Tiers:
  frontier        fable -> opus -> codex-astra            (sync; BEST, art direction)
  standard        claude -> codex -> grok-seat             (sync; general)
  writing         grok-seat -> claude -> codex            (sync; bulk writing first)
  frontier-async  astra -> fable -> opus -> codex-astra    (Astra first via bus)

Mechanics:
- Exhaustion signatures on a FAILED seat (402, balance exhausted, usage/quota/
  rate-limit) cool the ENTIRE pool (claude/codex: 60 min, grok/astra: 30 min).
- 3 consecutive generic failures cool the individual seat 15 min.
- Success resets the seat's failure count.
- Classification only happens on failure (rc != 0 or empty output), so a real
  answer that merely mentions "quota" is never misclassified.
- Astra is async: prompt dropped on the Air bus, reply lands in outbox/.
  --wait-astra polls for it; without it, dispatch is fire-and-forget (exit 0,
  prints the response filename to watch).
- No `timeout(1)` on macOS: subprocess.run(timeout=...) kills the local ssh.

Usage:
  seat_router.py [--tier T] [--file P] [--timeout S] [--max-turns N]
                 [--wait-astra S] [--status] ["prompt"]
"""
import json, os, re, subprocess, sys, time, base64

HERE = os.path.dirname(os.path.abspath(__file__))
MBP_HELPER = "/home/hatch/workspace/goals/ark-runner-v2-build-blitz/hidden_files/mbp.sh"
AIR = "air"
AIR_SSH = ["ssh", "-F", "/home/hatch/.ssh/lab_config", "-o", "ConnectTimeout=15",
           "-o", "BatchMode=yes", AIR]
STATE_FILE = os.path.join(HERE, ".seat-state.json")

CLAUDE = "/Users/stevenhaller/.local/bin/claude"
CODEX = "/opt/homebrew/bin/codex"

EXHAUSTED_RE = re.compile(
    r"402|payment required|balance exhausted|usage limit|quota|rate.?limit|"
    r"too many requests|credit.*(exhaust|deplet)|insufficient.*(credit|balance)",
    re.IGNORECASE)

# seat: (pool, host, argv-template | "astra")
# POOLS (corrected 2026-09-25): Fable 5.1 has its OWN small pool within Claude
# that depletes far before the general allocation — it is scarce and reserved
# for highest-intelligence work only. Opus/general Claude share the big pool.
SEATS = {
    "fable":       ("fable-pool", "mbp",
                    f"{CLAUDE} --model fable -p --max-turns {{mt}} < {{pf}}"),
    "opus-5-5":    ("claude-general", "mbp",  # Opus 5.5 via claude 2.1.282+
                    f"{CLAUDE} --model opus -p --max-turns {{mt}} < {{pf}}"),
    "codex-astra": ("codex-pro", "mbp",  # VERIFIED 2026-09-25: gpt-6-astra live via Codex Pro
                    f"{CODEX} exec -m gpt-6-astra --skip-git-repo-check - < {{pf}}"),
    "claude":      ("claude-general", "mbp",
                    f"{CLAUDE} -p --max-turns {{mt}} < {{pf}}"),
    "codex":       ("codex-pro", "mbp",
                    f"{CODEX} exec --skip-git-repo-check - < {{pf}}"),
    "grok-seat":   ("grok-sub", "mbp",
                    "~/bin/grok-seat run --file {pf} --kind draft --data-class INTERNAL "
                    "--timeout {to} --max-turns {mt} \"Follow the brief in the attached file.\""),
    "astra":       ("astra", "air-bus", None),
}
TIERS = {
    "frontier":       ["fable", "opus-5-5", "codex-astra"],
    "standard":       ["claude", "codex", "grok-seat"],
    "writing":        ["grok-seat", "claude", "codex"],
    "frontier-async": ["astra", "fable", "opus-5-5", "codex-astra"],
    # curator: routine twice-daily judging. Fable-free by design — Fable's
    # precious pool must never be spent on routine curation (2026-09-25).
    "curator":        ["opus-5-5", "codex-astra", "grok-seat"],
}
# fable-pool is PRECIOUS: small, depletes fast -> long cooldown when exhausted.
POOL_COOLDOWN_MIN = {"fable-pool": 240, "claude-general": 60, "codex-pro": 60,
                     "grok-sub": 30, "astra": 30}
PRECIOUS_POOLS = {"fable-pool"}
SEAT_COOLDOWN_MIN = 15
SEAT_FAIL_LIMIT = 3


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {"seats": {}, "pools": {}}


def save_state(s):
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(s, f)
    os.replace(tmp, STATE_FILE)


def cooled(entry):
    return time.time() < entry.get("cool_until", 0)


def run_mbp(cmd, timeout):
    p = subprocess.run([MBP_HELPER, cmd], capture_output=True, text=True,
                       timeout=timeout)
    return p.returncode, p.stdout or "", p.stderr or ""


def clean_output(out):
    # strip MBP claude-settings permission nag lines (stderr noise)
    lines = [l for l in out.splitlines()
             if not l.startswith("Permission allow rule")]
    return "\n".join(lines).strip()


def deliver_prompt_mbp(prompt):
    b64 = base64.b64encode(prompt.encode()).decode()
    pf = f"/tmp/seat-prompt-{os.getpid()}-{int(time.time())}.md"
    # chunk the base64 to stay clear of command-line limits
    run_mbp(f"echo {b64} | base64 -D > {pf} && wc -c < {pf}", 60)
    return pf


def try_sync_seat(name, pf, timeout, max_turns):
    pool, host, tmpl = SEATS[name]
    cmd = tmpl.format(pf=pf, mt=max_turns, to=timeout)
    try:
        rc, so, se = run_mbp(cmd, timeout + 120)
    except subprocess.TimeoutExpired:
        return False, "", "timeout"
    out = clean_output(so) or clean_output(se)
    if rc == 0 and out:
        return True, out, ""
    # failure: classify
    head = out[:2000]
    if EXHAUSTED_RE.search(head):
        return False, out, "exhausted"
    return False, out, "failed"


def astra_dispatch(prompt):
    """Drop a task on the Air bus (atomic protocol). Returns response filename."""
    fname = f"neo-to-astra-{time.strftime('%Y%m%d')}-seat-{int(time.time())}.md"
    body = ("# Seat task (video-skill router)\n\n## Context\n"
            "Routed from the one-shot video skill's seat bridge. Reply in kind.\n\n"
            "## Ask\n\n" + prompt + "\n")
    b64 = base64.b64encode(body.encode()).decode()
    tmp = f"/Users/sknh-air/neo-astra/inbox/.tmp-{fname}.part"
    fin = f"/Users/sknh-air/neo-astra/inbox/{fname}"
    cmd = (f"echo {b64} | base64 -D > {tmp} && mv {tmp} {fin} && "
           f"ls {fin}")
    p = subprocess.run(AIR_SSH + [cmd], capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        return None
    return fname


def astra_wait(fname, wait_secs):
    out = f"/Users/sknh-air/neo-astra/outbox/{fname}"
    deadline = time.time() + wait_secs
    while time.time() < deadline:
        p = subprocess.run(AIR_SSH + [f"cat {out} 2>/dev/null"],
                           capture_output=True, text=True, timeout=60)
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout
        time.sleep(20)
    return None


def main():
    args = sys.argv[1:]
    tier, pfile, timeout, max_turns, wait_astra = "standard", None, 600, 10, 0
    show_status, conduct, worker_tier = False, False, "writing"
    prompt_parts = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--tier": tier, i = args[i + 1], i + 2
        elif a == "--file": pfile, i = args[i + 1], i + 2
        elif a == "--timeout": timeout, i = int(args[i + 1]), i + 2
        elif a == "--max-turns": max_turns, i = int(args[i + 1]), i + 2
        elif a == "--wait-astra": wait_astra, i = int(args[i + 1]), i + 2
        elif a == "--worker-tier": worker_tier, i = args[i + 1], i + 2
        elif a == "--conduct": conduct, i = True, i + 1
        elif a == "--status": show_status, i = True, i + 1
        else: prompt_parts.append(a); i += 1

    state = load_state()

    if show_status:
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"seat router status @ {now}")
        for pool in sorted({p for p, _, _ in SEATS.values()}):
            e = state["pools"].get(pool, {})
            tag = " [PRECIOUS]" if pool in PRECIOUS_POOLS else ""
            health = ('COOLED until ' + time.strftime('%H:%M', time.localtime(e['cool_until']))
                      if cooled(e) else 'healthy')
            print(f"  pool {pool}{tag}: {health}")
        for t, names in TIERS.items():
            marks = []
            for n in names:
                e = state["seats"].get(n, {})
                marks.append(f"{n}{'❄'+str(e.get('fails',0)) if cooled(e) or e.get('fails') else ''}")
            print(f"  tier {t}: {' -> '.join(marks)}")
        return 0

    if tier not in TIERS:
        print(f"unknown tier {tier}", file=sys.stderr)
        return 1
    prompt = "".join(prompt_parts)
    if pfile and not prompt:
        with open(pfile) as f:
            prompt = f.read()
    if not prompt.strip():
        print("seat_router: no prompt", file=sys.stderr)
        return 1

    def cool_pool(pool):
        mins = POOL_COOLDOWN_MIN.get(pool, 30)
        state["pools"][pool] = {"cool_until": time.time() + mins * 60,
                                "reason": "exhausted", "at": time.strftime("%H:%M")}
        print(f"  pool {pool} exhausted -> cooled {mins}m", file=sys.stderr)

    def fail_seat(name):
        e = state["seats"].get(name, {"fails": 0})
        e["fails"] = e.get("fails", 0) + 1
        if e["fails"] >= SEAT_FAIL_LIMIT:
            e["cool_until"] = time.time() + SEAT_COOLDOWN_MIN * 60
            print(f"  seat {name} failed x{e['fails']} -> cooled {SEAT_COOLDOWN_MIN}m",
                  file=sys.stderr)
        state["seats"][name] = e

    if conduct:
        return conduct_mode(prompt, worker_tier, timeout, max_turns,
                            state, cool_pool, fail_seat)

    pf = deliver_prompt_mbp(prompt)
    try:
        ok, out, tried = run_tier(tier, prompt, pf, timeout, max_turns,
                                  wait_astra, state, cool_pool, fail_seat)
    finally:
        run_mbp(f"rm -f {pf}", 30)
        save_state(state)
    if ok:
        print(out)
        return 0
    print(f"seat_router: all seats failed (tried: {', '.join(tried) or 'none healthy'})",
          file=sys.stderr)
    return 1


def run_tier(tier, prompt, pf, timeout, max_turns, wait_astra,
             state, cool_pool, fail_seat):
    """Run the tier's seats in order. Returns (ok, output, tried)."""
    tried = []
    for name in TIERS[tier]:
        pool, host, _ = SEATS[name]
        if cooled(state["pools"].get(pool, {})):
            print(f"  skip {name} (pool {pool} cooled)", file=sys.stderr)
            continue
        if cooled(state["seats"].get(name, {})):
            print(f"  skip {name} (seat cooled)", file=sys.stderr)
            continue
        tried.append(name)
        print(f"  trying {name}...", file=sys.stderr)

        if host == "air-bus":
            fname = astra_dispatch(prompt)
            if not fname:
                fail_seat(name)
                continue
            if wait_astra > 0:
                resp = astra_wait(fname, wait_astra)
                if resp:
                    state["seats"][name] = {"fails": 0}
                    return True, resp, tried
                fail_seat(name)
                continue
            state["seats"][name] = {"fails": 0}
            return True, (f"ASTRA-DISPATCHED:{fname}\n"
                          f"watch: /Users/sknh-air/neo-astra/outbox/{fname}"), tried

        ok, out, kind = try_sync_seat(name, pf, timeout, max_turns)
        if ok:
            state["seats"][name] = {"fails": 0}
            return True, out, tried
        if kind == "exhausted":
            cool_pool(pool)
        else:
            fail_seat(name)
    return False, "", tried


def conduct_mode(goal, worker_tier, timeout, max_turns, state, cool_pool, fail_seat):
    """Fable 5.1 conducts: one precious planning call, lesser models execute.

    Fable writes the architecture/plan as JSON tasks; each task is dispatched
    to the worker tier. The expensive brain is spent once, on judgment — never
    on bulk execution.
    """
    if worker_tier not in TIERS:
        print(f"unknown worker tier {worker_tier}", file=sys.stderr)
        return 1
    if cooled(state["pools"].get("fable-pool", {})):
        print("conduct: fable-pool cooled — conductor unavailable, not substituting "
              "a lesser model for the architect role", file=sys.stderr)
        return 1

    plan_prompt = (
        "You are the conductor — the highest-intelligence planner. A worker tier "
        f"of lesser models ({worker_tier}) will execute your plan.\n\n"
        f"GOAL:\n{goal}\n\n"
        "Do all architecture and judgment yourself IN THE PLAN. Break the goal into "
        "2-6 concrete, self-contained tasks for the workers. Each task prompt must "
        "stand alone (include every fact, constraint, and acceptance criterion the "
        "worker needs — workers share no context).\n\n"
        "Output ONLY a JSON array, no prose, no markdown fences:\n"
        '[{"id": "t1", "prompt": "<exact self-contained worker prompt>", '
        '"accept": "<acceptance criteria>"}, ...]'
    )
    pf = deliver_prompt_mbp(plan_prompt)
    try:
        ok, out, kind = try_sync_seat("fable", pf, timeout, 15)
    finally:
        run_mbp(f"rm -f {pf}", 30)
    if not ok:
        if kind == "exhausted":
            cool_pool("fable-pool")
        else:
            fail_seat("fable")
        save_state(state)
        print("conduct: fable planning call failed", file=sys.stderr)
        return 1
    state["seats"]["fable"] = {"fails": 0}

    tasks = parse_plan(out)
    if tasks is None:
        # one retry with a stricter nudge (precious call — don't waste it silently)
        pf2 = deliver_prompt_mbp(plan_prompt + "\n\nREMINDER: output ONLY the JSON array.")
        try:
            ok2, out2, _ = try_sync_seat("fable", pf2, timeout, 15)
        finally:
            run_mbp(f"rm -f {pf2}", 30)
        if ok2:
            out = out2
            tasks = parse_plan(out)
    if tasks is None:
        save_state(state)
        print("conduct: fable did not return a parseable plan:\n" + out[:1500],
              file=sys.stderr)
        return 1

    log_conduct(goal, worker_tier, [t["id"] for t in tasks])
    print(f"conduct: fable planned {len(tasks)} tasks -> worker tier {worker_tier}",
          file=sys.stderr)
    all_ok, results = True, []
    for t in tasks:
        wpf = deliver_prompt_mbp(t["prompt"])
        try:
            ok, wout, tried = run_tier(worker_tier, t["prompt"], wpf, timeout,
                                       max_turns, 0, state, cool_pool, fail_seat)
        finally:
            run_mbp(f"rm -f {wpf}", 30)
        seat = tried[-1] if tried else "none"
        results.append((t["id"], seat, ok, wout, t.get("accept", "")))
        all_ok = all_ok and ok
        save_state(state)
    save_state(state)

    print(f"# Conducted run: {goal[:80]}")
    for tid, seat, ok, wout, accept in results:
        print(f"\n## task {tid} -> {seat} [{'OK' if ok else 'FAILED'}]"
              f"{' | accept: ' + accept if accept else ''}\n{wout}")
    return 0 if all_ok else 1


def parse_plan(out):
    """Tolerant JSON-array extraction from the conductor's reply."""
    s = out.find("[")
    e = out.rfind("]")
    if s < 0 or e <= s:
        return None
    try:
        tasks = json.loads(out[s:e + 1])
    except Exception:
        return None
    if not isinstance(tasks, list) or not tasks:
        return None
    clean = []
    for t in tasks:
        if isinstance(t, dict) and t.get("prompt"):
            clean.append({"id": str(t.get("id", f"t{len(clean)+1}")),
                          "prompt": t["prompt"],
                          "accept": str(t.get("accept", ""))})
    return clean or None


def log_conduct(goal, worker_tier, task_ids):
    """One-line routing record for the precious tier (lab-router rule 6)."""
    try:
        day = time.strftime("%Y-%m-%d")
        with open(os.path.expanduser(f"~/memory/{day}.md"), "a") as f:
            f.write(f"\n- conduct: fable planned [{', '.join(task_ids)}] -> {worker_tier} "
                    f"({time.strftime('%H:%M')}): {goal[:100]}\n")
    except Exception:
        pass


if __name__ == "__main__":
    sys.exit(main())
