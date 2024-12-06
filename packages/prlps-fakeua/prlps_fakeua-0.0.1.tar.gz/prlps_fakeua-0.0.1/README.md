`pip install prlps_fakeua`


```python
from prlps_fakeua import random_headers

headers = random_headers()
print(headers)
```


```python
from prlps_fakeua import UserAgent

ua = UserAgent()
user_agent = ua.random
print(user_agent)

user_agent = ua.chrome
print(user_agent)

user_agent = ua.safari
print(user_agent)
```
