CREATE role mps_hp login password 'mps_hp_db';
CREATE database mps_hp;
GRANT ALL PRIVILEGES ON database mps_hp TO mps_hp;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to mps_hp;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to mps_hp;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public to mps_hp;