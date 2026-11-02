import json
import time

from dotenv import load_dotenv
from typesafe_sdk import TypeSafeClient

from questions import CONFIDENCE_MIN, QUESTIONS, URGENT_MIN, WEIGHTS

load_dotenv()

PRICE_PER_MILLION_INPUT_TOKENS = 0.042  # TypeSafe社の定価（ドル）。無料版では請求されない


def priority_of(response):
    # 緊急度は3段階（0〜2）なので、2で割って0〜1にそろえる
    urgency = response.scores["urgency"].score / 2
    return (
        WEIGHTS["urgency"] * urgency
        + WEIGHTS["money_at_risk"] * response.nouls["money_at_risk"].noul
        + WEIGHTS["threatens_to_leave"] * response.nouls["threatens_to_leave"].noul
    )


def triage(client, text):
    response = client.system_one(state=text, questions=QUESTIONS)
    team = response.choices["team"]
    priority = priority_of(response)
    return {
        "team": team.choice if team.confidence >= CONFIDENCE_MIN else "human",
        "team_guess": team.choice,
        "confidence": team.confidence,
        "priority": priority,
        "urgent": priority >= URGENT_MIN,
        "input_tokens": response.usage.input_tokens,
    }


def main():
    with open("inquiries.json", encoding="utf-8") as f:
        inquiries = json.load(f)

    results = []
    with TypeSafeClient(compression=False) as client:
        for inquiry in inquiries:
            start = time.perf_counter()
            result = triage(client, inquiry["text"])
            result["seconds"] = time.perf_counter() - start
            result["id"] = inquiry["id"]
            results.append(result)
            print(
                inquiry["id"],
                result["team"],
                "確信度", round(result["confidence"], 2),
                "優先度", round(result["priority"], 2),
                "急ぎ" if result["urgent"] else "",
                round(result["seconds"], 2), "秒",
            )

    tokens = sum(r["input_tokens"] for r in results)
    cost = tokens / 1000000 * PRICE_PER_MILLION_INPUT_TOKENS
    print(len(results), "件", tokens, "トークン", "定価で約", round(cost, 5), "ドル")

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f)


main()
