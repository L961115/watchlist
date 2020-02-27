import os
#dotenv:管理env和flaskenv环境配置的库
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__),'.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from watchlist import app