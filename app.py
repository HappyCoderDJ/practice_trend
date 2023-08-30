import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# 폰트 설정
import os
import matplotlib.font_manager as fm 

font_path = './customFonts/NanumGothic-Regular.ttf'
fontprop = fm.FontProperties(fname=font_path)
plt.rc('font', family='NanumGothic')

# excel 데이터 불러오기 
data = pd.read_excel('practice_trend.xlsx', sheet_name="데이터", header=0)
data = data.replace("-", 0)

# 데이터 프레임으로 바꾸기
df = pd.DataFrame(data)

st.title("표기과목별 의원 수 변경 추이")

# Filter options
selected_subject = st.selectbox("표시과목 선택", df['표시과목별'].unique())
selected_regions = st.multiselect("지역 선택", df['시도별'].unique())
all_time_columns = list(df.columns[2:])
quarter_option = st.multiselect("분기 일괄 선택", ['1/4', '2/4', '3/4', '4/4'])

# 선택된 분기에 따라 column 선택
selected_time = [col for col in all_time_columns if any(q in col for q in quarter_option)]

st.success(f"선택된 표시과목: {selected_subject}, 선택된 지역: {selected_regions}, 선택된 분기: {quarter_option}")

# Draw a bar plot for original data
fig1, ax1 = plt.subplots(figsize=(12, 6))

# Draw a lineplot for difference
fig2, ax2 = plt.subplots(figsize=(12, 6))

for region in selected_regions:
    filtered_df = df[(df['표시과목별'] == selected_subject) & (df['시도별'] == region)][['표시과목별', '시도별'] + selected_time]
    
    # 차이 계산 및 추가
    diff = filtered_df[selected_time].diff(axis=1)
    diff['시도별'] = f"{region} 차이"
    diff['표시과목별'] = selected_subject
    filtered_df = pd.concat([filtered_df, diff])

    # 데이터 포인트를 점으로 표시하고 값을 그래프에 표시하기 위한 코드
    data_row = filtered_df.drop(['표시과목별', '시도별'], axis=1).iloc[1, :].dropna()
    
    # sns.lineplot으로 선 그래프 그리기
    sns.lineplot(data=data_row, markers=True, ax=ax2, label=f"{region} 차이")
    for x, y in data_row.items():
        ax2.text(x, y, f"{y}", ha='center', va='bottom')


    st.write(f"**{region}의 개원수 및 시기별차이**")
    st.dataframe(filtered_df)

ax2.set_title("시기별 개원수 차이")
ax2.set_xlabel("기간")
ax2.set_ylabel("개원수 차이")


st.pyplot(fig2)