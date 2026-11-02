from dotenv import load_dotenv
from typesafe_sdk import Score, TypeSafeClient

load_dotenv()

message = "クレジットカードで同じ注文が2回引き落とされています！今日中に対応してください。"

with TypeSafeClient(compression=False) as client:
    response = client.system_one(
        state=message,
        questions={
            "urgency": Score(
                instructions="この問い合わせは、どれくらい急いで対応する必要があるか",
                criteria=[
                    "急ぎではない。数日以内に返信すればよい",
                    "早めの対応が望ましい。今日か明日には返信したい",
                    "今すぐ対応が必要。お金の損失や期限が迫っている",
                ],
            ),
        },
    )

answer = response.scores["urgency"]
print("緊急度:", answer.score)
print("確信度:", answer.confidence)
print("確率:", answer.probabilities)
