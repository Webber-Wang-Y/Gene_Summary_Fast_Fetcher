import pandas as pd
import requests
import mygene
from tqdm import tqdm
import time

def fetch_precise_summaries():
    # ================= 配置区域 =================
    input_file = './genelist.csv'
    output_file = './gene_summaries_final.csv'
    
    # 请根据你 CSV 的实际表头修改这里
    col_symbol = 'Gene Symbol'  # 基因名列的表头
    col_uniprot = 'Uniprot ID'  # UniProt ID列的表头
    # ===========================================

    # 1. 读取 CSV
    print(f"正在读取 {input_file} ...")
    try:
        df_input = pd.read_csv(input_file)
        # 简单清洗数据：去空格
        df_input[col_symbol] = df_input[col_symbol].astype(str).str.strip()
        df_input[col_uniprot] = df_input[col_uniprot].astype(str).str.strip()
    except Exception as e:
        print(f"读取文件失败: {e}")
        return

    total_genes = len(df_input)
    print(f"共加载 {total_genes} 个基因数据。")
    
    final_results = []
    
    # ---------------------------------------------------------
    # 第一步: 批量获取 NCBI Summary (使用 MyGene)
    # ---------------------------------------------------------
    print("\n[Step 1/2] 正在通过 MyGene 获取 NCBI Summary (限制物种: Human)...")
    
    mg = mygene.MyGeneInfo()
    gene_symbols = df_input[col_symbol].tolist()
    
    # 使用 MyGene 批量查询
    # scopes='symbol': 按名字查
    # species='human': 严格限制为人类
    # fields='summary': 只拿 summary
    mg_results = mg.querymany(gene_symbols, scopes='symbol', fields='summary', species='human', verbose=True)   
    
    # 将结果转为字典映射: { 'TP53': 'summary text...', 'EGFR': '...' }
    ncbi_map = {}
    for item in mg_results:
        query = item.get('query')
        summary = item.get('summary')
        # 如果能找到 summary 且之前没存过（或之前存的是空的），则存入
        if query and summary:
            ncbi_map[query] = summary

    # ---------------------------------------------------------
    # 第二步: 获取 UniProt Function (使用 UniProt API)
    # ---------------------------------------------------------
    print("\n[Step 2/2] 正在通过 UniProt ID 获取详细 Function 描述...")
    
    # UniProt API 基础 URL
    uniprot_base_url = "https://rest.uniprot.org/uniprotkb/"

    # 使用 session 保持连接，提高循环请求速度
    session = requests.Session()
    # 设置重试机制，防止网络波动报错
    adapter = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount('https://', adapter)

    # 遍历每一行数据
    for index, row in tqdm(df_input.iterrows(), total=total_genes, unit="gene"):
        g_symbol = row[col_symbol]
        u_id = row[col_uniprot]
        
        # 1. 从刚才的 Map 中取 NCBI Summary
        ncbi_text = ncbi_map.get(g_symbol, 'Not Found')
        
        # 2. 在线查 UniProt Summary
        uniprot_text = "Not Found"
        
        # 只有当 ID 看起来有效时才查询
        if u_id and str(u_id).lower() != 'nan':
            try:
                # 直接通过 ID 查询: https://rest.uniprot.org/uniprotkb/P04637
                url = f"{uniprot_base_url}{u_id}"
                resp = session.get(url, timeout=10)
                
                if resp.status_code == 200:
                    data = resp.json()
                    
                    # --- 双重保险：检查物种是否为 Human ---
                    organism_id = data.get('organism', {}).get('taxonId', 0)
                    if organism_id == 9606: # 9606 是 Homo sapiens 的 ID
                        # 提取 Function 描述
                        comments = data.get('comments', [])
                        # 筛选类型为 FUNCTION 的文本
                        functions = [c['texts'][0]['value'] for c in comments if c['commentType'] == 'FUNCTION']
                        if functions:
                            uniprot_text = " ".join(functions) # 将多段描述合并
                    else:
                        uniprot_text = f"Skipped (Non-Human ID: TaxID {organism_id})"
                elif resp.status_code == 404:
                    uniprot_text = "Invalid UniProt ID"
                else:
                    uniprot_text = f"Error {resp.status_code}"
            except Exception as e:
                uniprot_text = f"Request Error"
                # print(f"Error for {u_id}: {e}")

        # 整合一行数据
        final_results.append({
            'Gene Symbol': g_symbol,
            'UniProt ID': u_id,
            'NCBI Gene Summary': ncbi_text,
            'UniProtKB/Swiss-Prot Summary': uniprot_text
        })
        
        # 稍微控制一下请求频率，虽然 UniProt 很耐造
        time.sleep(2)

    # 3. 保存结果
    df_out = pd.DataFrame(final_results)
    df_out.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n处理完成！结果已保存至: {output_file}")

if __name__ == "__main__":
    fetch_precise_summaries()