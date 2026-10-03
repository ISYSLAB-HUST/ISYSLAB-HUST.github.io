<!--
  ============================================================================
   研究方向 · Research
  ============================================================================
   同时驱动两处：首页「研究方向」卡片，以及「研究方向」页的五个板块。
   改这里，两边一起变。

   ── 字段 ────────────────────────────────────────────────────────────────
   no         可选。编号，不写就按顺序自动编 01、02……
   eyebrow    必填。板块上方的小标题（英文大写）
   title      必填。方向名称（英文）
   title_zh   必填。方向名称（中文）
   short      可选。首页卡片用的英文短介绍；不写就用 desc
   short_zh   可选。首页卡片用的中文短介绍
   desc       必填。英文详细介绍
   desc_zh    可选。中文详细介绍
   tags       可选。关键词，用 · 分隔（英文）
   tags_zh    可选。关键词（中文）
   image      可选。配图路径，例如 assets/img/research/01.png
   ============================================================================
-->

---
no: 01
eyebrow: LARGE LANGUAGE MODELS
title: Large Language Models and Applications
title_zh: 大模型技术与应用
short: Language-model technology and agents — domain adaptation, RAG, hallucination control, and applications in knowledge QA, survey writing and education.
short_zh: 语言模型与智能体技术——领域适配、检索增强、幻觉控制，落地知识问答、综述撰写与教育场景。
desc: Research on large language models and their applications — domain adaptation, retrieval-augmented generation and agent frameworks that combine tools, memory and planning. Application focus includes knowledge question answering, automated literature-survey generation (patented time-stamped survey generation methods) and AI-empowered teaching resources. The lab also explores language models for science (ProtFlash) and studies efficient fine-tuning, hallucination control and systematic evaluation of model output.
desc_zh: 围绕大语言模型技术及其应用的研究——领域适配、检索增强生成，以及融合工具、记忆与规划能力的智能体框架。应用聚焦知识问答、文献综述自动撰写（已获时序化综述生成方法发明专利）与 AI 赋能的教学资源建设；同时以蛋白质语言模型（ProtFlash）探索大模型的科学应用，并关注高效微调、幻觉控制与模型输出的系统化评测。
tags: Domain adaptation · RAG · Agents · Evaluation
tags_zh: 领域适配 · 检索增强 · 智能体 · 效果评测
image: assets/img/research/01.svg
---

---
no: 02
eyebrow: VIRTUAL REALITY & GAMES
title: Virtual Reality and Computer Games
title_zh: 虚拟现实与计算机游戏
short: VR and serious games — immersive interaction, redirected walking, adaptive gameplay and quantitative assessment from motion data.
short_zh: 虚拟现实与严肃游戏——沉浸交互、重定向行走、自适应玩法与基于运动数据的量化评估。
desc: Virtual reality and computer game technologies with a focus on interactive training and serious games — personalized redirected walking for natural locomotion in limited physical space, dynamic adjustment of rehabilitation games driven by user state, immersive rendering and interaction for AR/VR scenes (patented virtual sculpting and virtual-scene path generation), and quantitative balance assessment from motion trajectories. Applications include rehabilitation training, skill assessment and education. Current work adds multimodal sensing and AI-driven adaptation to these systems.
desc_zh: 面向交互训练与严肃游戏的虚拟现实与计算机游戏技术——有限物理空间中的个性化重定向行走、由用户状态驱动的康复游戏动态调整、AR/VR 场景的沉浸式渲染与交互（虚拟雕刻、虚拟场景训练路径生成等已获专利），以及基于运动轨迹的平衡能力量化评估；应用于康复训练、技能测评与教育场景。当前工作正为这些系统引入多模态感知与 AI 驱动的自适应机制。
tags: Serious games · Redirected walking · Immersive interaction · Assessment
tags_zh: 严肃游戏 · 重定向行走 · 沉浸交互 · 量化评估
image: assets/img/research/02.svg
---

---
no: 03
eyebrow: IMAGE & VIDEO PROCESSING
title: Image and Video Processing Technology
title_zh: 图像与视频处理技术
short: Visual computing for real acquisition scenarios — medical image analysis, detection and tracking, SLAM, video stitching and DNA-based image storage.
short_zh: 面向真实采集场景的视觉计算——医学影像分析、检测与追踪、SLAM、视频拼接与 DNA 图像存储。
desc: Image and video processing for challenging real-world acquisition scenarios — ultrasound image analysis (MS-Detector for muscle strain detection), chronic venous disease image classification, high-precision occupational lead-poisoning screening with machine-learning-enhanced LIBS, multi-object tracking and video-sequence stitching in video streams, visual SLAM with lightweight local descriptors for monocular navigation, and DNA-based image storage (contour image encoding with fountain codes). Current interests include deep models for medical image analysis, video understanding and lightweight deployment on edge devices.
desc_zh: 面向复杂真实采集场景的图像与视频处理——超声图像分析（肌肉劳损检测 MS-Detector）、慢性静脉疾病图像分类、机器学习增强 LIBS 光谱的铅中毒高精度筛查、视频流中的多目标追踪与序列影像拼接、面向单目导航的轻量级局部描述子视觉 SLAM，以及基于 DNA 的图像存储（喷泉码轮廓图像编码）。当前关注医学影像分析的深度模型、视频理解与边缘设备的轻量化部署。
tags: Medical imaging · Detection & tracking · SLAM · DNA storage
tags_zh: 医学影像 · 检测与追踪 · SLAM · DNA 存储
image: assets/img/research/03.svg
---

---
no: 04
eyebrow: MACROMOLECULE PREDICTION & SOFTWARE
title: Biological Macromolecule Prediction and Software
title_zh: 生物大分子预测与软件
short: Computational prediction and software for proteins, peptides and RNA — structure, function and interactions, released as servers and open-source tools.
short_zh: 蛋白质、多肽与 RNA 的计算预测与软件研发——结构、功能与相互作用，以服务器与开源工具发布。
desc: The lab's core strength — computational prediction of biological macromolecules and the software that delivers it. Structure and domain prediction from threading (ThreaDomEx, I-TASSER-MR) to deep learning and protein language models (ProtFlash, ProtSSSD, ProtFormer-Site); protein–RNA and protein–protein interaction site prediction (SPLiNet); neuropeptide informatics with the NeuroPep database and PLM-based predictors (NeuroPred-PLM, DeepNeuropePred); scalable structure alignment with Spark and OpenMP (pmTM-align); and bioactive-peptide resources (StraPep). Tools are released as web servers and open-source software; current work moves toward AI-driven protein design and drug-target discovery.
desc_zh: 课题组的核心优势方向——生物大分子的计算预测与配套软件研发。结构域与结构预测从穿线法（ThreaDomEx、I-TASSER-MR）发展到深度学习与蛋白质语言模型（ProtFlash、ProtSSSD、ProtFormer-Site）；蛋白质–RNA 与蛋白质–蛋白质相互作用位点预测（SPLiNet）；以 NeuroPep 数据库与语言模型预测器（NeuroPred-PLM、DeepNeuropePred）为核心的神经肽信息学；基于 Spark 与 OpenMP 的可扩展结构比对（pmTM-align）；以及生物活性肽资源库（StraPep）。成果以在线服务器与开源软件发布，当前正推进 AI 驱动的蛋白质设计与药物靶点发现。
tags: Protein LMs · Structure & function · Peptide informatics · Open-source tools
tags_zh: 蛋白质语言模型 · 结构与功能 · 神经肽信息学 · 开源工具
image: assets/img/research/04.svg
---

---
no: 05
eyebrow: AI SECURITY & PRIVACY
title: AI Security and Privacy Protection
title_zh: 人工智能安全与隐私保护
short: Trustworthy AI — robustness and privacy of intelligent systems, content-risk detection, data-rights protection and LLM safety.
short_zh: 可信人工智能——智能系统的鲁棒性与隐私、内容风险检测、数据权益保护与大模型安全。
desc: Security and privacy issues of intelligent systems — adversarial robustness and trustworthy deployment of deep models, privacy-preserving machine learning, and detection of risky content in dialogue (patented methods for dialogue emotion classification and violence-tendency assessment). The lab also works on data-rights protection with cryptographic techniques, from research on DNA cryptography to blockchain-based hierarchical rights confirmation and trading of digital assets. Current interests include the safety of large language models — jailbreak and prompt-injection defense, model watermarking and content provenance.
desc_zh: 面向智能系统的安全与隐私问题——深度模型的对抗鲁棒性与可信部署、隐私保护机器学习，以及对话中高风险内容的检测（对话情感倾向分类、催收暴力倾向评价等发明专利）。在数据权益保护方面开展密码学技术研究，从 DNA 密码学研究到基于区块链的数字资产分层确权与交易。当前关注大模型安全——越狱与提示注入防御、模型水印与内容溯源。
tags: LLM safety · Privacy-preserving learning · Data rights · Content security
tags_zh: 大模型安全 · 隐私保护学习 · 数据确权 · 内容安全
image: assets/img/research/05.svg
---
