# Hybrid imitation: short motion + photo montage

Read when a source combines one/few action clips with snapshots, posed photographs, photo pans/zooms, or a title image. This is a supported production mode, not a failed attempt at full-video imitation.

## Partition before generating

Create a complete interval table with: source range, visible content, `media_kind`, production method, asset/job ID, editing operation, and owner. Useful kinds are `motion`, `photo_hold`, `photo_editorial_move`, `transition`, and `title_card`; mark uncertain classifications for visual checking.

- **Motion:** generate a short clip from approved references and the chosen engine's prompt.
- **Photographs:** generate independent high-quality stills. Preserve source pose/expression/framing order; identity, body anatomy, light, and skin quality matter more than inventing motion.
- **Photo movement/transitions:** leave crop animation, scale, pan, timing, cuts, flashes, and blending to editing. Do not spend video generation on a photograph merely because the source editor zoomed it.
- **End-card:** create the still and, if requested, its text treatment as a separate version. Text can be placed in editing when exact spelling or editability is more important than generated typography.
- If the user says they will combine the assets, record `assembly_owner=user_editor`; the assistant's deliverable is the asset/prompt/edit-map package, not an automatically merged movie.

Do not infer that the first motion segment is exactly 3 seconds. Locate the actual end of its gesture/camera movement in the source. Separate source-action duration, generated duration, and trailing hold.

**Case example, not a default:** `task_qcws` used about 3.3 seconds of action in a 4-second generation, then a 0.7-second live pose hold. The rest was a photo montage. Future durations follow the inspected source and user choice. A held pose retains breath/hair settling; it is not an automatic frozen frame or repeat of the action.

## Plan the outputs

A typical approved plan contains:

1. one short motion job with a chosen engine/version, beat plan, ordered references, and complete prompt;
2. one independently generated still per required photograph, with repeated photos reused rather than regenerated;
3. any approved title-card variant, alongside its clean original;
4. an edit map listing clip/still order, source timings, crops/moves, duration/hold, and ownership.

Only motion jobs enter the video prompt. Still filenames and later montage instructions do not belong in the motion model's scene description.

## Reference set for the motion segment

Use the role-based branch in [reference-images.md](reference-images.md):

- front character view for identity, wardrobe, proportion, and relaxed closed lips;
- side or three-quarter view only where the body turn needs it;
- optional near-camera gesture view, e.g. hands forming a heart, for hand shape/perspective rather than a forced last frame;
- a separate empty location plate for world layout and light.

Use the minimum useful set; four files were useful in this case, not a fixed quota. White-background character references are extraction/identity assets, not white scenes to be displayed in the video. The location is present from the opening frame.

For the photo tail, generate **finished scene photographs**, not white-background character cutouts, unless the user explicitly plans to composite them.

## Image production and reuse

The main task writes exact image/edit prompts and reviews outputs. Follow the user's explicitly authorized new-task workflow; default standalone batches are 1–3 related stills per new task. Do not create empty tasks for images already approved. Keep output IDs and destinations stable across dispatch.

When removing a background from an approved image, first inspect it. Reuse through a background-only edit if face, body, pose, clothing, and lighting are already fit for the role. Regenerate if perspective, anatomy, identity, or framing is the actual defect; background removal cannot repair short-looking legs or an unsuitable camera angle. Generative edits can alter identity, so recheck the supposedly preserved face/hands afterward.

Refresh a changed prototype folder before dispatch. Track `reuse_from`, `supersedes`, and approval status so rejected earlier references do not silently re-enter the active set. Save every successful output before asking for revisions.

## Vertical and portrait QA

Use the requested aspect; for 9:16, plan the full pose and head/foot margins in the image rather than cropping a horizontal result. Check both identity and proportions: camera height, foreshortening, knee/ankle shape, weight bearing, and apparent leg length. Prefer a natural flattering view over anatomically implausible stretching or slimming.

Judge expressions at the source moment, not through a permanent smile. Preserve natural skin variation, believable face fill/rim light, stable hair roots, and fabric detail. A dynamic full-body frame and a final smiling close-up have different QA priorities.

For a requested title such as `the girl you never forgot`, inspect the source's actual last frame. Preserve the requested wording and deliberate case treatment, place it in usable negative space, check spelling/contrast/face clearance, and keep a no-text original. The title belongs to the final still, not automatically to the opening video.

## Completion gate

Deliver the approved asset set, complete model prompt, ordered role mapping, and concise edit map. Explicitly label missing/rejected assets. When the user owns editing, close at that handoff rather than scheduling generation or merging without a request.
