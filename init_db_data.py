from app import create_app
from models import db, FurnitureItem

def initialize_data():
    app = create_app()
    with app.app_context():
        # Check if we already have items
        if FurnitureItem.query.first():
            print("Database already initialized with furniture items.")
            return

        mock_items = [
            FurnitureItem(name="Modern Velvet Sofa", description="A sleek and comfortable velvet sofa, perfect for modern living rooms.", price=899.00, category="Seating"),
            FurnitureItem(name="Glass Coffee Table", description="Minimalist glass top coffee table with wooden legs.", price=250.00, category="Tables"),
            FurnitureItem(name="Abstract Floor Lamp", description="Contemporary floor lamp providing warm ambient lighting.", price=120.00, category="Lighting"),
            FurnitureItem(name="Classic Oak Wardrobe", description="Dark oak wardrobe with classic styling and ample space.", price=1200.00, category="Storage")
        ]

        db.session.bulk_save_objects(mock_items)
        db.session.commit()
        print("Successfully added mock furniture items to the database.")

if __name__ == '__main__':
    initialize_data()
