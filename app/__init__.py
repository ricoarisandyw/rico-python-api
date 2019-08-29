from flask import Flask, request
from flask import jsonify
from googletrans import Translator
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

print("__init__.py : Starting flask application.")
app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# === ROUTING
@app.route('/')
def index():
	return 'Server Works!'

@app.route('/translate-html',methods=['POST'])
def parse_html():
	_text = request.form['text']
	_src = request.form['src']
	_dest = request.form['dest']

	_parsed_html = BeautifulSoup(_text,'html.parser')
	_list = _parsed_html.prettify().split('\n')
	
	_container = []
	for _l in _list:
		if _l[0] == '<' and _l[-1] == '>':
			_container.append(_l)
		else:
			translator = Translator()
			result = translator.translate(_l,src=_src,dest=_dest)
			_container.append(result.text)

	return jsonify({
			'list':_container,
			'combined':''.join(_container)
		})
  
@app.route('/translate',methods=['POST'])
def translate():
	_src = request.form['src']
	_dest = request.form['dest']
	_text = request.form['text']
	translator = Translator()
	result = translator.translate(_text,src=_src,dest=_dest)
	obj = {
		'text':result.text,
		'lang':_dest,
		'src':_src
	}
	return jsonify(obj)

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    app.run(debug=options.debug, port=options.port)