# ready_made_address_lottemembers

### 1) 데이터 수집
get_commercial_area_data.ipynb

output : data/commercial_area.csv

### 2) 데이터 전처리
preprocess_commercial_area_data.ipynb

output : data/preprocessed_commercial_area.csv

### 3) 행정동별 스토리 생성
make_prompt_story.ipynb

output : data/prompt_story.csv

### 4) 프롬프트 입력값과 스토리 유사도 비교
get_area_recommendation.ipynb

### 5) 모니터링
```python
streamlit run app.py
```
