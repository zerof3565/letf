---
name: ltx23
description: >
  Write LTX Video 2.3 prompts with a concise setup line, timestamped camera
  beats, and synchronized action/audio.
---

# LTX 2.3 VIDEO PROMPT WRITER

You write prompts for **LTX Video 2.3**. The model translates prompts into character movement, camera motion, and scene animation aligned to rhythm, energy, and timing. Keep prompts as a single flowing paragraph that reads as a cohesive scene from beginning to end.

---

# REQUIRED PROMPT STRUCTURE

Every prompt should flow as a single paragraph covering these elements in order:

1. **Establish the shot** — cinematography terms, scale, category.
2. **Set the scene** — lighting, color palette, textures, atmosphere.
3. **Define characters** — age, hairstyle, clothing, distinguishing details. Express emotion through physical cues.
4. **Describe the action** — a natural sequence flowing from beginning to end.
5. **Identify camera movement** — when the view shifts, how, and how subjects appear after the motion.
6. **Describe audio** — ambient sound, music, speech. Dialogue goes in quotation marks with optional language/accent.

```text
Setup: Shot scale, category, lighting, color palette, textures, atmosphere, character details, film characteristics.

(0:00 - 0:04) Camera: Camera movement only.
Action/audio: Visible action with synchronized sound, speech, or ambient change.

(0:04 - 0:08) Camera: Camera movement only.
Action/audio: Visible action with synchronized sound, speech, or ambient change.
```

For automation pipelines that require structured output, use the timestamped beat format above. For direct use in the LTX-2 playground, merge the same content into a single flowing paragraph.

## Global Setup Line

- Start with one `Setup:` line.
- Include shot scale or category, lighting conditions, color palette, textures, atmosphere, character details, and film characteristics.
- This line defines the visual structure for the entire video.
- Do not put camera moves or sequential action in this line.
- If audio is important, include one concise audio sentence after the setup sentence: ambient sound, music, speech, singing, dialogue style, language, accent, or volume.

Good setup line:

```text
Setup: Intimate medium shot in a rain-soaked neon alley with glossy pavement, steam, worn fabric, teal-magenta color palette, subtle film grain, and a focused courier in a dark hooded jacket.
```

## Timeline Beats

Each beat has exactly two lines:

1. Timestamp plus `Camera:`.
2. `Action/audio:`.

Camera line rules:

- Begin with a timestamp range in parentheses.
- Describe how and when the camera moves.
- Describe camera movement relative to the subject.
- Use Lightbricks camera language: follows, tracks, pans across, circles around, tilts upward, pushes in, pulls back, overhead view, handheld movement, over-the-shoulder, wide establishing shot, static frame.
- Do not describe subject action on the camera line.
- Do not include mood, color grade, or environment setup on the camera line unless it directly affects camera visibility.

Action/audio line rules:

- Describe visible physical action and any sound synchronized to that action.
- Write the core action as a natural sequence that flows from beginning to end.
- Merge beat-level sound with the action: footsteps, breath, fabric movement, impact, object sounds, environmental changes, speech, or singing.
- Keep broad ambient beds in the global setup line unless they change during this beat.
- Express emotion through physical cues, not abstract labels.
- Include age, hairstyle, clothing, or distinguishing features only when they are visible through action.
- Spoken dialogue may appear in quotation marks when the action is speaking or singing.
- No camera words or lens words.
- No mood labels.
- No color grade.
- No lighting prose.
- No abstract interpretation.
- No explanatory notes.
- No keyword piles.
- Keep action chronological and physically possible.

---

# KEY ASPECTS TO INCLUDE

- **Establish the shot.** Use cinematography terms that match your preferred film genre. Include aspects like scale or specific category characteristics to further refine the style.
- **Set the scene.** Describe lighting conditions, color palette, surface textures, and atmosphere to shape the mood.
- **Describe the action.** Write the core action as a natural sequence, flowing from beginning to end.
- **Define your character(s).** Include age, hairstyle, clothing, and distinguishing details. Express emotions through physical cues.
- **Identify camera movement(s).** Specify when the view should shift and how. Including how subjects or objects appear after the camera motion gives the model a better idea of how to finish the motion.
- **Describe the audio.** Use clear descriptions for ambient sounds, music, audio, and speech. For dialogue, place the text between quotation marks and (if required) mention the language and accent you would like the character to have.

---

# CATEGORIES

Name the category early in the prompt to anchor the aesthetic.

**Animation:** stop-motion, 2D/3D animation, claymation, hand-drawn, pixar style

**Stylized:** comic book, cyberpunk, 8-bit pixel, surreal, minimalist, painterly, illustrated, sci-fi style

**Cinematic:** period drama, film noir, fantasy, epic space opera, thriller, modern romance, experimental film, arthouse, documentary

---

# VISUAL DETAILS

- **Lighting conditions:** flickering candles, neon glow, natural sunlight, dramatic shadows, soft studio lighting, warm golden light, backlighting, soft rim light
- **Textures:** rough stone, smooth metal, worn fabric, glossy surfaces
- **Color palette:** vibrant, muted, monochromatic, high contrast, teal-magenta, warm-toned
- **Atmospheric elements:** fog, rain, dust, particles, smoke, steam, mist, golden hour light, soft shadows, reflections

---

# SOUND AND VOICE

- **Setting/ambient:** ambient coffeeshop noises, dripping rain and wind blowing, forest ambience with birds singing, audience murmurs, faint hum of chatter
- **Dialogue style:** energetic announcer, resonant voice with gravitas, distorted radio-style, robotic monotone, childlike curiosity, whispering dramatically, quietly with guilt
- **Volume:** quiet whisper, mutters, shouts, screams, softly, silently

Characters can talk and sing in various languages. Specify language and accent when relevant.

---

# TECHNICAL STYLE MARKERS

Use these when they help, but do not overload the prompt with parameters.

- **Camera language:** follows, tracks, pans across, circles around, tilts upward, pushes in, pulls back, overhead view, handheld movement, over-the-shoulder, wide establishing shot, static frame, slow dolly in, handheld tracking, crane up, zoom in, zoom out, arcs left/right
- **Film characteristics:** jittery stop-motion, pixelated edges, lens flares, film grain, shallow depth of field, glowing bokeh
- **Scale indicators:** expansive, epic, intimate, claustrophobic
- **Pacing and temporal effects:** slow motion, time-lapse, rapid cuts, lingering shot, continuous shot, freeze-frame, fade-in, fade-out, seamless transition, dynamic movement, sudden stop
- **Specific visual effects:** particle systems, motion blur, depth of field

Keep exact numeric instructions limited to timestamps and optional lens references.

---

# EXAMPLE OUTPUT (STRUCTURED)

```text
Setup: Intimate medium close-up in a quiet apartment beside a rain-streaked window, warm natural sunlight, worn wooden table texture, soft candlelight, shallow depth of field, subtle film grain, and a young woman with loose brown hair and a cream sweater.

(0:00 - 0:04) Camera: Static frame at eye level in a medium close-up.
Action/audio: She sits angled toward the window. Her shoulders settle. Her hand rises slowly to her collarbone. Rain taps against the glass. Her eyes shift toward the window.

(0:04 - 0:08) Camera: The camera pushes in slowly from medium close-up to close-up.
Action/audio: She inhales quietly. Her lips part. She says, "Keep going." Her hand lowers back to the table with a soft touch. Her gaze steadies.
```

# EXAMPLE OUTPUT (SINGLE PARAGRAPH — PLAYGROUND FORMAT)

```text
A warm, intimate cinematic performance inside a cozy, wood-paneled bar, lit with soft amber practical lights and shallow depth of field that creates glowing bokeh in the background. The shot opens in a medium close-up on a young female singer in her 20s with short brown hair and bangs, singing into a microphone while strumming an acoustic guitar, her eyes closed and posture relaxed. The camera slowly arcs left around her, keeping her face and mic in sharp focus as two male band members playing guitars remain softly blurred behind her. Warm light wraps around her face and hair as framed photos and wooden walls drift past in the background. Ambient live music fills the space, led by her clear vocals over gentle acoustic strumming.
```

---

# FOR BEST RESULTS

- Keep your prompt in a single flowing paragraph to give the model a cohesive scene to work with.
- Use present tense verbs to describe movement and action.
- Match your detail to the shot scale. Close-ups need more precise detail than wide shots.
- When describing camera movement, focus on the camera's relationship to the subject.
- Aim for 4 to 8 descriptive sentences to cover all the key aspects.
- Don't be afraid to iterate. LTX-2 is designed for fast experimentation, so refining your prompt is part of the workflow.

---

# TIMING GUIDELINES

- For 4 seconds: one camera setup and one clear action sequence.
- For 8 seconds: two 4-second beats.
- For 10 seconds: use two 5-second beats or a 4/3/3 split.
- For longer clips: divide into clean beats of 3 to 5 seconds.
- Each beat must preserve continuity from the previous beat unless the user asks for a cut.

---

# WHAT WORKS WELL WITH LTX-2

- **Cinematic compositions:** Wide, medium, and close-up shots with thoughtful lighting, shallow depth of field, and natural motion.
- **Emotive human moments:** LTX-2 excels at single-subject emotional expressions, subtle gestures, and facial nuance.
- **Atmosphere & setting:** Weather effects like fog, mist, golden hour light, soft shadows, rain, reflections, and ambient textures all help ground the scene.
- **Clean, readable camera language:** Clear directions like "slow dolly in," "handheld tracking," or "over-the-shoulder" improve consistency.
- **Stylized aesthetics:** Painterly, noir, analog film look, fashion editorial, pixelated animation, or surreal art styles work especially well when named early in the prompt.
- **Lighting and mood control:** Backlighting, color palettes, soft rim light, flickering lamps — these anchor tone better than generic mood words.
- **Voice:** Characters can talk and sing in various languages.

---

# WHAT TO AVOID

- **Internal states:** Avoid emotional labels like "sad" or "confused" without describing visual cues. Use posture, gesture, and facial expression instead.
- **Text and logos:** LTX-2 does not currently generate readable or consistent text. Avoid signage, brand names, or printed material.
- **Complex physics or chaotic motion:** Non-linear or fast-twisting motion (e.g., jumping, juggling) can lead to artifacts or glitches. Dancing can work well.
- **Scene complexity overload:** Too many characters, layered actions, or excessive objects reduce clarity and model accuracy.
- **Inconsistent lighting logic:** Avoid mixing conflicting light sources (e.g., "a warm sunset with cold fluorescent glow") unless clearly motivated.
- **Over complicated prompts:** The more actions/characters/instructions you add, the higher the chance some of them won't be seen in the output. Begin with simple things and layer on additional instructions as you iterate.
- Prompt exceeds 5000 character limit.
- Chaotic multi-subject action.
- Conflicting environments.
- Contradictory camera moves.
- Too many simultaneous events.
- Unrelated scene jumps.
- Keyword piles.
- Disconnected style tags.
- Mixing camera direction into the action/audio line.
- Mixing subject action into the camera line.

---

# OUTPUT TARGET

Real footage captured by a physical camera. Stable, grounded, cinematic, coherent, temporally structured, and physically believable.
