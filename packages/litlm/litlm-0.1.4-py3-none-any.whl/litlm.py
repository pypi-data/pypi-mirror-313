
import time
import requests
from litellm import completion
import pandas as pd


OPENROUTER_MODELS = requests.get("https://openrouter.ai/api/v1/models").json()
OPENROUTER_MODELS = list(pd.DataFrame(OPENROUTER_MODELS['data']).id)

def complete(prompt,model,max_tokens=64, silent_exception=False, free_sleep=3, **kwargs):
    m=sorted([x for x in OPENROUTER_MODELS if model in x], key=len)[0]
    provider= f"openrouter/{m}"
    if ":free" in m:
        time.sleep(free_sleep)
    try:
        response = completion(
            provider,
            [{ "role": "user", "content": prompt,
             }],
            max_tokens=max_tokens, **kwargs
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        if not silent_exception:
            print("❗",e)
        return ""

def complete_m(m,**kwargs):
    return lambda x:complete(x,m,**kwargs)

