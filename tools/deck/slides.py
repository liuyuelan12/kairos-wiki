# -*- coding: utf-8 -*-
"""Kairos Pitch Deck v2 内容源（BGB 级，币安金）。简中 · token-light · 文案大胆。
供 build_html.py（→PDF）与 build_pptx.py（→PPTX）共用。图片路径相对项目根。
"""

LOGO = "wiki/品牌/logo/sunrise_flat_512.png"
LOGO_SM = "wiki/品牌/logo/sunrise_flat_256.png"

VCS = [
    {"file": "output/VClogos/paradigm.webp",        "name": "Paradigm",         "cap": "缔造 Polymarket、Kalshi 的顶级风投——赛道认知与资本的天花板"},
    {"file": "output/VClogos/dragonfly.webp",        "name": "Dragonfly",        "cap": "顶级跨境加密基金，深耕交易、基建与亚太生态"},
    {"file": "output/VClogos/animocaBrands.webp",    "name": "Animoca Brands",   "cap": "Web3 游戏与粉丝经济巨头——娱乐化事件的天然入口"},
    {"file": "output/VClogos/amber.webp",            "name": "Amber Group",      "cap": "头部数字资产金融与做市——直击「流动性」命门"},
    {"file": "output/VClogos/wintermute.webp",       "name": "Wintermute",       "cap": "全球领先算法做市商，深化订单簿与价格发现"},
    {"file": "output/VClogos/ConsenSys.webp",        "name": "Consensys",        "cap": "以太坊核心基建（MetaMask / Infura）——底层结算与入口"},
    {"file": "output/VClogos/chainlink.webp",        "name": "Chainlink",        "cap": "领先去中心化预言机——与「结算验证」天然咬合"},
    {"file": "output/VClogos/yzilabs.webp",          "name": "YZi Labs",         "cap": "原 Binance Labs——分发、上所与合规的战略通路"},
    {"file": "output/VClogos/vega.webp",             "name": "Vega",             "cap": ""},
    {"file": "output/VClogos/uzcapital.webp",        "name": "UZ Capital",       "cap": ""},
    {"file": "output/VClogos/BluemountCapital.png",  "name": "Bluemount Capital","cap": ""},
]

TEAM = [
    {"photo": "output/Team/animeStyleProfilePic/AtulKamble.png",        "name": "Atul Kamble", "role": "创始人 Founder",        "bio": "IIT (BHU) 出身、连续创业者。主导协议设计与战略——把预测市场重塑为人人可参与的事件金融基建。"},
    {"photo": "output/Team/animeStyleProfilePic/JesseLiu.png",          "name": "Jesse Liu",   "role": "联合创始人 Co-Founder", "bio": "深耕亚太加密市场，主导运营、资本与在地化落地，把「在地化」做成 Kairos 的突围点。"},
    {"photo": "output/Team/animeStyleProfilePic/SpencerShi.png",        "name": "Spencer Shi", "role": "BD 负责人 BD Lead",     "bio": "负责上所、做市商、预言机与白标合作落地，把顶级投资人资源转成可执行网络。"},
    {"photo": "output/Team/animeStyleProfilePic/DerekFung.png",         "name": "Derek Fung",  "role": "AI 产品设计 Product",   "bio": "把 CLOB、概率定价翻译成「看涨/看跌 + 概率%」的直觉体验，让零基础用户秒上手。"},
    {"photo": "output/Team/animeStyleProfilePic/PanagiotisSimatis.png", "name": "Panagiotis Simatis", "role": "AI 与数据库 AI & DB", "bio": "构建实时数据管道与 AI 系统，支撑市场创建、资讯智能与情绪分析。"},
    {"photo": "output/Team/animeStyleProfilePic/ibraheemInam.png",      "name": "Ibraheem Inam","role": "高级算法 Algorithm",    "bio": "负责撮合引擎、定价与风控算法，确保高波动下依然稳定、高效、可结算。"},
]

DA = "output/deck-assets/"

SLIDES = [
    # 1 封面
    {"layout": "cover", "kicker": "PITCH DECK · 2026", "brand": "Kairos",
     "sub": "AI 驱动的 Web3 预测市场 × RWA 事件协议",
     "lede": "把世界的每一个关键时刻，变成可交易、可验证的事件资产。",
     "chain": "汇聚共识 · 预见关键一刻",
     "hero": DA + "cover-hero.png", "backed_by": [v["file"] for v in VCS]},

    # 2 投资方（重点强调 · 大胆）
    {"layout": "investors", "kicker": "BACKED BY", "no": "01",
     "title": "缔造了这条赛道的资本，\n正在共建 Kairos。",
     "lede": "从 Polymarket、Kalshi 的缔造者，到全球顶级做市商与核心基础设施——Kairos 的投资人阵容，本身就是赢得这条赛道的底牌：认知、流动性、结算、分发，一次到位。",
     "vcs": VCS},

    # 3 赛道
    {"layout": "cards", "kicker": "THE WAVE", "no": "02", "title": "下一个现象级赛道：预测市场",
     "lede": "两年规模暴涨 130×。主流机构与媒体，已经替这条赛道做完了验证。", "cols": 2,
     "cards": [
         {"tag": "FUNDING", "h": "Kalshi", "t": "完成 10 亿美元 E 轮，估值升至 110 亿美元（Paradigm 领投）"},
         {"tag": "WALL STREET", "h": "Polymarket × ICE", "t": "纽交所母公司 ICE 战略投资最高 20 亿美元（估值约 90 亿）"},
         {"tag": "MEDIA", "h": "CNN · CNBC", "t": "与 Kalshi 达成官方 / 独家预测数据合作，预测即新闻"},
         {"tag": "MAINSTREAM", "h": "Robinhood · Google Finance", "t": "零售券商拟入场；预测赔率进入主流金融数据"},
     ]},

    # 4 为何是现在 — stat 网格
    {"layout": "statgrid", "kicker": "WHY NOW", "no": "03", "title": "预测市场的 iPhone 时刻",
     "lede": "联邦监管、交易基建、体育分发三股力量同时到位——红利属于早期类别的开创者。",
     "stats": [
         {"lab": "两年规模增长", "num": "130×", "hero": True},
         {"lab": "赛道活跃用户", "num": "17M+"},
         {"lab": "2026 监管覆盖（美国）", "num": "38 州"},
         {"lab": "CFTC 已为 Polymarket", "num": "开绿灯", "small": True},
         {"lab": "交易基建", "num": "CME", "small": True},
         {"lab": "体育分发", "num": "FanDuel·DraftKings", "small": True},
     ]},

    # 5 什么是预测市场
    {"layout": "concept", "kicker": "MECHANISM", "no": "04", "title": "什么是预测市场",
     "lede": "用交易价格聚合群体信息，把「价格」变成对未来事件的「概率」。",
     "callout": "Price ≈ P(Event)", "callout_sub": "事件发生兑付 1、不发生兑付 0；价格即市场隐含概率。",
     "example": "「2026 年底 BTC 会达到 200K 吗？」 价格 0.72 → 市场隐含约 72% 概率。",
     "hero": DA + "crystalball.png"},

    # 6 CLOB
    {"layout": "concept", "kicker": "MECHANISM", "no": "05", "title": "CLOB 定价原理",
     "lede": "一张「到期必定值 $1」的兑换券，被拆成互补的 YES / NO 两半。",
     "callout": "YES (p) + NO (1−p) ≈ $1", "callout_sub": "买 YES @0.18 ＝ 等价卖 NO @0.82（镜像报价）。",
     "example": "两侧合并为同一订单簿 → 集中流动性、收窄价差、加速价格发现。",
     "barviz": True},

    # 7 痛点
    {"layout": "cols", "kicker": "PROBLEM", "no": "06", "title": "这条赛道，仍有四道坎",
     "cols": 2,
     "items": [
         {"n": "01", "h": "流动性不足", "t": "早期与在地化市场流动性稀薄，滑点高、进出难。"},
         {"n": "02", "h": "理解门槛高", "t": "定价与机制偏金融化，多数用户缺乏清晰策略。"},
         {"n": "03", "h": "在地化 + 资金摩擦", "t": "缺本地话题、法币入口与友善体验。"},
         {"n": "04", "h": "结果验证困难", "t": "现实事件缺权威可验证来源，易生争议。"},
     ]},

    # 8 Kairos 是什么
    {"layout": "concept", "kicker": "KAIROS", "no": "07", "title": "Kairos 是什么",
     "lede": "一个由 AI 驱动、链上透明结算的 Web3「预测市场 × RWA 事件」协议——把真实世界趋势变成可定价、可交易、可验证的事件资产。",
     "chips": ["金融", "政治", "气候", "科技", "体育", "文化", "娱乐", "AI", "粉丝经济", "社会趋势"],
     "hero": DA + "orb.png"},

    # 9 如何运作
    {"layout": "flow", "kicker": "HOW IT WORKS", "no": "08", "title": "全链路事件资产化",
     "lede": "事件生成 — 流动性 — 结算验证，一条龙打通。",
     "steps": [
         {"b": "01", "h": "事件生成", "t": "AI + 创作者，把热点变结构化预测话题"},
         {"b": "02", "h": "流动性", "t": "CLOB + 做市 / 套利工具，提供交易深度"},
         {"b": "03", "h": "结算验证", "t": "预言机 + DAO 仲裁，链上可审计"},
     ]},

    # 10 对比
    {"layout": "spec", "kicker": "DIFFERENTIATION", "no": "09", "title": "Kairos 有何不同",
     "headers": ["维度", "传统预测市场", "Kairos"],
     "rows": [
         ["市场重心", "单一类别 / 小众市场", "多领域覆盖 + RWA 事件"],
         ["用户体验", "交易导向、操作复杂", "AI 辅助 + 引导式新手"],
         ["分发方式", "加密原生用户", "创作者驱动，覆盖社交与主流"],
         ["参与角色", "仅限交易者", "交易者 × 创作者 × 合作伙伴"],
         ["在地化", "弱", "多语言 + 本地话题 + 法币入口"],
     ]},

    # 11 核心机制（四支柱 + 3D 图标）
    {"layout": "fcards", "kicker": "CORE", "no": "10", "title": "四大支柱", "dot": True,
     "lede": "RWA 事件、可验证结算、AI 引擎与在地化——撑起每一笔预测的底层轨道。",
     "cards": [
         {"icon": DA + "icon-rwa.png", "tag": "RWA", "h": "事件资产化", "t": "把真实世界事件做成可交易标的，多领域覆盖。"},
         {"icon": DA + "icon-oracle.png", "tag": "ORACLE", "h": "结算验证", "t": "可验证数据源 + DAO 仲裁，链上结算可审计。"},
         {"icon": DA + "icon-ai.png", "tag": "AI", "h": "AI 引擎", "t": "市场创建、资讯智能与情绪分析，降低门槛。"},
         {"icon": DA + "icon-local.png", "tag": "LOCAL", "h": "在地化", "t": "多语言、本地话题与法币入口，贴近真实需求。"},
     ]},

    # 12 产品与体验
    {"layout": "flow", "kicker": "PRODUCT", "no": "11", "title": "从围观，到上瘾",
     "lede": "把专业交易，重塑为直觉、轻量、社交化的体验。", "numbered": True,
     "steps": [
         {"b": "1", "h": "探索", "t": "看见洞察而非复杂操作，从社交讯号到预测机会"},
         {"b": "2", "h": "尝试", "t": "秒级注册、零风险起步，AI 把交易翻成看涨/看跌 + 概率%"},
         {"b": "3", "h": "参与 & 分享", "t": "一键生成收益卡片——预测即内容，天然裂变"},
     ]},

    # 13 生态系统（radial）
    {"layout": "eco", "kicker": "ECOSYSTEM", "no": "12", "title": "生态系统", "dot": True,
     "lede": "一个可组合的协议：基金会治理，模块协同，三类伙伴共建——把事件资产化做成全球基建。",
     "center": "Kairos\n基金会",
     "inner": ["预测市场", "做市工具", "套利工具", "支付平台", "AI 模块", "生态激励"],
     "outer": ["Market Builders", "Oracle & Data", "Distribution"]},

    # 14 商业模式 + donut
    {"layout": "biz", "kicker": "BUSINESS", "no": "13", "title": "清晰、链上、可审计的盈利",
     "lede": "费用结构简单透明，所有费用于链上执行、可公开审计。",
     "fees": [
         {"k": "交易手续费", "v": "0.5%", "s": "每位成交方单边"},
         {"k": "结算手续费", "v": "2%", "s": "仅对获胜结果"},
     ],
     "donut": DA + "donut-gold.png", "donut_center": ["营收", "结构 · 示例"],
     "segs": [
         {"p": "50%", "n": "交易手续费", "side": "l", "top": 78},
         {"p": "25%", "n": "结算手续费", "side": "l", "top": 238},
         {"p": "15%", "n": "数据与 API", "side": "r", "top": 78},
         {"p": "10%", "n": "企业级整合", "side": "r", "top": 238},
     ],
     "note": "营收结构为示例配置，仅作说明，不构成承诺。"},

    # 15 增长与分发
    {"layout": "cols", "kicker": "GROWTH", "no": "14", "title": "创作者驱动的增长飞轮",
     "lede": "覆盖社交与主流平台，而非局限加密原生——三层分发，层层放大。", "cols": 3,
     "items": [
         {"n": "/ 全民合伙人", "h": "人人可裂变", "t": "任何用户都能邀请、参与共建，自下而上扩散。"},
         {"n": "/ 流量节点", "h": "区域增长引擎", "t": "经审核的高贡献分发者，承担区域化推广。"},
         {"n": "/ 白标代理", "h": "7–14 天上线", "t": "品牌化交付，流动性与主平台共享，集中深度。"},
     ]},

    # 16 市场机会
    {"layout": "statgrid", "kicker": "OPPORTUNITY", "no": "15", "title": "一个被低估的娱乐金融市场",
     "lede": "预测市场正演变为互动式娱乐——亚太是成长最快的市场，需求最强烈。",
     "stats": [
         {"lab": "核心人群", "num": "18–40", "hero": True},
         {"lab": "性别分布", "num": "55% / 45%"},
         {"lab": "成长最快区域", "num": "亚太", "small": True},
         {"lab": "文化引擎", "num": "TikTok · K-pop", "small": True},
         {"lab": "增长杠杆", "num": "在地化 + 活动", "small": True},
         {"lab": "形态", "num": "互动式娱乐", "small": True},
     ],
     "note": "人群与规模数据为行业示例 / 待自有模型重估。"},

    # 17 团队
    {"layout": "team", "kicker": "TEAM", "no": "16", "title": "团队", "dot": True,
     "lede": "横跨协议、AI、算法、工程与生态拓展的国际化团队——兼具金融科技的严谨与 Web3 的敏捷。",
     "members": TEAM, "note": "更多顾问与合作伙伴，将随网络临近上线陆续公布。"},

    # 18 路线图 + 结语
    {"layout": "roadmap", "kicker": "ROADMAP", "no": "17", "title": "执行优先的路线图",
     "phases": [
         {"ph": "PHASE 00", "h": "命名与品牌", "t": "名称、叙事、视觉识别。", "done": True, "badge": "DONE"},
         {"ph": "PHASE 01", "h": "启动与早期成长", "t": "平台上线；早期流动性冷启动。"},
         {"ph": "PHASE 02", "h": "流动性与基建", "t": "基础设施升级；做市与流动性优化。"},
         {"ph": "PHASE 03", "h": "产品 V2 + AI", "t": "Kairos V2；AI 探索能力深化。"},
         {"ph": "PHASE 04", "h": "生态成长", "t": "合作伙伴与创作者扩张；治理上线。"},
     ],
     "closing": "汇聚共识 · 预见未来",
     "note": "本文档仅供信息参考，不构成投资建议；示例数据以平台后续正式公告为准。"},
]
