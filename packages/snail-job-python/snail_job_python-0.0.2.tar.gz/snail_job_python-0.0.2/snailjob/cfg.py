import os
import random
import string

from dotenv import load_dotenv


def generate_hostid(length: int = 20) -> str:
    """生成 host-id

    Returns:
        str: host-id
    """
    return "py-" + "".join(random.choice(string.digits) for _ in range(length - 3))


load_dotenv(verbose=True)

SNAIL_USE_GRPC = os.getenv("SNAIL_USE_GRPC", "false").lower() == "true"

SNAIL_SERVER_HOST = os.getenv("SNAIL_SERVER_HOST", "127.0.0.1")
SNAIL_SERVER_PORT = os.getenv("SNAIL_SERVER_PORT", "17888")

SNAIL_VERSION = os.getenv("SNAIL_VERSION", "1.1.0")
SNAIL_HOST_IP = os.getenv("SNAIL_HOST_IP", "127.0.0.1")
SNAIL_HOST_PORT = os.getenv("SNAIL_HOST_PORT", "17889")
SNAIL_NAMESPACE = os.getenv("SNAIL_NAMESPACE", "764d604ec6fc45f68cd92514c40e9e1a")
SNAIL_GROUP_NAME = os.getenv("SNAIL_GROUP_NAME", "snail_job_demo_group")
SNAIL_TOKEN = os.getenv("SNAIL_TOKEN", "SJ_Wyz3dmsdbDOkDujOTSSoBjGQP1BMsVnj")

SNAIL_HOST_ID = generate_hostid()

SNAIL_HEADERS = {
    "host-id": SNAIL_HOST_ID,
    "host-ip": SNAIL_HOST_IP,
    "version": SNAIL_VERSION,
    "host-port": SNAIL_HOST_PORT,
    "namespace": SNAIL_NAMESPACE,
    "group-name": SNAIL_GROUP_NAME,
    "token": SNAIL_TOKEN,
    "content-type": "application/json",
}


SNAIL_LOG_LEVEL = os.getenv("SNAIL_LOG_LEVEL", "INFO")
SNAIL_LOG_FORMAT = os.getenv(
    "SNAIL_LOG_FORMAT",
    "%(asctime)s | %(name)-22s | %(levelname)-8s | %(message)s",
)
SNAIL_LOG_REMOTE_INTERVAL = int(os.getenv("SNAIL_LOG_REMOTE_INTERVAL", "10"))
SNAIL_LOG_REMOTE_BUFFER_SIZE = int(os.getenv("SNAIL_LOG_REMOTE_BUFFER_SIZE", "10"))
SNAIL_LOG_LOCAL_FILENAME = os.getenv("SNAIL_LOG_LOCAL_FILENAME", "log/snailjob.log")
SNAIL_LOG_LOCAL_BACKUP_COUNT = int(os.getenv("SNAIL_LOG_LOCAL_BACKUP_COUNT", "2"))


ROOT_MAP = "ROOT_MAP"
