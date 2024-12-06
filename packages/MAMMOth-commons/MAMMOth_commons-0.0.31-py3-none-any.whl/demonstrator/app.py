from flask import Flask
from flask_bootstrap import Bootstrap
from demonstrator.backend.routes import initialize_routes
from demonstrator.backend.database import Database
import webbrowser


if __name__ == "__main__":
    app = Flask(__name__)
    Bootstrap(app)
    host = "127.0.0.1"
    port = 5050

    import matplotlib

    matplotlib.use("Agg")  # forcefully disable any popups

    with Database() as database:
        initialize_routes(app, database)
        print(f"Running mammoth-commons demonstrator at http://{host}:{port}")
        webbrowser.open(f"http://{host}:{port}", new=0, autoraise=True)
        app.run(
            host=host,
            port=port,
            debug=False,  # debug mode creates database saving issues due to multiple instances running
            load_dotenv=False,
        )
