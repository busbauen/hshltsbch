from splitwise import Splitwise, Expense
from splitwise.user import ExpenseUser
from ipdb import set_trace
from flask import Flask, redirect, session, request

consumer_key = "OFxHQn9njY0OKV1exCz8V95Mi3p5Dk9tC10XPu4a"
consumer_secret = "ipkzAiNX8J2WNM7mf7zyy0DLKcd3qAXxKuyx0D9G"

#Splitwise.setDebug(True)

app = Flask(__name__)
app.secret_key = "hans"

@app.route("/login")
def login():
    sObj = Splitwise(consumer_key, consumer_secret)
    url, secret = sObj.getAuthorizeURL()
    session['secret'] = secret
    #with open("key.txt", "w") as f:
    #    f.write(secret)
    return redirect(url)

@app.route("/authorize")
def authorize():
    oauth_token    = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')

    sObj = Splitwise(consumer_key, consumer_secret)
    access_token = sObj.getAccessToken(oauth_token,session['secret'], oauth_verifier)
    session['access_token'] = access_token

    sObj.setAccessToken(session['access_token'])
    print(session['access_token'])
    friends = sObj.getCurrentUser()
    return str(friends)

@app.route("/")
def index():
    sObj = Splitwise(consumer_key, consumer_secret)
    sObj.setAccessToken({u'oauth_token_secret': u'u78abWn2RBFF0qVz7tKkoN3wm2USLxhJjPkXUCC0', u'oauth_token': u'kQuttkozbgRfzlel7GYpPZbR5oQUg3RwuejHCv1e'})
    robo6_id = [x.id for x in sObj.getGroups() if x.name == 'robo-test'][0]
    expenses = sObj.getExpenses(group_id=robo6_id)
    expenses = [(x.created_by.first_name, x.created_at, x.cost, x.description) for x in expenses if not x.deleted_by]
    print(expenses)
    g = sObj.getGroup(robo6_id)
    for member in g.members:
        for balance in member.balances:
            print(member.first_name, balance.amount)
    return ""

@app.route("/add")
def add():
    oauth = Splitwise(consumer_key, consumer_secret)
    oauth.setAccessToken({u'oauth_token_secret': u'u78abWn2RBFF0qVz7tKkoN3wm2USLxhJjPkXUCC0', u'oauth_token': u'kQuttkozbgRfzlel7GYpPZbR5oQUg3RwuejHCv1e'})
    robo6_id = [x.id for x in oauth.getGroups() if x.name == 'robo-test'][0]
    group = oauth.getGroup(robo6_id)
    users = {user.first_name: user.id for user in group.members}

    robo6_id = [x.id for x in oauth.getGroups() if x.name == 'robo-test'][0]
    cost = 10.12
    #expense = Expense(group_id=robo6_id)
    expense = Expense()
    expense.group_id = robo6_id
    expense.setCost(cost)
    expense.setDescription("Testing")
    
    user1 = ExpenseUser()
    user1.setId(users['kmille'])
    user1.setPaidShare(cost)
    user1.setOwedShare(cost/2.0)

    user2 = ExpenseUser()
    user2.setId(users['dummy'])
    user2.setPaidShare(0)
    user2.setOwedShare(cost/2.0)

    expense.setUsers([user1, user2])
    expense = oauth.createExpense(expense)
    print(expense)
    return ""


if __name__ == '__main__':
    app.run(debug=True)
