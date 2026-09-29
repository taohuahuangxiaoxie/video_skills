# 技能总索引

本仓库包含 **14 个顶层技能包、47 个技能入口**。按任务选择技能；整包安装不表示每次加载全部技能。

[安装与使用](README.md) · [包依赖](docs/INVENTORY.md) · [运行环境](docs/DEPENDENCIES.md) · [个人默认规则](preferences/AGENTS.fragment.md)

## 按任务查找

| 任务 | 首选入口 |
| --- | --- |
| 细化图片/视频提示词 | [Prompt Master](skills/prompt-master/SKILL.md) |
| 人物表情、换装发型和身份一致 | [FACS本地规则](skills/higgsfield-prompt-writing/skills/higgsfield-facs/SKILL.md) · [换装经验](skills/higgsfield-prompt-writing/skills/higgsfield-facs/references/wardrobe-identity-performance.md) |
| Seedance提示词 | [Prompt Master](skills/prompt-master/SKILL.md) → 按需补充[Seedance](skills/higgsfield-prompt-writing/skills/higgsfield-seedance/SKILL.md) |
| H3提示词 | [Prompt Master](skills/prompt-master/SKILL.md) → [H3格式](skills/h3-prompt-writing/SKILL.md) |
| 处理参考视频 | [24fps、等比低分辨率、无音轨](skills/video-reference-prep/SKILL.md) |
| 处理生成视频 | [首1尾3帧与生成元数据清理](skills/generated-video-finish/SKILL.md) |
| 生成深度参考 | [先预处理，再时序深度估计](skills/temporal-depth-reference/SKILL.md) |
| 视频生成版权拒绝 | [优先排查参考图片IP内容](skills/video-copyright-triage/SKILL.md) |
| 旧完整模仿流程 | [h3-video-mimic](skills/h3-video-mimic/SKILL.md)，仅显式调用 |

## 顶层技能包

| 包 | 用途 | 技能入口数 |
| --- | --- | --- |
| [prompt-master](skills/prompt-master/SKILL.md) | 提示词细化入口 | 1 |
| [higgsfield-prompt-writing](skills/higgsfield-prompt-writing/SKILL.md) | 表情、身份、摄影、Seedance 与相关子技能；保留完整依赖 | 34 |
| [video-reference-prep](skills/video-reference-prep/SKILL.md) | 参考视频：24fps、低分辨率、无音轨 | 1 |
| [generated-video-finish](skills/generated-video-finish/SKILL.md) | 成片：首1尾3、清理生成元数据 | 1 |
| [temporal-depth-reference](skills/temporal-depth-reference/SKILL.md) | 先预处理再生成真实时序深度 | 1 |
| [video-copyright-triage](skills/video-copyright-triage/SKILL.md) | 版权拒绝先排查图片IP内容 | 1 |
| [h3-prompt-writing](skills/h3-prompt-writing/SKILL.md) | H3模式与提示词格式 | 1 |
| [h3-comfyui-capacity-guide](skills/h3-comfyui-capacity-guide/SKILL.md) | 原工作站容量实测经验 | 1 |
| [cinematic-director](skills/cinematic-director/SKILL.md) | 镜头及导演层提示词 | 1 |
| [brand-promo-video-generator](skills/brand-promo-video-generator/SKILL.md) | 品牌宣传视频 | 1 |
| [minimalist-product-ad-generator](skills/minimalist-product-ad-generator/SKILL.md) | 简约产品广告 | 1 |
| [music-video-subtitle-generator](skills/music-video-subtitle-generator/SKILL.md) | 音乐视频及歌词字幕 | 1 |
| [h3-video-mimic](skills/h3-video-mimic/SKILL.md) | 旧模仿完整流程，仅显式调用 | 1 |
| [comfyui-shanghai-remote](skills/comfyui-shanghai-remote/SKILL.md) | 特定远程主机运维，仅明确请求时调用 | 1 |

## Higgsfield 子技能

下列子技能保留在同一包中以维持相对引用。当前本地父入口优先用于提示词；平台操作、上传和收费生成不因安装而自动获得授权。

| 子技能 | 中文说明 |
| --- | --- |
| [higgsfield-acting](skills/higgsfield-prompt-writing/skills/higgsfield-acting/SKILL.md) | 角色表演：动机、反应、动作节拍与眼神，按具体表演需要补充。 |
| [higgsfield-apps](skills/higgsfield-prompt-writing/skills/higgsfield-apps/SKILL.md) | Higgsfield 一键 Apps 的选择与使用指导。 |
| [higgsfield-assist](skills/higgsfield-prompt-writing/skills/higgsfield-assist/SKILL.md) | Higgsfield Assist 工作方式、效率与平台使用问题。 |
| [higgsfield-audio](skills/higgsfield-prompt-writing/skills/higgsfield-audio/SKILL.md) | 对白、口型、环境声、音效及音乐的提示词组织。 |
| [higgsfield-camera](skills/higgsfield-prompt-writing/skills/higgsfield-camera/SKILL.md) | 镜头运动、机位、景别及摄影描述。 |
| [higgsfield-canvas](skills/higgsfield-prompt-writing/skills/higgsfield-canvas/SKILL.md) | Higgsfield Canvas 节点画布和生成链路说明。 |
| [higgsfield-character-design](skills/higgsfield-prompt-writing/skills/higgsfield-character-design/SKILL.md) | 人物、世界和故事的前期设计与视觉设定。 |
| [higgsfield-cinema](skills/higgsfield-prompt-writing/skills/higgsfield-cinema/SKILL.md) | Cinema Studio 多镜头、光学设置与角色一致性工作流。 |
| [higgsfield-content-factory](skills/higgsfield-prompt-writing/skills/higgsfield-content-factory/SKILL.md) | 多条广告内容的规划、生产和活动流程；执行仍需对应授权。 |
| [higgsfield-facs](skills/higgsfield-prompt-writing/skills/higgsfield-facs/SKILL.md) | 自然表情与身份保持；含本地换装发型差异、笑意起落和切镜连续性规则。 |
| [higgsfield-gpt-image-2](skills/higgsfield-prompt-writing/skills/higgsfield-gpt-image-2/SKILL.md) | GPT Image 2 图片提示词、参考板和排版组织。 |
| [higgsfield-image-shots](skills/higgsfield-prompt-writing/skills/higgsfield-image-shots/SKILL.md) | 静态人物或场景图的构图、景别和取景。 |
| [higgsfield-marketing-studio](skills/higgsfield-prompt-writing/skills/higgsfield-marketing-studio/SKILL.md) | Marketing Studio 的广告预设与输入组织。 |
| [higgsfield-mixed-media](skills/higgsfield-prompt-writing/skills/higgsfield-mixed-media/SKILL.md) | 混合媒介、艺术化风格与预设组合。 |
| [higgsfield-models](skills/higgsfield-prompt-writing/skills/higgsfield-models/SKILL.md) | 模型选择与比较；具体规格和可用性需按当前平台核实。 |
| [higgsfield-moodboard](skills/higgsfield-prompt-writing/skills/higgsfield-moodboard/SKILL.md) | 情绪板、配色、视觉风格及跨图一致性。 |
| [higgsfield-motion](skills/higgsfield-prompt-writing/skills/higgsfield-motion/SKILL.md) | Higgsfield 动作、特效和转场预设描述。 |
| [higgsfield-motion-design](skills/higgsfield-prompt-writing/skills/higgsfield-motion-design/SKILL.md) | AI渲染广告短片、动态图形和品牌视觉的制作流程。 |
| [higgsfield-pipeline](skills/higgsfield-prompt-writing/skills/higgsfield-pipeline/SKILL.md) | 多镜头视频及不同工具之间的流程衔接。 |
| [higgsfield-prompt](skills/higgsfield-prompt-writing/skills/higgsfield-prompt/SKILL.md) | Higgsfield 提示词结构与图生视频、文生视频写法。 |
| [higgsfield-recall](skills/higgsfield-prompt-writing/skills/higgsfield-recall/SKILL.md) | 按适用范围检索既有失败和反馈记录；不替代当次用户要求。 |
| [higgsfield-recipes](skills/higgsfield-prompt-writing/skills/higgsfield-recipes/SKILL.md) | 动作、广告、舞蹈等类型的场景模板。 |
| [higgsfield-scene-engine](skills/higgsfield-prompt-writing/skills/higgsfield-scene-engine/SKILL.md) | 检查场景目标、障碍、转折与叙事结构。 |
| [higgsfield-seedance](skills/higgsfield-prompt-writing/skills/higgsfield-seedance/SKILL.md) | Seedance 镜头与参考素材描述、提示词结构和拒绝诊断。 |
| [higgsfield-seedance-2-5](skills/higgsfield-prompt-writing/skills/higgsfield-seedance-2-5/SKILL.md) | Seedance 2.5 的多模态参考与编辑提示词；不自动替换用户指定的2.0。 |
| [higgsfield-seedance-vfx](skills/higgsfield-prompt-writing/skills/higgsfield-seedance-vfx/SKILL.md) | 以现有视频为输入的特效、背景、光照等变化提示词。 |
| [higgsfield-shotlist-director](skills/higgsfield-prompt-writing/skills/higgsfield-shotlist-director/SKILL.md) | 将创意组织为连贯分镜、素材映射和可编辑镜头清单。 |
| [higgsfield-soul](skills/higgsfield-prompt-writing/skills/higgsfield-soul/SKILL.md) | 角色身份一致性；含本地多造型发型与表情连续性补充。 |
| [higgsfield-stack](skills/higgsfield-prompt-writing/skills/higgsfield-stack/SKILL.md) | Higgsfield CLI/MCP等执行接口的使用说明，按实际授权使用。 |
| [higgsfield-style](skills/higgsfield-prompt-writing/skills/higgsfield-style/SKILL.md) | 视觉风格、色调与影像质感描述。 |
| [higgsfield-troubleshoot](skills/higgsfield-prompt-writing/skills/higgsfield-troubleshoot/SKILL.md) | 生成失败、画面不符和质量问题的诊断。 |
| [higgsfield-vibe-motion](skills/higgsfield-prompt-writing/skills/higgsfield-vibe-motion/SKILL.md) | Vibe Motion 动态文字、图形和可编辑动画。 |
| [higgsfield-workspaces](skills/higgsfield-prompt-writing/skills/higgsfield-workspaces/SKILL.md) | 选择适合具体任务的Higgsfield工作区。 |

## 安装分组

| 分组 | 包数 | 用途 |
| --- | --- | --- |
| `core` | 6 | 提示词、表情和视频处理核心 |
| `h3` | 8 | 核心加H3 |
| `creative` | 10 | 核心加导演/广告/字幕 |
| `studio` | 12 | 日常创作推荐组合 |
| `legacy` | 1 | 旧模仿流程，自动补齐依赖 |
| `remote` | 1 | 特定远程主机，另配连接环境 |
| `all` | 14 | 全部技能包 |

表中分组包数为直接成员；选择单包或旧流程时，安装脚本还会补齐依赖。

本页由 `python scripts/build_index.py` 生成。用途数据来自 `manifest.json`，子技能中文描述来自 `docs/skill_descriptions.zh-CN.json`。
