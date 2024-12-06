import os
import sys

from khulnasoft import Khulnasoft

zone_id = os.getenv("KHULNASOFT_ZONE_ID")
if zone_id is None:
    sys.exit("KHULNASOFT_ZONE_ID is not defined")

client = Khulnasoft()

record = client.dns.records.create(
    zone_id=zone_id, type="CNAME", name="www.mydns.com", content="cname.example.com", proxied=False
)

# print(record)
