"""The configuration for the app"""
import os

class Config:
    """Parent configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    DB_PATH = os.getenv('DB_DEV')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing"""
    TESTING = True
    DEBUG = True
    DB_PATH = os.getenv('DB_TESTING')

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
