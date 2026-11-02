from typesafe_sdk import Choice, Noul, Score

# 担当の振り分けを自動で行う確信度の下限。これ未満は人が確認する
CONFIDENCE_MIN = 0.8

# 優先度の重み（合計1.0）
WEIGHTS = {
    "urgency": 0.5,
    "money_at_risk": 0.3,
    "threatens_to_leave": 0.2,
}

# 優先度がこの値以上なら「急ぎ」
URGENT_MIN = 0.5

QUESTIONS = {
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
    "urgency": Score(
        instructions="この問い合わせは、どれくらい急いで対応する必要があるか",
        criteria=[
            "急ぎではない。数日以内に返信すればよい",
            "早めの対応が望ましい。今日か明日には返信したい",
            "今すぐ対応が必要。お金の損失や期限が迫っている",
        ],
    ),
    "money_at_risk": Noul(
        instructions="送り主は、お金を失った、または失いそうだと訴えているか",
    ),
    "threatens_to_leave": Noul(
        instructions="送り主は、今後の利用をやめる、または外部に訴えると述べているか",
    ),
}
