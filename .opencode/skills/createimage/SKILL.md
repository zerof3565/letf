---
name: createimage
description: >
  Generate an image from a rough idea by rewriting it with the zitvogue prompt
  style, running scripts/create_image.py, and returning the generated image path.
---

# CREATE IMAGE WORKFLOW

Use this skill when the user invokes `/createimage ...` or asks to generate an
image from a short idea using the local ComfyUI Z-Image Turbo workflow.

## Workflow

1. Treat the user's arguments as the raw image idea.
2. Read `.opencode/skills/zit/SKILL.md` if the `zit` skill body is
    not already loaded.
3. Rewrite the raw idea by applying the `zit` skill's prompt-writing
    rules. Produce one polished single-paragraph positive prompt. Do not run
    `/zit` as a shell command; this is an agent prompt rewrite step.
4. From the repository root, run the script directly. Do not use a shell
   timeout command or any wrapper that kills the process after a fixed number
   of seconds:

   ```bash
    python3 scripts/create_image.py --positive "[rewritten prompt]"
    ```

    For storyboard or cinematic wide shots, pass `--width` and `--height` for a
    16:9 layout. Supported resolutions include up to 2048x1152:

    ```bash
    python3 scripts/create_image.py --positive "[rewritten prompt]" --width 2048 --height 1152
    ```

   Pass the rewritten prompt as one `--positive` argument, quoting or escaping it
    for the active shell.

5. The script forces ComfyUI `SaveImage` output to
   `/home/buu/Documents/ComfyUI/output/images/opencode/`. This is the only valid
   output directory for this workflow.
6. The script queues the job and exits immediately without waiting for
   completion. It prints the seed on a `queued prompt_id=... seed=...` line and
   the expected image file after an `expected output:` line. The script does NOT
   wait for ComfyUI to finish.
7. Do NOT poll `curl http://localhost:8188/queue` or wait for the job to
   complete. Do NOT use `/history/<prompt_id>`, broad output folder scans, or
   expected-path size polling as status checks.
8. Report back to the user with the `prompt_id`, `seed`, and expected output
   path from the script output. Do not wait for the generation to finish.
9. Return the generated image path(s) exactly as local paths under
   `/home/buu/Documents/ComfyUI/output/images/opencode/`, for example
   `/home/buu/Documents/ComfyUI/output/images/opencode/ZiT__00001_.png`. Do not
   convert them to SFTP URLs.
10. Always run 1 at a time if user requests to create multiple images. Never run
   in parallel.

## Response Rules

- Keep the final response short.
- Lead with the generated local image path(s).
- Do not include the rewritten prompt unless the user asks for it.
- If ComfyUI is unreachable, report the script error and tell the user that the
  local ComfyUI server must be running.
- If the script finishes without image paths, report the prompt_id and seed to
  the user. The job is still running on ComfyUI. Do not poll the queue or wait
  for completion. Do not fall back to `/history/<prompt_id>` or filesystem
  searches.
