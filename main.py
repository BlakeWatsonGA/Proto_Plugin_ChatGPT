import json
import quart
import quart_cors
from quart import Quart, request
from quart_cors import cors
from quart_sqlalchemy import SQLAlchemy

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reversed_strings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ReversedString(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.String(255), nullable=False)
    reversed_text = db.Column(db.String(255), nullable=False)

    def __init__(self, original_text, reversed_text):
        self.original_text = original_text
        self.reversed_text = reversed_text

    def to_dict(self):
        return {'id': self.id, 'original_text': self.original_text, 'reversed_text': self.reversed_text}

@app.route('/reverse', methods=['PUT'])
async def reverse_text():
    data = await request.get_data()
    text = data.decode('utf-8')
    reversed_text = text[::-1]

    # Store the reversed string in the database
    reversed_string = ReversedString(original_text=text, reversed_text=reversed_text)
    db.session.add(reversed_string)
    db.session.commit()

    # Generate a URL to access the reversed string in the database
    database_url = request.host_url + 'reversed_strings'
    return database_url

@app.route('/reversed_strings', methods=['GET'])
async def get_reversed_strings():
    reversed_strings = ReversedString.query.all()
    reversed_strings_dict = [r.to_dict() for r in reversed_strings]
    return {'reversed_strings': reversed_strings_dict}

@app.get("/.well-known/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/.well-known/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5003)


#@app.put("/todos/<string:username>")
#async def add_todo(username):
#    request = await quart.request.get_json(force=True)
#    if username not in _TODOS:
#        _TODOS[username] = []
#    _TODOS[username].append(request["todo"])
#    return quart.Response(response='OK', status=200)

#@app.get("/todos/<string:username>")
#async def get_todos(username):
#    return quart.Response(response=json.dumps(_TODOS.get(username, [])), status=200)

#@app.delete("/todos/<string:username>")
#async def delete_todo(username):
#    request = await quart.request.get_json(force=True)
#    todo_idx = request["todo_idx"]
    # fail silently, it's a simple plugin
#    if 0 <= todo_idx < len(_TODOS[username]):
#        _TODOS[username].pop(todo_idx)
#    return quart.Response(response='OK', status=200)

