import urllib.request
try:
    urllib.request.urlopen("http://localhost:8000/api/exercises/", data=b"hi")
except Exception as e:
    print(e)
