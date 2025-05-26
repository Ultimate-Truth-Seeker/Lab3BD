from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE VIEW product_index AS
            SELECT
              p.id,
              p.name,
              p.sku,
              p.status::text     AS status,
              p.category::text   AS category,
              p.created_at,
              p.updated_at,
              STRING_AGG(
                t.title || ' (' || pt.relevance || ')',
                ', ' ORDER BY t.title
              ) AS tags
            FROM crud_product p
            JOIN crud_producttag pt ON pt.product_id = p.id
            JOIN crud_tag t         ON t.id          = pt.tag_id
            GROUP BY p.id, p.name, p.sku, p.status, p.category, p.created_at, p.updated_at;
            """,
            reverse_sql="DROP VIEW IF EXISTS product_index;"
        )
    ]