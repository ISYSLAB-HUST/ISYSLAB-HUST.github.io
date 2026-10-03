<!--
  ============================================================================
   在线服务与数据库 · Online Servers & Databases
  ============================================================================
   「Software & Projects」页上半部分的唯一数据源。

   ── 字段 ────────────────────────────────────────────────────────────────
   name       必填。工具名称
   desc       必填。英文简介
   desc_zh    可选。中文简介
   url        必填。工具地址
   label      可选。链接显示文字，不写就用 url 去掉协议头
   ============================================================================
-->

---
name: ThreaDomEx
desc: A unified online server combining ThreaDom and DomEx for accurate protein domain prediction on both continuous and discontinuous domain structures. Supports interactive editing and re-detection of domain models.
desc_zh: 融合 ThreaDom 与 DomEx 的在线服务器，可对连续域与不连续域结构进行准确的蛋白质结构域预测，支持交互式编辑与重新识别结构域模型。
url: http://isyslab.info/ThreaDomEx
label: isyslab.info/ThreaDomEx
---

---
name: ThreaDom
desc: Protein domain prediction based on multiple threading programs. Reports boundaries more accurately than most predictors — especially for medium and hard targets — and detects discontinuous domains via boundary clustering.
desc_zh: 基于多线程程序进行蛋白质结构域预测。相比多数预测器边界判定更准确（在中等与困难靶标上尤其明显），并通过边界聚类识别不连续结构域。
url: https://zhanglab.ccmb.med.umich.edu/ThreaDom
label: zhanglab.ccmb.med.umich.edu/ThreaDom
---

---
name: DomEx
desc: Assembles continuous domain segments so that boundary predictors can detect discontinuous domains. Recalled 26.7% discontinuous domains at 72.7% precision in a 29-chain benchmark where ThreaDom failed. Source code and datasets available.
desc_zh: 通过组装连续结构域片段，使边界预测器能够识别不连续结构域。在 ThreaDom 失效的 29 条链基准上，以 72.7% 的精度召回 26.7% 的不连续结构域。提供源码与数据集。
url: http://isyslab.info/DomEx
label: isyslab.info/DomEx
---

---
name: NeuroPep
desc: The most complete neuropeptide database available. Release 1.0 holds 5,949 non-redundant entries from 493 organisms across 65 families, all manually curated from MEDLINE, UniProt and Neuropedia. Version 2.0 accompanied by the NeuroPep 2.0 paper.
desc_zh: 目前最完整的神经肽数据库。1.0 版收录来自 493 个物种、65 个家族的 5,949 条非冗余记录，全部由 MEDLINE、UniProt 与 Neuropedia 人工校正。2.0 版随 NeuroPep 2.0 论文同步发布。
url: http://isyslab.info/NeuroPep
label: isyslab.info/NeuroPep
---

---
name: StraPep
desc: A structure database of bioactive peptides: 1,199 peptides and 3,536 PDB chains across six categories (Toxin & Venom, Antimicrobial, Cytokine & Growth factor, Hormone, Neuropeptide, Others). Includes BLAST, mapping and secondary-structure tools.
desc_zh: 生物活性肽结构数据库：收录 1,199 条多肽与 3,536 条 PDB 链，分为毒素与毒液、抗菌、细胞因子与生长因子、激素、神经肽、其他六类，并提供 BLAST、映射与二级结构工具。
url: https://github.com/ISYSLAB-HUST/StraPep
label: github.com/ISYSLAB-HUST/StraPep
---

---
name: I-TASSER-MR
desc: Automated molecular replacement for distant-homology proteins using iterative fragment assembly and progressive sequence truncation. Generated full-length models at average TM-score 0.773 and found correct MR solutions for 95 of 161 targets.
desc_zh: 面向远源同源蛋白的自动分子置换方法，采用迭代片段组装与渐进式序列截断。生成的全长模型平均 TM-score 为 0.773，在 161 个靶标中为 95 个找到正确的分子置换解。
url: https://zhanglab.ccmb.med.umich.edu/I-TASSER-MR
label: zhanglab.ccmb.med.umich.edu/I-TASSER-MR
---
