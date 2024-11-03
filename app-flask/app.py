import os
from project import (
    create_app,
)  # Import the create_app function from your project module

app = create_app()  # Call the factory function to create your app

if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_RUN_PORT", 5000))
    app.run(host=host, port=port, debug=True)  # Run the app
