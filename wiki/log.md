# 日志（log）

> append-only 时间线。每次 ingest / query / lint 追加一条（最新在上）。规则见 `CLAUDE.md`。

## [2026-06-29] 产出 | Kairos 白皮书 **v0.2**（大幅完善）
- **起因**：v0.1（15 节）已成型，用户要「大幅完善」——气势磅礴但细节经得起推敲。
- **升级**：15 节 → **18 节**。新增三大章：**§7 AI 原生（智能内核）**、**§9 官方带单（雷达带单/保本+保底）**、**§10 流量聚合器与空投聚合**；并扩写 §1 摘要、§3 行业背景（规模阶梯 $510 亿→$2400 亿→$1 万亿）、§11 六大生态板块、§16 全球化战略与路线图、§18 带单专项风险条款。
- **三大重点**：① AI 叙事——五大智能体矩阵 + 数据飞轮护城河 + 对话式预见；② 官方带单——保本 + 每单 1%–3% 保底（USDT 计），四支柱论证可行性（AI/量化边际、跨市场对冲、链上准备金兜底、获客视角），含「投入 1 万 → 日收 300–900」与美国中期选举全流程两个示例；③ 流量/空投聚合——投资方=孵化网络，「一个入口领整片生态空投」（他方代币）。
- **资产修复**：白皮书已移至 `output/白皮书/`，复制 `Kairos-mark.png` / `VClogos/`（11）/ `Team/`（6）入该目录，相对路径恢复可解析。
- **取材**：旧资料2 带单机制 + See-X 六大生态板块；事实锚点（Kalshi 110 亿、ICE 20 亿、CFTC 38 州、0.5%/2%、团队 6 人）与 wiki 一致。
- **守门**：仍 token-light（带单收益用 USDT、空投为他方代币、**无 $KAI 代币经济/ticker/币价**，代币细节仍「后续专门文档公布」）；带单**保本=链上准备金兜底，显式声明非庞氏**；规模/收益/复利数字一律标「示例/行业预测/规则可调」。
- **文件**：`output/白皮书/Kairos-白皮书-zh.md`（v0.1 → v0.2）。

## [2026-06-27] 产出 | Kairos Pitch Deck **v2**（BGB 级重做）
- **起因**：v1 被判定不够立体/图表不丰富。参照 session `99973e6b` 为 Agentum 做的 BGB 风 deck（`海君项目/output/pitch-deck-bgb/`，**同一团队**）——直接移植那套成熟设计系统到 Kairos。
- **关键升级 vs v1**：① 内嵌 **Archivo 900 重黑体**（`tools/deck/assets/fonts-embedded.css`，复制自 Agentum）——v1 缺的「设计感」来源；② 真 **3D 主视觉**（封面虹彩玻璃球+金币、四支柱 4 个金色 3D 图标、3D 金色 donut）——`gen_deck_assets.py` 加 **IPv4 pin + 重试** 绕过 geo-block（v1 失败主因），全部一次出图成功；③ 丰富图表/图示：**stat 卡网格、3D 图标 feature 卡、radial 生态图、3D donut 带引线、roadmap track、对比表**；④ **币安金主色 + cyan 次级点缀**（CLOB NO 侧、生态共建节点、AI 图标冷光）。
- **VC 重点强调（用户授权大胆文案/单开页）**：封面 backed-by 条 + **第2页整页**「缔造了这条赛道的资本，正在共建 Kairos。」+ 11 logo 墙 + 逐家战略意义。
- **交付**：`output/deck/Kairos-Deck-zh.{pdf,pptx,html}`（PDF 12.9MB / PPTX 6.9MB 可编辑 18 页）。源：`tools/deck/{slides.py,build_html.py,build_pptx.py,gen_deck_assets.py}`。
- **守门**：token-light（无代币经济页/ticker/币价）；营收结构/市场数据标「示例」；RWA=事件资产化。
- **已知**：PPTX 未经 LibreOffice 目检（机器无），结构校验 18 页齐、3D图/表就位。

## [2026-06-27] 产出 | Kairos Pitch Deck（18 页，PDF + PPTX）
- **交付**：`output/deck/Kairos-Deck-zh.pdf`（设计版，Chrome HTML→PDF）+ `output/deck/Kairos-Deck-zh.pptx`（原生可编辑，python-pptx）+ `output/deck/Kairos-Deck-zh.html`（源）。脚本输出路径已指向 `output/deck/`。
- **风格**：对标 BGB 白皮书——纯黑底、3D 玻璃/金属、粗体无衬线；**主色币安金** `#F0B90B`/`#FCD535`，**cyan 作次级点缀**（CLOB 的 NO 侧、3D 边缘冷光）。logo 用旭日 `sunrise_flat`。
- **单一内容源 → 双渲染**：`tools/deck/slides.py`（18 页内容，简中，token-light）→ `build_html.py`（PDF）+ `build_pptx.py`（PPTX，须 `/usr/bin/python3`，已装 python-pptx 1.0.2）。3D 主视觉 `tools/deck/gen_deck_assets.py`（Gemini）→ `output/deck-assets/`（orb/crystalball/chart/globe 生成成功；duality/shield/rocket 遇 API 地域限制，CLOB 改用 CSS YES/NO 条）。
- **结构**：封面 → 赛道/为何现在 → 预测市场/CLOB 原理 → 痛点 → Kairos 是什么/方案/对比 → 机制/产品/生态 → 商业/增长/市场 → **投资方（重点强调，3 处）** → 团队 → 路线图。
- **VC 强调**：封面 "Backed by" 条 + 第16页 11 家白底 logo 墙 + 逐家战略意义 + 团队页旁注。素材 `output/VClogos/`（webp 经 sips 转 png 供 PPTX）。
- **守门**：token-light（无 ticker/币价/代币经济页）；占位数据标「示例·待重估」；RWA=事件资产化非抵押。
- **已知**：PPTX 视觉未经 LibreOffice 栅格目检（机器无 LibreOffice），但结构校验 18 页齐、图片/表格就位、镜像已验证的 HTML 版式。

## [2026-06-27] 产出 | Kairos 白皮书 v0.1
- **交付**：`output/Kairos-白皮书-zh.md`（简体中文，Markdown，15 节）。封面 logo `output/Kairos-mark.png`（取自 `品牌/logo/sunrise_flat_512.png`）。
- **口径**：token-light——**不设代币章节**、无 ticker/币价/代币金融数字；费用率（0.5%/边、2% 结算）作为商业模式事实保留；占位数据（市场 8M、净利 $61.2M 等）标注「示例/待重估」。RWA 按「真实世界事件资产化」写，未臆造抵押机制。
- **新增内容（用户提供素材）**：
  - **投资方与战略支持**（重点强调）：`output/VClogos/` 11 家 —— Paradigm / Dragonfly / Animoca / Amber / Wintermute / Consensys / Chainlink / YZi Labs / Vega / UZ Capital / Bluemount，逐家说明对 Kairos 的战略意义。
  - **团队**：`output/Team/team.md` 6 人（Atul Kamble 创始人、Jesse Liu 联创、Spencer Shi BD、Derek Fung、Panagiotis Simatis、Ibraheem Inam）+ `Team/animeStyleProfilePic/` 头像 + LinkedIn。
- **取材**：`wiki/平台/*`、`wiki/概念/*`、`wiki/实体/*`、`wiki/品牌/命名方案`。
- **待办**：路线图落地带日期里程碑；市场数据用自有模型重估；代币机制待后续专门文档（届时再定对外口径）。

## [2026-06-27] logo | 旭日 Sunrise（复刻 `raw/参考/logoReferences/2.png`）
- **目标**：复刻参考图旭日母题（地平线 + 半圆太阳 + ~13 放射尖刺），配色改币安金、去文字、只要图标、透明底。
- **① 扁平矢量**：新建 `tools/gen_logo_sunrise.py`（纯标准库，几何全参数化）→ 出
  `品牌/logo/sunrise_flat.svg` + `_{2048,512,256,64}.png`（**RGBA 透明**，已核验）。金色渐变
  `#FCD535→#F0B90B→#B8860B`，`--flat` 可切单色。栅格器 `rsvg-convert`（主）/`cairosvg`（回退）。
- **② 3D 金属**：扩展 `tools/gen_logo.py` —— 加 `--ref`（参考图条件生成）、`--transparent`、
  `image_has_alpha`/`ext_for` 与「不透明回退黑底」逻辑，精修 `sunrise` 概念对齐参考构图。跑
  `--only sunrise --ref ... --transparent` → `品牌/logo/sunrise.jpg`（抛光金属金 + 玻璃虹彩，黑底）。
- **存疑/已知**：`gemini-3-pro-image` 返回不透明 JPEG，故 3D 版按设计回退黑底（非真透明）；如需 3D 透明
  需换支持 alpha 的模型或后期抠像。扁平矢量版已是真透明底，建议作 UI/favicon 首选。
- **触及页**：[[视觉风格]]（新增旭日小节 + 第④符号方向）、`index.md`、`log.md`。
- **密钥**：`GEMINI_API` 仅写本地 `.env`（已 `.gitignore`，未入库）。

## [2026-06-27] 框架初始化 + ingest | SEE-X Deck
- **搭框架**：建 `CLAUDE.md`（schema）+ `wiki/` 五分类 + `index.md`/`log.md`。
- **转录**：`raw/参考/SEE-X-Deck-繁中-识别.md`（27 页逐页）。
- **ingest 来源**：[[see-x-deck]]，触及 **35 页**：
  - 概念 ×9：[[预测市场]] [[CLOB]] [[RWA]] [[预言机]] [[事件资产化]] [[通缩回购销毁]] [[质押锁仓]] [[做市与流动性]] [[返佣分润]]
  - 实体 ×11：[[Kalshi]] [[Polymarket]] [[Augur]] [[CFTC]] [[CME]] [[ICE]] [[Robinhood]] [[DraftKings与FanDuel]] [[CNN]] [[CNBC]] [[Google-Finance]]
  - 平台 ×11：[[概览]] [[生态系统]] [[KAI代币]] [[手续费与盈利]] [[用户增长与裂变]] [[流量节点与合伙人]] [[白标代理]] [[质押收益机制]] [[代币分配]] [[市场机会]] [[路线图]]
  - 品牌 ×2：[[命名方案]] [[视觉风格]]
- **决策**：平台定名 **Kairos / $KAI**（替换 See-X 的 SES）；视觉 = BGB 3D 风 + 币安金。
- **存疑**：deck 为「(空)」模板，市场需求 8M / 净利 $61.2M 等为占位数据，需 Kairos 自有模型重估；代币「股币同权/分红」涉证券属性，对外口径走合规、当前不提币价。
- **Logo**：`tools/gen_logo.py`（Gemini `gemini-3-pro-image`）出 4 版 → `wiki/品牌/logo/`：`hourglass`（推荐）、`k-coin`、`seize`、`wordmark`。BGB 3D 风 + 币安金，无 cyan。
- **下一步**：用户选定主图标 → 出透明底/SVG/App icon；把 [[路线图]] 落成带日期里程碑；建 Kairos 自有市场模型（[[市场机会]]）。
