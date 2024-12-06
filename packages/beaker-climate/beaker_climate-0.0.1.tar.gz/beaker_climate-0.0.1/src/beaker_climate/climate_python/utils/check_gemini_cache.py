import os
import google.generativeai as genai
from google.generativeai import caching
import datetime
import time

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

for c in genai.caching.CachedContent.list():
    print(c)

CachedContent(
    name='cachedContents/t2qym525vve1',
    model='models/gemini-1.5-flash-8b',
    display_name='api_assistant_esgf_client',
    usage_metadata={
        'total_token_count': 21279,
    },
    create_time=2024-11-18 15:31:08.973119+00:00,
    update_time=2024-11-18 15:31:08.973119+00:00,
    expire_time=2024-11-18 16:31:08.658662+00:00
)

# delete a cache with
c.delete()