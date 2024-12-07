from enum import Enum

class Environment(str, Enum):
    development = 'development'
    test = 'test'
    production = 'production'