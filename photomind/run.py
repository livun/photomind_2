from photomind import create_app

from flask import Flask
from flask_sslify import SSLify

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'XYZ')

sslify = SSLify(app)

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

    app.run(ssl_context=('cert.pem', 'key.pem'))
