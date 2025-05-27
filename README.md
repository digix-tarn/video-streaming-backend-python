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

key push 
----- VAPID Key Pair -----
Front Public Key:
 BEOy4QMOREHqq1wXxPTVBslzh0A-fm7O3E6aTB1NgeJthcW7VXwlfWidgH29p3pAn1nogkqg2Nbafw2IS2Lvfyo

Back Private Key (PEM):
 -----BEGIN PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQg4ALrV0LZoqni047n
bsOanGJkeea5fnuHD2rUVkOcm+KhRANCAARDsuEDDkRB6qtcF8T01QbJc4dAPn5u
ztxOmkwdTYHibYXFu1V8JX1onYB9vad6QJ9Z6IJKoNjW2n8NiEti738q
-----END PRIVATE KEY-----