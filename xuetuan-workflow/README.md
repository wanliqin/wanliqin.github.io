# 雪团桌面宠物 - 生成工作流备份

雪团（xuetuan）：会用动作表达工作状态的蓝眼灰白长毛桌面猫，8×11 精灵图集，每格 192×208。

本目录是雪团的**完整生成工作流**备份（2026-07-20 ~ 07-21 通过 Codex + 图像生成完成），与 `../xuetuan-source/`（精简源码）和 `../xuetuan-share/`（网页预览）互补。

## 目录结构

- `pet_request.json`：Codex 宠物配置（pet_id、展示名、描述、atlas 尺寸、动作行定义）
- `imagegen-jobs.json`：图像生成任务记录（每帧 prompt 与产物）
- `make_local_pet.py`：本地精灵图集合成脚本（PIL，圆形遮罩 + LANCZOS 缩放到 192×208 网格）
- `prompts/base-pet.md`：基础角色设定（身份一致性锚点）
- `prompts/rows/`：每个动作行（idle/running/waving/jumping/look-row-9/look-row-10/failed/review/waiting/running-left/running-right）的完整图像生成 prompt
- `prompts/row-retries/`：动作行的重试/微调 prompt（修正锚点、表情、对比度等）
- `prompts/look-cardinals.md`：四方向注视锚点
- `prompts/look-anchor-repairs/`：方向注视修复（000/090/180/270 度）
- `references-layout-guides/`：图集布局参考图（每行动作的排布示意）
- `reference-01.png`：主视觉参考
- `final/spritesheet-extended.png` / `.webp`：最终扩展版精灵图集

## 复现提示

角色身份一致性靠 `base-pet.md` 锚定：**先只生成主视觉并确认，再逐行生成动作条**，避免角色漂移。参考素材路径是本机生成路径，换机复现需调整 `make_local_pet.py` 中的输入路径。
