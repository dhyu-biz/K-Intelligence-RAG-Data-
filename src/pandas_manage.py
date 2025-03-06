import pandas as pd
from io import StringIO
import json


# 주어진 HTML 코드
html_content = """
<table class="rowtable"><caption>속도테스트를 위한 시스템 권장, 최소 사양과 측정항목</caption><colgroup><col width="28%"><col></colgroup><tbody><tr><th scope="row">권장사양</th><td><ul class="bulletlist"><li>운영체제 : 윈도우즈 10 이상 / 맥OS 지원</li><li>브라우저 : Edge/크롬/whale/파이어폭스 <p>* 윈도우10 하위버전 및 인터넷익스플로러는 마이크로소프트사의 지원중단 정책에 따라 사용중 오류가 발생할 수 있습니다.</p></li></ul></td></tr><tr><th scope="row">측정항목</th><td><ul class="bulletlist"><li>다운로드 업로드 속도(최대값, 최소값, 평균, 편차)</li><li>UDP Ping 패킷 지연(최대값, 최소값, 평균, 편차, 손실 등)</li><li>경로 추적 테스트</li><li>OS 정보, CPU / RAM 정보</li><li>브라우저 종류 및 버전정보 <p>*익스플로러는 호환성 보기를 해제하셔야 정확한 버전을 알 수 있습니다.</p></li></ul></td></tr></tbody></table>
"""

# HTML을 읽어서 DataFrame으로 변환
df_list = pd.read_html(StringIO(html_content))

# 첫 번째 테이블만 선택
df = df_list[0]

# 결과 출력
# print(df)


# 테스트 세트 준비
# eval_df = pd.DataFrame(columns=[ "데이터 형식" , "데이터 원시" ]) # , "질문", "답변"

# JSON 형식으로 데이터 저장
data_json = df.to_json(orient= 'records')
print(data_json)
# decoded_data = [{k: v.encode().decode('unicode_escape') for k, v in item.items()} for item in data_json]
# print("data_json\n", decoded_data)
# # eval_df.loc[ len (eval_df)] = [ "JSON" , data_json]

#
# # 데이터를 사전 목록으로 저장
# data_list_dict = df.to_dict(orient= 'records' )
# print("data_list_dict\n", data_list_dict)
# # eval_df.loc[ len (eval_df)] = [ "DICT" , data_list_dict]
#
# # 데이터를 CSV 형식으로 저장
# csv_data = df.to_csv(index= False )
# print("csv_data\n", csv_data)
# # eval_df.loc[ len (eval_df)] = [ "CSV" , csv_data]
#
# # 데이터를 다음으로 저장 탭으로 구분된 형식
# tsv_data = df.to_csv(index= False , sep= '\t' )
# print("tsv_data\n", tsv_data)
# # eval_df.loc[ len (eval_df)] = [ "TSV (탭으로 구분)" , tsv_data]
#
# # HTML 형식으로 데이터를 저장합니다
# html_data = df.to_html(index= False )
# print("html_data\n", html_data)
# # eval_df.loc[ len (eval_df)] = [ "HTML" , html_data]
#
# # LaTeX 형식으로 데이터를 저장합니다.
# latex_data = df.to_latex(index= False )
# print("latex_data\n", latex_data)
# # eval_df.loc[ len (eval_df)] = [ "LaTeX" , latex_data]

# Markdown 형식으로 데이터를 저장합니다.
markdown_data = df.to_markdown(index= False )
print("markdown_data\n", markdown_data)
# eval_df.loc[ len (eval_df)] = [ "Markdown" , markdown_data]

# # 데이터를 문자열로 저장합니다
# string_data = df.to_string(index= False )
# print("string_data\n", string_data)
# # eval_df.loc[ len (eval_df)] = [ "STRING" , string_data]
#
# # 데이터를 NumPy 배열로 저장합니다
# numpy_data = df.to_numpy()
# print("numpy_data\n", numpy_data)
# # eval_df.loc[ len (eval_df)] = [ "NumPy" , numpy_data]
#
# # 데이터를 XML 형식으로 저장합니다
# xml_data = df.to_xml(index= False )
# print("xml_data\n", xml_data)
# # eval_df.loc[ len (eval_df)] = [ "XML" , xml_data]