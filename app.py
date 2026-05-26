import os
from flask import Flask
from redis import Redis, RedisError

app = Flask(__name__)

# Fetch environment variables with fallback defaults
REDIS_HOST = os.environ.get("REDIS_HOST", "redis-service")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")

# Initialize Redis client
try:
    redis = Redis(
        host=REDIS_HOST, 
        port=6379, 
        password=REDIS_PASSWORD, 
        decode_responses=True, 
        socket_connect_timeout=2
    )
except Exception as e:
    redis = None

@app.route('/')
def hello():
    if not redis:
        return "Database Connection Error! Redis client is not initialized.", 500
    
    try:
        # Increment the visitor counter in Redis
        visits = redis.incr("counter")
        return f"<h3>Welcome!</h3><p>This page has been viewed <b>{visits}</b> times.</p>"
    except RedisError as e:
        return f"<h3>Database Error!</h3><p>Could not connect to Redis. Reason: {str(e)}</p>", 500

if __name__ == "__main__":
    # Run the Flask development server
    app.run(host="0.0.0.0", port=5000)
