import os

class Settings:
    DB_HOST = os.getenv("DB_HOST", "postgres")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME", "antifraud_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    
    RANDOM_SECRET = os.getenv("RANDOM_SECRET", "your-secret-key-min-128-chars-your-secret-key-min-128-chars")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRE_HOURS = 1
    
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
    ADMIN_FULLNAME = os.getenv("ADMIN_FULLNAME", "Admin User")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin123456")
    
    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()