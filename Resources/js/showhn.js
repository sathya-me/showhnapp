/* Data Model */


//url : http://api.thriftdb.com/api.hnsearch.com/items/_search?q=show+hn&type=submission&sortby=create_ts+desc&pretty_print=true

/*

{
            "item": {
                "_id": "5589401-e1174",
                "_noindex": false,
                "_update_ts": 1366642832215775,
                "cache_ts": "2013-04-22T15:00:06Z",
                "create_ts": "2013-04-22T14:35:57Z",
                "discussion": null,
                "domain": null,
                "id": 5589401,
                "num_comments": 0,
                "parent_id": null,
                "parent_sigid": null,
                "points": 1,
                "text": "I'm the author of Redis in Action, and over the last couple weeks whenever I've had some spare time, I've been working on a few side-projects (I know others exist, but I don't like the way they are structured or the way they work). One of them required that I build an object-Redis mapper for Python. When I started to want to use it in another project, I decided it was time to polish it up and release it.<p>Github: https://github.com/josiahcarlson/rom\nPypi: https://pypi.python.org/pypi/rom\nDocs: http://pythonhosted.org/rom<p>I've got to head to the office in a few minutes, but I'll be happy to answer any questions when I get in.",
                "title": "Show HN: Redis object mapper for Python",
                "type": "submission",
                "url": null,
                "username": "DrJosiah"
            },
            "score": 1.2615862
        }

*/

var post = new Post;
