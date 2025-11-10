CREATE TABLE IF NOT EXISTS Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT CHECK(rating BETWEEN 1 AND 5),
    user_id CHAR(36),
    place_id CHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_place UNIQUE (user_id, place_id),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (place_id) REFERENCES Place(id)
);