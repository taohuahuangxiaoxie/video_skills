"""Build the Chinese skill index from the manifest and curated descriptions."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def render():
    manifest = json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    descriptions = json.loads((ROOT/'docs/skill_descriptions.zh-CN.json').read_text(encoding='utf-8'))
    packages = manifest['packages']
    total = sum(p['skill_entries'] for p in packages)
    lines = ['# 技能总索引', '',
             f'本仓库包含 **{len(packages)} 个顶层技能包、{total} 个技能入口**。按任务选择技能；整包安装不表示每次加载全部技能。', '',
             '[安装与使用](README.md) · [包依赖](docs/INVENTORY.md) · [运行环境](docs/DEPENDENCIES.md) · [个人默认规则](preferences/AGENTS.fragment.md)', '',
             '## 按任务查找', '',
             '| 任务 | 首选入口 |', '| --- | --- |',
             '| 细化图片/视频提示词 | [Prompt Master](skills/prompt-master/SKILL.md) |',
             '| 人物表情、换装发型和身份一致 | [FACS本地规则](skills/higgsfield-prompt-writing/skills/higgsfield-facs/SKILL.md) · [换装经验](skills/higgsfield-prompt-writing/skills/higgsfield-facs/references/wardrobe-identity-performance.md) |',
             '| Seedance提示词 | [Prompt Master](skills/prompt-master/SKILL.md) → 按需补充[Seedance](skills/higgsfield-prompt-writing/skills/higgsfield-seedance/SKILL.md) |',
             '| H3提示词 | [Prompt Master](skills/prompt-master/SKILL.md) → [H3格式](skills/h3-prompt-writing/SKILL.md) |',
             '| 武侠／仙侠人物创意与剧本 | [人物选择、钩子与情绪兑现](skills/wuxia-emotional-storytelling/SKILL.md) |',
             '| 武侠／仙侠影像制作 | [唯美质感、机位表演与分段衔接](skills/wuxia-visual-direction/SKILL.md) |',
             '| 处理参考视频 | [24fps、等比低分辨率、无音轨](skills/video-reference-prep/SKILL.md) |',
             '| 处理生成视频 | [首1尾3帧与生成元数据清理](skills/generated-video-finish/SKILL.md) |',
             '| 生成深度参考 | [先预处理，再时序深度估计](skills/temporal-depth-reference/SKILL.md) |',
             '| 视频生成版权拒绝 | [优先排查参考图片IP内容](skills/video-copyright-triage/SKILL.md) |',
             '| 旧完整模仿流程 | [h3-video-mimic](skills/h3-video-mimic/SKILL.md)，仅显式调用 |', '',
             '## 顶层技能包', '', '| 包 | 用途 | 技能入口数 |', '| --- | --- | --- |']
    for package in packages:
        lines.append(f"| [{package['name']}]({package['path']}/SKILL.md) | {package['role']} | {package['skill_entries']} |")
    lines += ['', '## Higgsfield 子技能', '',
              '下列子技能保留在同一包中以维持相对引用。当前本地父入口优先用于提示词；平台操作、上传和收费生成不因安装而自动获得授权。', '',
              '| 子技能 | 中文说明 |', '| --- | --- |']
    discovered = set()
    for f in sorted((ROOT/'skills/higgsfield-prompt-writing/skills').glob('*/SKILL.md')):
        name=f.parent.name
        if name not in descriptions: raise ValueError(f'Chinese description missing: {name}')
        discovered.add(name)
        lines.append(f'| [{name}]({f.relative_to(ROOT).as_posix()}) | {descriptions[name]} |')
    if discovered != set(descriptions): raise ValueError('Description catalog contains obsolete entries')
    lines += ['', '## 安装分组', '', '| 分组 | 包数 | 用途 |', '| --- | --- | --- |']
    labels={'core':'提示词、表情和视频处理核心','h3':'核心加H3','creative':'核心加导演/广告/字幕/武侠短片','studio':'日常创作推荐组合','wuxia':'武侠仙侠故事与影像制作','legacy':'旧模仿流程，自动补齐依赖','remote':'特定远程主机，另配连接环境','all':'全部技能包'}
    for name,members in manifest['profiles'].items():
        lines.append(f'| `{name}` | {len(members)} | {labels.get(name,name)} |')
    lines += ['', '表中分组包数为直接成员；选择单包或旧流程时，安装脚本还会补齐依赖。', '',
              '本页由 `python scripts/build_index.py` 生成。用途数据来自 `manifest.json`，子技能中文描述来自 `docs/skill_descriptions.zh-CN.json`。', '']
    return '\n'.join(lines)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    target=ROOT/'INDEX.md';content=render()
    if args.check:
        if not target.exists() or target.read_text(encoding='utf-8')!=content:
            raise SystemExit('INDEX.md is outdated. Run python scripts/build_index.py.')
        print('Skill index is up to date.')
    else:
        target.write_text(content,encoding='utf-8',newline='\n')
        print('Updated INDEX.md')

if __name__=='__main__': main()
