# video_skills · 视频与人物创作技能库

用于人物参考图、换装舞蹈、Seedance / H3 提示词和视频预处理的个人 skills 仓库。包含 **16 个顶层技能包、49 个技能入口**，支持整组迁移、按需安装、依赖补齐和冲突备份。

**导航：** [技能总索引](INDEX.md) · [包与依赖](docs/INVENTORY.md) · [运行环境](docs/DEPENDENCIES.md) · [个人默认规则](preferences/AGENTS.fragment.md) · [验证记录](docs/VALIDATION.md) · [来源与许可](THIRD_PARTY_NOTICES.md)

## 常用入口

| 任务 | 技能 | 当前默认 |
| --- | --- | --- |
| 细化图片、视频和舞蹈提示词 | [prompt-master](skills/prompt-master/SKILL.md) | 沿用指定模型、素材、时长、画幅和语言 |
| 人物表情与多造型一致性 | [higgsfield-facs](skills/higgsfield-prompt-writing/skills/higgsfield-facs/SKILL.md) | 身份与发型分开；笑意自然起落，切镜不重置表情 |
| H3 提示词 | [h3-prompt-writing](skills/h3-prompt-writing/SKILL.md) | 按实际输入模式转换，保留动作与节奏 |
| 武侠／仙侠创意与剧本 | [wuxia-emotional-storytelling](skills/wuxia-emotional-storytelling/SKILL.md) | 人物选择串联钩子、情绪与结尾兑现 |
| 武侠／仙侠影像制作 | [wuxia-visual-direction](skills/wuxia-visual-direction/SKILL.md) | 唯美质感、机位微表情、素材衔接；生成素材不含配乐 |
| 处理参考视频 | [video-reference-prep](skills/video-reference-prep/SKILL.md) | 24fps、等比低分辨率、无音轨 |
| 处理生成视频 | [generated-video-finish](skills/generated-video-finish/SKILL.md) | 首1尾3帧、清理生成元数据；保留尺寸、帧间隔和同步音频 |
| 生成深度参考 | [temporal-depth-reference](skills/temporal-depth-reference/SKILL.md) | 先低分辨率24fps预处理，再真实时序深度估计 |
| 版权审核拒绝 | [video-copyright-triage](skills/video-copyright-triage/SKILL.md) | 优先检查参考图片中的可识别IP组合 |

以上是本人的工作偏好，用户当次明确要求优先。旧 `h3-video-mimic` 保持显式调用，不因“舞蹈模仿”关键词自动启动完整旧流程。

## 目录结构

```text
video_skills/
├── skills/                         # 16个顶层技能包，保留各自资源与许可
│   ├── prompt-master/
│   ├── higgsfield-prompt-writing/  # 父入口及33个子技能，保持相对目录
│   ├── h3-prompt-writing/
│   ├── video-reference-prep/
│   ├── generated-video-finish/
│   ├── temporal-depth-reference/
│   └── ...                        # 完整列表见INDEX.md
├── preferences/AGENTS.fragment.md # 可选合并的触发规则和个人偏好
├── scripts/manage.py             # 清单校验、选装、安装与备份
├── scripts/build_index.py        # 生成或检查中文技能索引
├── docs/                         # 依赖、清单、验证及中文描述数据
├── manifest.json                 # 分组、依赖、技能文件SHA-256
├── INDEX.md                      # 49个技能入口的中文索引
├── AGENTS.md                     # 本源码仓库的维护约定
└── THIRD_PARTY_NOTICES.md         # 保留上游作者与已有许可
```

## 在新电脑安装

需要 Git 和 Python 3.10+。`python` 指当前机器可用的 Python；Windows 也可使用 `py`。普通迁移脚本只依赖 Python 标准库。

```powershell
git clone https://github.com/taohuahuangxiaoxie/video_skills.git
cd video_skills
python scripts/manage.py verify

# 先预览：不写入本机技能目录
python scripts/manage.py install --profile studio --with-rules

# 确认预览符合需要后执行
python scripts/manage.py install --profile studio --with-rules --apply
```

默认安装到 `$CODEX_HOME/skills`，未设置时为用户目录下的 `.codex/skills`，与本仓库来源环境一致。`--with-rules` 将个人规则合并到上级 `AGENTS.md` 的受管区块，保留其他内容；不加此参数只安装技能。完成后开启新对话；若尚未发现技能，重新打开应用。

| 分组 | 顶层包数 | 适用范围 |
| --- | --- | --- |
| `studio` | 14 | 推荐日常创作：核心、H3、导演、广告、字幕和武侠短片 |
| `core` | 6 | 提示词、表情、版权和三类视频处理 |
| `h3` | 8 | 核心加H3提示词和容量经验 |
| `creative` | 12 | 核心加导演、广告、字幕和武侠短片 |
| `all` | 16 | 全部，含旧模仿流程和特定远程主机技能 |
| `wuxia` | 2 | 武侠／仙侠情绪故事与影像制作，可不安装通用创作包 |
| `legacy` / `remote` | 1起 | 单独选择旧流程或远程技能，自动补齐所需依赖 |

选择单个顶层技能包：

```powershell
python scripts/manage.py install --skill generated-video-finish --apply
```

该例会同时安装 `video-reference-prep` 共享脚本。不要只拷贝一个 `SKILL.md`，也不要把Higgsfield的子技能拆出或重复安装。

已有同名但不同内容的技能时，默认停止覆盖。查看预览后可加 `--replace`；原文件备份到安装目录上级的 `skill-migration-backups/`，不删除无关技能。`--dest <技能目录>` 可改安装位置；同时合并工程规则时使用 `--with-rules --rules-target <工程路径>/AGENTS.md`。

## 迁移范围

已包含技能文本、辅助脚本、模板、共享资源、触发规则及本轮经验。人物原型、服装和场景图、原片成片、ComfyUI模型与工作流、FFmpeg、虚拟环境、深度模型源码和权重、账号及SSH凭据需另行配置。系统或插件提供的imagegen等能力由目标应用提供。

视频脚本支持 `COMFYUI_WORKSPACE`、`FFMPEG`、`FFPROBE` 和显式命令参数。深度脚本还支持独立指定模型源码与权重。具体见[运行环境](docs/DEPENDENCIES.md)。远程主机连接约定和硬件容量数字来自原工作站，迁移后应按实际环境核对。

## 更新和维护

本仓库是后续版本管理入口。旧 `comfyui-skills` 目录和迁移ZIP为2026-09-29的导出快照；如已安装目录又有修改，先比较并同步到本仓库，避免旧副本覆盖新经验。

```powershell
# 更新已有技能后重建校验清单及索引
python scripts/manage.py refresh --apply
python scripts/build_index.py
python scripts/manage.py verify
python scripts/build_index.py --check
git diff --check
```

新增顶层包要登记 `manifest.json` 中的用途、依赖和分组；新增Higgsfield子技能需补充 `docs/skill_descriptions.zh-CN.json`。保持UTF-8/LF文本格式，保证Windows与其他环境检出后的文件哈希一致。

本轮发型与表情规则集中在[换装身份与表情参考](skills/higgsfield-prompt-writing/skills/higgsfield-facs/references/wardrobe-identity-performance.md)，并接入FACS、Soul、Prompt Master及个人触发规则。编辑旧提示词时需替换“全程微笑、持续露齿”等冲突句。

本仓库保留混合来源的原作者与许可，不作统一重新授权；具体见[来源与许可](THIRD_PARTY_NOTICES.md)。文件清单校验验证复制完整性，不能代替目标机器依赖配置及实际画面验收。
