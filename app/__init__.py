from litestar import Litestar

from app.controllers import ItemController


app = Litestar([ItemController])
