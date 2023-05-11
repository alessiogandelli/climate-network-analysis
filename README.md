# climate-network-analysis

https://stackoverflow.com/questions/49222857/modulenotfounderror-no-module-named-graph-tool



# problems 
- retweet on twitter: Trump will become #POTUS ...
- retweet on dataset: RT @pablorodas: Trump will become #POTUS in th.

this means that when retweeting you are also mentioning the author, so an edge between the tweet and the the original author is created


# from bipartite to mono 

should be directed? should i simplY take the connected components?

for a in  authors
    for all tweets of a
        if tweet mention b
            add edge a->b
        if tweet retweet t2
            add edge a-> author(t2)


multi layer network, the same set of nodes one layer per topic 