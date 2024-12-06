from os import environ
from dotenv import load_dotenv
import uuid


load_dotenv()  # Only needed for developing, on production Docker .env file is used

CONSUL_HOST = environ.get("CONSUL_HOST", "192.168.7.201")
CONSUL_PORT = environ.get("CONSUL_PORT", 8500)
CONSUL_DNS_PORT = environ.get("CONSUL_DNS_PORT", 8600)
PORT = int(environ.get("PORT", '80'))
SERVICE_NAME = environ.get("SERVICE_NAME", "service1")
# SERVICE_ID = environ.get("SERVICE_ID", "s1r0")
# GENERATE UUID FOR SERVICE_ID
SERVICE_ID = SERVICE_NAME + "_" + str(uuid.uuid4())
IP = environ.get("IP", "127.0.0.1")