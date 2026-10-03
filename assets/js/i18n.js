/* ============================================================
   iSyslab site — bilingual strings + language manager
   English is the default (academic audience); 中文 is a switch.

   Markup contract
   ----------------
     <span data-i18n="nav.home">Home</span>            -> textContent swap
     <h1 data-i18n="home.hero.title" data-i18n-html>   -> innerHTML swap
   The hard-coded text inside the element is the EN fallback, so the
   page stays readable and SEO-indexable even with JS disabled.

   Page-level <title> / <meta description> are driven by
   <body data-page="home"> + STRINGS[lang]['page.home.title'|'page.home.desc'].

   Keys present in `en` but missing in `zh` fall back to English.

   Language resolution order:  ?lang=zh  >  localStorage  >  English.
   ============================================================ */

(function (window) {
  'use strict';

  var STORAGE_KEY = 'isyslab-lang';

  var STRINGS = {
    en: {
      /* ---------- shared chrome ---------- */
      'brand': 'iSyslab',
      'brand.sub': "Zhidong's Research Group @ HUST",
      'nav.home': 'Home',
      'nav.research': 'Research',
      'nav.people': 'People',
      'nav.pubs': 'Publications',
      'nav.patents': 'Patents',
      'nav.software': 'Software',
      'nav.teaching': 'Teaching',
      'nav.news': 'News',
      'nav.gallery': 'Gallery',
      'nav.join': 'Join Us',

      'footer.tagline': 'Intelligent Systems Lab @ HUST<br>AI software &amp; applications for gaming, bioinformatics and healthcare',
      'footer.site': 'Site',
      'footer.explore': 'Explore',
      'footer.contact': 'Contact',
      'footer.school': 'School of Software Engineering, Huazhong University of Science and Technology',
      'footer.address': '1037 Luoyu Road, Wuhan, Hubei, China',
      'footer.postcode': 'Postcode 430073',
      'footer.copyright': '© 2026 iSyslab · Intelligent Systems Lab, HUST',

      /* ---------- page metadata ---------- */
      'page.home.title': 'iSyslab · Intelligent Systems Lab, HUST',
      /* 'page.home.desc' is generated from content/about.md — see tools/build.py */
      'page.research.title': 'Research · iSyslab, HUST',
      'page.research.desc': 'Five research directions spanning large language models, VR and games, image and video processing, biological macromolecule prediction and software, and AI security and privacy.',
      'page.people.title': 'People · iSyslab, HUST',
      'page.people.desc': 'Faculty, postdocs and staff of iSyslab — Intelligent Systems Lab, Huazhong University of Science and Technology.',
      'page.pubs.title': 'Publications · iSyslab, HUST',
      'page.pubs.desc': '46 publications, 2001–2026 — iSyslab, Intelligent Systems Lab, Huazhong University of Science and Technology.',
      'page.news.title': 'News · iSyslab, HUST',
      'page.news.desc': 'Publications, projects and lab life — updates from iSyslab.',
      'page.join.title': 'Join Us & Contact · iSyslab, HUST',
      'page.join.desc': "Positions are open year-round — apply by email. We welcome postdocs, master's & PhD students and undergraduate researchers.",
      'page.software.title': 'Software & Projects · iSyslab, HUST',
      'page.software.desc': 'Online servers and databases, plus open-source research code — maintained and released by iSyslab.',
      'page.patents.title': 'Patents · iSyslab, HUST',
      'page.patents.desc': 'Chinese invention patents and utility models from iSyslab, including cross-institution collaborations.',
      'page.teaching.title': 'Teaching & Textbooks · iSyslab, HUST',
      'page.teaching.desc': 'Courses taught by iSyslab faculty, and the textbooks they authored on big data, blockchain and intelligent software.',
      'page.gallery.title': 'Gallery · iSyslab, HUST',
      'page.gallery.desc': 'Moments from the lab — group photos, conference talks and research demos.',

      /* ---------- home ---------- */
      'home.hero.title': 'AI Software &amp; Applications,<br>Built for the Real World',
      /* 'home.hero.sub' (the lab introduction) is rendered from
         content/about.md into a bilingual span — edit it there. */
      'home.cta.primary': 'Explore Our Research',
      'home.cta.secondary': 'View Publications',
      'home.cta.join': 'Join Us',
      'home.stat.pubs': 'Publications',
      'home.stat.tools': 'Software & Projects',
      'home.stat.areas': 'Research Areas',
      'home.visual.caption': 'Huazhong University of Science &amp; Technology<br>Wuhan, China',

      'home.res.eyebrow': 'RESEARCH',
      'home.res.title': 'Research Interests',
      'home.res.sub': 'Five directions from large language models and VR to biological macromolecule software and AI security — from algorithms to usable systems.',
      'home.res.all': 'All directions →',

      'home.c1.title': 'Image &amp; Video Processing',
      'home.c1.sub': '图像与视频处理',
      'home.c1.desc': 'Visual computing for image and video analysis — enhancement, restoration and understanding in real acquisition scenarios.',
      'home.c2.title': 'VR &amp; Rehabilitation Games',
      'home.c2.sub': '虚拟现实与康复游戏',
      'home.c2.desc': 'Virtual reality and serious games for rehabilitation — interactive training, motion tracking and quantitative assessment.',
      'home.c3.title': 'Machine Learning &amp; CUDA Acceleration',
      'home.c3.sub': '机器学习与 CUDA 加速',
      'home.c3.desc': 'Machine-learning models accelerated on GPUs with CUDA — bringing deep-learning workloads to practical speed.',
      'home.c4.title': 'Bioinformatics Algorithms &amp; Software',
      'home.c4.sub': '生物信息学算法与软件研发',
      'home.c4.desc': 'Algorithm and software R&amp;D for bioinformatics — sequence analysis, domain prediction and protein language models.',
      'home.c5.title': 'Cloud-based Data Processing',
      'home.c5.sub': '基于云平台的数据处理',
      'home.c5.desc': 'Scalable data-processing pipelines on cloud platforms for large-scale scientific and biomedical datasets.',
      'home.c6.title': 'Protein Structure, Function &amp; Interaction Prediction',
      'home.c6.sub': '蛋白质结构、功能与互作网络预测',
      'home.c6.desc': 'Computational prediction of protein structure, function and interaction networks — from threading to protein language models.',
      'home.c7.title': 'Medical Big Data Analysis',
      'home.c7.sub': '医疗大数据分析',
      'home.c7.desc': 'Analysis of large-scale medical data — imaging, clinical records and omics — to support diagnosis and research.',

      'home.news.eyebrow': 'NEWS',
      'home.news.title': 'Latest News',
      'home.news.all': 'All news →',

      'home.pub.eyebrow': 'SELECTED PUBLICATIONS',
      'home.pub.title': 'Selected Publications',
      'home.pub.all': 'All publications →',

      'home.join.title': 'Join iSyslab',
      'home.join.desc': "We recruit postdocs, master's &amp; PhD students and undergraduate researchers year-round. Postdoc salary starts from RMB 200,000/year.",
      'home.join.btn': 'View Open Positions',

      /* ---------- news items (shared home + news page) ---------- */
      'news.1.date': 'Feb 2024',
      'news.1.text': 'NeuroPep 2.0 published in Journal of Molecular Biology — the updated neuropeptide &amp; receptor annotation database',
      'news.1.text.long': 'NeuroPep 2.0 published in Journal of Molecular Biology — the updated neuropeptide &amp; receptor annotation database is now available',
      'news.2.date': 'Jan 2024',
      'news.2.text': 'DeepNeuropePred published in Computational and Structural Biotechnology Journal — robust neuropeptide cleavage-site prediction',
      'news.2.text.long': 'DeepNeuropePred published in Computational and Structural Biotechnology Journal — robust neuropeptide cleavage-site prediction from protein language models',
      'news.3.date': 'Oct 2023',
      'news.3.text': 'ProtFlash published in Cell Reports Physical Science — a lightweight protein language model for the protein landscape',
      'news.3.text.long': 'ProtFlash published in Cell Reports Physical Science — a lightweight protein language model deciphering the protein landscape',
      'news.4.date': 'Mar 2023',
      'news.4.text': 'NeuroPred-PLM published in Briefings in Bioinformatics — interpretable neuropeptide prediction with protein language models',
      'news.4.text.long': 'NeuroPred-PLM published in Briefings in Bioinformatics — interpretable and robust neuropeptide prediction',
      'news.tag.paper': 'Paper',

      'news.eyebrow': 'NEWS',
      'news.title': 'News',
      'news.sub': 'Publications, projects and lab life — updates from iSyslab.',

      /* ---------- research page ---------- */
      'res.eyebrow': 'RESEARCH AREAS',
      'res.title': 'Research',
      'res.sub': 'Five research directions spanning large language models, VR and games, image and video processing, biological macromolecule prediction and software, and AI security and privacy.',

      'res.r1.eyebrow': '01 / IMAGE &amp; VIDEO PROCESSING',
      'res.r1.title': 'Image and Video Processing',
      'res.r1.cn': '图像与视频处理',
      'res.r1.desc': 'Visual computing methods for the analysis, enhancement and understanding of image and video data — from hand-pose estimation with wearable sensors to clinical image classification.',
      'res.r1.tags': 'Hand pose estimation · Image classification · Video understanding',

      'res.r2.eyebrow': '02 / VR &amp; REHABILITATION GAMES',
      'res.r2.title': 'Virtual Reality and Rehabilitation Games',
      'res.r2.cn': '虚拟现实与康复游戏',
      'res.r2.desc': 'VR serious games designed for rehabilitation training — combining interactive gameplay with motion tracking and quantitative assessment of patient recovery.',
      'res.r2.tags': 'Serious games · Motion tracking · Rehabilitation assessment',

      'res.r3.eyebrow': '03 / MACHINE LEARNING &amp; CUDA',
      'res.r3.title': 'Machine Learning and CUDA Acceleration',
      'res.r3.cn': '机器学习与 CUDA 加速',
      'res.r3.desc': 'Machine-learning models with GPU acceleration — using CUDA to bring deep-learning and scientific-computing workloads to practical speed, e.g. scalable structure alignment with Spark and OpenMP.',
      'res.r3.tags': 'GPU computing · Model training · Performance engineering',

      'res.r4.eyebrow': '04 / BIOINFORMATICS ALGORITHMS &amp; SOFTWARE',
      'res.r4.title': 'Algorithm and Software R&amp;D in Bioinformatics',
      'res.r4.cn': '生物信息学算法与软件研发',
      'res.r4.desc': 'Our core strength: algorithms and software for bioinformatics — protein domain prediction, neuropeptide identification and protein language models such as ProtFlash, released as web servers and open-source tools.',
      'res.r4.tags': 'Protein LMs · Domain prediction · Web servers',

      'res.r5.eyebrow': '05 / CLOUD-BASED DATA PROCESSING',
      'res.r5.title': 'Data Processing based on Cloud Platform',
      'res.r5.cn': '基于云平台的数据处理',
      'res.r5.desc': 'Scalable data-processing pipelines on cloud platforms, built for large-scale scientific and biomedical datasets.',
      'res.r5.tags': 'Cloud pipelines · Large-scale data · Distributed computing',

      'res.r6.eyebrow': '06 / PROTEIN STRUCTURE &amp; FUNCTION',
      'res.r6.title': 'Protein Structure, Function and Interaction Network Prediction',
      'res.r6.cn': '蛋白质结构、功能与互作网络预测',
      'res.r6.desc': 'From threading-based methods (ThreaDomEx, I-TASSER-MR) to protein language models (ProtFlash) — predicting protein structure, function and interaction networks, including ab initio folding fueled by metagenomics.',
      'res.r6.tags': 'Structure prediction · Ab initio folding · Interaction networks',

      'res.r7.eyebrow': '07 / MEDICAL BIG DATA',
      'res.r7.title': 'Medical Big Data Analysis',
      'res.r7.cn': '医疗大数据分析',
      'res.r7.desc': 'Analysis of large-scale medical data — imaging, clinical records and omics — in collaboration with clinicians, to support diagnosis and biomedical research.',
      'res.r7.tags': 'Clinical data · Imaging · Omics integration',

      /* ---------- people ---------- */
      'people.eyebrow': 'PEOPLE',
      'people.title': 'People',
      'people.sub': 'Faculty, collaborating faculty, postdocs and staff, current students, colleagues and alumni of iSyslab.',
      'people.faculty': 'Faculty',
      'people.postdoc': 'Postdoc &amp; Staff',
      'people.alumni': 'Colleagues &amp; Alumni',
      'people.alumni.note': 'To be added — former members, colleagues and their next steps will be listed here.',

      /* ---------- publications ---------- */
      'pub.eyebrow': 'PUBLICATIONS',
      'pub.title': 'Publications',
      'pub.filter.all': 'All',

      /* ---------- patents ---------- */
      'pat.eyebrow': 'PATENTS',
      'pat.title': 'Patents',
      'pat.sub': 'Chinese invention patents and utility models, including cross-institution collaborations.',
      'pat.filter.all': 'All',

      /* ---------- teaching & textbooks ---------- */
      'teach.eyebrow': 'TEACHING & TEXTBOOKS',
      'teach.title': 'Teaching & Textbooks',
      'teach.sub': 'Courses taught by iSyslab faculty, and the textbooks and monographs they authored.',
      'teach.courses': 'Courses',
      'teach.courses.sub': 'Course listings by instructor.',

      'book.title': 'Textbooks',
      'book.sub': 'Textbooks and monographs authored by iSyslab faculty.',


      /* ---------- software & projects (merged) ---------- */
      'sw.crumb': 'Software &amp; Projects',
      'sw.title': 'Software &amp; Projects',
      'sw.sub': 'Online servers and curated databases, plus the research code we release on GitHub — all free for academic use.',
      'sw.sec1': 'Online Servers &amp; Databases',
      'sw.sec1.sub': '6 tools · Bioinformatics',
      'sw.c1.desc': 'A unified online server combining ThreaDom and DomEx for accurate protein domain prediction on both continuous and discontinuous domain structures. Supports interactive editing and re-detection of domain models.',
      'sw.c2.desc': 'Protein domain prediction based on multiple threading programs. Reports boundaries more accurately than most predictors — especially for medium and hard targets — and detects discontinuous domains via boundary clustering.',
      'sw.c3.desc': 'Assembles continuous domain segments so that boundary predictors can detect discontinuous domains. Recalled 26.7% discontinuous domains at 72.7% precision in a 29-chain benchmark where ThreaDom failed. Source code and datasets available.',
      'sw.c4.desc': 'The most complete neuropeptide database available. Release 1.0 holds 5,949 non-redundant entries from 493 organisms across 65 families, all manually curated from MEDLINE, UniProt and Neuropedia. Version 2.0 accompanied by the NeuroPep 2.0 paper.',
      'sw.c5.desc': 'A structure database of bioactive peptides: 1,199 peptides and 3,536 PDB chains across six categories (Toxin &amp; Venom, Antimicrobial, Cytokine &amp; Growth factor, Hormone, Neuropeptide, Others). Includes BLAST, mapping and secondary-structure tools.',
      'sw.c6.desc': 'Automated molecular replacement for distant-homology proteins using iterative fragment assembly and progressive sequence truncation. Generated full-length models at average TM-score 0.773 and found correct MR solutions for 95 of 161 targets.',
      'sw.sec2': 'Open-source Repositories',
      'sw.sec2.sub': '6 repositories · github.com/ISYSLAB-HUST',
      'sw.r1.desc': 'A lightweight protein language model — deciphers the protein landscape at a fraction of the compute cost of large-scale PLMs.',
      'sw.r2.desc': 'Topology prediction of α-helical transmembrane proteins with deep transfer learning.',
      'sw.r3.desc': 'A robust and universal tool to predict cleavage sites from neuropeptide precursors by protein language model.',
      'sw.r4.desc': 'An interpretable and robust model for neuropeptide prediction by protein language model.',
      'sw.r5.desc': 'Predicting protein domain boundary from sequence using deep residual network and Bi-LSTM.',
      'sw.r6.desc': 'DNA storage in life, implemented with RaptorQ fountain codes.',
      'sw.view': 'View on GitHub',

      /* ---------- gallery ---------- */
      'gal.crumb': 'Gallery',
      'gal.title': 'Gallery',
      'gal.sub': 'Moments from the lab — group photos, conference talks and research demos.',
      'gal.a1': 'Lab Photos',
      'gal.a2': 'Events',
      'gal.a3': 'Research Highlights',
      'gal.count1': '1 photo',
      'gal.p1': 'Lab Group Photo 2024',
      'gal.p2': 'Conference Presentation 2024',
      'gal.p3': 'Research Project Demo',
      'gal.note': 'Add more photos to /assets/img/gallery/ — the grid grows automatically.',

      /* ---------- misc ---------- */
      'crumb.home': 'Home'
    },

    zh: {
      /* ---------- shared chrome ---------- */
      'brand': 'iSyslab',
      'brand.sub': '薛志东课题组 @ 华中科技大学',
      'nav.home': '首页',
      'nav.research': '研究方向',
      'nav.people': '团队成员',
      'nav.pubs': '论文发表',
      'nav.patents': '专利',
      'nav.software': '软件与项目',
      'nav.teaching': '教学与教材',
      'nav.news': '新闻动态',
      'nav.gallery': '实验室相册',
      'nav.join': '加入我们',

      'footer.tagline': '智能系统实验室@HUST<br>面向游戏、生物信息与医疗的人工智能软件与应用研发',
      'footer.site': '网站导航',
      'footer.explore': '更多内容',
      'footer.contact': '联系方式',
      'footer.school': '华中科技大学软件学院',
      'footer.address': '湖北省武汉市珞喻路 1037 号',
      'footer.postcode': '邮编 430073',
      'footer.copyright': '© 2026 iSyslab · 智能系统实验室',

      /* ---------- page metadata ---------- */
      'page.home.title': 'iSyslab 智能系统实验室 · 华中科技大学',
      /* 'page.home.desc' is generated from content/about.md — see tools/build.py */
      'page.research.title': '研究方向 · iSyslab 智能系统实验室',
      'page.research.desc': '五个研究方向，覆盖大模型技术与应用、虚拟现实与计算机游戏、图像与视频处理、生物大分子预测与软件、人工智能安全与隐私保护。',
      'page.people.title': '团队成员 · iSyslab 智能系统实验室',
      'page.people.desc': 'iSyslab 智能系统实验室的指导教师、博士后与专职人员名单。',
      'page.pubs.title': '论文发表 · iSyslab 智能系统实验室',
      'page.pubs.desc': '2001–2026 年共 46 篇论文，含中文期刊论文。',
      'page.news.title': '新闻动态 · iSyslab 智能系统实验室',
      'page.news.desc': '论文发表、项目进展与实验室日常动态。',
      'page.join.title': '招生与联系 · iSyslab 智能系统实验室',
      'page.join.desc': '长期招收博士后、硕士与博士研究生及本科科研实习生，邮件联系申请。',
      'page.software.title': '软件与开源项目 · iSyslab 智能系统实验室',
      'page.software.desc': 'iSyslab 在线服务与数据库，以及在 GitHub 开源的研究代码。',
      'page.patents.title': '专利 · iSyslab 智能系统实验室',
      'page.patents.desc': '课题组中国发明专利与实用新型，含跨单位合作成果。',
      'page.teaching.title': '教学与教材 · iSyslab 智能系统实验室',
      'page.teaching.desc': '课题组成员承担的课程，以及主编的大数据、区块链与智能软件方向教材。',
      'page.gallery.title': '实验室相册 · iSyslab 智能系统实验室',
      'page.gallery.desc': '实验室合影、学术会议与研究演示的影像记录。',

      /* ---------- home ---------- */
      'home.hero.title': '面向真实世界的<br>人工智能软件与应用',
      /* 'home.hero.sub' (the lab introduction) is rendered from
         content/about.md into a bilingual span — edit it there. */
      'home.cta.primary': '浏览研究方向',
      'home.cta.secondary': '查看论文成果',
      'home.cta.join': '加入我们',
      'home.stat.pubs': '发表论文',
      'home.stat.tools': '软件与开源项目',
      'home.stat.areas': '研究方向',
      'home.visual.caption': '华中科技大学<br>中国 · 武汉',

      'home.res.eyebrow': '研究方向',
      'home.res.title': '研究兴趣',
      'home.res.sub': '五个研究方向，覆盖大模型、虚拟现实与游戏、图像视频处理、生物大分子预测与 AI 安全——从算法研究到可用系统。',
      'home.res.all': '全部方向 →',

      'home.c1.title': '图像与视频处理',
      'home.c1.sub': 'Image &amp; Video Processing',
      'home.c1.desc': '面向图像与视频的分析计算——真实采集场景下的增强、复原与理解。',
      'home.c2.title': '虚拟现实与康复游戏',
      'home.c2.sub': 'VR &amp; Rehabilitation Games',
      'home.c2.desc': '面向康复训练的虚拟现实与严肃游戏——交互训练、动作追踪与量化评估。',
      'home.c3.title': '机器学习与 CUDA 加速',
      'home.c3.sub': 'Machine Learning &amp; CUDA Acceleration',
      'home.c3.desc': '使用 CUDA 在 GPU 上加速机器学习模型——让深度学习负载达到实用速度。',
      'home.c4.title': '生物信息学算法与软件研发',
      'home.c4.sub': 'Bioinformatics Algorithms &amp; Software',
      'home.c4.desc': '生物信息学的算法与软件研发——序列分析、结构域预测与蛋白质语言模型。',
      'home.c5.title': '基于云平台的数据处理',
      'home.c5.sub': 'Cloud-based Data Processing',
      'home.c5.desc': '云平台上可扩展的数据处理流水线，服务大规模科学与生物医学数据。',
      'home.c6.title': '蛋白质结构、功能与互作网络预测',
      'home.c6.sub': 'Protein Structure, Function &amp; Interaction',
      'home.c6.desc': '蛋白质结构、功能与互作网络的计算预测——从穿线法到蛋白质语言模型。',
      'home.c7.title': '医疗大数据分析',
      'home.c7.sub': 'Medical Big Data Analysis',
      'home.c7.desc': '大规模医疗数据分析——影像、临床记录与组学——支撑临床诊断与医学研究。',

      'home.news.eyebrow': '新闻动态',
      'home.news.title': '最新动态',
      'home.news.all': '全部动态 →',

      'home.pub.eyebrow': '代表性成果',
      'home.pub.title': '精选论文',
      'home.pub.all': '全部论文 →',

      'home.join.title': '加入 iSyslab',
      'home.join.desc': '长期招收博士后、硕士与博士研究生以及本科科研实习生。博士后年薪 20 万元起。',
      'home.join.btn': '查看招生信息',

      /* ---------- news items ---------- */
      'news.1.date': '2024 年 2 月',
      'news.1.text': 'NeuroPep 2.0 发表于 Journal of Molecular Biology——更新版神经肽及其受体注释数据库',
      'news.1.text.long': 'NeuroPep 2.0 发表于 Journal of Molecular Biology——更新版神经肽及其受体注释数据库现已上线',
      'news.2.date': '2024 年 1 月',
      'news.2.text': 'DeepNeuropePred 发表于 Computational and Structural Biotechnology Journal——稳健的神经肽切割位点预测',
      'news.2.text.long': 'DeepNeuropePred 发表于 Computational and Structural Biotechnology Journal——基于蛋白质语言模型的稳健神经肽切割位点预测',
      'news.3.date': '2023 年 10 月',
      'news.3.text': 'ProtFlash 发表于 Cell Reports Physical Science——轻量级蛋白质语言模型',
      'news.3.text.long': 'ProtFlash 发表于 Cell Reports Physical Science——解析蛋白质序列景观的轻量级语言模型',
      'news.4.date': '2023 年 3 月',
      'news.4.text': 'NeuroPred-PLM 发表于 Briefings in Bioinformatics——可解释的神经肽预测模型',
      'news.4.text.long': 'NeuroPred-PLM 发表于 Briefings in Bioinformatics——基于蛋白质语言模型的可解释、稳健的神经肽预测方法',
      'news.tag.paper': '论文',

      'news.eyebrow': '新闻动态',
      'news.title': '新闻动态',
      'news.sub': '论文发表、项目进展与实验室日常动态。',

      /* ---------- research page ---------- */
      'res.eyebrow': '研究方向',
      'res.title': '研究方向',
      'res.sub': '五个研究方向，覆盖大模型技术与应用、虚拟现实与计算机游戏、图像与视频处理、生物大分子预测与软件、人工智能安全与隐私保护。',

      'res.r1.eyebrow': '01 / 图像与视频处理',
      'res.r1.title': '图像与视频处理',
      'res.r1.cn': 'Image and Video Processing',
      'res.r1.desc': '面向图像与视频数据的分析、增强与理解的视觉计算方法——从可穿戴传感器的手部姿态估计到临床图像分类。',
      'res.r1.tags': '手部姿态估计 · 图像分类 · 视频理解',

      'res.r2.eyebrow': '02 / 虚拟现实与康复游戏',
      'res.r2.title': '虚拟现实与康复游戏',
      'res.r2.cn': 'Virtual Reality and Rehabilitation Games',
      'res.r2.desc': '面向康复训练的虚拟现实严肃游戏——将交互玩法与动作追踪、康复程度的量化评估相结合。',
      'res.r2.tags': '严肃游戏 · 动作追踪 · 康复评估',

      'res.r3.eyebrow': '03 / 机器学习与 CUDA 加速',
      'res.r3.title': '机器学习与 CUDA 加速',
      'res.r3.cn': 'Machine Learning and CUDA Acceleration',
      'res.r3.desc': '利用 GPU 与 CUDA 加速机器学习模型，让深度学习与科学计算负载达到实用速度，例如基于 Spark 与 OpenMP 的大规模结构比对。',
      'res.r3.tags': 'GPU 计算 · 模型训练 · 性能优化',

      'res.r4.eyebrow': '04 / 生物信息学算法与软件',
      'res.r4.title': '生物信息学算法与软件研发',
      'res.r4.cn': 'Algorithm and Software R&amp;D in Bioinformatics',
      'res.r4.desc': '实验室的核心优势方向：生物信息学算法与软件——蛋白质结构域预测、神经肽识别，以及 ProtFlash 等蛋白质语言模型，均以在线服务与开源工具形式发布。',
      'res.r4.tags': '蛋白质语言模型 · 结构域预测 · 在线服务',

      'res.r5.eyebrow': '05 / 云平台数据处理',
      'res.r5.title': '基于云平台的数据处理',
      'res.r5.cn': 'Data Processing based on Cloud Platform',
      'res.r5.desc': '面向大规模科学与生物医学数据的云平台可扩展数据处理流水线。',
      'res.r5.tags': '云端流水线 · 大规模数据 · 分布式计算',

      'res.r6.eyebrow': '06 / 蛋白质结构与功能',
      'res.r6.title': '蛋白质结构、功能与互作网络预测',
      'res.r6.cn': 'Protein Structure, Function and Interaction Network Prediction',
      'res.r6.desc': '从穿线法方法（ThreaDomEx、I-TASSER-MR）到蛋白质语言模型（ProtFlash）——预测蛋白质结构、功能与互作网络，包括以海洋宏基因组驱动的从头折叠。',
      'res.r6.tags': '结构预测 · 从头折叠 · 互作网络',

      'res.r7.eyebrow': '07 / 医疗大数据',
      'res.r7.title': '医疗大数据分析',
      'res.r7.cn': 'Medical Big Data Analysis',
      'res.r7.desc': '与临床医生合作，对影像、临床记录与组学等大规模医疗数据进行分析，支撑临床诊断与医学研究。',
      'res.r7.tags': '临床数据 · 医学影像 · 组学融合',

      /* ---------- people ---------- */
      'people.eyebrow': '团队成员',
      'people.title': '团队成员',
      'people.sub': 'iSyslab 的指导教师、合作指导教师、博士后与专职研究人员、在读学生、同事与校友。',
      'people.faculty': '指导教师',
      'people.postdoc': '博士后与专职人员',
      'people.alumni': '同事与校友',
      'people.alumni.note': '待补充——往届成员、共事过的同事及其去向将在此列出。',

      /* ---------- publications ---------- */
      'pub.eyebrow': '论文发表',
      'pub.title': '论文发表',
      'pub.filter.all': '全部',

      /* ---------- 专利 ---------- */
      'pat.eyebrow': '专利',
      'pat.title': '专利',
      'pat.sub': '课题组中国发明专利与实用新型，含跨单位合作成果。',
      'pat.filter.all': '全部',

      /* ---------- 教学与教材 ---------- */
      'teach.eyebrow': '教学与教材',
      'teach.title': '教学与教材',
      'teach.sub': '课题组成员承担的课程，以及主编的教材与专著。',
      'teach.courses': '开设课程',
      'teach.courses.sub': '按授课教师列出。',

      'book.title': '教材',
      'book.sub': '课题组成员主编的大数据、区块链与智能软件方向教材。',


      /* ---------- software & projects (merged) ---------- */
      'sw.crumb': '软件与项目',
      'sw.title': '软件与开源项目',
      'sw.sub': '实验室维护的在线服务与数据库，以及在 GitHub 开源发布的研究代码，均对学术用途免费开放。',
      'sw.sec1': '在线服务与数据库',
      'sw.sec1.sub': '6 个工具 · 生物信息学',
      'sw.c1.desc': '整合 ThreaDom 与 DomEx 的统一在线服务，可在连续与非连续结构域上准确预测蛋白质结构域，支持结构域模型的交互式编辑与重新识别。',
      'sw.c2.desc': '基于多穿线程序的蛋白质结构域预测方法，边界预测精度优于多数同类工具（对中等与困难目标尤其明显），并通过边界聚类识别非连续结构域。',
      'sw.c3.desc': '将连续的片段组装起来，使边界预测方法能够识别非连续结构域。在 ThreaDom 失败的 29 条链基准集上，以 72.7% 的精度召回 26.7% 的非连续结构域。源码与数据集已公开。',
      'sw.c4.desc': '目前最完整的神经肽数据库。1.0 版收录来自 493 个物种、65 个家族的 5,949 条非冗余条目，全部从 MEDLINE、UniProt 与 Neuropedia 人工审编。2.0 版随 NeuroPep 2.0 论文发布。',
      'sw.c5.desc': '生物活性肽结构数据库：涵盖毒素与毒液、抗菌肽、细胞因子与生长因子、激素、神经肽及其他六大类，共 1,199 条多肽与 3,536 条 PDB 链，提供 BLAST、序列映射与二级结构工具。',
      'sw.c6.desc': '面向远同源蛋白的自动分子置换方法，采用迭代片段组装与渐进式序列截断。全长模型平均 TM-score 达 0.773，在 161 个测试目标中为 95 个找到了正确的分子置换解。',
      'sw.sec2': '开源代码仓库',
      'sw.sec2.sub': '6 个仓库 · github.com/ISYSLAB-HUST',
      'sw.r1.desc': '轻量级蛋白质语言模型——以远低于大规模 PLM 的计算开销解析蛋白质序列景观。',
      'sw.r2.desc': '基于深度迁移学习的 α-螺旋跨膜蛋白拓扑结构预测。',
      'sw.r3.desc': '基于蛋白质语言模型的通用、稳健的神经肽前体切割位点预测工具。',
      'sw.r4.desc': '基于蛋白质语言模型的可解释、稳健的神经肽预测模型。',
      'sw.r5.desc': '使用深度残差网络与 Bi-LSTM 从序列预测蛋白质结构域边界。',
      'sw.r6.desc': '基于 RaptorQ 喷泉码的在体 DNA 存储实现。',
      'sw.view': '在 GitHub 查看',

      /* ---------- gallery ---------- */
      'gal.crumb': '实验室相册',
      'gal.title': '实验室相册',
      'gal.sub': '实验室的精彩瞬间——合影、学术报告与研究演示。',
      'gal.a1': '实验室合影',
      'gal.a2': '学术活动',
      'gal.a3': '研究亮点',
      'gal.count1': '1 张照片',
      'gal.p1': '实验室合影 2024',
      'gal.p2': '学术会议报告 2024',
      'gal.p3': '研究项目演示',
      'gal.note': '将照片放入 /assets/img/gallery/ 即可自动扩展相册。',

      /* ---------- misc ---------- */
      'crumb.home': '首页'
    }
  };

  /* Merge strings generated at build time from content/about.md. They win
     over the table above, so the markdown file stays the single source of
     truth for the lab introduction. Absent when the page is opened straight
     from the source tree (no build) — the hard-coded fallbacks then apply. */
  (function mergeBuildStrings() {
    var src = window.BUILD_STRINGS;
    if (!src) return;
    ['en', 'zh'].forEach(function (l) {
      var extra = src[l];
      if (!extra || !STRINGS[l]) return;
      Object.keys(extra).forEach(function (key) {
        STRINGS[l][key] = extra[key];
      });
    });
  })();

  var lang = 'en';
  /* Priority: ?lang= (shareable deep link) > stored preference > EN default */
  var fromQuery = /[?&]lang=(en|zh)\b/.exec(window.location.search);
  if (fromQuery) {
    lang = fromQuery[1];
  } else {
    try {
      var saved = window.localStorage.getItem(STORAGE_KEY);
      if (saved === 'zh' || saved === 'en') lang = saved;
    } catch (e) { /* localStorage unavailable — keep default */ }
  }

  /* Apply the language attribute as early as possible so the switch
     highlight never flashes the wrong state. `lang` is kept in sync too —
     it drives the bilingual content generated from content/*.md. */
  if (document.documentElement) {
    document.documentElement.setAttribute('data-lang', lang);
    document.documentElement.setAttribute('lang', lang === 'zh' ? 'zh-CN' : 'en');
  }

  function dict(l) { return STRINGS[l] || STRINGS.en; }

  /* ---------- language-aware links ----------
     The chosen language is carried in the URL (?lang=zh) and propagated to
     every internal page link. This keeps the language stable across
     navigation even when localStorage is unavailable (sandboxed preview
     iframes, private windows, file:// origins) — and makes Chinese pages
     directly linkable. */
  function withLang(href) {
    if (!href || /^(https?:|mailto:|tel:|javascript:|#)/i.test(href)) return href;
    if (!/\.html($|[?#])/.test(href)) return href;
    var hash = '';
    var h = href.indexOf('#');
    if (h > -1) { hash = href.slice(h); href = href.slice(0, h); }
    /* drop any stale lang param first so switching back to EN is clean */
    href = href.replace(/([?&])lang=(en|zh)\b/g, '$1')
               .replace(/\?&/, '?')
               .replace(/[?&]+$/, '');
    if (lang === 'zh') href += (href.indexOf('?') > -1 ? '&' : '?') + 'lang=zh';
    return href + hash;
  }

  function syncLinks() {
    var links = document.querySelectorAll('a[href]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var next = withLang(a.getAttribute('href'));
      if (next !== a.getAttribute('href')) a.setAttribute('href', next);
    }
  }

  /* ---------- translation helper (used by main.js templates) ---------- */
  function t(key) {
    var d = dict(lang);
    return d[key] != null ? d[key] : (STRINGS.en[key] != null ? STRINGS.en[key] : '');
  }

  /* ---------- walk the DOM and swap every marked node ---------- */
  function translate() {
    var d = dict(lang);
    var nodes = document.querySelectorAll('[data-i18n]');
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var key = el.getAttribute('data-i18n');
      var val = d[key];
      if (val == null) val = STRINGS.en[key];
      if (val == null) continue;
      if (el.hasAttribute('data-i18n-html')) el.innerHTML = val;
      else el.textContent = val;
    }

    /* page <title> + meta description */
    var page = document.body && document.body.getAttribute('data-page');
    if (page) {
      var ttl = d['page.' + page + '.title'] || STRINGS.en['page.' + page + '.title'];
      var dsc = d['page.' + page + '.desc'] || STRINGS.en['page.' + page + '.desc'];
      if (ttl) document.title = ttl;
      if (dsc) {
        var m = document.querySelector('meta[name="description"]');
        if (m) m.setAttribute('content', dsc);
      }
    }

    /* aria labels that are language-dependent */
    var imgs = document.querySelectorAll('[data-i18n-aria]');
    for (var j = 0; j < imgs.length; j++) {
      var k2 = imgs[j].getAttribute('data-i18n-aria');
      var v2 = d[k2] || STRINGS.en[k2];
      if (v2) imgs[j].setAttribute('aria-label', v2.replace(/<[^>]+>/g, ''));
    }

    /* keep every internal link on the current language */
    syncLinks();
    markSwitch();
  }

  /* Reflect the active language on the EN / 中文 controls. */
  function markSwitch() {
    var btns = document.querySelectorAll('[data-lang-set]');
    for (var i = 0; i < btns.length; i++) {
      var on = btns[i].getAttribute('data-lang-set') === lang;
      btns[i].setAttribute('aria-pressed', on ? 'true' : 'false');
    }
  }

  /* ---------- public API ---------- */
  var I18N = {
    get lang() { return lang; },
    t: t,
    strings: STRINGS,

    /* Boot: translate everything, then wire the EN / 中文 switch. */
    init: function () {
      translate();

      var btns = document.querySelectorAll('[data-lang-set]');
      for (var i = 0; i < btns.length; i++) {
        btns[i].addEventListener('click', function () {
          I18N.set(this.getAttribute('data-lang-set'));
        });
      }
    },

    set: function (l) {
      if (l !== 'en' && l !== 'zh') return;
      lang = l;
      /* Persist the choice. Two independent mechanisms so a blocked
         localStorage never breaks the switch:
           1. localStorage  — remembers across visits
           2. ?lang= in the URL — survives navigation within the session */
      try { window.localStorage.setItem(STORAGE_KEY, l); } catch (e) { /* ignore */ }
      try {
        var u = new window.URL(window.location.href);
        if (l === 'zh') u.searchParams.set('lang', 'zh');
        else u.searchParams.delete('lang');
        window.history.replaceState(null, '', u.toString());
      } catch (e) { /* file:// or sandboxed origin — links still carry it */ }
      document.documentElement.setAttribute('data-lang', l);
      document.documentElement.setAttribute('lang', l === 'zh' ? 'zh-CN' : 'en');
      translate();
    }
  };

  window.I18N = I18N;
})(window);
