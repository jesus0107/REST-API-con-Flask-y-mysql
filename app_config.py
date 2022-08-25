class DevelopmentConfig:
    DEBUG = True
    MYSQL_HOST = "localhost"
    MYSQL_USER = "jesus"
    MYSQL_PASSWORD = "P@ssword1"
    MYSQL_DB = "api_flask"


settings = {
    'development': DevelopmentConfig
}