import json
import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

@app.route('/')
async def index():
    return "Welcome!"

@app.put('/reverse')
async def reverse_text():
    """
    Reverse the provided text
    """
    request = await quart.request.get_json(force=True)
    text = request["text"]
    reversed_text = text[::-1]
    json_response = json.dumps({"text": reversed_text})
    return quart.Response(json_response, mimetype="text/json", status=200)

@app.put('/dots')
async def dot_text():
    """
    Add dots between every 3 characters in the text
    """
    request = await quart.request.get_json(force=True)
    text = request["text"]
    dotted_text = '...'.join(text[i:i+3] for i in range(0, len(text), 3))
    json_response = json.dumps({"text": dotted_text})
    return quart.Response(json_response, mimetype="text/json", status=200)

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

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()