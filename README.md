# EDAhelper

## SQL 데이터 다운로드 및 병합

#### SQL Query 실행 및 DataFrame 화 (*Done*)

    1. Connection 생성
    2. Feature 그룹 별 Query 실행 (Yaml)
    3. DataFrame 변환
    4. 생성 DataFrame에 feature group 부여 (buy, pnt, online, etc.)
        - feature group에는 여러개의 DataFrame 존재 가능 (Dictionary)
    5. 생성 DataFrame은 개별 저장
    
#### 사용할 Feature group 선택 시, DataFrame 병합 (*WIP*)
    1. Feature group 별 전처리 pipeline 지정
    2. Feature group 별 전처리 완료 DataFrame을 merge
    3. 최종 DataFrame을 input으로서 저장
    
##### 전처리 pipeline에 필요한 기능 (*WIP*)
    1. category, numeric, string column 할당
    2. category 전처리
        - unknown 추가?
        - dummy화
        - low variance feature 삭제
    3. numeric 전처리
        - log / log & square / sqrt 변환 자동 판정 (*Done*) 
            - median과 mean 값의 비율 차이 비교 (3*(mean - median)/std)
        - shift 1~N
        - fill NA
        - outlier clipping
    4. string 전처리
        - fill NA
    5. Labelling
        
#### Machine Learning 실시
    1. Input Data Loading
    2. Train/Test split
    3. ML
    
    
#### Validation 실시
    1. confusion matrix
    2. precision recall
    3. ROC curve
