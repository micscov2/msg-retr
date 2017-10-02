import pickle
from redis import StrictRedis

s_redis = StrictRedis(host="localhost", port=6379, db=0)
keys = []

def get_client_name_to_sock_mapping():
	client_name_to_sock_mapping = {} #pickle.HIGHEST_PROTOCOL
	for key in keys:
		if s_redis.get(key) is None:
			continue
		client_name_to_sock_mapping[key] = pickle.loads(s_redis.get(key))
		
	return client_name_to_sock_mapping

def set_client_name_to_sock_mapping(key, value):
	keys.append(key)
	s_redis.set(key, pickle.dumps(value, pickle.HIGHEST_PROTOCOL))
