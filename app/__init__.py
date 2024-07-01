from litestar import Litestar

from app.controllers import ItemController
from app.database import db_plugin


app = Litestar([ItemController], debug=True, plugins=[db_plugin])
