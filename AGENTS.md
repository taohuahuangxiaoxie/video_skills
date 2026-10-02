# video_skills 仓库维护约定

- 本仓库保存创作 skills 的可迁移源码。顶层包数量以 `manifest.json` 为准；Higgsfield的子技能维持原相对目录，不要把子技能复制到顶层造成重复发现或断开引用。
- 修改规则时优先更新所属skill；跨技能触发偏好在 `preferences/AGENTS.fragment.md`。用户授权后才安装到其本机技能目录。不要从旧迁移ZIP或历史staging覆盖本仓库的新修改。
- 人物身份与发型、自然表情的详细规则集中在 `higgsfield-facs` 的本地规则及其 `references/wardrobe-identity-performance.md`；Prompt Master、Soul和父入口只保留必要路由。旧 `h3-video-mimic` 保持显式调用策略。
- 保留上游许可和作者信息；原工作站容量数字只是历史经验。不要把密码、账号配置、私钥、素材视频、模型权重或虚拟环境加入仓库。
- 文本采用UTF-8与LF。`manifest.json` 记录技能包原始字节的SHA-256，不能在刷新清单后单独改包内文件而不再次更新。
- 修改后按需运行 `python scripts/manage.py refresh --apply`、`python scripts/build_index.py`、`python scripts/manage.py verify`、`python scripts/build_index.py --check`。Python运行时由当前电脑提供。
- 新增顶层包要登记manifest中的用途、依赖与分组；新增子技能的中文描述写入 `docs/skill_descriptions.zh-CN.json`。`INDEX.md` 由脚本生成，不直接手改。
- 不将安装skill理解为授权外部上传、收费生成或远程操作。用户明确要求提交/推送时按其指定远端执行，不强推、不覆盖无关修改。
