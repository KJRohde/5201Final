from confluent_kafka import Consumer
import json

consumer = Consumer({'bootstrap.servers': 'localhost:9092',
                        'group.id': 'high-bids',
                        'auto.offset.reset': 'earliest'})
consumer.subscribe(['valid-bids'])
highest_bids = {}

while True:
    msg = consumer.poll(1)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue
    bid = json.loads(msg.value().decode('utf-8'))
    auction = bid['auction_id']
    current = highest_bids.get(auction, {"amount": 0})
    if bid['amount'] > current['amount']:
        highest_bids[auction] = bid
        print(f"New high for {auction}: {bid['amount']} by User {bid['user_id']}")
        with open("bids_log.txt", "a") as f:
            f.write(json.dumps(bid) + "\n")
            print("Saved:", bid)