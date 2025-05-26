BEGIN;
--
-- Create model Product
--
CREATE TABLE "crud_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "sku" varchar(30) NOT NULL UNIQUE, "status" varchar NOT NULL, "category" varchar NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
--
-- Create model Tag
--
CREATE TABLE "crud_tag" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(50) NOT NULL UNIQUE, "description" text NOT NULL);
--
-- Create model ProductTag
--
CREATE TABLE "crud_producttag" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "relevance" integer unsigned NOT NULL CHECK ("relevance" >= 0), "product_id" bigint NOT NULL REFERENCES "crud_product" ("id") DEFERRABLE INITIALLY DEFERRED, "tag_id" bigint NOT NULL REFERENCES "crud_tag" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field tags to product
--
CREATE TABLE "new__crud_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "sku" varchar(30) NOT NULL UNIQUE, "status" varchar NOT NULL, "category" varchar NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "new__crud_product" ("id", "name", "sku", "status", "category", "created_at", "updated_at") SELECT "id", "name", "sku", "status", "category", "created_at", "updated_at" FROM "crud_product";
DROP TABLE "crud_product";
ALTER TABLE "new__crud_product" RENAME TO "crud_product";
CREATE INDEX "crud_producttag_product_id_5a6303c1" ON "crud_producttag" ("product_id");
CREATE INDEX "crud_producttag_tag_id_f3bc52d4" ON "crud_producttag" ("tag_id");
--
-- Create constraint unique_product_tag on model producttag
--
CREATE TABLE "new__crud_producttag" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "relevance" integer unsigned NOT NULL CHECK ("relevance" >= 0), "product_id" bigint NOT NULL REFERENCES "crud_product" ("id") DEFERRABLE INITIALLY DEFERRED, "tag_id" bigint NOT NULL REFERENCES "crud_tag" ("id") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "unique_product_tag" UNIQUE ("product_id", "tag_id"));
INSERT INTO "new__crud_producttag" ("id", "relevance", "product_id", "tag_id") SELECT "id", "relevance", "product_id", "tag_id" FROM "crud_producttag";
DROP TABLE "crud_producttag";
ALTER TABLE "new__crud_producttag" RENAME TO "crud_producttag";
CREATE INDEX "crud_producttag_product_id_5a6303c1" ON "crud_producttag" ("product_id");
CREATE INDEX "crud_producttag_tag_id_f3bc52d4" ON "crud_producttag" ("tag_id");
--
-- Create constraint check_relevance_range on model producttag
--
CREATE TABLE "new__crud_producttag" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "relevance" integer unsigned NOT NULL CHECK ("relevance" >= 0), "product_id" bigint NOT NULL REFERENCES "crud_product" ("id") DEFERRABLE INITIALLY DEFERRED, "tag_id" bigint NOT NULL REFERENCES "crud_tag" ("id") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "unique_product_tag" UNIQUE ("product_id", "tag_id"), CONSTRAINT "check_relevance_range" CHECK (("relevance" >= 1 AND "relevance" <= 10)));
INSERT INTO "new__crud_producttag" ("id", "relevance", "product_id", "tag_id") SELECT "id", "relevance", "product_id", "tag_id" FROM "crud_producttag";
DROP TABLE "crud_producttag";
ALTER TABLE "new__crud_producttag" RENAME TO "crud_producttag";
CREATE INDEX "crud_producttag_product_id_5a6303c1" ON "crud_producttag" ("product_id");
CREATE INDEX "crud_producttag_tag_id_f3bc52d4" ON "crud_producttag" ("tag_id");
--
-- Create constraint unique_name_category on model product
--
CREATE TABLE "new__crud_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "sku" varchar(30) NOT NULL UNIQUE, "status" varchar NOT NULL, "category" varchar NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, CONSTRAINT "unique_name_category" UNIQUE ("name", "category"));
INSERT INTO "new__crud_product" ("id", "name", "sku", "status", "category", "created_at", "updated_at") SELECT "id", "name", "sku", "status", "category", "created_at", "updated_at" FROM "crud_product";
DROP TABLE "crud_product";
ALTER TABLE "new__crud_product" RENAME TO "crud_product";
COMMIT;
