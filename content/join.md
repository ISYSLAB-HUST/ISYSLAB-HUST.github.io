<!--
  ============================================================================
   招生与联系 · Join Us & Contact
  ============================================================================
   本页（join.html）的全部内容都在这个文件里维护，保存后预览自动刷新。
   一条记录一段，段落之间用单独一行的三个短横线分隔；
   用 kind 字段区分记录类型：header / position / contact / map。

   ── 字段 ────────────────────────────────────────────────────────────────
   【kind: header】页面标题区（只有一条，放在文件最前面）
     eyebrow / eyebrow_zh    眉题小字
     title   / title_zh      页面大标题
     sub     / sub_zh        副标题
     pos_h2  / pos_h2_zh     「招生方向」小节标题
     contact_h2 / contact_h2_zh  「联系方式」小节标题

   【kind: position】招生方向卡片（每条一张卡片）
     role    / role_zh       招生类别
     req     / req_zh        要求说明
     note    / note_zh       补充一行小字（可省略）

   【kind: contact】联系方式卡片
     label   / label_zh      栏目名（邮箱 / 地址 / 办公室…）
     value   / value_zh      内容
     link                    可选。写了就渲染成链接（如 mailto:...）

   【kind: map】地图（只有一条）
     image                   图片路径（assets/img/map.png）
     alt     / alt_zh        图片描述
     link                    「在高德地图中查看」的跳转地址
     link_text / link_text_zh  链接文字

   ── 维护提示 ────────────────────────────────────────────────────────────
   · 英文和中文各写一行；中文留空时英文界面回落到英文字段、中文界面回落到英文。
   · 字段值写在冒号后面同一行；字段之间允许空行。
  ============================================================================
-->

---
kind: header
eyebrow: JOIN US & CONTACT
eyebrow_zh: 招生与联系
title: Join Us & Contact
title_zh: 招生与联系
sub: Positions are open year-round — apply by email. We welcome postdocs, master's & PhD students and undergraduate researchers.
sub_zh: 长期开放申请，邮件投递即可。欢迎博士后、硕士与博士研究生以及本科科研实习生加入。
pos_h2: Open Positions
pos_h2_zh: 招生方向
contact_h2: Contact
contact_h2_zh: 联系方式
---

---
kind: position
role: Postdoctoral Researchers
role_zh: 博士后研究人员
req: PhD in Computer Science, Bioinformatics or related fields; strong programming skills; experience in machine learning or bioinformatics.
req_zh: 计算机、生物信息学或相关专业博士；编程能力强；有机器学习或生物信息学研究经验。
note: Salary from RMB 200,000/year · research funding support · international collaboration opportunities.
note_zh: 年薪 20 万元起 · 提供科研经费支持 · 国际合作交流机会。
---

---
kind: position
role: Master's & PhD Students
role_zh: 硕士 / 博士研究生
req: Join via the school's admission process (summer camp / pre-recommendation / unified exam). Research in bioinformatics, machine learning and medical AI.
req_zh: 通过学院招生流程报考（夏令营 / 预推免 / 统考）。研究方向为生物信息学、机器学习与医疗人工智能。
note: Excellent applicants are encouraged to contact us in advance.
note_zh: 欢迎优秀考生提前联系。
---

---
kind: position
role: Undergraduate Students
role_zh: 本科实习生
req: Research internships and final-year projects — get involved in the lab's ongoing projects early.
req_zh: 提供科研实习与毕业设计机会，可尽早参与实验室在研项目。
note: Available topics and supervision details to be added.
note_zh: 可参与课题与指导安排待补充。
---

---
kind: contact
label: Email
label_zh: 邮箱
value: zdxue@hust.edu.cn
link: mailto:zdxue@hust.edu.cn
---

---
kind: contact
label: Address
label_zh: 地址
value: 1037 Luoyu Road, Hongshan District, Wuhan, China
value_zh: 中国 湖北省武汉市洪山区珞喻路 1037 号华中科技大学软件学院
---

---
kind: contact
label: Office
label_zh: 办公室
value: Enming Building (East Campus), School of Software Engineering, HUST
value_zh: 华中科技大学东校区恩明楼 软件学院
---

---
kind: map
image: assets/img/map.png
alt: Map — School of Software Engineering, HUST (Enming Building, East Campus)
alt_zh: 地图 — 华中科技大学东校区恩明楼（软件学院）
link: https://ditu.amap.com/search?query=%E5%8D%8E%E4%B8%AD%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6%E8%BD%AF%E4%BB%B6%E5%AD%A6%E9%99%A2
link_text: Open in Amap Maps
link_text_zh: 在高德地图中查看
