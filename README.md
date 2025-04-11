# video-streaming-backend-python

start python main.py

install pip install -r requirements.txt

freeze  pip freeze > requirements.txt


CREATE TABLE files (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    org_name VARCHAR(255) NOT NULL,
    path_upload TEXT NOT NULL,
    time_play TEXT NOT NULL,
    location TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE files
ADD COLUMN path_steam TEXT NOT NULL DEFAULT '',
ADD COLUMN path_thumbnail TEXT NOT NULL DEFAULT '';