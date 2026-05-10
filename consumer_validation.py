from confluent_kafka import Consumer, Producer
import json

consumer = Consumer({'bootstrap.servers': 'localhost:9092',
                        'group.id': 'validation',
                        'auto.offset.reset': 'earliest'})
producer = Producer({'bootstrap.servers': 'localhost:9092'})
consumer.subscribe(['live-bids'])

while True:
    msg = consumer.poll(1)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue
    bid = json.loads(msg.value().decode('utf-8'))
    if bid['amount'] > 0:
        print("Valid:", bid)
        producer.produce('valid-bids', value=json.dumps(bid))
    else:
        print("Invalid:", bid)

