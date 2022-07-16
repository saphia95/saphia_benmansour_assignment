DROP TABLE IF EXISTS pages;
DROP TABLE IF EXISTS videos;
DROP TABLE IF EXISTS video_insight;

CREATE TABLE pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL
);

CREATE TABLE videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    page_id INTEGER NOT NULL,
    FOREIGN KEY(page_id) REFERENCES pages(id) ON DELETE CASCADE
);

CREATE TABLE video_insight (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    video_id INTEGER NOT NULL,
    likes INTEGER NOT NULL,
    views INTEGER NOT NULL,
    FOREIGN KEY(video_id) REFERENCES videos(id) ON DELETE CASCADE
);
