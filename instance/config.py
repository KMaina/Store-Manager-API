"""The configuration for the app"""
import os

class Config:
    """Parent configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing"""
    TESTING = True
    DEBUG = True
    DATABASE_URL = os.getenv('DB_TESTING')

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    TESTING = False
    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
