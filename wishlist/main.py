from fastapi import FastAPI, Request, Depends, Form
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_302_FOUND
from sqlalchemy.orm import Session
from database.db_depends import get_db
from models import Item

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@app.get('/')
def home(request: Request, db_session: Session = Depends(get_db)):
    wishlist = db_session.query(Item).all()
    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                       'wishlist': wishlist}
                                      )


@app.post('/add')
def add(title: str = Form(...), description: str = Form(...), price: int = Form(...), db_session: Session = Depends(get_db)):
    new_item = Item(title=title, description=description, price=price)
    db_session.add(new_item)
    db_session.commit()

    url = app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@app.get('/update/{item_id}')
def update(item_id: int, db_session: Session = Depends(get_db)):
    item = db_session.query(Item).filter(Item.id == item_id).first()
    item.is_complete = not item.is_complete
    db_session.commit()

    url = app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_302_FOUND)


@app.get('/delete/{item_id}')
def delete(item_id: int, db_session: Session = Depends(get_db)):
    item = db_session.query(Item).filter(Item.id == item_id).first()
    db_session.delete(item)
    db_session.commit()

    url = app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_302_FOUND)





