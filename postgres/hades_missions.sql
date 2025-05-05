-- Set the database.
\c postgres

-- Change the password for the postgres user.
ALTER USER postgres PASSWORD 'postgres';

-- Create a new superuser with a specific password.
CREATE USER hades WITH CREATEDB SUPERUSER PASSWORD 'hades';

-- Create a new database.
CREATE DATABASE hades_missions;

-- Grant all privileges on the newly created database to the new user.
GRANT ALL PRIVILEGES ON DATABASE hades_missions TO hades;

-- Set the database.
\c hades_missions

-- Enable the pgcrypto extension on the hades_missions database.
create extension if not exists pgcrypto;

-- Create a table.
create table users (
  email    text primary key,
  password text not null
);

-- Insert a record.
insert into users values (
  'victor.fernandez19.mil@army.mil',
  crypt('MySuperLongPassphrase2024!', gen_salt('bf'))
);