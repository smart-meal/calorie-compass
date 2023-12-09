from flask_cors import CORS
from api import create_app

app = create_app()
CORS(app)  # Enable CORS

if __name__ == '__main__':
    app.run(debug=True)
