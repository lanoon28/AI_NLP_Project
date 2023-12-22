import torch
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
import re

# 사전 훈련된 BERT 모델을 시퀀스 분류를 위해 로드합니다.
model = BertForSequenceClassification.from_pretrained('bert-base-multilingual-cased', num_labels=3)
# 저장된 모델 가중치를 로드합니다.
model.load_state_dict(torch.load('/Users/jeonjaehong/goorm_python/GB_Company/sentiment_model.pth'))
# 모델을 평가 모드로 설정합니다.
model.eval()

# 주어진 모델, 토크나이저, 입력 문장으로 감정을 예측하는 함수입니다.
def predict_sentiment(model, tokenizer, sentence):
    model.eval()

    # 입력 문장을 토큰화하고 인코딩합니다.
    encoding = tokenizer.encode_plus(
        sentence,
        add_special_tokens=True,
        truncation=True,
        max_length=128,
        return_tensors='pt',
        padding='max_length',
        return_attention_mask=True,
        return_token_type_ids=False,
    )

    # 모델에 입력을 전달합니다.
    input_ids = encoding['input_ids']
    attention_mask = encoding['attention_mask']

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)

    # 예측된 결과를 확인합니다.
    logits = outputs.logits
    preds = torch.argmax(logits, dim=1).item()

    return preds

# 토크나이제이션
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

# 감정 분석을 위한 예시 문장
# example_sentences = [
#     ["최근 글로벌 경제 불안으로 인해 국내 주식 시장에서는 큰 변동이 예상되고 있습니다.",
#      "금리 인상과 관련하여 투자자들은 자산 배분 전략을 재고하고 있으며, 안전자산으로의 이동이 두드러지고 있습니다.",
#      "2022년 상반기 기업 실적 발표가 시작되었는데, 몇몇 대기업들은 예상보다 높은 이익을 기록하고 있습니다.",
#      "국제 무역 전반을 주도하는 중국의 생산 활동이 둔화되고 있어, 이는 세계 경제에 미치는 영향을 우려케 하고 있습니다.",
#      "디지털 화폐 시장에서는 최근 비트코인의 가격이 급등하며 투자자들의 관심을 끌고 있습니다."],
#     ["최근 글로벌 경제 불안으로 인해 국내 주식 시장에서는 큰 변동이 예상되고 있습니다.",
#      "금리 인상과 관련하여 투자자들은 자산 배분 전략을 재고하고 있으며, 안전자산으로의 이동이 두드러지고 있습니다.",
#      "2022년 상반기 기업 실적 발표가 시작되었는데, 몇몇 대기업들은 예상보다 높은 이익을 기록하고 있습니다.",
#      "국제 무역 전반을 주도하는 중국의 생산 활동이 둔화되고 있어, 이는 세계 경제에 미치는 영향을 우려케 하고 있습니다.",
#      "디지털 화폐 시장에서는 최근 비트코인의 가격이 급등하며 투자자들의 관심을 끌고 있습니다."]
# ]

# 문장 목록에 대한 감정 분석을 수행하는 함수입니다.
def PN_Ana(corpus):
    gb_list = []
    for sentences in corpus:
        a = 0  # 중립적 감정을 카운트하는 변수
        b = 0  # 긍정적 감정을 카운트하는 변수
        c = 0  # 부정적 감정을 카운트하는 변수

        # print('다음 항목')
        # print()

        # 코퍼스의 각 문장에 대해 감정을 예측합니다.
        for sentence in sentences:
            predicted_label = predict_sentiment(model, tokenizer, sentence)
            # print()
            # 예측된 감정을 카운트합니다.
            if predicted_label == 0:
                a += 1
                # print(f'{sentence} : 중립적 문장{a}')
            elif predicted_label == 1:
                b += 1
                # print(f'{sentence} : 긍정적 문장{b}')
            elif predicted_label == 2:
                c += 1
                # print(f'{sentence} : 부정적 문장{c}')
        # print(f'긍정 : {b}')
        # print(f'부정 : {c}')
        # 코퍼스 전체에 대한 감정을 분석하고 출력합니다.
        if b + c < a * 0.5:
            print('중립적인 기사')
            gb_list.append(0)
        elif b > c:
            print(f'긍정적인 기사: {b / (a + b + c) * 100}%')
            if b+c == 0:
                gb_list.append(0)
            PN_result = (b / (b + c))*100 - (c / (b + c)*100)
            gb_list.append(PN_result)
        else:
            print(f'부정적인 기사: {c / (a + b + c) * 100}%')
            if b+c == 0:
                gb_list.append(0)
            PN_result = (b / (b + c))*100 - (c / (b + c)*100)
            gb_list.append(PN_result)
    return gb_list
            


def split_sentences(text):
    # 마침표, 물음표, 느낌표를 기준으로 문장을 분리합니다.
    # 마침표 뒤에 따옴표가 있는 경우는 제외합니다.
    sentences = re.split(r'(?<=[.!?])(?!\d)', text)
    # 빈 문자열을 제거하여 리스트에서 제외합니다.
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

# # 테스트를 위한 긴 텍스트
# long_text = "안녕하세요. 반갑습니다! 파이썬으로 긴 글을 문장별로 구분하는 코드를 만들어 봅시다. 이 코드는 정규표현식을 사용하여 문장을 분리합니다. 어떠신가요?"
# # 문장 분리 함수 호출
# sentences = split_sentences(long_text)
# # print(sentences)
# # 분리된 문장 출력
# for sentence in sentences:
#     print(sentence)

# 예시 문장에 대한 감정 분석을 수행합니다.
# PN_Ana(example_sentences)
