# -*- coding: utf-8 -*-
import responder
from responder import API
import time
import traceback

from alchemydb import Session, engine
from models import Tasks

from sqlutils import alchemytojson, alchemytodict
from todo import add_todo
from todo import delete_todo
from todo import update_todo
from todo import get_todo
from todo import get_todo_list

api = responder.API(
   cors=True,
   allowed_hosts=["*"],
)

@api.route("/")
def hello_html(req, resp):
    resp.html = api.template('hello.html')

@api.route("/api/task/{id}")
def users_json(req, resp, *, id):
    session = Session()
    try:
        user = session.query(Tasks).filter_by(id=id).first()
        resp.headers = {"Content-Type": "application/json; charset=utf-8"} 
        resp.content = alchemytojson(user) 
    except Exception:
        traceback.print_exc()
        resp.media ={"errmessage":"Error occured"}
    finally:
        session.close()
        print(engine.pool.status())

@api.route("/api/tasks")
def users_json(req, resp):
    session = Session()
    try:
        users = session.query(Tasks).all()
        resp.headers = {"Content-Type": "application/json; charset=utf-8"} 
        resp.content = alchemytojson(users) 
    except Exception:
        traceback.print_exc()
        resp.media ={"errmessage":"Error occured"}
    finally:
        session.close()
        print(engine.pool.status())

class UpdateGetDeleteTodo:
   def on_get(self, req, resp, *, id):
       todo = get_todo(id)
       resp.media = {
           "status": True,
           "todo": todo
       }
   async def on_put(self, req, resp, *, id):
       @api.background.task
       def process_update_todo(name, text):
           time.sleep(3)
           update_todo(id, name, text)
       data = await req.media()
       name = data['name']
       text = data['text']
       process_update_todo(name, text)
       resp.media = {
           'status': True
       }
   async def on_delete(self, req, resp, *, id):
       @api.background.task
       def process_delete_todo():
           time.sleep(3)
           delete_todo(id)
       process_delete_todo()
       resp.media = {
           'status': True
       }

class AddGetTodo:
   def on_get(self, req, resp):
       todos = get_todo_list()
       resp.media = {
           "status": True,
           "todos": todos
       }
   async def on_post(self, req, resp):
       @api.background.task
       def process_add_todo(name, text):
           time.sleep(3)
           add_todo(name, text)
       data = await req.media()
       name = data['name']
       text = data['text']
       process_add_todo(name, text)
       resp.media = {
           'status': True
       }

api.add_route("/api/todo", AddGetTodo)
api.add_route("/api/todo/{id}", UpdateGetDeleteTodo)

if __name__ == "__main__":
   port = 5042
   api.run(port=port)