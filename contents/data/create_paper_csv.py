from googletrans import Translator
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import asyncio

async def translate_paper_info(paper_info):
    translator = Translator()
    try:
        # 非同期翻訳
        translated_title = await translator.translate(paper_info[1], src='en', dest='ja')
        translated_abstract = await translator.translate(paper_info[2], src='en', dest='ja')
        paper_info.append(translated_title.text)
        paper_info.append(translated_abstract.text)
    except Exception as e:
        print(f"Translation error: {e}")
        paper_info.append("Translation failed")
        paper_info.append("Translation failed")
    return paper_info

def find_paper_info(paper):
    try:
        # 各論文ページのHTMLから情報を取得
        paper_url = paper.find("a").get("href")
        paper_html = requests.get(paper_url).text
        paper_soup = BeautifulSoup(paper_html, "html.parser")

        # 論文情報を抽出
        paper_author = paper_soup.find("div", class_="authors").text.strip()
        paper_title = paper_soup.find("h1", class_="title mathjax").text.strip()
        paper_abstract = paper_soup.find("blockquote", class_="abstract mathjax").text.strip()

        return [paper_author, paper_title, paper_abstract]
    except Exception as e:
        print(f"Error fetching paper info: {e}")
        return ["Error", "Error", "Error"]

async def create_papers_csv(today):
    # arXivのURL（検索単語は"quantum physics"）
    target_date = (today - timedelta(days=3)).strftime('%Y-%m-%d')
    next_date = (today - timedelta(days=2)).strftime('%Y-%m-%d')
    pagesize = 200
    start_num = 0
    arxiv_url = (
        f"https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=quantum+physics"
        f"&terms-0-field=all&classification-physics_archives=all&classification-include_cross_list=include"
        f"&date-year=&date-filter_by=date_range&date-from_date={target_date}&date-to_date={next_date}"
        f"&date-date_type=submitted_date&abstracts=show&size={pagesize}&order=-announced_date_first&start={start_num}"
    )

    # CSVファイルにデータを書き込む
    csv_filename = f"./{target_date}.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        header = ["title", "authors", "abstract", "authors_trans", "abstract_trans"]
        writer.writerow(header)

        # HTMLを取得
        try:
            arxiv_html_page = requests.get(arxiv_url).text
            arxiv_soup = BeautifulSoup(arxiv_html_page, "html.parser")

            # 各論文のHTMLに分割
            papers = arxiv_soup.find_all("li", class_="arxiv-result")
            for paper in papers:
                paper_info = find_paper_info(paper)
                translated_paper_info = await translate_paper_info(paper_info)
                writer.writerow(translated_paper_info)

        except Exception as e:
            print(f"Error fetching arXiv data: {e}")

if __name__ == "__main__":
    today = datetime.today()
    asyncio.run(create_papers_csv(today))
