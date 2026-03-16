# Gene Summary Fast Fetcher

**Language:** [English](#english) | [中文](#chinese)

<a id="english"></a>
## 📖 Overview
This project provides a fast, stable, and anti-bot-free Python script to fetch gene summaries (such as NCBI Gene Summary) in bulk. 
**This project is AI-assisted. Most of the code and documentation (including this README.md) were generated or refined with the help of artificial intelligence tools. While I strive for accuracy, please verify critical information and use it at your own discretion. If you encounter any issues or have concerns, feel free to open an issue or contact me directly.**

**Why not web scraping?** 
Traditional web scraping tools (e.g., targeting GeneCards) often face severe IP blocking and Cloudflare CAPTCHA loops. This script solves that problem by using the official [MyGene.info](https://mygene.info/) API. It is incredibly fast, completely bypasses browser automation, and is highly suitable for bioinformatics pipelines.

## ✨ Features
- **Lightning Fast:** Fetches hundreds of genes in seconds.
- **No Anti-Scraping Issues:** Uses official REST APIs, meaning no Cloudflare blocks or headless browser configurations are needed.
- **Accurate Data:** Directly sources RefSeq and Uniprot information.

## ⚙️ Prerequisites
You need Python 3.7+ and the following libraries:
- `mygene`
- `pandas`

Install them via pip:
```bash
pip install mygene pandas
```

## Core Logic
1. NCBI Summary: Retrieved via the MyGene API using Gene Symbol + species='human'. This is because the NCBI Summary is based on the gene (Entrez Gene) level.
2. UniProt Function: Extracted precisely via the UniProt API using the UniProt ID you provided. This is at the protein level. To be on the safe side, the AI has added a double-check in the code to ensure that the returned data is also for Human (TaxID: 9606).
3. **If you need to retrieve gene summary/function information for other species, please ensure you check and modify the relevant sections of the code!**

## 🚀 Usage
1. By default, the code is designed for use when you already have the **Gene Symbol (gene name) and UniProt ID**. It is intended for genes from the **human species**; data retrieved and downloaded in bulk from Genecards should already contain both pieces of information. If you wish to filter based on only one of these, you can modify the code accordingly.
2. Prepare a CSV file named `genelist.csv` in the root directory. The first column should contain your target gene symbols (e.g., TP53, EGFR). The second column should contain the corresponding uniprot ID of the gene(e.g., P04637).
3. Run the script
4. The results will be saved automatically in `gene_summaries_api.csv`.

## 🙏 Acknowledgments
- This repository was originally inspired by the idea from[AcidBarium/GeneCardsWebScraper](https://github.com/AcidBarium/GeneCardsWebScraper). However, due to strict Cloudflare protections on GeneCards, this project was entirely rewritten to utilize the `MyGene.info` API for a robust and legitimate data retrieval method. This script can scrape NCBI summaries and UniProt summaries, but it cannot retrieve GeneCard summaries.
- Data provided by [MyGene.info](https://mygene.info/).

---

<a id="chinese"></a>
## 📖 项目简介
本项目提供了一个快速、稳定且无视反爬机制的 Python 脚本，用于批量获取基因的功能描述（如 NCBI Gene Summary）。
**本项目由AI辅助完成。部分代码和文档借助AI生成或优化。由于本人相关基础较差，可能存在疏漏，请在使用前自行甄别关键信息。如遇到任何问题，欢迎提交Issue或直接联系我。**

**为什么不使用网页爬虫？**
传统的爬虫方案（如爬取 GeneCards）极易触发 Cloudflare 验证码死循环和 IP 封禁。本项目彻底摒弃了 Selenium/浏览器自动化的方式，转而调用官方的 [MyGene.info](https://mygene.info/) API。速度极快，且非常适合集成到生物信息学分析流程中。

## ✨ 特性
- **极速获取**：只需几秒钟即可完成数百个基因的查询。
- **无视反爬**：纯 API 调用，无需配置浏览器驱动，告别验证。
- **数据权威**：直接获取 NCBI RefSeq 和 UniProt 等权威数据库的 Summary。

## ⚙️ 环境依赖
建议使用 Miniconda 或直接安装 Python 3.7+。依赖以下库：
- `mygene`
- `pandas`

安装命令：
```bash
pip install mygene pandas
```

## 核心逻辑
1. NCBI Summary: 使用 Gene Symbol + species='human' 通过 MyGene API 获取。这是因为 NCBI Summary 是基于基因（Entrez Gene）层面的。
2. UniProt Function: 直接使用你提供的 UniProt ID 通过 UniProt API 精准提取。这是基于蛋白层面的。为了保险起见，AI在代码里增加了一个双重检查，确保返回的数据也是 Human (TaxID: 9606)。
3. **如果需要检索其他物种的基因summary/function信息，请注意检查并修改代码相关部分！**

## 🚀 使用方法
1. 代码默认情况下适用于手头已经有**Gene Symbol（基因名） 和 UniProt ID**的情况。并且是**human species**的基因，如果是从Genecards批量检索下载的数据应该会有这两个信息。如果只想根据一个进行筛选的话可以自行修改一下代码。
2. 在代码同级目录下准备一个名为 `genelist.csv` 的文件，第一列命名为Gene Symbol，填入你需要查询的基因名称（例如 TP53）；第二列命名为Uniprot ID，填写基因对应的uniprot ID(例如: P04637)。
3. 在终端运行脚本。
4. 运行结束后，当前目录会生成 `gene_summaries_api.csv` 文件，包含查询结果。

## 🙏 致谢
- 本项目开发初衷受到了 [AcidBarium/GeneCardsWebScraper](https://github.com/AcidBarium/GeneCardsWebScraper) 启发。但由于目标网站日益严苛的反爬策略，本项目在Gemini3.0-pro-preview建议下完全重构，改用 `MyGene.info` 接口，以提供更稳定、合规的数据获取方式。这个代码可以爬到NCBI summary和uniprot summary，只有genecard summary是获取不到的。
- 感谢 [MyGene.info](https://mygene.info/) 提供强大的 API 接口支持。
