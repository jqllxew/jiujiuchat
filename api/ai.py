import httpx
from openai import OpenAI

OpenAI(api_key="", base_url="", http_client=httpx.Client(proxy=""))
