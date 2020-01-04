from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost
from wordpress_xmlrpc.methods.users import GetUserInfo


url = 'http://www.py4seo.com/xmlrpc.php'
login = 'admin'
passw = '1234567'

client = Client(url, login, passw)

posts = client.call(GetPosts({'number': 10000}))

post = WordPressPost()

post.title = 'My post'
post.content = 'This is a wonderful blog post about XML-RPC.'

post.id = client.call(NewPost(post))

# whoops, I forgot to publish it!
post.post_status = 'publish'

client.call(EditPost(post.id, post))
