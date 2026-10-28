# Silin Chen · Academic homepage

个人学术主页，默认琥珀配色，布局参考 https://v587su.github.io/ 。提供十二套配色：原有雾蓝、松绿、陶土、灰紫、黑白、深夜，以及新增酒红、青瓷、琥珀、蔷薇、靛蓝、墨绿夜。

## 预览

在项目目录运行：

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

- 主页：http://127.0.0.1:8765/index.html
- 全部配色：http://127.0.0.1:8765/colors.html
- 新增六套：http://127.0.0.1:8765/colors.html?set=new
- 指定配色：`index.html?theme=mist`；其他值为 `pine`、`clay`、`mauve`、`ink`、`midnight`、`wine`、`celadon`、`amber`、`rose`、`indigo`、`forest`。

默认配色为琥珀 Amber（2026-10-20 确定）。主页右下角可以即时切换；明确给定的 URL 配色优先于浏览器保存的配色。浏览器存储不可用时，切换和链接仍然有效。对比页中的 iframe 固定传入配色，不会改写保存的偏好。

## 更新内容

- `index.html`：个人信息、简介、接收动态和论文。论文直接写入 HTML，不依赖 JavaScript 渲染。
- `styles.css`：每套主题的 CSS 变量，以及桌面／手机布局。
- `theme-init.js`、`app.js`：初始配色、切换与论文筛选。
- `colors.html`、`colors.css`、`colors.js`：配色对比与缩略图尺寸。
- `assets/avatar.png`：用户提供的主页头像，源文件为工作区根目录的 `大头照.png`；保留原始图片，网页用圆形样式展示。
- `content.json`：本轮整理的论文数据快照，作为内容参考；页面运行不读取它。修改快照不会自动更新 HTML。

11 条论文来自用户指定的 Google Scholar。完整作者优先使用 arXiv 元数据，其余使用 Scholar 详情。SeeRepo、AdverTest 的会议状态另经会议官网核对；Context Compression 的 EMNLP 状态另见作者主页。LLMs as Continuous Learners 使用会议官网正式标题，按 2024-11-21 首发日期归入 2024 年，venue 保留 Internetware 2026；IP&M 记录按 2026 年 8 月线上发表时间分组，venue 保留 2027 年卷期年份。共同一作：SeeRepo 依据论文正文，LLMs as Continuous Learners 依据用户 Scholar 的明确星号标记；筛选包含第一作者及共同第一作者。论文元数据仍建议在正式发布前由作者确认。

源记录位于工作区 `docs/research/`，不需要随网站发布。身份、单位、实验室、科研经历和邮箱采用用户于 2026-10-19 提供的简介；CV 尚未提供。三位导师姓名链接至各自主页。Kaggle 地址使用 GitHub 个人资料中链接的 chensilin 账户。Survey 的标题、Paper 按钮与 News 链接均使用用户指定的 Preprints.org 地址。

## 部署

这是纯静态网页，无需安装依赖或构建。发布目标为 GitHub Pages：`https://cslsolow.github.io/`。`127.0.0.1` 地址仅用于本机开发预览。

GitHub Pages 配置步骤，主页地址为 `https://cslsolow.github.io/`：

1. 在 `cslsolow` 账号下创建公开仓库 `cslsolow.github.io`。
2. 将本站文件放到仓库根目录，确保 `index.html` 位于根目录；上传 `styles.css`、`theme-init.js`、`app.js`、`assets/avatar.png`、`assets/favicon.svg`，以及需要保留的配色对比页。根目录的 `.nojekyll` 用于直接托管静态页面。
3. 在仓库的 Settings → Pages 中选择 Deploy from a branch，再选 `main` 分支和 `/ (root)`，保存。
4. 等待部署成功，访问公开地址并检查头像、琥珀色和论文链接，随后即可分享。电脑无需持续运行本地服务器。

只发布 `academic-homepage` 中的网站文件；上级目录的 `docs/research`、研究证据、截图和原始头像不属于发布内容。`.gitignore` 排除旧头像与 macOS 文件。

官方步骤：https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site

## 本轮验证

- JavaScript 语法检查。
- 两个 HTML 页面的资源、锚点和重复 ID 检查。
- 本地 HTTP 200 检查。
- 六套主题正文、次要文字、链接与选中标签的颜色对比度检查（至少 4.5:1）。
- 浏览器检查：配色切换与 URL、存储恢复、论文分类／年份组合、无结果与重置；桌面和窄屏布局。

## News

News 位于 About 和 Publications 之间，列出 Information Processing & Management 的期刊正式上线消息，以及 ASE、ISSTA、EMNLP 和 Internetware 2026 的四条会议接收消息，加上 SWE-Exp 于 2025-08-06 在 SWE-bench Verified 榜单的开源模型及开源 scaffold 类别排名第二消息（榜单链接：https://www.swebench.com/），另有 RSIHub 于 2026-09-03 被 Meta-Agents Workshop at NeurIPS 2026 接收的消息，共七条。SWE-Exp 的排名及日期、RSIHub 的接收状态及日期均采用用户提供的信息。RSIHub 标题暂时链接至 https://github.com/simple-agent-lab/RSIHub 。News 显示年月，按事件日期倒序；接收与正式上线分别表述。消息链接至论文、出版社、会议官网或论文作者主页。已移除独立 Open source 栏；论文已有的 Code 链接保留。

Planning over Actions 的论文链接采用 DOI `10.1016/j.ipm.2026.105092`。出版社通知确认最终版本于 2026-08-14 上线，News 与 Publications 使用这一时间；其卷期为 2027 年 1 月，仍在 venue 中注明。7 月的邮件为小修，不作为接收证据。

## 年月与排序

Publications 按正式线上发表日期倒序；尚无正式日期的预印本按首发日期，LLMs as Continuous Learners 按 2024-11-21 的首发日期排序（2026-10-28 按用户要求修正），会议标签和接收 News 保留 Internetware 2026。每条论文展示月份，日期提示区分首发、正式上线和卷期。

News：EMNLP 为 Aug 2026（官方主会通知时间），IP&M 为 Aug 2026（出版社正式上线通知），ISSTA 为 Jul 2026（最终录用通知，不用六月 conditional acceptance），ASE 为 Jun 2026（官方通知时间与当月 arXiv 接收声明相符），Internetware 为 May 2026（各轮通知均在五月）。

公开目录内没有邮件正文、私有审稿链接或邮件附件。工作区 `docs/research/publication-date-evidence.json` 只记录日期结论、依据类型和公开来源。

## 浏览器缓存与预览更新

修改页面、CSS、JavaScript 或头像后，运行：

```sh
python3 scripts/refresh-preview-assets.py
```

脚本根据页面和资源内容生成同一个版本指纹，更新 HTML、iframe、CSS、JavaScript 和图片的本地链接。`asset-version.json` 中包含最新入口。重复运行不会无故改变版本。

这用于避免旧版只支持六个主题的 `theme-init.js` 被缓存后，把新配色回退为保存的松绿色。已用旧脚本和已有松绿偏好复现，再验证版本化后六个 iframe 内部的主题与实际背景色逐一匹配。回归证据在工作区 `docs/research/theme-cache-regression.json`。

## 标签页图标

`assets/favicon.svg` 使用黑底、金色 SC 字母和细金边。字母由 SVG 路径绘制，不依赖外部字体。修改图标后同样运行资源版本脚本，避免浏览器继续显示旧图标。

## 论文类别图标

每篇论文标题前显示主题配色的内嵌 SVG 图标，年月旁有可见英文类别；鼠标悬停图标可查看说明，屏幕阅读器可读到类别名称。当前按主要贡献分为 Scaffold、Benchmark、Survey、Data generation、Self-improvement 和 Empirical study。分类为基于论文和项目说明的主要贡献进行的编辑归类，来源保存在 content.json 的 research_type_source。SkillForge 和 LLMs as Continuous Learners 的经验／技能改进归为 Self-improvement，不自动等同于参数训练；新论文如确有模型训练贡献，再添加 Training 类别。类别不改变原有作者、年份筛选和论文顺序。
