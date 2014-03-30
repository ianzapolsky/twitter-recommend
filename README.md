# twitter-recommendation

Experimentation with Twitter bots.

### description

The current model looks for tweets where it is mentioned and replies to them
with a book recommendation fetched via the Amazon Product Advertising API based 
on the hashtags contained within the tweet. Tweets with no hashtags and tweets 
that do not directly mention the bot are ignored.

### requirements/relevant links

When running the files within this directory, be sure that your 
system/environment satisfies the requirements in requirements.txt.

This bot uses [twitter][tp] and [amazonproduct][ap], two Python wrappers for 
the Twitter and Amazon APIs.

### contributors

- [ianzapolsky](https://github.com/ianzapolsky)

[tp]:https://github.com/sixohsix/twitter
[ap]:http://python-amazon-product-api.readthedocs.org/en/latest/
