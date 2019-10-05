from flask import Flask, request
from flask import jsonify
import requests as http
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

@app.route('/google/translate-html',methods=['POST'])
def translate_html():
	_text = request.form['text']
	_src = request.form['src']
	_dest = request.form['dest']

	_parsed_html = BeautifulSoup(_text,'html.parser')
	_pretty = _parsed_html.prettify()
	print("Pretty : ",_pretty)
	_list = _pretty.split('\n')

	_container = []
	for _l in _list:
		if len(_l)>0:
			if _l[0] == '<' and _l[-1] == '>':
				_container.append(_l)
			elif _l == "":
				_last_index = _l[len(_container)-1]
				_l[len(_container)-1] = _last_index + " "
			else:
				translator = Translator()
				result = translator.translate(_l,src=_src,dest=_dest)
				_container.append(result.text)

	return jsonify({
			'list':_container,
			'combined':''.join(_container)
		})
  
@app.route('/google/translate',methods=['POST'])
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

@app.route('/google/youtube',methods=['GET'])
def youtube():
	URL = "https://www.googleapis.com/youtube/v3/search"
	
	# Parameter
	_query = request.args.get('q')
	channelId = request.args.get('channelId') # ex : 'UC_cFJ1ceU-8McyPauUuEQzQ'
	eventType = request.args.get('eventType') # ex :completed, live, upcoming

	# defining a params dict for the parameters to be sent to the API 
	PARAMS = {
		'part':'snippet',
		'key':'AIzaSyBWFcApIG5KNG7ncnmzG7UCnP7fLdgaWaw',
		'order':'relevance',
		'q':_query,
		'type':'video',
		'channelId':channelId,
		'maxResults':'50'
	} 
	  
	# sending get request and saving the response as response object 
	_r = http.get(url = URL, params = PARAMS) 
	  
	# extracting data in json format 
	_data = _r.json()
	_items = _data['items']
	_simply_items = []
	for _i in _items:
		_simply_items.append({
				'id' : _i['snippet']['channelId'],
				'video_id' : _i['id']['videoId'],
				'title' : _i['snippet']['title'],
				'channel' : _i['snippet']['channelTitle'],
				'thumbnail' : _i['snippet']['thumbnails']['default']['url'],
			})
	return jsonify(_simply_items)

@app.route('/google/maps',methods=['GET'])
def maps():
	_query = request.args.get('q')
	print(_query)
	URL = "https://maps.googleapis.com/maps/api/geocode/json"
	# location given here 
	location = _query
	  
	# defining a params dict for the parameters to be sent to the API 
	PARAMS = {'address':location,'key':'AIzaSyBWFcApIG5KNG7ncnmzG7UCnP7fLdgaWaw'} 
	  
	# sending get request and saving the response as response object 
	r = http.get(url = URL, params = PARAMS) 
	  
	# extracting data in json format 
	data = r.json()
	return jsonify(data)

# SWAGGER DOCUMENTATION
# docs = FlaskApiSpec(app)

# docs.register(maps)
# docs.register(youtube)
# docs.register(translate)
# docs.register(translate_html)

# app.add_url_rule('/stores', view_func=StoreResource.as_view('Store'))
# docs.register(StoreResource)

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    app.run(debug=options.debug, port=options.port)