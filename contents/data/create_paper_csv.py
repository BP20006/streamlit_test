from googletrans import Translator
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def find_paper_ifno(paper):
  # 各論文ページのHTMLから情報を取得
  paper_url = paper.find("a").get("href")
  paper_html = requests.get(paper_url).text
  paper_soup = BeautifulSoup(paper_html, "html.parser")

  # 投稿日時が実行時の日付から２日以内なら論文情報を取得
  paper_author = paper_soup.find("div", class_="authors").text
  paper_title = paper_soup.find("h1", class_="title mathjax").text
  paper_abst = paper_soup.find("blockquote", class_="abstract mathjax").text

  # 日付と論文の情報（投稿日、著者、タイトル、概要）を返す
  return [paper_author, paper_title.replace('\n', ''), paper_abst.replace('\n', '')]


async def translate_paper_info(paper_info):
    translator = Translator()
    # paper_info[1] と paper_info[2] を非同期で翻訳
    translated_text1 = await translator.translate(paper_info[1], src='en', dest='ja')
    translated_text2 = await translator.translate(paper_info[2], src='en', dest='ja')

    # 結果をリストに追加
    paper_info.append(translated_text1.text)
    paper_info.append(translated_text2.text)

    return paper_info

def create_papers_csv(today):
  # arxivのURL（検索単語は"quantum physics"）
  # １ページの論文数は50
  target_date = (today - timedelta(days=5)).strftime('%Y-%m-%d')
  next_date = (today - timedelta(days=4)).strftime('%Y-%m-%d')
  pagesize = 200
  start_num = 0
  arxiv_url = f'https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=quantum+physics&terms-0-field=all&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date={target_date}&date-to_date={next_date}&date-date_type=submitted_date&abstracts=show&size={pagesize}&order=-announced_date_first&start={start_num}'
  # CSVファイルにデータを書き込む
  f = open(f'{target_date}.csv', mode='w', newline='', encoding='utf-8')
  writer = csv.writer(f)
  header = ['title', 'authors', 'abstract', 'authors_trans', 'sbstract_stans']
  writer.writerow(header)

  loop_frag = True

  # htmlを取得
  arxiv_html_page = requests.get(arxiv_url).text
  arxiv_soup = BeautifulSoup(arxiv_html_page, "html.parser")

  # 各論文のHTMLに分割
  papers = arxiv_soup.find_all("li", class_="arxiv-result")
  for paper in papers:

      paper_info = find_paper_ifno(paper)
      writer.writerow(translate_paper_info(paper_info))

  f.close()

if __name__ == "__main__":
  today = datetime.today()
  create_papers_csv(today)
