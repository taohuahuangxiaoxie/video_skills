---
name: h3-comfyui-capacity-guide
description: >-
  Advise on resolution multipliers, VRAM-safe reference modes, and chunking for MiniMax H3 and
  SDVR2 in the user's ComfyUI workflow. Use when choosing image-only or video-reference pixel
  multipliers, planning a 15-second generation, selecting SDVR2 upscale scale or segment length,
  or diagnosing a stall likely caused by VRAM. Treat the stored figures as empirical limits for
  this workstation, not universal model limits. Do not use for creative prompt writing or generic
  ComfyUI setup.
---

# H3 ComfyUI Capacity Guide

Use the user's successful and failed runs as the primary capacity evidence for this workstation.
Give a recommended starting value and a cautious next step; do not present an untested value as safe.

## Scope and provenance

- These limits and quality decisions were reported by the user from the current ComfyUI workstation on 2026-09-07 and 2026-09-08.
- They apply to the stated 15-second H3 and SDVR2 workflows. Different duration, frame count, model, reference count, attention implementation, tiling, or concurrent GPU load can change the limit.
- A generation that hangs near or above a boundary counts as a failed capacity test even if no explicit out-of-memory message appears.
- This skill gives parameter and chunking advice. It does not authorize remote execution, browser control, uploads, or generation.

## Empirical capacity baselines

| Workflow case | Verified workable setting | Verified failure boundary | Default advice |
| --- | --- | --- | --- |
| H3 multi-reference with images only, 15 seconds | `0.9` pixel multiplier | `1.0` hangs from insufficient VRAM | Use at most `0.9`; lower it when other memory demands increase. |
| H3 multi-reference containing video, 15 seconds | `0.7` pixel multiplier | Values above `0.7` hang | Treat any video reference as the video-reference case and cap at `0.7`. |
| SDVR2 super-resolution | `0.7` source/pixel multiplier, `2×` linear upscale, processed in segments of at most 5 seconds | Processing the full 15 seconds at once hangs | Keep chunks at `≤5 s`; do not infer that a full 15-second run is safe. |

Do not raise these ceilings without a new successful user test. When the user reports a new result, preserve the old result and record the changed workflow parameters before revising a baseline.

## Observed SDVR2 portrait-quality result

On 2026-09-07, a 5-second upscale from an H3 images-only `0.9`-multiplier source completed in about 10 minutes with these settings: SeedVR2 3B Int8, `2×`, Euler/simple, `denoise=1.00`, `color_correction_method=lab`, split latent enabled, and temporal overlap `1`. The user judged the result usable but reported an ink/oil-paint character, over-emphasized skin texture, and an unattractive neck shadow in the upward-looking shot.

Treat this as a **capacity success but a portrait-quality caution**, not evidence that `2×` is the preferred setting. The run changed several quality-relevant variables at once, so do not attribute the defects to LAB, overlap, or scale alone.

A follow-up lower-scale/lower-restoration-strength test retained the same painterly character while losing the high-pixel finish the user preferred. The user then tested `1.25×`, `denoise=1.00`, and color correction `none`; its final result still did not meet expectations. This establishes the workflow preference: when H3 images-only output is generated at `0.9`, skip SDVR2 by default and deliver the native H3 output. Run super-resolution only when the user explicitly enables it for that task.

## Recommendation logic

1. Determine whether the H3 reference set contains any video. Images-only and video-reference limits are different even at the same 15-second duration.
2. Use the verified ceiling only when maximizing quality is the user's priority. Reduce the starting value when duration, reference count, concurrent processes, temporal window, or output scale is higher than the verified run.
3. For a `0.9` H3 output, default `upscale=false`. Do not recommend SDVR2 merely because it can run; the FCXT tests showed that higher pixel dimensions did not translate to a preferred portrait result.
4. When the user explicitly enables SDVR2, treat spatial scale and temporal chunk length as separate memory levers. Prefer reducing the upscale factor or chunk duration instead of attempting the entire 15-second video.
5. Keep every segment's model, scale, width, height, frame rate, color settings, and encoding settings identical so later concatenation does not introduce seams or require avoidable transcoding.

## Diagnosing portrait texture, shadows, and temporal seams

- `denoise=1.00` requests full restoration in the official workflow. A lower value was tested as a portrait-quality remedy for this asset but did not remove the reported look and reduced the preferred restoration finish. Keep `1.00` unless a different source shows evidence that restoration strength is the problem.
- `2×` doubles both dimensions and creates four times the output pixels. It produced the strongest high-pixel finish but also made the portrait side effects conspicuous. For FCXT, the final trial used `1.25×` as a compromise; retain the earlier `2×` result as comparative evidence rather than the active setting.
- Color correction is post-processing, not the source of synthesized geometry or pores. Use `none` as the diagnostic control. If it prevents the dirty shadow but shifts the overall palette, try `wavelet` as the compromise. Use `lab` only when its frame-local color match leaves skin and shadow gradients natural; reserve `adain` for quick global mean/variance matching rather than complex dappled portrait light.
- Temporal overlap shares and blends latent frames between internal chunks. Increase `1` to `2` only when a repeating internal chunk seam, flicker, or texture step is visible. It is not a general sharpness control, does not repair a bad neck shadow throughout a shot, and does not blend separately generated 5-second files at their external boundaries.
- Run quality A/B tests on the same representative `0.5–1.0 s` interval containing the difficult neck shadow. Change one variable per test; otherwise the cause cannot be identified.

Parameter semantics are documented in the official [SeedVR2 workflow template](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/utility_seedvr2_3b_int8_upscale_video.json), [post-processing documentation](https://github.com/Comfy-Org/embedded-docs/blob/main/comfyui_embedded_docs/docs/SeedVR2PostProcessing/en.md), and [temporal-chunk documentation](https://github.com/Comfy-Org/embedded-docs/blob/main/comfyui_embedded_docs/docs/SeedVR2TemporalChunk/ja.md).

## Spatial-load comparison for SDVR2

Use this only as a rough comparison, because actual VRAM also depends on latent tensors, temporal windows, tiling, and model implementation:

`approximate output megapixels = source megapixels × linear upscale²`

The verified reference case is approximately `0.7 × 2² = 2.8` output megapixels per frame.

For a `0.9`-multiplier source:

- `1.25×` gives approximately `0.9 × 1.25² = 1.406` megapixels per frame: tested on FCXT with `denoise=1.00` and `none` color correction, but the final quality remained below expectations.
- `1.5×` gives approximately `0.9 × 1.5² = 2.025` megapixels per frame: conservative first test.
- `1.75×` gives approximately `0.9 × 1.75² = 2.756` megapixels per frame: near the verified 2.8-MP output workload, but still unverified because the source tensors are larger.
- `2×` gives approximately `0.9 × 2² = 3.6` megapixels per frame: about 29% more output pixels than the verified case and should not be the first 5-second test.

For a `0.9` H3 source, recommend no super-resolution by default. If the user explicitly enables the optional SDVR2 stage, use the table only for capacity planning and perform a short visual test before committing all segments; do not infer preferred quality from a successful run.

## Preparing for FFmpeg concatenation

- Split by source timeline without gaps or repeated frames: nominally `[0,5)`, `[5,10)`, and `[10,end]` for a 15-second source.
- Use deterministic ordered filenames such as `part_01`, `part_02`, and `part_03`.
- Before concatenation, inspect duration, dimensions, frame rate, codec, pixel format, time base, and audio layout of every segment.
- Use stream-copy concatenation only when the streams are compatible. Otherwise normalize them to one common format and concatenate with a controlled re-encode.
- Verify the two boundaries frame by frame for duplication, omission, a luminance jump, or an audio discontinuity.
