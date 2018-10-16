"""The configuration for the app"""

class Config(object):
    """Parent configuration class."""
    pass

class DevelopmentConfig(Config):
    """Configurations for Development."""
    pass


class TestingConfig(Config):
    """Configurations for Testing"""
    pass

class StagingConfig(Config):
    """Configurations for Staging."""
    pass

class ProductionConfig(Config):
    """Configurations for Production."""
    pass

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}