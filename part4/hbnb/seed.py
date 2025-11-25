from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

# create app + context
app = create_app()
app.app_context().push()

# drop and create tables
db.drop_all()
db.create_all()

# Step 1: Add Users
user1 = User(
    first_name="Carla",
    last_name="C",
    email="carla.c@example.com",
    password="password123"
)
user1.hash_password("password123")

user2 = User(
    first_name="Dana",
    last_name="L",
    email="dana.l@example.com",
    password="password567"
)
user2.hash_password("password567")

user3 = User(
    first_name="Kat",
    last_name="B",
    email="kat.b@example.com",
    password="password456",
    is_admin=True
)
user3.hash_password("password456")

user4 = User(
    first_name="Mel",
    last_name="H",
    email="mel.h@example.com",
    password="password789",
    is_admin=True
)
user4.hash_password("password789")

db.session.add_all([user1, user2, user3, user4])
db.session.commit()

# Step 2: Add Amenities
wifi = Amenity(
    name="Wifi"
)

swimming_pool = Amenity(
    name="Swimming Pool"
)

sauna = Amenity(
    name="Sauna"
)

cinema_room = Amenity(
    name="Cinema Room"
)

kitchen = Amenity(
    name="Kitchen"
)

db.session.add_all([wifi, swimming_pool, sauna, cinema_room, kitchen])
db.session.commit()

# Step 3: Add Places without Amenities, link them in Step 4
place1 = Place(
    title="Cozy Home",
    description="A cozy apartment with wifi",
    price=200,
    latitude=-34.5667,
    longitude=142.2937,
    user_id=user1.id
)

place2 = Place(
    title="Summer House",
    description="A happy house with swimming pool and cocktails",
    price=400,
    latitude=-40.5667,
    longitude=145.2937,
    user_id=user2.id
)

place3 = Place(
    title="Modern Home",
    description="Modern, well-equipped home with cinema room",
    price=500,
    latitude=-45.5667,
    longitude=146.2937,
    user_id=user3.id
)

place4 = Place(
    title="Weekend Getaway",
    description="Immerse yourself in a relaxing sauna and swimming pool",
    price=600,
    latitude=-48.5667,
    longitude=149.2937,
    user_id=user3.id
)

db.session.add_all([place1, place2, place3, place4])
db.session.commit()

# Step 4: Assign Amenity to Place (follow the place amenity relationships)
place1.amenities=[wifi, kitchen]
place2.amenities=[swimming_pool, kitchen]
place3.amenities=[cinema_room, kitchen]
place4.amenities=[swimming_pool, sauna]

# Step 5: Add Review (Notes: the review layout below is done following how the constructor for review model was set up, so it looks different to the ones above)
review1 = Review(
    rating=5,
    text="Amazing stay! Responsive host",
    place=place1.id,
    user=user2.id
)

review2 = Review(
    rating=3,
    text="Love the swimming pool! A little expensive",
    place=place2.id,
    user=user1.id
)

review3 = Review(
    rating=5,
    text="Beautiful home!",
    place=place3.id,
    user=user1.id
)

review4 = Review(
    rating=4,
    text="Perfect weekend getaway",
    place=place4.id,
    user=user3.id
)

db.session.add_all([review1, review2, review3, review4])
db.session.commit()
