from app import create_app
from waitress import serve
import logging
import os

if __name__ == "__main__":
    app = create_app()
    
    # Configure production logging
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    logging.basicConfig(
        filename='logs/gruha_alankara.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    
    app.logger.info('Gruha Alankara startup via Waitress WSGI')
    
    print("Starting production server on http://0.0.0.0:8080")
    serve(app, host='0.0.0.0', port=8080)
