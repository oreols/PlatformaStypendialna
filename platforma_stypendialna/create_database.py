import MySQLdb
from django.conf import settings

def create_database():
    db_connection = MySQLdb.connect(
        host=settings.DATABASES['default']['HOST'],
        user=settings.DATABASES['default']['USER'],
        passwd=settings.DATABASES['default']['PASSWORD']
    )
    cursor = db_connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.DATABASES['default']['NAME']}")
    cursor.close()
    db_connection.close()

if __name__ == "__main__":
    create_database()