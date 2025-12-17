# 实验九 网络爬虫与自动化：软科中国大学排名2024前30名爬取（最终完整版）
import requests
from bs4 import BeautifulSoup
import csv
import time
def get_html_content():
    """获取排名页面HTML内容（稳定访问）"""
    url = "https://www.shanghairanking.cn/rankings/bcur/2024"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        time.sleep(1)
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        response.encoding = "utf-8"
        print("✅ 页面访问成功！")
        return response.text
    except Exception as e:
        print(f"❌ 页面访问失败：{str(e)}")
        return None
def parse_rank_data(html):
    """解析数据（修复名称提取逻辑）"""
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    rank_data = []
    # 定位排名表格
    table = soup.find("table", class_="rk-table")
    if not table:
        print("❌ 未找到排名表格")
        return []
    # 提取前30行数据（跳过表头）
    rows = table.find_all("tr")[1:31]
    for idx, row in enumerate(rows, 1):
        try:
            cells = row.find_all("td")
            # 核心修复：定位class="univ-name"的div提取大学名称
            name_elem = cells[1].find("div", class_="univ-name")
            name = name_elem.text.strip() if name_elem else cells[1].text.strip()
            # 其他字段提取
            province = cells[2].text.strip() if len(cells)>=3 else "未知省市"
            type_ = cells[3].text.strip() if len(cells)>=4 else "未知类型"
            score = cells[4].text.strip().replace(",", "") if len(cells)>=5 else "0.0"
            
            rank_data.append({
                "排名": idx,
                "大学名称": name,
                "省市": province,
                "类型": type_,
                "总分": score
            })
            print(f"✅ 解析第{idx}名：{name} | {province} | {type_} | 总分：{score}")
        except Exception as e:
            print(f"❌ 解析第{idx}名失败：{str(e)}")
            continue
    return rank_data

def save_to_csv(data):
    """保存为CSV文件"""
    if not data:
        print("❌ 无数据可保存！")
        return
    save_path = "软科中国大学排名2024_前30名.csv"
    headers = ["排名", "大学名称", "省市", "类型", "总分"]
    try:
        with open(save_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"\n🎉 数据保存成功！文件路径：{save_path}")
        print(f"📊 共保存{len(data)}条数据")
    except PermissionError:
        print("❌ 保存失败：请关闭已打开的CSV文件！")
    except Exception as e:
        print(f"❌ 保存失败：{str(e)}")

# 主程序执行
if __name__ == "__main__":
    print("===== 实验九 网络爬虫与自动化 开始执行 =====")
    html_content = get_html_content()
    rank_result = parse_rank_data(html_content)
    save_to_csv(rank_result)
    print("===== 实验九 网络爬虫与自动化 执行结束 =====")
# 在这里编写代码
