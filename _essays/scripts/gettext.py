from bs4 import BeautifulSoup

html = open('content.txt', encoding='utf-8').read()

soup = BeautifulSoup(html, 'html.parser')

output_lines = []

for tr in soup.select('tbody tr'):
    td_list = tr.find_all('td')
    if len(td_list) < 4:
        continue
    
    date = td_list[0].get_text(strip=True)
    venue = td_list[1].get_text(strip=True)
    name = td_list[2].get_text(strip=True)
    
    # 获取所有非空链接
    links = [a['href'].strip() for a in td_list[3].find_all('a') if a.get('href', '').strip()]
    
    if links or date or venue or name:
        output_lines.append(f"日期: {date}")
        output_lines.append(f"地点: {venue}")
        output_lines.append(f"名称: {name}")
        if links:
            output_lines.append("链接:")
            output_lines.extend(links)
        output_lines.append('')  # 每条记录之间空一行

# 输出到文本文件
with open('dates_venues_names_links.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))
