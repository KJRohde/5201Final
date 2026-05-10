from confluent_kafka import Producer
import json, random, datetime, time

config={'bootstrap.servers': 'localhost:9092'}
producer = Producer(config)
auction_ids = ['Brewer Tickets', 'T-shirt', 'Coffee Mug', 'Beer', 'Food Voucher']
users = ['Kyle', 'Brenda', 'Sue', 'Dean', 'Dale']

# Simulate sending bids every 3 seconds
while True:
    bid = {
        "auction_id": random.choice(auction_ids),
        "user_id": random.choice(users),
        "amount": random.randint(100, 1000),
        "timestamp": datetime.datetime.now().strftime('%H:%M:%S')
    }
    producer.produce('live-bids', value=json.dumps(bid))
    print("Sent:", bid)
    time.sleep(2)

# Take user input from streamlit page and use those bids instead of random ones. This just simulates that user input
