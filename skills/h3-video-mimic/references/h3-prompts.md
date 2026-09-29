# Chinese H3 image-reference prompts

Read only after the H3 branch and its references are selected. Read the available `h3-prompt-writing` skill and select the actual input mode before choosing its guide; H3 is not another name for a Seedance prompt.

## Input-mode gate

- Ordinary character/scene/gesture role references use **Ref2VA**: read the full-reference guide and use the six fields below.
- For an exact first-and-last-frame request, verify whether the active local workflow uses native **FL2VA** or Ref2VA with actual supported frame bindings. Do not infer hard binding merely from two uploaded images or the words “first/last” in prose.
- Native **I2VA / FL2VA / L2VA** use the base-mode guide and its three fields: `integrated_multimodal_description`, `overall_soundscape`, `non_diegetic_music`. Describe the visible bridge between the supplied endpoints; do not wrap that prompt in Ref2VA's six-section schema.
- If Ref2VA genuinely provides the requested frame bindings on the selected surface, retain six fields and identify those picture-anchor roles explicitly.
- Keep the user's H3 choice. When the current workflow's binding capability is unknown, name what must be checked before the final handoff rather than promising an exact endpoint or silently switching engines/workflows.

The remaining six-section guidance applies to **Ref2VA only**. Base modes follow their selected guide instead.

## Ref2VA schema and mapping

Use these six English field names in this order, with Chinese contents unless requested otherwise:

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

- Define reusable visible content with `<Subject N>`, citing its source `<Picture N>` files. For example, the same person may come from Pictures 1–3 and the location from Picture 4.
- Only create a standalone picture definition when that image actually anchors a first/last frame, keyframe, or composition. Do not silently turn role references into keyframes.
- Resolve every label consistently. Image-only input has no `<Video N>` or `<Audio N>`; analysis of a source video does not mean it was uploaded.
- A separate map lists exact ordered absolute paths, labels, roles, retained/excluded attributes, and any actual shot/frame binding.
- Use `[reference generation]` for role-only reference generation. Use the appropriate combined task type only when genuine keyframe roles exist.
- One continuous take has one `[Shot 1]`; its timing phases are not extra shots. Follow the H3 guide's timestamp notation, using meaningful second/tenth-second beat targets rather than invented frame precision.

## Priorities and invariants

Identity/body continuity → scene/wardrobe/geometry → readable action with endpoint → camera path → expression change → light/hair/cloth → necessary sound and targeted failure constraints.

Keep identity, wardrobe, palette, and world-light facts in shared sections. In role mode, explicitly release pose and expression: character backgrounds are excluded, the scene exists from the opening, a gesture picture supplies hand shape rather than a forced final crop.

In hybrid production, describe **only the motion job**, never the later still-image sequence.

## Motion and performance

Read [motion-review.md](motion-review.md) for the shared camera, jump, smile, hand, and particle rules.

One primary action and a simple motivated camera are the low-risk default. A documented compound move requested by the user is an intentional exception: express one continuous path with clear phase boundaries instead of deleting it. For simple portraits, small 5–15 degree arcs may be enough; do not substitute those small arcs for a source whose visible orbit is important.

Keep buildings and sunlight fixed in world space while allowing camera-induced parallax. Hard cuts, if the source actually contains them, must be explicit and retain only the current shot's scene/wardrobe/props.

Allocate performance to the visible time:
- sub-second frames: one readable state, not a facial-acting sequence;
- brief full-body motion: posture, eyes, and broad action;
- final close-up: eye contact → corners/cheeks → lips part → the requested smile, then hold.

Do not impose a smile on every frame or suppress a user-requested bright smile through a blanket “closed mouth only” rule. A near-hand reference does not set the expression for the entire shot.

## Local preprocessing and troubleshooting

Structured prompting is a hand-authored input, not a claim to replicate H3 Context-IR. Do not promise that six headings or more detail restore a missing hosted preprocessing stage.

Separate:
1. omitted/contradictory instructions, e.g. “low jump” when the user wants a larger leap;
2. whether an explicitly requested pose occurs, e.g. calves folding backward while airborne;
3. timing/coordination naturalness after the pose is present;
4. model/workflow settings, only as verified for the actual run.

Preserve successful camera/identity/expression sections when revising a leg pose. Do not keep attributing defects to 4-step acceleration when the user's acceleration-off test gave no improvement. Conversely, a reported lack of improvement is not proof about every H3 checkpoint or preprocessing path.

For scene jumps in a one-take job, inspect reference-role conflicts and sequential full-scene image anchors before adding camera commands. Use fewer non-conflicting role assets if appropriate. For a genuinely dense montage, return to the production-mode/suitability gate.

## Audio and delivery

If silent output is requested, `overall_soundscape` explicitly requests silence and `non_diegetic_music` is `N/A`. Otherwise the soundscape covers only agreed ambience/foley; dialogue belongs at its event in the description under the full H3 rules.

Deliver the complete versioned prompt, exact picture map, action/generated/hold duration, and H3-only settings. Preserve older versions. An excerpt may explain a change, but is not the only usable prompt artifact.

Check the schema appropriate to the actual input mode (six fields for Ref2VA, three for base modes), all supplied-reference roles/bindings, one-take versus real cuts, time coverage, identity/scene invariants, actual airborne gesture timing, expression endpoint, and sound choice before handoff.
