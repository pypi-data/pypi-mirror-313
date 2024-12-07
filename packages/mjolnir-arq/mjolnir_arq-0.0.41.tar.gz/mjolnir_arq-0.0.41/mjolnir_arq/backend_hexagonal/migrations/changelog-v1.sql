--RUN 
--NAME=Marlon Andres Leon Leon
--DESCRIPTION=Crea las tablas iniciales
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE
    language (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
        name VARCHAR(100) NOT NULL,
        code VARCHAR(10) UNIQUE NOT NULL,
        native_name VARCHAR(100),
        state BOOLEAN NOT NULL DEFAULT TRUE,
        created_date TIMESTAMP NOT NULL DEFAULT NOW (),
        updated_date TIMESTAMP NOT NULL DEFAULT NOW ()
    );


CREATE TABLE
    translation (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
        key VARCHAR(255) NOT NULL,
        language_code VARCHAR(10) NOT NULL REFERENCES language (code),
        translation TEXT NOT NULL,
        context VARCHAR(255),
        state BOOLEAN NOT NULL DEFAULT TRUE,
        created_date TIMESTAMP NOT NULL DEFAULT NOW (),
        updated_date TIMESTAMP NOT NULL DEFAULT NOW (),
        UNIQUE (key, language_code, context)
    );

--FIN RUN

--ROLLBACK
DROP TABLE IF EXISTS "translation";
DROP TABLE IF EXISTS "language";


--FIN ROLLBACK