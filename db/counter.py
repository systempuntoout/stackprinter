from google.appengine.ext import db
import random

#Counter sharded
NUM_SHARDS = 20

class SimpleCounterShard(db.Model):
    """Shards for the counter"""
    count = db.IntegerProperty(required=True, default=0)

def get_count():
    """Retrieve the value for a given sharded counter."""
    total = 0
    for counter in SimpleCounterShard.all():
        total += counter.count
    return total

def increment():
    """Increment the value for a given sharded counter."""
    def txn():
        index = random.randint(0, NUM_SHARDS - 1)
        shard_name = "shard" + str(index)
        counter = SimpleCounterShard.get_by_key_name(shard_name)
        if counter is None:
            counter = SimpleCounterShard(key_name=shard_name)
        counter.count += 1
        counter.put()
    db.run_in_transaction(txn)