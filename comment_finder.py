import requests
import sys
import re

TIMEOUT = []

RE_SCRIPT = re.compile(r'<script[\s\S]*</script>')
RE_STYLE = re.compile(r'<style[\s\S]*</style>')
RE_LINK = re.compile(r'<link[\s\S]*rel=["\']stylesheet["\'][\s\S]*</link?')

RE_JS_M = re.compile(r'/\*[\s\S]*?\*/')
RE_JS_S = re.compile(r'//[^\n]')
RE_HTML = re.compile(r'<!--[\S\s]*-->')

RE_URLS = re.compile(r'<a[\s\S]*</a>')

def get_text(url:str)->str:
	try:
		resp = requests.get(url, timeout=10)
	except requests.exceptions.ConnectTimeout:
		global TIMEOUT
		TIMEOUT.append(url)
		return None
		
	if resp.status_code == 404:
		return None
	
	return resp.text


def process_url(url:str)->None:
	print(f'Processing {url}')
	text = get_text(url)

	if text is None:
		return
	
	# Extract comments
	js_m = RE_JS_M.findall(text)
	js_s = RE_JS_S.findall(text)
	html = RE_HTML.findall(text)

	for i in js_m + js_s + html:
		print(i)

	# Get other links in the page
	scripts = [get_url_from_tag(x, url) for x in RE_SCRIPT.findall(text)]
	styles = [get_url_from_tag(x, url) for x in RE_STYLE.findall(text)]
	links = [get_url_from_tg(x, url) for x in RE_LINK.findall(text)]
	urls = [get_url_from_tag(x, url) for x in RE_URLS.findall(text)]
	
	urls_to_visit = scripts + styles + urls
	for u in urls_to_visit:
		process_url(u)

def get_url_from_tag(text, parent_url):
	if 'src' in text:
		attr_name = 'src'
	elif 'href' in text:
		attr_name = 'href'
	else:
		print(f'`src` or `href` not in text: {text}')
		return
	
	text = text.replace(' ','')
	text = text[text.find(f'{attr_name}="')+len(attr_name)+2:]
	text = text[:text.find('"')]

	return rel_to_abs(text, parent_url)

def rel_to_abs(url, parent_url):
	if url.startswith('./'):
		return parent_url + url[1:]
	elif url.startswith('/'):
		return parent_url + url
	elif not url.startswith('http'):
		return parent_url + '/' + url
	return url

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('1 argument only', file=sys.stderr)
		sys.exit(-1)
	
	process_url(sys.argv[1])

	if len(TIMEOUT) != 0:
		print('Timeout URLS:')
		print(TIMEOUT)
