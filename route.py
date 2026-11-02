from dotenv import load_dotenv
from typesafe_sdk import Choice, TypeSafeClient

load_dotenv()

message = "注文した品物がまだ届きません。注文番号はA-1021です。発送予定日から1週間たっています。"

with TypeSafeClient(compression=False) as client:
    response = client.system_one(
        state=message,
        questions={
            "team": Choice(
                instructions="この問い合わせは、どの担当が対応すべきか",
                criteria={
                    "shipping": "配送状況、届かない、配送先の変更",
                    "returns": "返品、交換、返金、破損や不良品",
                    "payment": "支払い、請求、二重引き落とし、領収書",
                    "product": "商品の仕様や使い方についての質問",
                    "other": "上のどれにも当てはまらないもの",
                },
            ),
        },
    )

answer = response.choices["team"]
print("担当:", answer.choice)
print("確信度:", answer.confidence)
print("確率:", answer.probabilities)
