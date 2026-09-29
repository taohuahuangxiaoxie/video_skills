---
name: video-reference-prep
description: "Prepare a reference video when the user says 处理一下参考视频, 预处理参考视频, lower reference resolution/frame rate, or prepare motion input. Defaults to 24 fps CFR, lower aspect-preserving resolution and no audio. Excludes generated-video finishing and does not itself create depth."
---

# Reference video preparation

Apply these defaults directly; do not ask the user to repeat them. Explicit current settings win.

- 24 fps constant frame rate. Standard portrait 9:16 → 576×1024; landscape 16:9 → 1024×576; square → at most 768×768. Other ratios fit the corresponding orientation box, even dimensions, without crop/stretch/padding. Do not upscale an already smaller source.
- Remove all audio, subtitles and data streams; produce H.264/yuv420p MP4. Preserve full visible frame and source motion speed, orientation, action order and effective duration. Frame-rate conversion may drop/duplicate frames but must not interpolate motion or retime. Do not automatically trim first/last frames or black tails.
- Preserve the input. Save a clearly named sibling such as `<stem>_ref_576x1024_24fps_silent.mp4`; choose a new version if it exists. Work in the source task directory.

Use `scripts/video_ops.py reference INPUT --output OUTPUT`. The standard-library script locates FFmpeg/FFprobe in PATH or `E:/work/comfyui/tools/ffmpeg/bin`; `--ffmpeg`, `--ffprobe`, `--fps`, and `--max-long/--max-short` can override explicit requests. `--plan-only` probes without encoding. Use the available Python runtime; on this machine the bundled Python is `C:/Users/dell/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`.

The script verifies full decode, dimensions, exact frame grid, frame count, duration (within one target frame of source video duration), and zero audio streams, and writes a JSON processing report next to the output. If source timing is malformed, do not silently use the container's longer audio duration as the motion duration. Inspect representative action frames before delivery when motion details matter. Deliver a clickable absolute output link with dimensions, fps, duration, and audio status.

Depth generation additionally uses `../temporal-depth-reference/SKILL.md`; do not infer a request for depth from ordinary reference preprocessing. Ambiguous “处理视频” needs context to distinguish reference versus generated output; do not accidentally cut a reference or downsample a finished result.

## Runtime portability

Resolve FFmpeg/FFprobe via explicit `--ffmpeg` / `--ffprobe`, `FFMPEG` / `FFPROBE` environment variables, PATH, or `<COMFYUI_WORKSPACE>/tools/ffmpeg/bin` (current directory when unset). Do not assume the old drive letter or username exists. The helper needs Python stdlib and FFmpeg/FFprobe.
