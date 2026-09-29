# Continuous camera, performance, and evidence-driven revision

Read for compound movement, weak/unnatural actions, persistent smiles, scene jumps, or comparative model feedback. These are shot-craft and case-derived heuristics, not guaranteed model controls.

## Separate three kinds of movement

1. **Subject:** body turn direction, start/end orientation, gesture phase, and ground contact.
2. **Camera:** path around the subject, lateral direction, distance change, framing, and the point where a move ends.
3. **World/secondary motion:** buildings and trees fixed in world space; hair, cloth, and sparse particles respond to forces.

An orbit should create continuous parallax: near and distant objects shift differently. Do not say both “orbit the subject” and “background pixels remain fixed.” Keep the horizon level and the light direction world-locked; the environment is not a rotating disc.

## Compound path when the source needs it

One simple camera move is the low-risk default, not a reason to erase explicitly requested choreography. For an orbit plus pull-back/push-in, write one continuous path with ordered phases:

- opening: a short single-direction arc while pulling back slightly, revealing the full body;
- middle: continue the same arc, smoothly reduce the distance while retaining feet/head during the jump;
- before the final hand gesture: end lateral orbit; align to the subject;
- ending: advance only along the viewing axis, settle at the intended close-up, then hold.

Specify what the finished frame shows. Physical approach changes near/far perspective; “zoom in” alone may only enlarge the picture. Avoid simultaneous contradictory operations, repeated reversals, full-circle demands where a short arc suffices, and unrelated pan/roll/shake effects.

An angle such as 45–60 degrees is a directorial proposal unless measured from evidence, not an exact reconstruction. Keep temporal phases broad enough to read; timestamps are guidance, not deterministic animation commands. A continuous take has one shot label, not a new “shot” for every beat.

## Action presence, pose, and naturalness are separate

Diagnose the exact missing feature before writing “more powerful”:

- **Event absent:** did she leave the ground, or only lift her feet/knees?
- **Pose absent:** did the requested calf retraction occur while airborne, rather than only at takeoff/landing?
- **Coordination weak:** are hip rise, knee flexion, arm swing, acceleration, landing weight, and secondary motion timed together?
- **View conceals it:** can the camera see the rearward calf silhouette, or does the frontal view hide it? Propose a small body/view adjustment only when needed; do not silently replace otherwise approved camera work.

For the requested playful backward-leg jump, a compact clause is:

> 双脚离地后，双膝自然弯曲，小腿向身后收起、脚跟抬向臀部；落地前展开小腿，让双脚回到身体下方，再屈膝缓冲。

This is a pose variant, not a requirement for every jump. Do not substitute “jump higher,” a knee-to-chest tuck, back-arching contortion, or knees locked through flight. Do not add arbitrary joint angles, exact forces, or millisecond schedules unless they clarify a genuine defect.

A correct pose does not prove natural transitions. When calf retraction appears but the motion remains stiff, preserve that successful instruction and compare the actual takeoff/flight/landing sequence before expanding the prompt.

## Expression and close-hand timing

- Do not let a smiling close-up reference fix the expression for the entire video.
- For a late sweet smile, begin with relaxed closed lips. Eye contact arrives first; then mouth corners lift, cheeks rise, lips part enough to reveal upper teeth, and the eyes soften while remaining attentive.
- Locate this transition near the end of the action, not inside a sub-second distant spin/jump. Preserve the user's intended bright smile rather than universally restricting every shot to a tiny smile.
- Complete the hand shape at chest level before sending it toward the camera. Keep hand growth continuous through perspective; preserve a clear face through the opening when that is the intended framing.
- Stop the forward hands and camera together at the hold; retain subtle breathing and settling hair.

## Hair and particles

Hair/ribbons/skirt trails follow body acceleration, continue briefly after a stop, then settle. Keep roots and the main hair mass coherent. Do not combine a fast spin with a separate strong wind, elaborate particle vortex, and multiple hair instructions unless those effects are actually required.

Use a few petals at the edges, drifting under gravity and a consistent breeze. Keep the face and gesture clear; do not use a petal wipe to disguise a scene change in an intended continuous take.

## Bounded feedback loop

1. Preserve the full prompt/reference version and exact reported settings.
2. Name what already works and the one concrete failure. Distinguish user report from frame inspection.
3. Check whether the desired behavior was actually requested. “Calves do not retract” is not proof of inability if the prompt only said “jump.”
4. Revise the failing layer only; replace contradictory wording instead of appending more restrictions. Keep camera/identity/expression unchanged when they are working.
5. Compare the same input set and, where exposed, the same seed/settings. A seed does not make outputs comparable across different model families. Do not promise that a cheap preview will reproduce the identical final take.
6. Once the instruction is followed, separately judge naturalness and consistency. If repeated targeted trials have little benefit, recommend the working engine or request the paired clips for phase-by-phase comparison; do not prescribe endless prompt growth.

Do not change workflow settings, execute a new generation, or generate new reference images merely because feedback was reported.

## Case evidence: task_qcws, 2026-09-09

User-reported observations, not a controlled paired-video benchmark:

- Sequential full-scene action images produced an obvious scene change in an intended single take. The subsequent design separated white-background character views, a gesture reference, and an empty campus plate. This is a justified reference-role strategy, not proof that it eliminates all cuts.
- The user preferred Seedance 2.0's camera/action naturalness to the local H3 results for this lively short clip. Earlier prompt files targeted Seedance 2.5; preserve that distinction rather than assigning every result to 2.5.
- More explicit force/camera wording gave little reported improvement. Turning off 4-step acceleration also gave no reported improvement. Do not keep blaming acceleration or claim this proves identical behavior for every full-precision workflow.
- Earlier H3 wording requested “low/light jump” or omitted the airborne leg shape. Explicit post-takeoff calf retraction subsequently made that pose appear; the user still found the whole motion less natural than Seedance.
- Therefore separate instruction omission, pose compliance, timing naturalness, and current system performance. Do not conclude an absolute H3 capability ceiling from an underspecified instruction.
- Platform prompt enhancement and H3 Context-IR were discussed, but their contribution was not isolated. Do not claim either is present/absent in a particular run or that reproducing a structured text format reproduces the official preprocessing system.

Retain these narrow observations for routing and test design. A user reporting that “other aspects are fine” narrows the repair; it is not authorization to overhaul the whole shot.
