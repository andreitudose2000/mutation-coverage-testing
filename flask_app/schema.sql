DROP TABLE IF EXISTS test;
DROP TABLE IF EXISTS heat;
DROP TABLE IF EXISTS user_info;
DROP TABLE IF EXISTS user_weight;
DROP TABLE IF EXISTS user_sitting;

CREATE TABLE test (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  some_text TEXT UNIQUE NOT NULL,
  another_text TEXT NOT NULL,
  a_date DATETIME
);

CREATE TABLE heat (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  head_rest INTEGER NOT NULL,
  back_rest INTEGER NOT NULL,
  arm_rest INTEGER NOT NULL,
  bum_rest INTEGER NOT NULL,
  updated_on DATETIME NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE TABLE user_info (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_height NUMERIC NOT NULL,
  chair_height NUMERIC NOT NULL,
  desk_height NUMERIC NOT NULL,
  updated_on DATETIME NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE TABLE user_weight (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  mass NUMERIC NOT NULL,
  updated_on DATETIME NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE TABLE user_sitting (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  is_sitting INTEGER NOT NULL,
  updated_on DATETIME NOT NULL DEFAULT (datetime('now','localtime'))
)