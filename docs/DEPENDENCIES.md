# 迁移依赖与配置

## 文本及生图

Prompt Master、FACS、H3 提示词及导演指导可读取 Markdown 使用。真正生图仍依赖目标环境的图像工具；技能文件不携带账号、工具授权或平台额度。Higgsfield 中平台专用子技能按实际任务和可用工具使用，模型规格快照需按任务核验时效。

## 普通视频处理

需要 Python 3.10+、FFmpeg 和 FFprobe。转码脚本仅用 Python 标准库。

```powershell
$env:COMFYUI_WORKSPACE = 'D:\work\comfyui'
$env:FFMPEG = 'D:\tools\ffmpeg\bin\ffmpeg.exe'
$env:FFPROBE = 'D:\tools\ffmpeg\bin\ffprobe.exe'
```

这些是示例位置，按新电脑实际安装修改；以上变量只在当前终端有效，也可设置为用户环境变量。参数 `--ffmpeg` / `--ffprobe` 优先；PATH 或工程 `tools/ffmpeg/bin` 也可用。

```powershell
python <技能目录>/video-reference-prep/scripts/video_ops.py reference input.mp4 --output reference.mp4
python <技能目录>/video-reference-prep/scripts/video_ops.py finish output.mp4 --output finished.mp4
```

参考预处理默认为24fps、等比低分辨率、无音轨；成片处理保留原分辨率、逐帧时间和同步音频，仅首1尾3帧及元数据处理。不能互相混用。

## 真实时序深度

在目标机器另行安装 Video Depth Anything 官方源码及 Small/vits 权重，重建可用 Python 环境；不复制原 `.venv`。该脚本使用 CPU/float32，需要 torch、numpy、opencv-python 和官方模型推理依赖。依赖版本按官方源码及目标 Python/PyTorch 环境解决，不能保证一份虚拟环境跨系统可用。

默认相对工程位置：

```text
tools/depth/source/Video-Depth-Anything-main/
tools/depth/checkpoints/video_depth_anything_vits.pth
```

可通过 `--workspace`、`--model-root`、`--checkpoint` 指定其他位置。调用时使用已经安装依赖的 Python：

```powershell
python <技能目录>/temporal-depth-reference/scripts/make_depth.py input.mp4 --output depth.mp4 --workspace D:/work/comfyui
```

流程始终先低分辨率24fps静音预处理，再加载模型估计真实深度；未安装模型时不会以普通灰度代替。`--cuts` 使用预处理视频内的帧号，不使用原高帧率视频帧号。

## 按需技能

- `h3-comfyui-capacity-guide` 的容量数据是原工作站实测经验；换显卡、工作流和精度后重新判断。
- `comfyui-shanghai-remote` 保存了原工作站连接约定，没有携带密码。只有需要连接同一台主机时才沿用；先配置本地凭据路径、VPN 和主机信息。安装技能不授权远程执行。
- `h3-video-mimic` 已关闭隐式调用，不会因出现“舞蹈模仿”自动触发旧流程。
- `generated-video-finish` 和 `temporal-depth-reference` 依赖 `video-reference-prep` 的共享脚本，安装时必须保持同级目录；不要单独拷贝 SKILL.md。
- Higgsfield 包保留相对结构。若只抽取 FACS 一个 SKILL.md，会丢失本轮表情参考和关联路由。
- `wuxia` 分组包含人物情绪故事与影像制作两份文本技能，可独立于具体视频模型使用；建议成组安装以保留相互引用。进入提示词细化时按实际需求结合 Prompt Master、FACS 或模型专用技能，不要求安装生成引擎、素材或模型权重。
