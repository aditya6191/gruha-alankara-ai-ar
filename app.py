from flask import Flask, render_template
from models import db

def create_app():
    """
    Create and configure the Gruha Alankara Flask application.
    """
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    import logging
    @app.errorhandler(500)
    def internal_error(exception):
        app.logger.error(exception)
        return "500 Internal Server Error", 500

    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.warning(f"404 Not Found: {error}")
        return "404 Resource not found", 404

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/design')
    def design():
        return render_template('design.html')

    from flask import request, jsonify
    import os
    from werkzeug.utils import secure_filename
    from models import User, Design, Booking, FurnitureItem
    
    @app.route('/preview', methods=['GET', 'POST'])
    def preview():
        """
        Handles both the initial preview (GET) and full AI pipeline (POST).
        GET: used when navigating directly or with query params.
        POST: triggered from the design form with optional image upload.
        """
        from ai_services.design_generator import generate_room_design

        if request.method == 'POST':
            room_type = request.form.get('room_type', 'living_room')
            style_preference = request.form.get('style_preference', 'modern')

            # Simulated File Upload handling
            uploaded_image = request.files.get('room_photo')
            original_path = ""
            if uploaded_image and uploaded_image.filename != '':
                filename = secure_filename(uploaded_image.filename)

                # Make uploads dir if not exists
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])

                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                uploaded_image.save(path)
                original_path = path

                # Pre-process image
                from ai_services.image_processor import process_uploaded_image
                processed_path = process_uploaded_image(path)
                if processed_path:
                    original_path = processed_path

            # AI Generation Simulation (always returns a placeholder path for now)
            generated_img = generate_room_design(original_path, style_preference)

            # Auto-provision a dummy user for DB consistency testing
            user = User.query.filter_by(username='testuser').first()
            if not user:
                user = User(username='testuser', email='test@example.com', password_hash='dummy')
                db.session.add(user)
                db.session.commit()

            # Create Design DB record
            new_design = Design(
                user_id=user.id,
                room_type=room_type,
                style_preference=style_preference,
                original_image_path=original_path,
                generated_image_path=generated_img
            )
            db.session.add(new_design)
            db.session.commit()

            return render_template(
                'preview.html',
                design_id=new_design.id,
                room_type=room_type,
                style_preference=style_preference,
                generated_image_path=generated_img,
            )

        # Fallback for direct GET access or when the form submits as GET
        room_type = request.args.get('room_type', 'living_room')
        style_preference = request.args.get('style_preference', 'modern')
        # No image on simple GET; we still show the placeholder design
        generated_img = generate_room_design("", style_preference)

        return render_template(
            'preview.html',
            room_type=room_type,
            style_preference=style_preference,
            generated_image_path=generated_img,
        )

    @app.route('/api/book', methods=['POST'])
    def api_book():
        """
        Books a furniture item for the test user.
        Ensures a user and furniture item exist so bookings don't fail silently.
        """
        data = request.get_json(silent=True) or {}
        item_id = data.get('furniture_item_id')

        # Ensure we always have a user to attach the booking to
        user = User.query.filter_by(username='testuser').first()
        if not user:
            user = User(username='testuser', email='test@example.com', password_hash='dummy')
            db.session.add(user)
            db.session.commit()

        if not item_id:
            return jsonify({"error": "Missing furniture_item_id"}), 400

        try:
            item_id_int = int(item_id)
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid furniture_item_id"}), 400

        # Ensure a furniture item exists for this booking (simple default record)
        item = FurnitureItem.query.get(item_id_int)
        if not item:
            item = FurnitureItem(
                id=item_id_int,
                name="Modern Velvet Sofa",
                description="AI-recommended modern velvet sofa.",
                price=899.0,
                model_3d_path="models/sofa.glb",
                category="sofa",
            )
            db.session.add(item)
            db.session.commit()

        # Record Booking
        new_booking = Booking(
            user_id=user.id,
            furniture_item_id=item.id,
            status='confirmed'
        )
        db.session.add(new_booking)
        db.session.commit()

        # Audio confirmation via Buddy
        from ai_services.assistant import BuddyAgent
        from ai_services.voice import generate_audio
        agent = BuddyAgent()

        agent_resp = agent.respond_to(f"book item {item.id}", 'en')
        audio_path = generate_audio(agent_resp, 'en', f'booking_{new_booking.id}.mp3')

        return jsonify({
            "message": "Booking successful",
            "booking_id": new_booking.id,
            "buddy_says": agent_resp,
            "audio_file": audio_path
        })

    @app.route('/api/chat')
    def api_chat():
        from ai_services.assistant import BuddyAgent
        agent = BuddyAgent()
        response = agent.respond_to("I need to book the velvet sofa.", 'en')
        return {"agent_reply": response}

    @app.route('/api/speak')
    def api_speak():
        from ai_services.voice import generate_audio
        file_path = generate_audio("నమస్కారం, నేను మీ ఇంటీరియర్ డిజైన్ బడ్డీని.", 'te', 'hello_buddy.mp3')
        return {"audio_path": file_path}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
