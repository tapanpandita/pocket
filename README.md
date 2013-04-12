Pocket
======

A python wrapper for the [pocket api](http://getpocket.com/api/docs).

Installation
------------
```
pip install pocket
```

Usage
------

You'll need your pocket consumer key. You can find this from your account page.
You will also need the access token for the account you want to modify.
Then, you need to create an instance of the pocket object

```python
import pocket

pocket_instance = pocket.Pocket(consumer_key, access_token)
```

### Chaining Modify Methods

TODO

### OAUTH

TODO

For detailed documentation of the methods available, please visit the official [pocket api documentation](http://getpocket.com/api/docs).
