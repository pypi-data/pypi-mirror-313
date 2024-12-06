import os
import sys

from khulnasoft import Khulnasoft

account_id = os.getenv("KHULNASOFT_ACCOUNT_ID")
if account_id is None:
    sys.exit("KHULNASOFT_ACCOUNT_ID is not defined")


client = Khulnasoft()

t = client.workers.ai.run(
    "@cf/meta/m2m100-1.2b",
    account_id=account_id,
    text="I'll have an order of the moule frites",
    target_lang="french",
    source_lang="english",
)

# print(t['translated_text'])
