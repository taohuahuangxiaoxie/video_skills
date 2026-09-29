# 技能清单

快速浏览各技能中文说明和点击入口，请看[技能总索引](../INDEX.md)。本页侧重顶层安装包与依赖。

本包有14个顶层安装目录，包含Higgsfield的33个子技能，共47个SKILL.md。目录依赖保留，不重复安装展开后的同名子技能。

| 安装包 | 用途 | 直接依赖 | 子目录内SKILL数（含入口） |
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

`studio`是建议的新电脑日常组合；`all`包含旧流程与远程主机约定。技能安装不代表自动使用所有技能。

系统/插件内置的imagegen、skill-creator及浏览器/文档等能力应由目标应用提供。本次未打包与该工程无关的microgrid-workspace，也未复制历史skills-sync副本。
