# Manual generation handoff and optional assembly

## Shared package

For every motion job provide: complete prompt path; exact ordered reference paths/roles; selected engine/version/surface; source range; action duration, generated length and trailing hold; aspect; output count; sound choice; and expected save location.

- H3: provide the actual input mode and matching workflow, current preview/formal pixel multiplier and actual acceleration/Attention settings. For native first/last-frame jobs, map the actual frame slots; do not label a role-image upload as hard endpoint binding.
- Seedance: provide the selected surface's reference mode and verified duration/aspect options, not ComfyUI pixel multipliers.
- Hybrid: also provide ordered finished stills, title-card variants, and the edit map. Photo assets are not extra references for the motion job.

The user runs video generation manually by default. No browser control, SSH/API, uploading or automatic downloading without scope-specific authorization.

## H3 preview/capacity defaults

- When enabled, the optional `0.3` preview uses the current images, prompt, duration, aspect, acceleration and Attention configuration; do not automatically re-enable a 4-step LoRA. It remains in ComfyUI unless the user asks for download/analysis.
- Keep the local workflow `03-MiniMax-Ref-Kitchen-Attention` for the established H3 Ref2VA branch only; native frame-bound modes need a verified matching workflow.
- The tested 15-second image-only setup used `0.9` while `1.0` stalled under VRAM pressure. This is local capacity evidence, not a universal H3 ceiling.
- A different tested 15-second video-reference workflow used `0.7`; source video is not part of the default image-only mimic package.
- One output and no upscale by default. Earlier FCXT upscaling trials completed but often added unwanted skin/ink texture and neck shadows.
- For explicitly requested upscale/capacity work, use the available `h3-comfyui-capacity-guide` and inspect actual settings. Do not apply this branch's numbers to Seedance.
- A preview checks feasibility and prompt behavior, not an identical future take. Recheck final-resolution output.

## Review

Check:
1. correct identity, cast and anatomy;
2. reference roles respected, no white-background insertion or unexpected scene cut;
3. world-fixed geography/light, continuous parallax and intended camera endpoint;
4. requested action/airborne pose, then separately timing/coordination and landing weight;
5. expression progression rather than one fixed smile;
6. natural hand growth/contact and hair/cloth response;
7. no severe ghost boundary, text, audio or foreign objects contrary to the brief.

Use [motion-review.md](motion-review.md) for bounded fixes and case evidence. Preserve what works; do not infer exact defects in unseen clips from a general user report.

## User-owned editing: finish at asset handoff

When `assembly_owner=user_editor`, deliver the complete video instructions/reference map, approved ordered stills/title variants, timing/crop/transition notes, and list any outstanding defects. Stop there. Do not demand downloaded clips, run FFmpeg, synthesize the whole photo tail as video, or leave an artificial “merge pending” blocker.

## Assistant assembly, only when requested

Use the manifest's explicit order, never raw directory enumeration. Keep `07-video-output/`, legacy `07-h3-output/`, or the user's actual chosen directory.

Before concatenation, probe duration, frame rate, geometry, sample aspect, codec, pixel format, time base, and audio streams.

- Stream-copy concat only when streams and timestamps are compatible; otherwise normalize video to agreed geometry/frame rate and H.264/yuv420p, and normalize requested audio to a compatible format.
- For a hybrid edit, render still duration/crop/pan/zoom and cuts from the approved edit map; do not invent new transitions or extend the action.
- Trim handles or small frame-grid overruns to the planned duration. Use exact frames in FFmpeg, sensible tenths in the human-facing plan.
- Write a new version under `08-final/`; preserve originals, source segments, approved stills and prior merges.
- Verify full decode, duration, frame count, stream presence and every edit boundary; listen when audio exists.

Few isolated bad frames may be repaired only after inspection and within the requested editing scope. Do not disguise systemic identity/motion failures as a trivial post-production repair.
