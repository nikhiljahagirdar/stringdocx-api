-- Drop and create subscription table
DROP TABLE IF EXISTS subscription CASCADE;
CREATE TABLE IF NOT EXISTS subscription (
    id SERIAL PRIMARY KEY,
    plan_name VARCHAR(255) NOT NULL DEFAULT '',
    plan_details TEXT,
    stripe_monthly_price_id VARCHAR(255),
    stripe_yearly_price_id VARCHAR(255),
    monthly_price DECIMAL(10, 2),
    yearly_price DECIMAL(10, 2),
    createdOn TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updatedOn TIMESTAMP WITH TIME ZONE NULL
);
-- Drop and create company table
DROP TABLE IF EXISTS company CASCADE;
CREATE TABLE IF NOT EXISTS company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NULL,
    city VARCHAR(255) NULL,
    state VARCHAR(255) NULL,
    zip_code VARCHAR(20) NULL,
    country VARCHAR(255) NULL,
    phone_number VARCHAR(20) NULL,
    email VARCHAR(255) NULL,
    company_website VARCHAR(255) NULL,
    logo VARCHAR(255) NULL,
    subscription_id INTEGER NULL,
    createdOn TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updatedOn TIMESTAMP WITH TIME ZONE NULL,
    CONSTRAINT fk_subscription FOREIGN KEY (subscription_id) REFERENCES subscription(id)
);
-- Drop and create user table
DROP TABLE IF EXISTS "user" CASCADE;
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(20) NULL,
    profile_picture VARCHAR(255) NULL,
    password_hash VARCHAR(255),
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    subscription_id INTEGER,
    companyName  Varchar(255) NULL,
    doc_count INTEGER DEFAULT 0, -- Add doc_count column with a default value
    createdOn TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updatedOn TIMESTAMP WITH TIME ZONE NULL,
    CONSTRAINT fk_subscription FOREIGN KEY (subscription_id) REFERENCES subscription(id)
);

DROP TABLE IF EXISTS "usercompany" CASCADE;
CREATE TABLE IF NOT EXISTS "usercompany" (
   id SERIAL PRIMARY KEY,
   user_id INTEGER NOT NULL,
   company_id INTEGER NOT NULL,
   CONSTRAINT fk_user_company FOREIGN KEY (user_id) REFERENCES "user"(id),
   CONSTRAINT fk_company_user FOREIGN KEY (company_id) REFERENCES company(id)
 );

DROP TABLE IF EXISTS pdfMasterConfig CASCADE;
CREATE TABLE IF NOT EXISTS pdfMasterConfig (
    id SERIAL PRIMARY KEY,
	configType VARCHAR(255) NOT NULL,
    configName VARCHAR(255) NOT NULL,
    configValue VARCHAR(255) NOT NULL,
    configDescription TEXT,
    isChild BOOLEAN DEFAULT FALSE,
    createdOn TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updatedOn TIMESTAMP WITH TIME ZONE
);

-- Drop and create pdffile table
DROP TABLE IF EXISTS pdffile CASCADE;
CREATE TABLE IF NOT EXISTS pdffile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    filename VARCHAR(255) NOT NULL,
    path VARCHAR(255) NOT NULL,
    size BIGINT NOT NULL,
    original_filename VARCHAR(255)  NOT NULL,
    processed_filename VARCHAR(255) NULL,
    processed_path VARCHAR(255) NULL,
    processing_start_time TIMESTAMP WITH TIME ZONE,
    processing_end_time TIMESTAMP WITH TIME ZONE,
    status varchar(50) DEFAULT FALSE,
    status_message VARCHAR(255) NULL,
    createdOn TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updatedOn TIMESTAMP WITH TIME ZONE NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES "user"(id)
);

DROP TABLE IF EXISTS pdfUserConfig CASCADE;

CREATE TABLE IF NOT EXISTS pdfUserConfig (
    id SERIAL PRIMARY KEY,
    config_id INTEGER REFERENCES pdfMasterConfig(id),
    user_id INTEGER REFERENCES "user"(id),
    doc_id INTEGER REFERENCES pdffile(id),
    createdOn TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updatedOn TIMESTAMP WITH TIME ZONE
);

-- Drop and create pdfqc table
DROP TABLE IF EXISTS pdfqc CASCADE;
CREATE TABLE IF NOT EXISTS pdfqc (
    id SERIAL PRIMARY KEY,
    doc_id INTEGER,
    is_security BOOLEAN DEFAULT FALSE,
    is_encrypted BOOLEAN DEFAULT FALSE,
    has_bookmarks BOOLEAN DEFAULT FALSE,
    has_tags BOOLEAN DEFAULT FALSE,
    has_media BOOLEAN DEFAULT FALSE,
    has_images BOOLEAN DEFAULT FALSE,
    has_fonts BOOLEAN DEFAULT FALSE,
    has_tables BOOLEAN DEFAULT FALSE,
    has_links BOOLEAN DEFAULT FALSE,
    has_annotations BOOLEAN DEFAULT FALSE,
    has_form_fields BOOLEAN DEFAULT FALSE,
    createdOn TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updatedOn TIMESTAMP WITH TIME ZONE NULL,
    CONSTRAINT fk_pdf_file FOREIGN KEY (doc_id) REFERENCES pdffile(id)
);

-- Drop and create bookmarkitem table
DROP TABLE IF EXISTS bookmarkitem CASCADE;
CREATE TABLE IF NOT EXISTS bookmarkitem (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    page_number INTEGER NOT NULL,
    level INTEGER NOT NULL,
    pdf_file_id INTEGER,
    createdOn TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updatedOn TIMESTAMP WITH TIME ZONE NULL,
    CONSTRAINT fk_pdf_file_bookmark FOREIGN KEY (pdf_file_id) REFERENCES pdffile(id)
);



-- Drop and create spellcheckresult table
DROP TABLE IF EXISTS spellcheckresult CASCADE;
CREATE TABLE IF NOT EXISTS spellcheckresult (
    id SERIAL PRIMARY KEY,
    page_number INTEGER NOT NULL,
    line_number INTEGER NOT NULL,
    word VARCHAR(255) NOT NULL,
    suggestions JSONB,
    message VARCHAR(255) NOT NULL,
    pdf_file_id INTEGER,
    createdOn TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updatedOn TIMESTAMP WITH TIME ZONE NULL,
    CONSTRAINT fk_pdf_file_spellcheck FOREIGN KEY (pdf_file_id) REFERENCES pdffile(id)
);


DROP TABLE IF EXISTS sitestatus CASCADE;
CREATE TABLE IF NOT EXISTS sitestatus (
    id SERIAL PRIMARY KEY,
    status_type VARCHAR(100) NOT NULL,
    status_message VARCHAR(255) NOT NULL,
    pdf_file_id INTEGER,
    createdOn TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updatedOn TIMESTAMP WITH TIME ZONE NULL ,
    CONSTRAINT fk_pdf_file_spellcheck FOREIGN KEY (pdf_file_id) REFERENCES pdffile(id)
);

Drop and create UserSubscription table
DROP TABLE IF EXISTS "usersubscription" CASCADE;
CREATE TABLE IF NOT EXISTS "usersubscription" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    subscription_id INTEGER NOT NULL,
    stripe_customer_id VARCHAR(255) NOT NULL,
    stripe_subscription_id VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL, -- e.g., active, canceled, past_due
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE,
    createdOn TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updatedOn TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_user_subscription FOREIGN KEY (user_id) REFERENCES "user"(id),
    CONSTRAINT fk_subscription_user FOREIGN KEY (subscription_id) REFERENCES subscription(id)
);

 Drop and create UserPayment table
DROP TABLE IF EXISTS "userpayment" CASCADE;
CREATE TABLE IF NOT EXISTS "userpayment" (
    id SERIAL PRIMARY KEY,
    user_subscription_id INTEGER NOT NULL,
    stripe_payment_id VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    status VARCHAR(50) NOT NULL, -- e.g., succeeded, pending, failed
    payment_date TIMESTAMP WITH TIME ZONE NOT NULL,
    createdOn TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updatedOn TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_user_subscription_payment FOREIGN KEY (user_subscription_id) REFERENCES "usersubscription"(id)
);

-- Insert some subscriptions

INSERT INTO subscription (plan_name, plan_details, stripe_monthly_price_id, stripe_yearly_price_id, monthly_price, yearly_price) VALUES
('Basic', 'Basic plan details', 'price_123', 'price_456', 9.99, 99.99),
('Premium', 'Premium plan details', 'price_789', 'price_101', 19.99, 199.99),
('Enterprise', 'Enterprise plan details', 'price_112', 'price_131', 29.99, 299.99);



