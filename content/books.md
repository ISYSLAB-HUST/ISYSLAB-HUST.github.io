<!--
  ============================================================================
   教材 · Textbooks
  ============================================================================
   「教材」页的唯一数据源。一本教材一段，段落之间用单独一行的三个短横线分隔。

   ── 字段 ────────────────────────────────────────────────────────────────
   date            必填。出版年月，格式 YYYY-MM（写成 2025-06）。
                   页面按它倒序排列，并渲染成「Jun 2025 / 2025年6月」。
   title           书名（英文界面显示）
   title_zh        书名（中文界面显示）
                   中文教材只填 title_zh 也可以，英文界面会回落到它。
                   注意：中文教材没有官方英文名，这里的英文是工作译名，不是正式书名。
   authors         作者（英文，顿号改成逗号，用「, 」分隔）
   authors_zh      作者（中文，用「、」分隔，末尾可加「等」）
   role            署名角色（英文）：Editor-in-chief / Associate editor / Co-author
   role_zh         署名角色（中文）：主编 / 副主编 / 编著
   publisher       出版社（英文）
   publisher_zh    出版社（中文）
   isbn            ISBN，例如 978-7-115-48307-2
   series          丛书 / 项目定位（英文）
   series_zh       丛书 / 项目定位（中文）
   note            可选。补充说明（英文）
   note_zh         可选。补充说明（中文）

   ── 维护提示 ────────────────────────────────────────────────────────────
   · 数据来源：人民邮电出版社官网与人邮教育社区、各高校图书馆 OPAC、
     发行渠道（新华国采 / 文轩 / 当当）、以及实验室官网 isyslab.info 的「教材」栏目。
   · 字段值写在冒号后面同一行；字段之间允许空行。
   · 页数、定价等细目写进 note，正文只保留书名 / 作者 / 出版社 / ISBN 等主干信息。
   · 署名单位而非个人的教材（如《大数据技术》署名「华为技术有限公司」），
     authors 照抄署名、**不填 role 字段**，实际编写情况写进 note。
   · 英文书名与出版社名是工作译名，正式对外引用请以中文原名为准。
   ============================================================================
-->

---
date: 2025-06
title: Blockchain Development in Rust
title_zh: Rust语言区块链开发实战
authors: Zhidong XUE (Editor-in-chief), Shiqi OU, Xuchao ZHANG
authors_zh: 薛志东 主编；区士颀、章许超 副主编
role: Editor-in-chief
role_zh: 主编
publisher: Posts & Telecom Press
publisher_zh: 人民邮电出版社
isbn: 978-7-115-66635-2
series: Blockchain Technology Development Series
series_zh: 区块链技术开发系列
note: National key publication of the 14th Five-Year Plan. 196 pp., ¥59.80. Covers Rust, ink! smart contracts and Substrate, ending with a Substrate Kitties development walk-through.
note_zh: “十四五”时期国家重点出版物出版专项规划项目。196 页，定价 59.80 元。涵盖 Rust 语言、ink! 智能合约与 Substrate 框架，末章为 Substrate Kitties 开发实例。
---

---
date: 2021-09
title: Big Data Technology — Fundamentals and Practice
title_zh: 大数据技术基础与实战
authors: Zhidong XUE (Editor-in-chief), Shuangshuang ZHANG, Jingxiang LU et al.
authors_zh: 薛志东 主编；张双双、卢璟祥 等
role: Editor-in-chief
role_zh: 主编
publisher: Posts & Telecom Press
publisher_zh: 人民邮电出版社
isbn: 978-7-115-56719-2
series: Higher-Education IT Talent Development Series · National Planned Textbook of the 14th Five-Year Plan for Vocational Education
series_zh: 高等学校信息技术人才能力培养系列教材 · “十四五”职业教育国家规划教材
note: ¥59.80, 7th printing. Hands-on walk-through of the Hadoop ecosystem — Linux cluster setup, HDFS, MapReduce, Hive, HBase, Flume and Spark, plus image/video processing on a big-data platform.
note_zh: 定价 59.80 元，已第 7 次印刷。以实战为主线贯通 Hadoop 生态——Linux 集群搭建、HDFS、MapReduce、Hive、HBase、Flume 与 Spark，并含利用大数据平台处理图像与视频。
---

---
date: 2021-07
title: Big Data Technology
title_zh: 大数据技术
authors: Huawei Technologies Co., Ltd. (compiled by)
authors_zh: 华为技术有限公司 编著
publisher: Posts & Telecom Press
publisher_zh: 人民邮电出版社
isbn: 978-7-115-55607-3
series: Huawei ICT Certification Series · HCIA-Big Data designated textbook · Huawei ICT Academy designated textbook
series_zh: 华为 ICT 认证系列丛书 · HCIA-Big Data 认证指定教材 · 华为 ICT 学院指定教材
note: 252 pp., ¥69.80. Written by the iSyslab team under Zhidong XUE together with Huawei engineers. Thirteen chapters — distributed file systems and ZooKeeper, Hive, HBase, MapReduce and YARN, Spark, Flink, Flume and Loader, Kafka, secure cluster mode, Elasticsearch, Redis, and Huawei's big data solutions.
note_zh: 252 页，定价 69.80 元。由薛志东带领 iSyslab 实验室师生与华为技术专家共同编写。共 13 章：分布式文件系统与 ZooKeeper、Hive、HBase、MapReduce 与 YARN、Spark、Flink、Flume / Loader、Kafka、高可靠集群安全模式、Elasticsearch、Redis，以及华为大数据解决方案。
---

---
date: 2018-08
title: Big Data Technology Fundamentals
title_zh: 大数据技术基础
authors: Zhidong XUE (Editor-in-chief), Zehua LYU, Changqing CHEN, Hao HUANG et al.
authors_zh: 薛志东 主编；吕泽华、陈长清、黄浩 等
role: Editor-in-chief
role_zh: 主编
publisher: Posts & Telecom Press
publisher_zh: 人民邮电出版社
isbn: 978-7-115-48307-2
series: Data Science and Big Data Technology Programme Series — an MoE Computer Science Teaching Committee × Huawei ICT collaboration
series_zh: 数据科学与大数据技术专业系列规划教材（教育部高等学校计算机类专业教学指导委员会—华为 ICT 产学合作项目）
note: Designated textbook of Huawei ICT Academy. 304 pp., ¥55.00. Ten chapters from big-data software foundations and distributed storage to MapReduce, Spark and data visualisation; PPT, source code and lab datasets are provided.
note_zh: 华为信息与网络技术学院指定教材。304 页，定价 55.00 元。共 10 章，从大数据软件基础、分布式存储讲到 MapReduce、Spark 与数据可视化；配套 PPT、源代码与实验数据。
---
