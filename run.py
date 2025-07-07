# is-it-in-yet/run.py

from app import create_app

# Call the application factory to create the Flask app instance.
app = create_app()

if __name__ == '__main__':
    # The entry point for running the Flask development server.
    # debug=True will automatically reload the server when you make code changes
    # and show detailed error pages. This should be False in production.
    app.run(debug=True)