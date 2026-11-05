---
name: xyq-project-workflow
description: Apply this user's project defaults when generating, resuming or delivering Xiaoyunque / 小云雀 video jobs through the official CLI. Covers model choice, reference modes, submission recovery and delivery. Official xyq skills remain online-installed external dependencies; this skill does not implement their API or authorize generation from a consultation.
metadata:
  version: "1.0.0"
---

# 小云雀项目视频工作流

这是用户自己的制作规则层。实际命令读取在线安装的官方 `xyq-skill`，按当前需求加载对应命令文档。用户本次明确要求、已确认素材和参数优先；不要因安装本技能而创建任务、上传素材或收费生成。

## 官方依赖与更新

- 官方来源：[Pippit-dev/cli](https://github.com/Pippit-dev/cli)。`xyq-skill`、`xyq-short-drama-skill`、`xyq-marketing-skill`、CLI 二进制和缓存不进入本人的技能源码、迁移包或 GitHub。正常本机运行安装可以保留；不要修改官方技能来存个人偏好。
- 新一轮小云雀执行任务开始时，联网检查官方稳定版与已安装版本；有更新时按官方入口更新 CLI 和配套技能。首次安装为 `npx @pippit-dev/cli@latest install`，当前稳定版更新入口为 `pippit-tool-cli update --channel stable`。执行前核对当前官方说明与帮助，不改用 canary。同一批任务复用已检查的版本，不在轮询中途升级。
- 官方技能的 `ensure-cli.js` 只确保所需命令可用，不等于已联网检查最新版本。记录实际 CLI 路径与版本，不固定旧电脑安装路径。更新失败时保留可用版本，说明本次未更新；按实际支持能力决定是否能继续，不能声称已经使用最新版。
- 按官方文档检查登录，复用有效授权。读取当前模型列表和目标模型详情，验证时长、比例、分辨率、参考模式与素材限制；不把历史例子的上限、版本、积分单价写成服务保证。
- 已有任务查询、取件优先恢复原任务；不为版本检查或文档变化重提已有任务。仅编写提示词或咨询方案不要求登录、上传或付费。

## 本人的执行默认

| 项目 | 规则 |
| --- | --- |
| 模型 | 小云雀视频默认 Seedance 2.0 Fast VIP，key `seedance2.0_fast_vision`；先验证当前可用性。 |
| 升级或重生成 | 效果不佳先交付并说明问题。用户确认后才换 Seedance 2.0 VIP / 2.5 或再次付费生成；模型不可用也不自动替换。 |
| 模式 | 默认沿用已确认的多参考。局部替换且用户要求锁定两端时使用首尾帧；不能只因有两张图就自动切模式。 |
| 画幅、时长、质量 | 沿用当前任务已确认值；不强制填满模型时长。不把某项目的 16:9、720p、15 秒或个人空间推广成所有任务默认。 |
| 空间 | 开始时确定实际空间并记录，上传、提交、查询、余额核对固定同一空间。已有任务沿用其原空间，不按积分自动换团队。 |
| 输出 | 当前 task 的 `out` 目录；原片、原始下载与后期预览分开保存。 |

需要细化提示词时先使用 `prompt-master`；复刻和衔接按其 [复刻参考](../prompt-master/references/video-recreation-continuity.md)，局部接回按 [替换参考](../prompt-master/references/video-local-replacement.md)。用户已批准的提交稿直接使用，不在执行阶段再翻译、润色或改变素材顺序。普通片段生成不自动转入短剧 Agent、营销 Agent 或 Canvas。

当前 CLI 的易混用之处（以后仍以已核对的官方接口为准）：

- 多参考使用 `--task-type reference`，素材路径按已确认顺序传入。
- 首尾帧使用 `--generate-type 1`，两个 `--image` 按首帧、尾帧顺序传入，不混入 `--task-type reference`。验证选定模型实际支持两端约束。
- 生成素材参数接收本地文件路径；URL、asset ID 的用法另查官方上传文档，不直接填进路径参数。宿主为 Codex 且接口支持时传 `--source codex`。

## 提交、恢复与交付

1. 读取当前任务入口与选定制作包，确认图片各自职责、顺序、提示词版本及输入模式。只在用户已授权范围内提交，已有授权不重复询问。
2. 提交前保存本次模型、实际版本、空间、时长、画幅、分辨率、提示词原文与有序素材路径；长任务可保存文件哈希。使用本地提交标记防止同一任务脚本误执行两次；标记本身不证明服务端提交成功。
3. 成功响应立即落盘真实 thread/run ID、空间和网页链接并交付链接。结果未知或本地落盘失败时保留原始响应，核查原任务；不能自动再提交一次收费任务。
4. 后续只轮询原 ID。按官方结果契约先检查错误，再检查是否结束及真实媒体；`completed=true`、退出码为零或拿到 URL 都不单独证明成功。查询或下载失败只恢复查询或下载，不重新生成。
5. 记录提交前后的同空间余额。无明细账单时报告“余额减少”，不要把差值写成永久单价；并发消费时说明不能准确归因。
6. 下载后检查文件存在、可完整解码、尺寸、时长、帧数、时间戳和音轨。抽查开始、关键动作、切镜和结尾；瞬时事件需加密抽帧或播放，粗联系表不足以断言未发生。分别记录技术通过、观察到的偏差和用户是否验收。
7. 最终交付可预览媒体、实际提示词、参考图与其文件夹完整绝对路径。任务记录保留模型、模式、任务 ID、参数、顺序、余额变化和未解决问题。更新唯一的当前执行入口，旧版本保留但标明被替代。

不因生成完成自动套用参考视频降规格、去音轨或成片首尾裁帧流程；这些处理由用户请求和适用技能决定。收费重试、模型升级、账号持久设置变更都不由质量检查自动触发。素材或版权审核失败按实际错误处理，必要时调用 `video-copyright-triage`；不能静默删参考、换剧情或反复付费试探。
