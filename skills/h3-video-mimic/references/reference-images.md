# Replacement images: roles, anchors, and finished stills

Choose the image's role **before** writing its generation prompt. An extracted source frame can inform pose/style without becoming a first/last frame fed to the video model.

## Role-based continuous-motion references

Default for a subject moving within one scene while the camera moves around/approaches them:

| Asset | Supplies | Does not lock |
| --- | --- | --- |
| Front character view | identity, wardrobe, natural proportions; relaxed closed lips when a late smile is planned | initial scene, standing pose, whole-clip expression |
| Side/three-quarter character view | face/profile, hair and body silhouette needed for a turn | another person or a separate shot |
| Optional close gesture view | hand shape, near-hand perspective, useful face detail | exact last frame, crop, camera endpoint, permanent smile |
| Empty scene plate | architecture, ground, vegetation, geography, light and palette | character identity, pixel-fixed background, single immutable camera position |

Use clean white backgrounds for this user's character-role assets unless the user chooses otherwise. The white is not part of the generated scene. The subject appears in the scene from frame one; all person views depict the same identity. Reference numbers denote input roles, not playback order.

Use a minimal useful set, not a mandatory three-view sheet or fixed four-image quota. Avoid contradictory poses, duplicate smiling close-ups, multi-panel layouts, or excess references that add no identity/geometry information. A gesture reference is optional and not synonymous with an end-frame constraint.

## Keyframe anchors and finished photographs

Use first/last-frame or shot-composition anchors when a specific endpoint, transition, opening composition, or hard-cut shot needs one. Name that role explicitly and verify support on the active surface. Do not apply the role-reference default to a user's explicit first/last-frame request.

For standalone montage photographs, generate the complete scene image with source-inspired pose, composition, wardrobe role, and lighting. These images go to the editor, not into the preceding video job.

## Build the image prompt

- Prototype evidence defines face geometry, identity, hair identity, and natural body proportions.
- Source frames define only the requested pose/blocking, setting, wardrobe role, perspective, light, or shot intention.
- State which source person is replaced. In multi-person frames, preserve mapping, left/right placement, gaze, contact, and limb ownership.
- Keep one compact identity lock and stable approved prototype set across related images.
- Use the requested aspect ratio. Do not carry the former 4:3 default into a 9:16 task.
- Preserve believable adult anatomy and natural skin/hair/fabric texture. Check head/neck/shoulder scale, arm and hand size, knees/ankles, weight bearing, and foreshortening.
- If legs appear short/thick, inspect camera height, crop, foreshortening, stance, and actual proportion before requesting changes. A flattering view is not permission to stretch limbs or distort anatomy.
- Keep scenic details local. A campus, petals, costume, or sun direction from one still must not leak into unrelated images.

## Reuse or regenerate

Inspect existing approved images first. Copy an already suitable asset into the active package, recording provenance; do not regenerate it because a new task was started.

For white-background variants, prefer a narrowly scoped background-only edit when the approved face, pose, hands, clothes, and perspective are already correct. Explicitly preserve those features and recheck them afterward; an image edit is not guaranteed pixel-preserving. Regenerate if identity, anatomy, angle, or framing is the defect.

Refresh the actual prototype files after a user update. Version revisions and record `supersedes`; do not restore a rejected early reference when a later approved one exists. Preserve clean no-text originals of title-card variants.

## New-task dispatch and QA

- The main task writes exact prompts, assigns IDs/paths, tracks progress, inspects outputs, and updates the active manifest. It does not generate images directly in this user's agreed workflow.
- Create new tasks only with explicit run-level authorization to do so. If tools or authority are missing, explain and ask for the necessary fallback; do not silently change the production contract.
- Use one new task per related video-reference group. For standalone montage stills, use batches of 1–3 related images unless the user requests another grouping. Dispatch only missing or revised assets.
- Every task receives exact prompts, ordered existing reference paths and roles, destination, no-overwrite instruction, and a request for final saved paths. Use the available image-generation/editing skill and tool inside that task.
- Every requested image revision uses a new task, not an appended prompt in the old task. User-requested parallel batches may run concurrently.
- Record task IDs and expected assets; wait for completion, verify saved files, copy successful outputs into the active run, then inspect before presenting them.
- Preserve approved assets even if other assets in the batch fail.

Review identity across views; body/hand anatomy; mapping and contacts; requested framing; scene/wardrobe/light; natural expressions, skin and hair; and unwanted text/background contamination. In role sets, additionally check role clarity and ensure the scene plate is empty. In finished stills, verify the intended pose/expression instead of applying a uniform smile.

Stop for manual review by default. Judge against the user's stated priorities, not an invented stricter aesthetic bar.
