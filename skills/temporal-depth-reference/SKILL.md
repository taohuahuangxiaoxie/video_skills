---
name: temporal-depth-reference
description: "Generate true temporal black-and-white depth video when the user says 生成深度视频, 黑白深度参考, or convert a clip to depth. Preprocess high-resolution/high-frame-rate source to lower resolution, 24 fps CFR and silence before inference; use local Video Depth Anything. Excludes ordinary grayscale conversion and does not auto-enable ControlNet."
---

# Temporal depth reference

## Defaults and order

1. Select the user-specified original motion source, not a generated result or older clip by accident. First use `../video-reference-prep/SKILL.md`: 24 fps CFR, no audio, standard portrait 576×1024 / landscape 1024×576, aspect preserved, no upscaling. **Reduce high resolution and high frame rate before model inference**, not just after rendering. Preserve the processed RGB intermediate and its report. An existing intermediate may be reused only after verifying it belongs to this source, is CFR24, fits the low-resolution box, and has no audio.
2. Inspect cuts in the prepared 24fps clip. Continuous footage is one shot. For actual hard cuts, estimate each shot separately using the unchanged official temporal routine to prevent cross-cut ghosting; use one grayscale mapping across the whole result. Candidate detection needs visual confirmation; do not treat every flash or fast movement as a cut.
3. Run actual temporal relative inverse-depth estimation with local Video Depth Anything Small/vits. Near is bright, far is dark. Never substitute plain desaturation, edge maps or fake depth. Do not change the official temporal alignment/window behavior. No per-frame automatic contrast normalization.
4. Output the prepared clip's dimensions and 24fps, without audio. Keep every prepared frame and source rhythm; no implicit head/tail trimming, freezing, looping, speeding or extra action. Same normal video-reference input; not a claim that ControlNet is enabled. Fine expression cannot be recovered from depth: image references and short expression prompts carry it.

## Local execution

`scripts/make_depth.py INPUT --output OUTPUT` first invokes the shared reference-preparation helper, then performs inference. Options: `--prepared` (only for a verified existing low-resolution 24fps silent input), `--cuts 25,58,...` (interior frame numbers in the **prepared** clip), `--input-size 392`, `--threads 6`, `--workspace <project-root>`, optional `--model-root`, `--checkpoint`, `--ffmpeg`, `--ffprobe`. Workspace defaults to `COMFYUI_WORKSPACE` or the current directory. Defaults use local CPU float32 and the existing model/checkpoint; do not install/download or use a remote host just because no local model is found.

Use a Python environment with Video Depth Anything dependencies. On the original Windows workstation: `<project-root>/tools/depth/.venv/Scripts/python.exe`. Recreate the environment on the destination; do not copy a virtual environment between machines. Model code: `tools/depth/source/Video-Depth-Anything-main`; weights: `tools/depth/checkpoints/video_depth_anything_vits.pth`. Preserve source/processed RGB, raw depth chunks, progress and JSON report in a new output-specific working directory. Do not reuse another clip's cached depth arrays. For long footage with memory pressure, process verified shots in order; any additional segmentation must preserve official overlap/alignment and cannot silently break motion continuity.

Before delivery verify complete decode, same number of frames as the prepared clip, CFR24 timestamps, aspect/dimensions, effective duration and no audio; inspect opening, representative gestures, cut boundaries and ending. Show the actual depth artifact. Missing runtime/checkpoint is a concrete block, not permission to return grayscale and call it depth.
