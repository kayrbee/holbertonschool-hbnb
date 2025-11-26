INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin) VALUES
('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin','HBnB', 'admin@hbnb.io','$2a$12$Ynth2LxJjEaO4Uj/yYNnuOpOSAuZbzHcPmdbQG6b81vJ3N4jJtPyG',TRUE),
('36c9050e-ddd3-4c3b-9731-9f487208bbc2','Carla','C','carla.c@example.com','$2a$12$Ynth2LxJjEaO4Uj/yYNnuOpOSAuZbzHcPmdbQG6b81vJ3N4jJtPyG',FALSE),
('36c9050e-ddd3-4c3b-9731-9f487208bbc3','Dana','L','dana.l@example.com','$2a$12$Ynth2LxJjEaO4Uj/yYNnuOpOSAuZbzHcPmdbQG6b81vJ3N4jJtPyG',FALSE),
('36c9050e-ddd3-4c3b-9731-9f487208bbc4','Kat','B','kat.b@example.com','$2a$12$Ynth2LxJjEaO4Uj/yYNnuOpOSAuZbzHcPmdbQG6b81vJ3N4jJtPyG',FALSE),
('36c9050e-ddd3-4c3b-9731-9f487208bbc5','Mel','H','mel.h@example.com','$2a$12$Ynth2LxJjEaO4Uj/yYNnuOpOSAuZbzHcPmdbQG6b81vJ3N4jJtPyG',FALSE);

INSERT OR IGNORE INTO amenities (id, name) VALUES
('36c9050e-ddd3-4c3b-9731-9f487208bba1', 'Wifi'),
('36c9050e-ddd3-4c3b-9731-9f487208bba2', 'Swimming Pool'),
('36c9050e-ddd3-4c3b-9731-9f487208bba3', 'Sauna'),
('36c9050e-ddd3-4c3b-9731-9f487208bba4', 'Cinema Room'),
('36c9050e-ddd3-4c3b-9731-9f487208bba5', 'Kitchen');

INSERT OR IGNORE INTO places (id, title, image_url, description, price, latitude, longitude, user_id)  VALUES
('36c9050e-ddd3-4c3b-9731-9f487208bbf1',
 'Cozy Home',
 'images/cozy-home.jpg',
 'A cozy apartment with wifi',
 9,
 -34.5667,
 142.2937,
 '36c9050e-ddd3-4c3b-9731-9f487208bbc2'),
('36c9050e-ddd3-4c3b-9731-9f487208bbf2',
 'Summer House',
 'images/summer-house.jpg',
 'A happy house with swimming pool and cocktails',
 49,
 -40.5667,
 145.2937,
 '36c9050e-ddd3-4c3b-9731-9f487208bbc3'),
('36c9050e-ddd3-4c3b-9731-9f487208bbf3',
 'Modern Home',
 'images/modern-home.jpg',
 'Modern, well-equipped home with cinema room',
 99,
 -45.5667,
 146.2937,
 '36c9050e-ddd3-4c3b-9731-9f487208bbc4'),
('36c9050e-ddd3-4c3b-9731-9f487208bbf4',
 'Weekend Getaway',
 'images/weekend-getaway.jpg',
 'Immerse yourself in a relaxing sauna and swimming pool',
 600,
 -48.5667,
 149.2937,
 '36c9050e-ddd3-4c3b-9731-9f487208bbc5');

INSERT OR IGNORE INTO place_amenity (place_id, amenity_id) VALUES
('36c9050e-ddd3-4c3b-9731-9f487208bbf1', '36c9050e-ddd3-4c3b-9731-9f487208bba1'),
('36c9050e-ddd3-4c3b-9731-9f487208bbf1', '36c9050e-ddd3-4c3b-9731-9f487208bba5'),
('36c9050e-ddd3-4c3b-9731-9f487208bbf2', '36c9050e-ddd3-4c3b-9731-9f487208bba2'),
('36c9050e-ddd3-4c3b-9731-9f487208bbf2', '36c9050e-ddd3-4c3b-9731-9f487208bba5'),
('36c9050e-ddd3-4c3b-9731-9f487208bbf3', '36c9050e-ddd3-4c3b-9731-9f487208bba4'),
('36c9050e-ddd3-4c3b-9731-9f487208bbf3', '36c9050e-ddd3-4c3b-9731-9f487208bba5'),
('36c9050e-ddd3-4c3b-9731-9f487208bbf4', '36c9050e-ddd3-4c3b-9731-9f487208bba2'),
('36c9050e-ddd3-4c3b-9731-9f487208bbf4', '36c9050e-ddd3-4c3b-9731-9f487208bba3');

INSERT OR IGNORE INTO reviews (id, text, rating, place_id, user_id) VALUES
('36c9050e-ddd3-4c3b-9731-9f487208bbe1', "Amazing stay! Responsive host", 5, '36c9050e-ddd3-4c3b-9731-9f487208bbf1', '36c9050e-ddd3-4c3b-9731-9f487208bbc3'),
('36c9050e-ddd3-4c3b-9731-9f487208bbe2', "Love the swimming pool! A little expensive", 3, '36c9050e-ddd3-4c3b-9731-9f487208bbf2', '36c9050e-ddd3-4c3b-9731-9f487208bbc2'),
('36c9050e-ddd3-4c3b-9731-9f487208bbe3', "Beautiful home!", 5, '36c9050e-ddd3-4c3b-9731-9f487208bbf3', '36c9050e-ddd3-4c3b-9731-9f487208bbc2'),
('36c9050e-ddd3-4c3b-9731-9f487208bbe4', "Perfect weekend getaway", 4, '36c9050e-ddd3-4c3b-9731-9f487208bbf4', '36c9050e-ddd3-4c3b-9731-9f487208bbc4');
