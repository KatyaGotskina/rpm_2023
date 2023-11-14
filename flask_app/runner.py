from app import app
from app.models import User, Categories, Orders, Products, Role, RolesForUsers, OrdersToProducts
from app.models import db

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Categories=Categories, Orders=Orders,  Products=Products, Role=Role, RolesForUsers=RolesForUsers, OrdersToProducts=OrdersToProducts)

if __name__ == '__main__':
    app.run()