# Intake, source analysis, and production partition

## Run layout

Keep the existing run when resuming. For new runs, use:

```text
mimic_run_NNN/
  00-analysis/
  01-keyframes/source/
  02-cast/
  03-reference-prompts/
  04-reference-images/
  04-script/
  05-h3-prompts/          only when H3 is used
  05-seedance-prompts/    only when Seedance is used
  06-preview-notes/
  07-video-output/        legacy 07-h3-output is also valid
  08-final/
  99-metadata/
```

Create only relevant directories. Use explicit IDs, e.g. `H3-01`, `SD20-01`, `SD25-01`, `STILL-01`. Preserve legacy IDs and files; never rename a run just to fit this layout. Source extraction frames are analysis evidence, not an automatic generator keyframe list.

## Source analysis

1. Use FFprobe to record duration, exact video duration, frame rate, dimensions/aspect, streams, and audio. Prefer available project FFmpeg binaries.
2. Detect candidate cuts, then visually inspect dense contact sheets and boundary frames. Thresholds can miss fades or mistake flashes for cuts.
3. For each interval record source start/end, cast, location, clothing, framing, camera, main action, expression, light, sound, and representative frame. Add `media_kind`: live/generated motion, photo hold, photo editorial pan/zoom, transition, title-card, or uncertain.
4. Distinguish whole-frame photo scaling from subject motion and true perspective change. Check local body/hair motion and near/far parallax; do not classify a still solely from a scene-score threshold.
5. Locate where the action actually finishes, including a final approaching hand. Record source-action duration separately from the requested generation length and trailing hold.
6. Separate music from ambience/foley/dialogue. Transcribe only audible dialogue the user wants recreated; do not copy or generate source music by default.

Use second/tenth-second precision in the review. Keep exact frame/timestamp values in extraction/assembly metadata, not as false prompt precision. Mark uncertain observations as uncertain.

## Cast and prototypes

- Inventory recurring identities and map each to actual prototype files. Ask one concise mapping question only if ambiguous.
- After the user updates a prototype directory, list it again. Replace stale references to removed MP4s/images; preserve already approved useful outputs.
- Keep a small consistent set of front, three-quarter, and profile evidence. Do not average different identities.
- Replace identity while retaining source pose intention, screen direction, relationships, and clothing role unless the user changes them or the pose is anatomically implausible.
- Define identity preservation, flattering but natural body proportions, expression naturalness, and light/texture as separate QA axes.

## Partition and route

Read the production-mode gate in `SKILL.md`. For `hybrid_motion_stills`, read [hybrid-motion-stills.md](hybrid-motion-stills.md) before grouping anything for a video model.

Present the approved partition as source range → motion job / still asset / editorial operation, plus owner. Do not collapse or omit photo shots to fit a video-model quota. If the source is genuinely dense motion, disclose every proposed consolidation.

Choose the engine for the motion part only. For orbit + quick turn/jump, recommend Seedance as this user's empirical preference, then record the version/surface the user accepts. Preserve an explicit H3 choice and route its parameters only into H3 jobs.

For continuous character motion with camera parallax, plan role references. Reserve first/last-frame or composition anchors for an actual endpoint/transition requirement.

## Grouping actual motion

- Split on real cuts, environment/wardrobe changes, or meaningful continuity boundaries, not equal seconds.
- Preserve shot order and relative rhythm.
- For H3 only: jobs at most 15 seconds, normally 3–7 useful references, with seven the tested local ceiling rather than a universal specification.
- For Seedance: verify the chosen version/surface's supported duration and inputs when writing the actual handoff. Do not inherit H3's image count, pixel multiplier, or workflow.
- If the supported generated length exceeds the action, plan a natural endpoint hold or an explicitly trimmed handle. Do not automatically slow the action to fill the extra time.

## Deliverables and memory

Keep the probe, shot inventory, style/motion analysis, cast map, extraction manifest, Chinese script, production partition, and run manifest. Names may retain existing H3-specific history; new documents should identify the actual engine.

Add these routing fields to the manifest without deleting legacy fields:

```text
production_mode: motion_video | hybrid_motion_stills | dense_montage
requested_engine / selected_engine / engine_version / execution_surface
reference_strategy: role_references | keyframe_anchors | authorized_video_reference
aspect_ratio
assembly_owner: user_editor | assistant_ffmpeg
external_image_upload_authorized / image_task_creation_authorized
motion_jobs: source_range, action_duration, generated_duration, hold_duration,
             prompt_path, reference_map, review_state
stills: source_range, asset_id, path, edit_operation, review_state,
        reuse_from, supersedes
next_gate
```

This is a field guide, not a required schema migration or permission grant. Store observations separately from user reports and hypotheses. Record script direction as visible behavior and camera geometry, not a list of emotional adjectives.
