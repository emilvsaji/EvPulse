"""
Simple server startup script without auto-reload
"""
from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("Starting EVPulse API server...")
    print("Server will be available at http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    app.run(debug=True, port=5000, host='0.0.0.0', use_reloader=False)
