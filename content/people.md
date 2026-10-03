<!--
  ============================================================================
   团队成员 · People
  ============================================================================
   「团队成员」页的唯一数据源。一个人一段，段落之间用单独一行的三个短横线分隔。

   ── 分组 ────────────────────────────────────────────────────────────────
   group 字段决定这个人出现在哪一组，可选值：

     faculty        指导教师
     collaborators  合作指导教师
     staff          博士后与专职研究人员（含研究助理）
     students       在读学生
     alumni         同事与校友

   页面上的分组顺序固定为上面这个顺序，与文件里段落的先后无关。
   某一组暂时没有人时，页面会显示「待补充」，不会整组消失。
   一个人同时有多个身份时（例如既是出站博士后又是合作者），
   就写两段、分别归到对应分组，页面会在两栏各出现一次。

   ── 字段 ────────────────────────────────────────────────────────────────
   group          必填。见上面的取值
   name           必填。英文名，姓氏可大写，例如 Lei WANG
   name_zh        推荐。中文名，中文版网页显示它
   role           必填。职称／岗位／年级（英文）
   role_zh        推荐。职称／岗位／年级（中文）
   affiliation    可选。所在单位（英文）—— 合作者常用
   affiliation_zh 可选。所在单位（中文）
   bio            可选。简介（英文）—— faculty / collaborators 显示为完整简介；
                  其余分组显示为一行小字研究方向
   bio_zh         可选。简介（中文）
   email          可选。邮箱
   lead           可选。写 true 会渲染成置顶的大卡片（一般只给负责人用）
   initial        可选。圆形头像里的字母，不写就自动取名字首字母
   photo          可选。头像图片路径，例如 assets/img/people/xue.jpg

   ── 维护提示 ────────────────────────────────────────────────────────────
   · 新增一个人：复制一段现成的记录，改字段值即可。
   · 字段值写在冒号后面同一行；字段之间允许空行。
  ============================================================================
-->

<!-- ======================== 指导教师 · faculty ======================== -->

---
group: faculty
name: Zhidong XUE
name_zh: 薛志东
role: Professor
role_zh: 研究员 · 博士生导师
lead: true
photo: assets/img/people/xue-zhidong.jpg
bio: Professor at the School of Software Engineering, HUST, where he leads iSyslab. His research spans biomedical big data, video processing and analysis, big data technologies, and rehabilitation games. He has led projects funded by the National Natural Science Foundation of China and Huawei, published in journals such as Nucleic Acids Research and Bioinformatics, and authored three textbooks. He serves as Director of the Data Science and Big Data Committee of the Operations Research Society of Hubei, and holds committee positions in the bioinformatics societies of CCF, CAAI and CIE.
bio_zh: 华中科技大学软件学院研究员、博士生导师，iSyslab 实验室负责人。主要研究方向为生物医学大数据、视频处理与分析、大数据技术与康复游戏。主持国家自然科学基金、华为委托项目等课题，在 Nucleic Acids Research、Bioinformatics 等期刊发表论文，主编教材 3 部。兼任湖北省运筹学会数据科学与大数据技术专委会主任，以及 CCF、CAAI、CIE 生物信息相关专委会委员/理事。
email: zdxue@hust.edu.cn
---

<!-- 王燕老师：暂时从指导教师名单下线（2026-10-01，待后续补充/确认资料后再放回）。
     恢复方式：把下面整段前后的注释标记删掉即可，字段与照片（assets/img/people/wang-yan.png）都保留着。
---
group: faculty
name: Yan WANG
name_zh: 王燕
role: Associate Professor
role_zh: 副教授 · 博士生导师
photo: assets/img/people/wang-yan.png
bio: Associate professor and doctoral supervisor at the School of Life Science and Technology, HUST. Her research focuses on bioinformatics, including structure prediction of proteins and protein complexes, virtual drug screening and molecular design, and omics data mining. She has published 20 papers as first or corresponding author in journals such as Genome Biology, Cell Reports Physical Science and Nucleic Acids Research, has led two NSFC grants, and received the First Prize of the Ministry of Education Natural Science Award (4th contributor).
bio_zh: 华中科技大学生命科学与技术学院副教授、博士生导师。主要从事生物信息学研究，包括蛋白质及蛋白质复合体结构预测、虚拟药物筛选与分子设计、组学数据分析与挖掘。以第一或通讯作者在 Genome Biology、Cell Reports Physical Science、Nucleic Acids Research 等期刊发表论文 20 篇；主持国家自然科学基金 2 项；曾获教育部自然科学一等奖（第四完成人）。
email: yanw@hust.edu.cn
-->

<!-- ======================== 合作指导教师 · collaborators ========================
     合作教师用与指导教师同样的大卡片（照片 + 简介 + 单位 + 邮箱）。
     affiliation 填所在单位，会显示在名字下面那一行。
======================================================================== -->

---
group: collaborators
name: Zehua LYU
name_zh: 吕泽华
role: Associate Professor
role_zh: 副教授 · 硕士生导师
affiliation: School of Software Engineering, Huazhong University of Science and Technology
affiliation_zh: 华中科技大学软件学院
photo: assets/img/people/lv-zehua.png
bio: Associate professor at the School of Software Engineering, HUST. He received his PhD in engineering from HUST in 2007, completed postdoctoral research in control science and engineering, and joined the school in 2010. His teaching and research focus on databases, data science and big data. He has won the HUST Teaching Competition First Prize, the Hubei Young Teachers Teaching Competition Second Prize, and the "Hubei Young Teaching Expert" title.
bio_zh: 华中科技大学软件学院副教授、硕士生导师。2007 年获华中科技大学工学博士学位，在控制科学与工程流动站完成博士后研究，2010 年入职软件学院。主要从事数据库、数据科学与大数据方向的教学与科研。曾获华中科技大学教学竞赛一等奖、湖北省青年教师教学竞赛二等奖及"湖北青年教学能手"称号。
email: lvzehua@hust.edu.cn
---

---
group: collaborators
name: Shiqi OU
name_zh: 区士颀
role: Assistant Professor
role_zh: 讲师 · 硕士生导师
affiliation: School of Software Engineering, Huazhong University of Science and Technology
affiliation_zh: 华中科技大学软件学院
photo: assets/img/people/ou-shiqi.png
bio: Assistant professor and MSc supervisor at the School of Software Engineering, HUST. His research covers computer graphics and computer-aided geometric design, with current projects on VR for rehabilitation training, computer animation, and applied web development. He has published as corresponding author in PRCV (EI), EuroVR (EI) and Sensors (SCI), and holds several national invention patents. He teaches Virtual Reality, Object-Oriented Programming and related courses.
bio_zh: 华中科技大学软件学院讲师、硕士生导师，工学博士。研究领域为计算机图形学与计算机辅助几何设计，当前主要课题为面向康复训练的 VR 开发、计算机动画技术及应用型 Web 项目开发。以通讯作者在 PRCV（EI）、EuroVR（EI）、Sensors（SCI）等会议和期刊发表论文多篇，合作获国家发明专利多项。主讲《虚拟现实》《面向对象程序设计》等课程。
email: smartvision@sina.com
---

---
group: collaborators
name: Lei WANG
name_zh: 王雷
role: Associate Research Professor
role_zh: 特任副研究员
affiliation: School of Chemistry, Central China Normal University
affiliation_zh: 华中师范大学化学学院
photo: assets/img/people/wang-lei.jpeg
bio: Associate research professor at the School of Chemistry, Central China Normal University. He earned his PhD in bioinformatics at HUST and was a postdoc in computer science there. His research applies AI to bioinformatics, covering protein/RNA structure and function prediction, neuropeptide computing, and peptide drug design. He developed ProtFlash, NeuroPred-PLM, DeepNeuropePred, ProtFormer-Site and SSAlign, with publications in Cell Reports Physical Science, Briefings in Bioinformatics and Journal of Molecular Biology; his open-source tools have earned 500+ GitHub stars.
bio_zh: 华中师范大学化学学院特任副研究员，华中科技大学生物信息学博士、计算机科学与技术流动站博士后。研究方向为人工智能与生物信息学，涵盖蛋白质/RNA 结构与功能预测、神经肽计算与肽药物智能设计。开发了 ProtFlash、NeuroPred-PLM、DeepNeuropePred、ProtFormer-Site、SSAlign 等模型与工具，成果发表于 Cell Reports Physical Science、Briefings in Bioinformatics、Journal of Molecular Biology 等；开源项目累计获 GitHub 500+ Stars。
email: wanglei@ccnu.edu.cn
---

<!-- ======================== 博士后与专职研究人员 · staff ========================
     含研究助理。这一组的 bio 只作一行研究方向显示。
========================================================================== -->

---
group: staff
name: Hongyang YE
name_zh: 叶宏阳
role: Research Assistant · MSc
role_zh: 研究助理 · 硕士
photo: assets/img/people/ye-hongyang.jpg
bio: Lecturer for the Big Data and AI training programme at the HUST School of Continuing Education, and a senior AI development engineer with five years of Python experience. His research covers protein language models, structure-aware representation learning and intelligent bioinformatics analysis, and he explores LLM applications such as intelligent teaching assistants and automated assessment.
bio_zh: 华中科技大学教育培训学院大数据与人工智能培训项目讲师，人工智能高级开发工程师，5 年 Python 开发经验。研究方向：蛋白质语言模型、结构感知表示学习、生物信息智能分析；并关注大模型在教学提效（智能助教、自动评测）与智能体应用中的落地。
---

<!-- ======================== 在读学生 · students ========================
     这一组渲染成紧凑名单（三列网格：姓名 / 年级学位 / 邮箱），不是卡片，
     所以千万别加 photo、bio——写了也不会显示。
     按年级排序：博士 → 硕2024 → 硕2025 → 硕2026（顺序即文件顺序）。
     姓名与年级来自钉钉「人员分组-博士生/硕2024/硕2025/硕2026」，
     邮箱来自资料库「团队成员邮箱表」；未提供邮箱的留空即可。
====================================================================== -->

---
group: students
name: Haozhe ZHAO
name_zh: 赵浩哲
role: PhD student
role_zh: 博士研究生
email: 15632059828@163.com
---

---
group: students
name: Xiaohan ZHONG
name_zh: 钟枭晗
role: PhD student
role_zh: 博士研究生
email: xhanzhong@hust.edu.cn
---

---
group: students
name: Mingxia WANG
name_zh: 王明霞
role: PhD student
role_zh: 博士研究生
email: 1401732230@qq.com
---

---
group: students
name: Yating HUANG
name_zh: 黄雅婷
role: MSc student, 2024 intake
role_zh: 2024 级硕士研究生
email: 1137363187@qq.com
---

---
group: students
name: Yinghang HE
name_zh: 贺应航
role: MSc student, 2024 intake
role_zh: 2024 级硕士研究生
email: 798058131@qq.com
---

---
group: students
name: Shuo LYU
name_zh: 吕硕
role: MSc student, 2024 intake
role_zh: 2024 级硕士研究生
email: 1983007976@qq.com
---

---
group: students
name: Yiyao DU
name_zh: 杜怡瑶
role: MSc student, 2024 intake
role_zh: 2024 级硕士研究生
email: dyy9521@163.com
---

---
group: students
name: Jun LUO
name_zh: 罗俊
role: MSc student, 2024 intake
role_zh: 2024 级硕士研究生
email: luojun21@foxmail.com
---

---
group: students
name: Zhaofeng HUANG
name_zh: 黄兆锋
role: MSc student, 2025 intake
role_zh: 2025 级硕士研究生
---

---
group: students
name: Zhuojing GUO
name_zh: 郭卓静
role: MSc student, 2025 intake
role_zh: 2025 级硕士研究生
email: 1250141836@qq.com
---

---
group: students
name: Ximing PAN
name_zh: 潘溪铭
role: MSc student, 2025 intake
role_zh: 2025 级硕士研究生
email: 3074934657@qq.com
---

---
group: students
name: Xinyao TAI
name_zh: 邰馨瑶
role: MSc student, 2025 intake
role_zh: 2025 级硕士研究生
---

---
group: students
name: Ziyi GUAN
name_zh: 关子逸
role: MSc student, 2025 intake
role_zh: 2025 级硕士研究生
email: 1500133537@qq.com
---

---
group: students
name: Yuhan ZHANG
name_zh: 张裕函
role: MSc student, 2025 intake
role_zh: 2025 级硕士研究生
email: zhangyuhanjob@163.com
---

---
group: students
name: Wensha CHEN
name_zh: 陈文沙
role: MSc student, 2025 intake
role_zh: 2025 级硕士研究生
email: 2647372285@qq.com
---

---
group: students
name: Xindi LIU
name_zh: 刘新迪
role: MSc student, 2025 intake
role_zh: 2025 级硕士研究生
email: 2426560650@qq.com
---

---
group: students
name: Zhe HU
name_zh: 胡喆
role: MSc student, 2026 intake
role_zh: 2026 级硕士研究生
email: kasumippp123@gmail.com
---

---
group: students
name: Boyu GONG
name_zh: 龚博宇
role: MSc student, 2026 intake
role_zh: 2026 级硕士研究生
email: wuyazai_11@163.com
---

---
group: students
name: Zhirui FU
name_zh: 傅志锐
role: MSc student, 2026 intake
role_zh: 2026 级硕士研究生
email: zhiruifu@hust.edu.cn
---

---
group: students
name: Xiaocheng YAN
name_zh: 颜晓程
role: MSc student, 2026 intake
role_zh: 2026 级硕士研究生
email: 2191253899@qq.com
---

---
group: students
name: Zekai LI
name_zh: 李泽楷
role: MSc student, 2026 intake
role_zh: 2026 级硕士研究生
email: 2986731967@qq.com
---

---
group: students
name: Yuncheng MA
name_zh: 马云程
role: MSc student, 2026 intake
role_zh: 2026 级硕士研究生
email: 1732600429@qq.com
---

---
group: students
name: Jie YUAN
name_zh: 袁劼
role: MSc student, 2026 intake
role_zh: 2026 级硕士研究生
email: 2674670263@qq.com
---

<!-- ======================== 同事与校友 · alumni ========================
     在 role 里写上届次/原岗位和去向，一行就能说明白。
     仍在课题组合作的校友照常写进 collaborators，两栏各出现一次。
==================================================================== -->

---
group: alumni
name: Lei WANG
name_zh: 王雷
role: Former postdoc · now Associate Research Professor, Central China Normal University
role_zh: 出站博士后 · 现华中师范大学化学学院特任副研究员
---

---
group: alumni
name: Jingxiang LU
name_zh: 卢璟祥
role: Former project manager · Ph.D. student, National Radio and Television Research Center, HUST
role_zh: 原项目经理 · 现华中科技大学国家广电研究中心博士
---

<!-- 示例校友（占位，已由上面两条真实记录取代，需要时照此复制）：
---
group: alumni
name: Alumnus A
name_zh: 示例校友甲
role: MSc 2024 · now at Tencent
role_zh: 2024 届硕士 · 现就职于腾讯
---
-->
