# Monzo Flask

This is a weekend project to access Monzo's API with a 20 hour project to get me back into Python and challenge myself to learn to access and parse JSON feeds.


The code is pretty well documented (mostly) and with an understanding of Jinja2 and Python functions you should be able to work out what everything does.

**The run down on getting going:**

> * Use the [Monzo Playground]('https://developers.monzo.com/api/playground') to replace the following on lines 12/13 of 'Monzo.py'
>   > clientID = '**user_id_goes_here**' and authCode = '**access_token_goes_here**'
> * Run **sudo python /path/to/Monzo.py**
> * Visit http://127.0.0.1/ and the interface should be served there

**Functionality I want to add:**
* Plot transactions on a map
* Work out spending in relation to budgets
* Improve speed, the wait too long at the moment - such as by caching
