---
name: wan22
description: Write, rewrite, or refine prompts for Wan 2.2 image-to-video generation. Use when the user asks to create an image-to-video prompt or refine an existing one.
---

# Skill: wan22

Write, rewrite, or refine prompts for Wan 2.2 image-to-video generation.

## Core Principles

1. Wan 2.2 uses a Mixture-of-Experts (MoE) architecture. The model will "fill in the gaps" when a prompt is vague — producing cinematic chaos (unexpected characters, random actions, style drift).

2. Good Wan 2.2 prompts are **80–120 words** and explicitly describe shot type, motion, camera movement, environment, and constraints.

3. Wan 2.2 responds well to camera language. Pan directions, dolly in/out, tilt, tracking shots, crash zooms, and camera rolls are all reliably followed on the first try.

4. When CFG=1 (common in Lightning and Rapid AIO workflows), classic negative prompts are effectively disabled. Phrase "no X" constraints as **positive statements** instead.

5. Wan 2.2 works best with clips **<= 5 seconds** (<= 120 frames at 24 fps). Use 480p (540x960 or 960x540) for quick tests; 720p (720x1280 or 1280x720) for publication.

## Prompt Formulas

### Image-to-Video Formula

The source image already establishes subject, scene, and style. Focus on motion and camera:

    Prompt = Motion Description + Camera Movement

- **Motion Description**: What moves in the image (people, animals, objects). Use adverbs like "quickly" or "slowly" to control pace and intensity.
- **Camera Movement**: Specify desired camera behavior. Use "static shot" or "fixed shot" for no camera motion.

### Sound Formula (Wan 2.5)

Adds voices, sound effects, and BGM for native audio generation:

    Prompt = Subject + Scene + Motion + Sound Description

- **Voice** = `"the character's spoken lines"` + emotion + intonation + speech rate + timbre + accent
  - E.g., `"love is not getting but giving."` — relaxed tone, moderate pace, bright clear voice, American English.
- **Sound Effects** = sound source object + action + ambient sound
  - E.g., A piece of glass falls from a table onto a wooden floor, making a "shatter" sound, in a quiet indoor environment.
- **Background Music** = BGM + style
  - E.g., On a rainy night, in a gloomy narrow corridor with a window at the end, suspense-style background music plays.

### Reference-to-Video Formula (Wan 2.6)

Generate videos based on a reference input character (person, cartoon, pet, or prop). Up to 2 characters per video.

    Prompt = @Starring Role + Action + Dialogue + Scene

- **@Starring Role**: Reference a character video using `@`. Up to 2 starring roles. Each can be cited multiple times throughout the prompt.
- **Action**: Movement or state of the starring role — stationary, subtle motion, dynamic motion, local or overall.
- **Dialogue**: Spoken content — solo lines or multi-role conversations.
- **Scene**: Environment including background and foreground.

- E.g., "This is a playfairytale scene. @A is hopping and playing on the grass, @B is playing the piano under an apple tree nearby, and an apple falls onto @B's head. @A cheerfully points at @B and says, 'You're going to become a scientist!'"

### Multi-Shot Formula (Wan 2.6)

Generate coherent narrative videos with multiple shots. Enable "Smart Multi-Shot" for simple prompts.

    Prompt = Overall Description + Shot Number + Timestamp + Subject Behavior

- **Overall Description**: Brief overview of story theme, narrative style, main emotions, or core events.
- **Shot Number**: Assign numbers to distinguish scenes/segments.
- **Timestamp**: Time range for each shot (e.g., `[0-3s]`).
- **Subject Behavior**: Detailed actions, speech, expressions, and postures per shot.

- E.g., "This story is told from a third-person perspective and presents a short play about giving up and gaining hope. Shot 1 [0-3s]: The main character sits alone in the corner of the playground, looking down at a letter in their hands. Then, they quietly sigh, their eyes reflecting confusion and sadness. Shot 2 [4-6s]: Hard cut transition, fixed camera, close-up on the main character's eyes, glistening with tears, displaying feelings of loss and helplessness. Shot 3 [7-10s]: Hard cut transition, scene shifts to a simple classroom. The second main character stands with a gentle yet determined gaze, dressed plainly and smiling warmly, walking toward the first main character."

## Prompt Structure (Image-to-Video, Advanced)

Write prompts in this order (the model processes them sequentially):

    Camera motion -> Reveal / payoff

### 1. Cast and Count (be explicit)

State exactly who is in the scene and who is NOT. Wan 2.2 is trained on busy cinematic material and will add extras unless told otherwise.

    "exactly two people: one man and one woman, both in their 30s"
    "No other people in the frame. No background characters."

### 2. Setting and Time

Anchor the environment and time of day so the model does not shift locations mid-clip.

    "Indoor restaurant, warm candlelit evening, wooden table, blurred
    background tables, no TV screens, no windows in frame."

Include:
- Location type (indoor/outdoor, specific venue)
- Time of day (daylight, night, sunrise, sunset, dawn, dusk, twilight)
- Lighting quality (soft, hard, volumetric, neon, firelight, fluorescent, overcast, practical, edge, side, bottom, high contrast, low contrast, silhouette)
- Background details (cluttered, minimalist, specific objects)

### 3. Camera and Framing

This is a first-class component of Wan 2.2 prompts. Specify:

**Shot type:**
- Extreme close-up, close-up, close shot, medium close-up, medium shot, medium wide, wide-angle, panorama, establishing shot

**Camera position:**
- Eye-level, low-angle, high-angle, overhead, ground-level, over-the-shoulder, flat shot, straight-on

**Composition:**
- Center composition, balanced composition, left/right weighted composition, symmetrical composition, short-side composition, clean single shot, clean two-shot

**Lens / optical:**
- Telephoto lens, wide-angle lens, fisheye lens, medium lens, long-focus lens, shallow depth of field, soft bokeh, anamorphic bokeh

**Camera motion (Wan 2.2 follows these reliably):**
- Static camera (if no movement desired)
- pan left / pan right
- tilt up / tilt down
- dolly in / dolly out
- push in / pull back
- tracking shot (following shot)
- arc shot / orbiting shot
- crane up
- handheld shot
- crash zoom / rapid zoom in
- camera roll (full 360)
- drone shot / aerial shot

### 4. Subject Motion (primary focus)

Describe what the main subject does — this is the core of every image-to-video prompt. Be specific about the type, speed, amplitude, and sequence of movements.

    "The woman raises her right arm, her hand opening to reveal a glowing
    golden talisman. She steps forward with deliberate grace, her left hand
    trailing through the air as if casting a spell. She tilts her head back,
    eyes closing, then opens them with sudden intensity."

Prioritize **subject-driven motion** over environmental effects:

- **Arm/hand gestures**: raising, reaching, pointing, waving, clasping, opening/closing hands, tracing shapes in the air
- **Head/face**: tilting, turning, nodding, looking up/down/at camera, blinking, smiling, frowning, mouth opening to speak
- **Body movement**: stepping, turning, spinning, leaning, crouching, standing, kneeling, dancing, fighting stances
- **Full-body actions**: walking, running, jumping, leaping, falling, floating, martial arts sequences
- **Clothing/fabric interaction**: sleeves sweeping, hem lifting, cape billowing, fabric catching wind — always tied to the subject's movement

Describe motion with **speed and amplitude**:
- Speed: slowly, gradually, suddenly, sharply, slowly building, accelerating, decelerating
- Amplitude: subtle, slight, moderate, large, dramatic, exaggerated

Describe motion with **temporal sequencing**:
- "First..., then..., finally..."
- "At 0s..., by 2s..., by end..."
- "The movement begins as..., peaks when..., settles into..."

Avoid making the environment do all the work. Wind-blown hair, flowing fabric, and particle effects are secondary to what the **subject** is doing.

### 5. Motion Boundaries (positive constraints)

Because negative prompts may not work at CFG=1, state what must NOT happen as a positive constraint:

    "There are only these two people and nobody else ever enters the frame."
    "They remain seated at the table the whole time."
    "The camera does not move. No zoom. No pan. No cut."

### 6. Visual Style and Mood

Place style tags **late** in the prompt so they don't overshadow structure:

    "cinematic, naturalistic lighting, soft shallow depth of field,
    subtle film grain, realistic skin tones, movie-grade color grading"

Style categories:
- Cinematic / filmic / photorealistic / documentary
- Animated / cartoon / 3D rendered / CGI stylized / 2D anime
- Felt style / puppet animation / claymation / pixel art
- Watercolor painting / oil painting / line art / impressionist / surreal
- 3D game scene / black and white animation
- Cyberpunk / steampunk / wasteland / vintage / retro
- Color grading: teal-and-orange, bleach-bypass, warm tone, cold tone, high saturation, low saturation, desaturated colors

## Aesthetic Control Reference

### Light Source

| Type | Effect |
|---|---|
| **Sunny lighting** | Natural bright illumination, warm golden tones |
| **Artificial lighting** | Indoor lamp, desk light, overhead |
| **Moonlight** | Cool, dim, silvery, profound mood |
| **Practical lighting** | Visible light source in frame (bulb, candle) |
| **Firelight** | Warm, flickering, orange, cozy or eerie |
| **Fluorescent** | Cool, flat, greenish-blue, institutional |
| **Overcast** | Soft, diffused, even, no hard shadows |
| **Mixed** | Multiple light sources, varied color temperatures |

### Lighting Type

| Type | Effect |
|---|---|
| **Soft light** | Gentle shadows, smooth transitions |
| **Hard light** | Sharp shadows, high definition |
| **Top light** | Dramatic overhead, skull-like shadows |
| **Side light** | Dramatic half-light, strong shadows |
| **Edge / rim light** | Backlit outline, separates subject from background |
| **Underlighting** | Unnatural, eerie, upward illumination |
| **Silhouette** | Subject dark against bright background |
| **High contrast** | Deep blacks, bright highlights |
| **Low contrast** | Flat, muted, even |

### Time of Day

| Type | Effect |
|---|---|
| **Sunrise** | Soft golden light, serene, hopeful |
| **Daylight** | Bright, neutral, clear visibility |
| **Dusk** | Fading light, deep blue sky, first streetlights |
| **Sunset** | Warm orange-red tones, cinematic, nostalgic |
| **Dawn** | Pale light, cool tones, quiet, tentative |
| **Night** | Dark, practical lights, moody, dramatic |

### Shot Size

| Term | Framing |
|---|---|
| **Extreme close-up** | Eyes, mouth, small detail |
| **Close-up** | Face fills frame |
| **Close shot** | Head and shoulders |
| **Medium close-up** | Chest up |
| **Medium shot** | Waist up |
| **Medium wide** | Knees up |
| **Wide shot** | Full body + environment |
| **Wide-angle / Establishing** | Sweeping landscape or large scene |

### Composition

| Term | Effect |
|---|---|
| **Center composition** | Subject dead center, balanced |
| **Balanced composition** | Elements distributed across frame |
| **Left/right weighted** | Subject on one side, negative space on the other |
| **Symmetrical** | Mirror-like, formal, orderly |
| **Short-side** | Subject pushed to one side, leading into open space |

### Lens

| Term | Effect |
|---|---|
| **Medium lens** | Natural perspective, standard view |
| **Wide lens** | Expanded field of view, distorted edges |
| **Long-focus / Telephoto** | Compressed perspective, shallow depth of field |
| **Fisheye** | Extreme distortion, circular or ultra-wide |

### Color Tone

| Term | Effect |
|---|---|
| **Warm colors** | Golden, orange, red tones, cozy, inviting |
| **Cool colors** | Blue, gray, cyan tones, calm, detached |
| **Saturated colors** | Vivid, intense, high energy |
| **Desaturated colors** | Muted, cinematic, moody, nostalgic |

## Motion Reference

| Type | Description |
|---|---|
| **Walking / Running** | Forward locomotion, vary pace and posture |
| **Jumping / Leaping** | Vertical or horizontal air time |
| **Dancing** | Rhythmic movement, specify style |
| **Swimming / Floating** | Weightless or fluid motion |
| **Small-scale** | Head tilt, blink, smile, nod, gesture, breathing |
| **Large-scale** | Leap, sprint, spin, shatter, burst, dissolve |
| **Partial** | Swaying, flickering, pulsing, rippling, drifting |

## Character Emotion

| Emotion | Visual Cues |
|---|---|
| **Angry** | Furrowed brow, tense jaw, clenched fists, narrowed eyes |
| **Fear** | Dilated pupils, parted lips, sweat, rigid posture |
| **Happy** | Smiling, shining eyes, relaxed posture, open expression |
| **Sad** | Empty gaze, tears, slumped shoulders, downcast eyes |
| **Surprised** | Wide eyes, raised eyebrows, parted mouth, startled posture |

## Camera Movement Reference

| Term | What it does |
|---|---|
| pan left / right | Camera rotates horizontally |
| tilt up / down | Camera rotates vertically |
| dolly in | Camera moves physically closer |
| dolly out | Camera moves physically away |
| push in | Same as dolly in (common phrasing) |
| pull back | Same as dolly out |
| tracking shot | Camera follows subject laterally |
| arc shot | Camera circles around subject |
| crane up | Camera rises vertically |
| handheld | Shaky, documentary-style movement |
| crash zoom | Very fast, dramatic zoom in |
| camera roll | Camera rotates around lens axis |
| static | No camera movement |
| aerial / drone shot | High-altitude or flying perspective |

## Visual Effects Reference

| Effect | Description |
|---|---|
| **Tilt-shift** | Miniature world illusion, narrow focus band |
| **Time-lapse** | Accelerated time, blurred motion of clouds/people |
| **Motion blur** | Speed lines, directional blur |
| **Slow motion** | Dramatic time dilation, 120fps feel |

## Negative Prompt Guidance

The default negative prompt in most Wan 2.2 workflows is:

    "bright colors, overexposed, static, blurred details, subtitles,
    style, artwork, painting, picture, still, overall gray, worst quality,
    low quality, JPEG compression residue, ugly, incomplete, extra fingers,
    poorly drawn hands, poorly drawn faces, deformed, disfigured, malformed
    limbs, fused fingers, still picture, cluttered background, three legs,
    many people in the background, walking backwards"

At CFG=1 this may have limited effect. Rely primarily on positive constraints for control.

## Common Mistakes

- **Too vague:** "A person walking in a park" — no shot type, no camera, no motion detail, no style.
- **Overstuffing:** Conflicting style cues (e.g., "cinematic + cartoon + watercolor") confuse the model. Limit to 1–2 style tags.
- **Forgetting motion:** Without camera/movement direction, scenes can feel static or the model improvises unwanted motion.
- **Relying on negatives at CFG=1:** Classic negative prompts are effectively disabled in 4-step Lightning workflows. Use positive constraints instead.
- **Too long clips:** Clips longer than 5 seconds (120+ frames) increase artifact risk and processing time.

## Prompt Examples

### Example 1 — Cinematic Drama (Image-to-Video)

    "The camera slowly dollies in from a wide shot to a medium close-up. The
    cowboy's weathered face remains mostly still, only his eyes scanning the
    horizon with subtle shifts. His hat brim casts a soft shadow over his eyes.
    Dust particles drift in the golden hour light. Cinematic grading, shallow
    depth of field, soft bokeh, epic western atmosphere."

### Example 2 — Fantasy (Image-to-Video)

    "The camera spirals in from above, capturing the mage's hesitant gestures
    as arcane sparks dance between their fingers. Fireflies flicker around
    ancient twisted trees and distant magical runes pulse gently on mossy
    stones. The tattered robes sway faintly in an unseen breeze. Lifelike
    lighting, rich magical effects, cinematic visual storytelling, moody
    atmospheric tones."

### Example 3 — Character (Image-to-Video)

    "The cat tilts its head forward with a warm, affectionate gaze, its large
    googly eyes wobbling slightly. It holds the rose steady in its front paws,
    chest breathing softly. The ears twitch once, then remain still. Soft
    natural lighting, clean simple background, photorealistic style, medium
    shot at eye level, static camera."

### Example 4 — Cyberpunk Tracking (Image-to-Video)

    "The camera tracks forward at shoulder height behind the hooded courier as
    he weaves through crowds. Neon kanji signs flicker overhead, casting
    volumetric pink-blue backlight through steam vents. Puddles mirror the
    glow. Lens flare, shallow depth of field. Moody, Blade-Runner vibe."

### Example 5 — Pull Back Reveal (Image-to-Video)

    "Camera dollies back and tilts up simultaneously, revealing the climber
    and a vast sunrise-lit alpine ridge behind him. The ice axe remains
    planted, only the climber's breathing causes subtle chest movement. Crisp
    morning air, golden rim-light, subtle lens flare."

### Example 6 — Multi-Shot (Wan 2.6)

    "This story is told from a third-person perspective and presents a short
    play about giving up and gaining hope. Shot 1 [0-3s]: The main character
    sits alone in the corner of the playground, looking down at a letter in
    their hands. Then, they quietly sigh, their eyes reflecting confusion and
    sadness. Shot 2 [4-6s]: Hard cut transition, fixed camera, close-up on
    the main character's eyes, glistening with tears, displaying feelings of
    loss and helplessness. Shot 3 [7-10s]: Hard cut transition, scene shifts
    to a simple classroom. The second main character stands with a gentle yet
    determined gaze, dressed plainly and smiling warmly, walking toward the
    first main character."

## Response Rules

- Lead with the rewritten prompt only (no explanation unless asked).
- The prompt should be 80–120 words.
- Follow the ordered structure: shot/framing -> camera motion -> subject action -> environment -> style tags.
- Include explicit cast count and motion boundaries.
- Do NOT include the negative prompt unless the user explicitly asks for it.
- If the user provides an image-to-video prompt, use the I2V formula: "Movement + Camera Movements" (describe what moves in the image, then specify camera behavior).
- For Wan 2.6 features (starring roles, multi-shot, reference-to-video), adapt the formula accordingly.

Base directory for this skill: file:///home/buu/Documents/websearch/.opencode/skills/wan22
Note: file list is sampled.
