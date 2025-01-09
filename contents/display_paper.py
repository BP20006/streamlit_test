import streamlit as st
import pandas as pd
import pyperclip

def create_ChatGPT_script(title, abstract, url):
    # フォーマットに埋め込む
    script = f"""
まず、下記の文章を日本語で短く要約したものを「日本語概要」とラベル付けしてください。
{abstract}
次に、以下のフォーマットに「日本語概要」を加えてそれのみを出力してください。
タイトル：
{title}
概要：
「日本語概要」
URL：
{url}
"""

    return script


st.sidebar.markdown("[ChatGPTのリンク](https://chat.openai.com)")

# サイドバーでCSVファイルを選択
csv_files = {
    "12/11": "contents/data/2024-12-11.csv",
    "12/12": "contents/data/2024-12-11.csv",
    "12/13": "contents/data/2024-12-11.csv",
    "12/14": "contents/data/2024-12-11.csv",
    "12/15": "contents/data/2024-12-11.csv"
}

selected_file = st.sidebar.selectbox("表示する日にちを選んでください", list(csv_files.keys()))

# 選択されたCSVファイルを読み込む
csv_file = csv_files[selected_file]
data = pd.read_csv(csv_file)

# タイトルの設定
st.header("arXivチェック支援サイト")
st.subheader("共有までの手順")
st.text('1. 自分が担当する日にちをサイドバーから選ぶ')
st.text('2. 気になる論文をクリック')
st.text('3. ChatGPTのスクリプトをコピーする')
st.text('4. ChatGPTにスクリプトを送信して共有用文章を作成')
st.text('5. Slackで共有')

# 行ごとに情報を取得
for index, row in data.iterrows():
    title_trans = row['title_trans'].replace("タイトル：", "")
    with st.expander(f"{index + 1} : {title_trans}"):
        # 最初はtitle_transを表示
        st.write(f"**Title**: {row['title']}")
        st.write(f"**Abstract**: {row['abstract']}")
        st.write(f"**Abstract Translated**: {row['abst_trans']}")

        # ChatGPTスクリプト作成（仮の関数）
        for_chat_GPT = create_ChatGPT_script(row['title'], row['abstract'], "sample.com")

        st.text_area("ChatGPTスクリプト", for_chat_GPT, height=150)
        # if st.button("ChatGPTスクリプト", key=f"button_{index}"):
        #     pyperclip.copy(for_chat_GPT)  # 文字列をクリップボードにコピー
        #     st.success("文字列がクリップボードにコピーされました！")
