---
name: createvideo
description: >
  Generate a video from a rough idea by rewriting it with the ltx23 prompt
  structure, running scripts/create_video.py, and returning the generated video
  path and seed. Max duration is 12 seconds.
---

# CREATE VIDEO WORKFLOW

Use this skill when the user invokes `/createvideo ...` or asks to generate a
video from a short idea using the local ComfyUI LTX 2.3 workflow.

## Workflow

1. Treat the user's arguments as the raw video idea.
2. Read `.opencode/skills/ltx23/SKILL.md` if the `ltx23` skill body is not
   already loaded.
3. `positive`: rewrite the raw idea by applying the `ltx23` skill's
   prompt-writing rules. Produce one structured positive prompt using the
   required LTX format and do not exceed 5000 characters limit. Do not run
   `/ltx23` as a shell command; this is an agent prompt rewrite step. Pass the
   rewritten prompt as `--positive "[rewritten prompt]"`. This setting is not
   optional but mandatory.
4. `duration`: pass it as `--duration N` with user's indicated duration (maximum 12), and if
   none given by the user then you must provide a duration matching the prompt.
   This setting is not optional but mandatory.
5. `aspect`: pass it as `--aspect 16:9` or `--aspect 9:16` with the user's
   indicated aspect ratio or orientation. Use `16:9` for landscape, horizontal,
   wide, cinematic, or 512x288 requests. Use `9:16` for portrait, vertical,
   phone, social, reel, short, or 288x512 requests. If none is given by the
   user, choose the aspect ratio that best matches the prompt. This setting is
   not optional but mandatory.
6. Parse optional generation settings from the user's request:
   - `seed`: pass it as `--seed N` only when the user explicitly provides a
     15-digit integer seed.
   - Do not invent or expose fps, width, height, sampler, or model flags.
7. From the repository root, run the script directly. Do not use a shell
   timeout command or any wrapper that kills the process after a fixed number
   of seconds:

   ```bash
   python3 scripts/create_video.py --duration "N" --aspect "16:9|9:16" --positive "[rewritten prompt]"
   ```

   Add `--seed N` when parsed in step 6. Pass the
   rewritten prompt as one `--positive` argument, quoting or escaping it for
   the active shell.

8. The script queues the job and exits immediately without waiting for
    completion. It prints the seed on a
    `queued prompt_id=... seed=...` line and the expected video file after an
    `expected output:` line. The script does NOT wait for ComfyUI to finish.
 9. Do NOT poll `curl http://localhost:8188/queue` or wait for the job to
    complete. Do NOT use `/history/<prompt_id>`, broad output folder scans, or
    expected-path size polling as status checks. Do NOT keep checking the queue.
 10. Report back to the user with the `prompt_id`, `seed`, and expected output
    path from the script output. Do not wait for the generation to finish.
 11. Return the generated video path(s) to the user as clickable local file links.
    Include the seed that was used.

## Response Rules

- Keep the final response short.
- Lead with the generated video link(s), then the seed.
- Do not include the rewritten prompt unless the user asks for it.
- If ComfyUI is unreachable, report the script error and tell the user that the
  local ComfyUI server must be running.
- If the script rejects a seed, explain that `--seed` must be a 15-digit
  integer.
- If the script finishes without video paths, report the prompt_id and seed to
  the user. The job is still running on ComfyUI. Do not poll the queue or wait
  for completion. Do not fall back to `/history/<prompt_id>` or filesystem
  searches.
