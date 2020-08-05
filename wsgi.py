import os
from books import create_app
from config import *

env = os.getenv('ENV')

# Choose the environment config
if env == 'prod':
    config = Config
elif env == 'test':
    config = TestingConfig
else:
    config = DevelopmentConfig

# Creating the app with chosen configuration
app = create_app(config)
