# AI_NLP_Project

# 1. 프로젝트 개요

---

> **서비스명**
> 

주식 투자 어시스트

> **한줄 소개**
> 

주식 투자의 도움이 되는 기업의 정보를 NLP를 활용하여 서비스 이용자에게 제공하는 서비스 

> **개발 동기**
> 

주식 투자의 관심도가 증가함에 따라 아무것도 모른채 투자하는 투자자도 같이 증가하였습니다. 저희는 여기서 정보의 비대칭으로 인해 피해를 입는 투자자가 있음을 알게되었고 그 비대칭을 해결해보고자 해당 서비스를 개발하였습니다.

# 2. 세부 내용

---

> 최초 기획안
> 
- **동작 방안 - 최소 구현**
    1. 24시간의 기사 데이터 수집
    2. 수집된 데이터를 딥러닝 모델 구현
    3. 판단된 정보를 바탕으로 최소 하나의 인사이트 도출

- **동작 방안 - 중간 구현**
    1. 과대/소 적합을 방지하기 위해 추가적인 데이터 수집
    2. 모델의 각종 피쳐값등을 조절하여 최적화 모델 구현 및 api 제공
    3. 기능을 동작하게할 웹페이지 구축

- **동작 방안 - 완전 구현**
    1. 하나의 앱 혹은 웹으로 구현
    2. 사용자가 특정 기업을 검색하였을 경우 관련 인사이트 모두 제공
    3. 수집된 데이터를 높은 수준으로 예측하는 모델 구축

- **구현 방안**
    1. 네이버 뉴스를 통해 오전 8시를 기준으로 매일 기사를 수집 및 DB 업데이트
    2. 수집된 데이터를 바탕으로 모델이 평가 및 결과 업데이트 
    3. api를 통해 필요한 인사이트를 도출
    4. 도출된 데이터를 사용자에게 제공

# 3. 기대 효과

---

> 기대 효과
> 
- 정보의 비대칭성 완화
- 보다 안정적인 투자 가능

> ToDo (발전 가능성)
> 
- 서비스 반응성 향상 (학습속도 최적화 및 도출속도와 정확도 향상)
- 사용자 데이터를 학습하여 다양한 기능 확장
- 주식(MTS) 서비스와 연계하여 정확도와 신뢰성 향상# AI_NLP_Project
