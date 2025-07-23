from app import create_app
from app.models import user
from dotenv import load_dotenv
load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=True)
