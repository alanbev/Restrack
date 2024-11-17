import panel as pn
from ui.find_investigations import Find_investigations
from ui.login import Login

my_login=Login()
user_name=my_login.username
print(user_name)
user_name = 'user1' # bypass login which in not returning user name!
#my_investigations = Find_investigations(user_name)
