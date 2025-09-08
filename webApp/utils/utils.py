import redis, json
r = redis.Redis(host="localhost", port=6379, db=0)

def publishEvent(event_type, payload):
    message = json.dumps({"event": event_type, "data": payload})
    r.publish("uninest", message)