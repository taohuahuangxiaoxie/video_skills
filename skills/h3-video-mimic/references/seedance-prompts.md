# Seedance branch for dynamic imitation

Read when Seedance is selected, particularly orbiting cameras with quick turns/jumps and lively performance. In this workflow `SD` refers to Seedance. Preserve the user's exact version and execution surface: 2.0 and 2.5 are not interchangeable labels.

## Select the dialect, not just the model name

For actual prompt delivery, read the available `higgsfield-seedance` skill for 2.0 or `higgsfield-seedance-2-5` for 2.5. Apply only the guidance relevant to the active surface; verify current duration/input limits if needed. Generic shot-craft defaults must not erase the user's explicit single-take compound camera move, Chinese prompt, or chosen duration.

If those skills are unavailable, retain the concrete role/action/camera plan below and verify the active model's documented reference syntax. Do not invent an API, camera preset, parameter, or upload role.

Do not paste H3's six fields or `<Subject N>` tokens into Seedance. Use the actual surface's image handles, typically `@Image1` etc., matching exact uploaded order. Do not relabel an earlier 2.5 output as 2.0.

## Required deliverable

Provide a complete Chinese prompt plus an ordered asset-role map and a compact settings header: engine/version/surface, duration, aspect, selected reference mode, and sound choice. Preserve the user's generated length; identify action end and trailing hold separately.

Use character identity + side view + optional gesture + separate empty scene for continuous character/camera motion, unless an actual first/last-frame requirement overrides it. Explicitly exclude white character backgrounds and reference playback order. A gesture reference is not a mandatory end frame.

Keep one scene and one shot. Assign each text block a purpose: roles, continuous camera path, connected action/performance, light and restrained secondary motion. Positive world and identity locks are preferable to a long negative list.

Read [motion-review.md](motion-review.md) for:
- world-fixed architecture with camera-induced parallax;
- short orbit with slight initial pull-back, then approach, then straight final push;
- airborne calf retraction when requested, followed by pre-landing extension;
- late gradual smile and near-camera hand perspective;
- pose compliance versus naturalness, and conservative attribution of platform effects.

## Worked 4-second example

This is an adaptable **draft**, not a newly tested generation. It illustrates the `task_qcws` scene: about 3.3 seconds of action plus 0.7 seconds held pose, vertical framing, four role images. Do not impose its clothes, campus, timings, jump style, petals, or orbit angle on other sources.

Header outside the prompt: selected Seedance version; 4 seconds; 9:16; image-role references; silent. Match the surface's actual image-handle spelling before use.

```text
单人校园短镜头，一镜到底，正常实时速度，整体明朗、欢快、有青春活力。

参考用途：@Image1 定义人物正面身份、服装与自然体型；@Image2 补充同一人的侧脸和身体轮廓。@Image3 只参考双手心形及近手透视，表情按动作发展，不绑定末帧。前三张的白底不进入画面。@Image4 是全片唯一校园，保留建筑、樱花树、道路和日光方向；人物从开场就在校园中。四图按用途取材，不按顺序展示。

摄影机前2秒沿人物前方从左向右走约45–60度短弧线，先稍向外退，露出完整全身，再沿同方向平滑收近，跳起和落地时头顶、双腿与鞋部完整可见。建筑与树木固定在校园空间，随摄影机移动产生连贯视差，地平线保持水平。到人物落地时结束环绕，之后只正面直线推进，到3.3秒停住。

前约1秒，人物从半侧身利落转身约一圈，收势后朝向镜头，嘴唇轻合、嘴角放松。随后短促屈膝蹬地跳起，双臂打开；腾空后自然弯膝，小腿向身后收起，落地前再伸脚回到身体下方并屈膝缓冲，约2秒站稳。头发、缎带和裙摆稍滞后于身体扬起，再自然回落。

落地后持续看向镜头，双手先在胸前合成心形，再连续送近镜头，身体稍前靠。笑容由嘴角轻轻上扬开始，随后脸颊抬起、嘴唇自然分开，逐渐露出上排牙齿，到3.3秒展开甜美灿烂的笑容，眼睛明亮、下颌放松。摄影机推进使双手逐渐放大为柔焦前景，心形中央保留清晰眼睛和笑脸。

最后0.7秒保持近镜比心、甜笑和对视，仅有呼吸与发梢余动。春日日光勾亮发丝，面部柔和明亮，保留皮肤与衣料细节。少量花瓣从画面边缘飘落，面部和心形中央通透。同一人物、同一服装、同一场景，连续拍摄。全片静音，无字幕。
```

## Review before handoff

- Version, surface, duration, aspect and reference map agree.
- Only supplied/authorized image references appear; no fictitious uploaded video.
- Timing stages belong to one take, not `Shot 1/2/3` cut instructions.
- Roles define identity/location/gesture without freezing all poses or expressions.
- The motion phase does not include the later photo montage or title artwork.
- The complete prompt replaces the previous one; do not append a fix to a conflicting old block.
- State that this is a prompt proposal unless the user has actually approved a generated result.

Seedance is the preferred trial for this user's dynamic scenario, not a promise of a perfect take. Preserve and judge usable outputs rather than assuming a preview can be exactly recreated at a different resolution or setting.
