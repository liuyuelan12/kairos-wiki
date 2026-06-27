# 日志（log）

> append-only 时间线。每次 ingest / query / lint 追加一条（最新在上）。规则见 `CLAUDE.md`。

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
