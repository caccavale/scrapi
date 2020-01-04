# scrapi

ScrAPI is an afternoon project that "wraps" any website in a _very_ dumb restful API.

It is run with `python3 scrapi <website>` and spawns a flask instance on the default `127.0.0.1:5000`.  You can then query this endpoint like you would the website:

`python3 scrapi github.com` queried with `curl 127.0.0.1:5000/caccavale?links=a&` -> would return a json with key `links` to all things with css selector `a` on the page `github.com/caccavale`.

### Advanced Usage...
When I originally made this my roommate [Matt](https://github.com/mattrberry) said it had to be less that ~~50~~ _cough_-- 60 lines.  As such, I've tried to fit as much _dumb_ functionality within those bounds.  If you use scrapi as a library, you can pass in your own cookies with by setting the optional kwarg `cookies` upon construction.  You can also enable caching with `cache=True` and change the cache size with `max_cache` (optimally a power of 2).

### Examples:
```
python3 scrapi caccavale.github.io &
curl "127.0.0.1:5000/?links=a&"
>> {"links": ["<a href=\"mailto:samcaccavale@gmail.com\">email</a>", "<a href=\"http://github.com/caccavale\">github</a>"]}
```
As a module:
```
python3
from scrapi import Scrapi
Scrapi('caccavale.github.io',
        cache=True,
        max_cache=256,
        cookies='favorite=chocolate_chip').run()
```
Note, these are equivalent:
```
python scrapi github.com/caccavale &
curl 127.0.0.1:5000/?<stuff>
```

```
python scrapi github.com &
curl 127.0.0.1:5000/caccavale/?<stuff>
```
