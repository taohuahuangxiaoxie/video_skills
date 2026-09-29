---
name: generated-video-finish
description: "Finish an AI-generated video when the user says 处理生成视频, 处理成片, trim generated output, or remove AIGC/AGIC generation metadata. Defaults to deleting the first 1 and last 3 decoded frames and cleaning generation metadata while preserving resolution, frame timing and synchronized audio. Excludes reference preprocessing."
---

# Generated video finishing

User-approved defaults: remove the first **1 decoded/display-order frame** and last **3 decoded/display-order frames**, and clear AIGC/platform generation metadata. Do this without repeating confirmation. Current explicit trim counts, audio or size instructions override defaults. For an explicitly metadata-only/no-trim request, keep all frames. If there are at most four frames, explain that the default cut would leave nothing and ask for smaller cut counts rather than producing an empty file.

- Probe actual decoded count and presentation timestamps; VFR clips cannot be cut by assuming `1/fps`. Retain indexes `1..N-4` inclusive (zero-based), normalize retained PTS to zero, and verify N−4 frames with original relative PTS. Accurate non-keyframe cuts require decoding/re-encoding, not approximate stream-copy seeks.
- Preserve original resolution and timing; do **not** apply reference-video 24fps/downscale defaults. Keep audio if present and trim it to the corresponding source-video time range. Explicit silence requests override this. Preserve input and write a new sibling `<stem>_trimmed_clean.mp4` or unused version.
- Clear global/stream metadata and chapters, including AIGC, LvMetaInfo, UserComment, platform names, generation/propagation identifiers and comment tags. Re-encoding avoids copying old codec user data. On ordinary SDR H.264 output, remove SEI and verify metadata after writing. For HDR/10-bit/color-managed material preserve necessary color/HDR signaling; do not blindly strip all SEI or down-convert—adapt the cleanup and disclose any unresolved generated tags.
- Metadata cleanup does not prove removal of visible picture watermarks or invisible pixel-level marks. Do not claim those were removed. If visible text remains, report it or handle the separately requested visual edit; no silent crop or watermark inpainting.

Use the shared installed helper `../video-reference-prep/scripts/video_ops.py finish INPUT --output OUTPUT`. It accepts `--head`, `--tail` and `--mute`; defaults are 1, 3 and preserve audio. It has no dependency beyond Python stdlib and FFmpeg/FFprobe. `--plan-only` shows exact kept indexes/times. Verify full decode, dimensions, N−4 frames, retained PTS, audio duration and absence of generation tags; the helper writes a JSON report. Do not run finishing twice on an already finished derivative unless the user wants another trim; prefer the original source.

Deliver the new video with a concise description of actual edits. Cleaning metadata is not a reason to claim a video is human-shot or guaranteed to pass moderation.
