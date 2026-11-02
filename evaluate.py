import json

with open("inquiries.json", encoding="utf-8") as f:
    answers = {i["id"]: i for i in json.load(f)}
with open("results.json", encoding="utf-8") as f:
    results = json.load(f)

auto = [r for r in results if r["team"] != "human"]

guess_ok = sum(r["team_guess"] == answers[r["id"]]["team"] for r in results)
auto_ok = sum(r["team"] == answers[r["id"]]["team"] for r in auto)
urgent_ok = sum(r["urgent"] == answers[r["id"]]["urgent"] for r in results)

print("担当の判定（全件）の正解:", guess_ok, "/", len(results))
print("自動で振り分けた件数:", len(auto), "/", len(results))
print("自動で振り分けた分の正解:", auto_ok, "/", len(auto))
print("人に回した件数:", len(results) - len(auto))
print("急ぎの判定の正解:", urgent_ok, "/", len(results))

print("間違えたもの:")
for r in results:
    a = answers[r["id"]]
    if r["team_guess"] != a["team"] or r["urgent"] != a["urgent"]:
        print(
            r["id"],
            "担当", r["team_guess"], "正解", a["team"],
            "確信度", round(r["confidence"], 2),
            "急ぎ", r["urgent"], "正解", a["urgent"],
        )
