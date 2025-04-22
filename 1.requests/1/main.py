import requests

# r = requests.get('https://xkcd.com/353/')
# print(r)
# print(r.status_code)  # 200
# print(r.ok)  # True  , if the status code is less than 400 response
# print(dir(r))
# print(help(r))
# print(r.text)  # get the html content of the request page
# print(r.headers) # get the headers that come back with the response


# ----------------------------------------------------------------


# r = requests.get('https://imgs.xkcd.com/comics/python.png')
# with open('comic.png', 'wb') as f:
#     f.write(r.content)


# ----------------------------------------------------------------


# payload = {'page': 2, 'count': 25}
# r = requests.get('https://httpbin.org/get', params=payload)
# # print(r.url)  # https://httpbin.org/get?page=2&count=25
# print(r.text)
"""
In requests.get(), the params argument is used because, in a GET request, data is typically sent in the query string (URL parameters).
"""

# ----------------------------------------------------------------


# payload = {'username': 'john', 'password': 'secret'}
# r = requests.post('https://httpbin.org/post', data=payload)
# print(type(r.text))   # <class 'str'>
# r_dict = r.json() 
# print(type(r_dict))   # <class 'dict'>
# print(r_dict['form'])
"""
In requests.post(), the data argument is used because, in a POST request, data is sent in the request body rather than in the URL.
"""


# ----------------------------------------------------------------


r = requests.get('https://httpbin.org/basic-auth/islam/password', auth=('islam', 'password'))
print(r.text)  


# ----------------------------------------------------------------


r = requests.get('https://httpbin.org/delay/1', timeout=3)
print(r.text)  # wait for 1 second before sending the request

r = requests.get('https://httpbin.org/delay/6', timeout=3)
print(r.text)  # TimeoutError: The read operation timed out