import streamlit as st

# タイトルの設定
st.header("Latex入力支援サイト")

# 最上部にテキストエリアを配置するための空コンテナ
textarea_container = st.empty()

# Session Stateに表示テキストを格納するため、最初にキーを定義しておく
if "display_text" not in st.session_state:
    st.session_state["display_text"] = ""

# ボタンを押されたときにSession Stateのテキストを更新する関数
def update_text(new_text):
    st.session_state["display_text"] = new_text

# 図の挿入---------------------------------------
insert_figure = st.expander('図の挿入')

figure_position = insert_figure.selectbox('図の位置', ['h', 't', 'b', 'p'], index=0)
figure_width = insert_figure.slider('図の幅', 0.0, 2.0, 0.5, step=0.05)
figure_path = insert_figure.text_input('ファイルパス', 'ファイルパス')
figure_label = insert_figure.text_input('ラベル', 'ラベル')
figure_caption = insert_figure.text_input('キャプション', 'キャプション')

# ボタンを複数配置し、押されたらそれぞれ違う文字列を表示
if insert_figure.button("生成"):
    figure_code = f"""\\begin{{figure}}[{figure_position}]
    \\centering
    \\includegraphics[width={figure_width}\\textwidth]{{{figure_path}}}
    \\caption{{{figure_caption}}}
    \\label{{fig:{figure_label}}}
\\end{{figure}}"""
    update_text(figure_code)

# 図の挿入---------------------------------------

# 特殊記号---------------------------------------
sp_symbols = st.expander('特殊記号')

sp_symbols_labels = [["≃", "≠", "∝", "≡"],
                     ["⇔", "<x>", "···", "⊥"],
                     ["N", "Z", "R", "C"]]
sp_symbols_commands = [["\\simeq", "\\neq", "\\propto", "\\equiv"],
                       ["\\Leftrightarrow", "\\langle x \\rangle", "\\dots", "\\perp"],
                       ["\\mathbb{N}", "\\mathbb{Z}", "\\mathbb{R}", "\\mathbb{C}"]]

# ボタンをグリッド状に表示
for i, row_labels in enumerate(sp_symbols_labels):
    columns = sp_symbols.columns(len(row_labels))  # 行ごとに列を作成
    for j, label in enumerate(row_labels):
        # ボタンを配置し、押されたらコマンドを格納
        if columns[j].button(label):
            figure_code = sp_symbols_commands[i][j]
            update_text(figure_code)

# 特殊記号---------------------------------------

# 場合分け---------------------------------------
cases = st.expander('場合分け')

cases_labels = ["cases環境", "cases*環境", "dcases, dcases*環境"]
cases_commands = ["""\\begin{equation}
  f(x)=
  \\begin{cases}
    0 & \\text{if $x>0$,} \\\\
    1 & \\text{if $x=0$,} \\\\
    2 & \\text{if $x<0$.}
  \\end{cases}
\\end{equation}""",
                       """\\begin{equation}
  f(x)=
  \\begin{cases*}
    0 & if $x>0$, \\\\
    1 & if $x=0$, \\\\
    2 & if $x<0$.
  \\end{cases*}
\\end{equation}""",
                       """\\begin{equation}
  \\begin{rcases}
    0 & if $x>0$, \\\\
    1 & if $x=0$, \\\\
    2 & if $x<0$.
  \\end{rcases}
  =f(x)
\\end{equation}"""]

# ボタンをグリッド状に表示
columns = cases.columns(3)
for i, label in enumerate(cases_labels):
    # ボタンを配置し、押されたらコマンドを格納
    if columns[i].button(label):
        figure_code = cases_commands[i]
        update_text(figure_code)

# 場合分け---------------------------------------

# テンプレートのダウンロード---------------------------------------
template = st.expander('テンプレートのダウンロード')

with open("contents/latex/abst.tex", "rb") as file:
    img_data = file.read()

columns = template.columns(2)

# ダウンロードボタン
columns[0].download_button(
    label="概要",
    data=img_data,
    file_name="abstract.tex",
    mime="application/x-tex"
)

# ダウンロードボタン
columns[1].download_button(
    label="論文（大学用）",
    data=img_data,
    file_name="abstract.tex",
    mime="application/x-tex"
)

# テンプレートのダウンロード---------------------------------------

# text_areaでSession Stateの内容を表示
textarea_container.text_area("結果", st.session_state["display_text"], height=200)
