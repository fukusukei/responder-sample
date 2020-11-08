# -*- coding: utf-8 -*-
import responder
import traceback

from alchemydb import Session, engine
from models import User

from sqlutils import alchemytojson, alchemytodict

api = responder.API()

@api.route("/")
def hello_html(req, resp):
    resp.html = api.template('hello.html')

@api.route("/api/user/{id}")
def users_json(req, resp, *, id):
    session = Session()
    try:
        user = session.query(User).filter_by(id=id).first()
        resp.headers = {"Content-Type": "application/json; charset=utf-8"} 
        resp.content = alchemytojson(user) 
    except Exception:
        traceback.print_exc()
        resp.media ={"errmessage":"Error occured"}
    finally:
        session.close()
        print(engine.pool.status())

@api.route("/api/users")
def users_json(req, resp):
    session = Session()
    try:
        users = session.query(User).all()
        resp.headers = {"Content-Type": "application/json; charset=utf-8"} 
        resp.content = alchemytojson(users) 
    except Exception:
        traceback.print_exc()
        resp.media ={"errmessage":"Error occured"}
    finally:
        session.close()
        print(engine.pool.status())

if __name__ == '__main__':
    print(__name__)
    api.run()