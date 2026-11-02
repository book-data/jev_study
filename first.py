from dotenv import load_dotenv
from typesafe_sdk import Noul, TypeSafeClient

load_dotenv()

message = "届いたマグカップが割れていました。返品して返金してもらえますか。"

with TypeSafeClient(compression=False) as client:
    response = client.system_one(
        state=message,
        questions={
            "wants_refund": Noul(
                instructions="この問い合わせの送り主は、返金を求めているか",
            ),
        },
    )

print(response.nouls["wants_refund"].noul)
