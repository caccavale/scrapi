# scrapi

ScrAPI is a really dump afternoon project that "wraps" any website in a _very_ dumb restful API.

It is run with `python3 scrapi <website>` and spawns a flask instance on the default `127.0.0.1:5000`.  You can then query this endpoint like you would the constructed website:

`python3 scrapi github.com` queried with `curl 127.0.0.1:5000/caccavale?links=a&` -> would return all things things with css selector `a` in json with key `links` on the page `github.com/caccavale`.

You might ask why this is useful.  It is not.

Also, setting the script up with domain `github.com/caccavale` and querying `/?<stuff>` is equivalent to querying `/caccavale?<stuff>` on `github.com`.

Example:
```
python3 scrapi caccavale.github.io
curl "127.0.0.1:5000/?links=a&"
>> {"links": ["<a href=\"mailto:samcaccavale@gmail.com\">email</a>", "<a href=\"http://github.com/caccavale\">github</a>"]}
```