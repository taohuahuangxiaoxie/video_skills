# 技能清单

快速浏览用途和技能入口，请看[技能总索引](../INDEX.md)。

本仓库有20个顶层安装包，Higgsfield保留33个子技能，共53个SKILL.md。

| 安装包 | 用途 | 直接依赖 | 入口数 |
| --- | --- | --- | --- |
| prompt-master | 提示词细化入口 | higgsfield-prompt-writing, video-copyright-triage | 1 |
| higgsfield-prompt-writing | 表情、身份、摄影、Seedance 与相关子技能；保留完整依赖 | 无本包硬依赖 | 34 |
| video-reference-prep | 参考视频：24fps、低分辨率、无音轨 | 无本包硬依赖 | 1 |
| generated-video-finish | 成片：首1尾3、清理生成元数据 | video-reference-prep | 1 |
| temporal-depth-reference | 先预处理再生成真实时序深度 | video-reference-prep | 1 |
| video-copyright-triage | 版权拒绝先排查图片IP内容 | 无本包硬依赖 | 1 |
| h3-prompt-writing | H3模式与提示词格式 | prompt-master | 1 |
| h3-comfyui-capacity-guide | 原工作站容量实测经验 | 无本包硬依赖 | 1 |
| cinematic-director | 镜头及导演层提示词 | 无本包硬依赖 | 1 |
| brand-promo-video-generator | 品牌宣传视频 | 无本包硬依赖 | 1 |
| minimalist-product-ad-generator | 简约产品广告 | 无本包硬依赖 | 1 |
| music-video-subtitle-generator | 音乐视频及歌词字幕 | 无本包硬依赖 | 1 |
| h3-video-mimic | 旧模仿完整流程，仅显式调用 | prompt-master, h3-prompt-writing, h3-comfyui-capacity-guide, video-reference-prep, generated-video-finish, temporal-depth-reference | 1 |
| comfyui-shanghai-remote | 特定远程主机运维，仅明确请求时调用 | 无本包硬依赖 | 1 |
| wuxia-emotional-storytelling | 武侠仙侠人物创意与剧本：钩子、人物选择和情绪兑现 | 无本包硬依赖 | 1 |
| wuxia-visual-direction | 武侠仙侠影像制作：唯美质感、机位表演和可剪素材 | 无本包硬依赖 | 1 |
| action-choreography-reference | 动作与武器物理、受力接触、群战衔接参考 | 无本包硬依赖 | 1 |
| cinematic-audiovisual-language | 影视镜头语法、连续性、运镜与声画节奏 | action-choreography-reference | 1 |
| master-shot-camera-planning | 由关键画面反推空间关系、机位与切镜路线 | cinematic-audiovisual-language | 1 |
| seedance-2-5-fight-director | Seedance 2.5 战斗剧本、动作波段与可执行提示词 | action-choreography-reference, cinematic-audiovisual-language, higgsfield-prompt-writing | 1 |

`wuxia-production`适用于武侠战争和Seedance 2.5制作；`studio`用于日常多类型创作。技能内部提及但未随包提供的其他专家技能按实际安装情况使用，不应声称已安装。

系统/插件内置的imagegen等工具由目标应用提供。这里只迁移技能源码，不含账号、素材、模型或生成权限。
