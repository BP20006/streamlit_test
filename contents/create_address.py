import streamlit as st

# タイトルの設定
st.header("学番アドレス作成支援サイト")
st.subheader("作成の手順")
st.text('1. サイドバーからメールを送りたい学生たちの学科と入学年を入力')
st.text('2. 送りたい学生たちの学番下３桁をチェックボックスから選択')
st.text('3. テキストエリアの内容をコピー')
st.text('4. メールの宛先にペーストして送信')

# 最上部にテキストエリアを配置するための空コンテナ
textarea_container = st.empty()

department = str(st.sidebar.text_input('学科専攻コード'))
enter_year = str(st.sidebar.text_input('入学年'))

# 初期値としてのテキストエリア内容
if "s_adress" not in st.session_state:
    st.session_state["s_adress"] = ""

# 縦横グリッド状にチェックボックスを並べる
options = []
for i in range(15):
    sub_options = []
    for j in range(10):
        s_id = str(i * 10 + (j + 1)).zfill(3)
        sub_options.append(s_id)
    options.append(sub_options)

# セッション状態の初期化
if "checkbox_states" not in st.session_state:
    st.session_state["checkbox_states"] = {s_id: False for row in options for s_id in row}

# 一括操作用の関数
def select_all():
    for s_id in st.session_state["checkbox_states"]:
        st.session_state["checkbox_states"][s_id] = True
    update_email_addresses()

def clear_all():
    for s_id in st.session_state["checkbox_states"]:
        st.session_state["checkbox_states"][s_id] = False
    update_email_addresses()

# 選択されたチェックボックスに対応するメールアドレスを生成しテキストエリアに表示
def update_email_addresses():
    selected_ids = [
        s_id for s_id, checked in st.session_state["checkbox_states"].items() if checked
    ]
    email_addresses = [f"{department}{enter_year}{s_id}@shibaura-it.ac.jp" for s_id in selected_ids]
    st.session_state["s_adress"] = ", ".join(email_addresses)  # カンマ区切りで結合

# テキストエリアの更新（ページ最上部）
textarea_container.text_area(
    "学版メールアドレス一覧", st.session_state["s_adress"], height=100
)

# 一括選択と解除のボタン
col1, col2 = st.columns(2)
with col1:
    if st.button("全選択"):
        select_all()
with col2:
    if st.button("全解除"):
        clear_all()

# チェックボックスをグリッド状に表示
for row in options:
    cols = st.columns(len(row))
    for col, s_id in zip(cols, row):
        with col:
            if st.checkbox(
                s_id, value=st.session_state["checkbox_states"][s_id], key=s_id
            ):
                st.session_state["checkbox_states"][s_id] = True
            else:
                st.session_state["checkbox_states"][s_id] = False
    # メールアドレスを更新
    update_email_addresses()

# テキストエリアの内容をリアルタイムで更新
textarea_container.text_area(
    "学版メールアドレス一覧", st.session_state["s_adress"], height=100
)
