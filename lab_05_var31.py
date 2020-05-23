# py_ver == "3.6.9"
import flask
import requests
import validators
import re

app = flask.Flask(__name__)


@app.route("/colour")
def set_colour():
    return """
            <html>
            <script>
            window.changeColour = function() {
            document.body.style.backgroundColor = location.hash.replace('#', '');
            console.log(document.body.style.backgroundColor)
            document.getElementsByName("text")[0].innerHTML = decodeURI(location.hash.replace('#', ''));
            console.log(decodeURI(location.hash), location.hash)
            console.log(document.getElementsByName("text")[0].innerHTML)
            }
            </script>
            <body>
            <p name="text"></p>
            <div style="height:100vh" onmousemove=changeColour()></div>
            </body>
            </html>
            """


@app.route('/send_proxy_request')
def send_proxy_request():
    return """
            <html>
                <title>What to GET</title>
                <body>
                    <form action="/proxy_get">
                        Enter URL: <input name="url" type="text" />
                        <input name="submit" type="submit">
                    </form>
                </body>
            </html>
"""

def url_validation(url):
    regex = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


@app.route('/proxy_get', methods=['GET', 'POST'])
def proxy_get():
    url = flask.request.args.get('url')

    try:
        domain = url.split('/')[2]
    except:
        flask.redirect('/send_proxy_request')

    with open("domain_white_list.txt", 'r') as domain_white_list:
        for true_domain in domain_white_list:
            true_domain = "".join(true_domain.split())
            if url.startswith(('http://', 'https://')) and validators.url(url) and domain == true_domain:
                result = requests.get(url)
                return "%s" % result.text
        return flask.redirect('/send_proxy_request')

@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Content-Security-Policy'] = "default-src 'self'"
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

if __name__ == '__main__':
    app.run(port=5050)
