from expy.core import EnvironmentLoader

env_loader = EnvironmentLoader(".env.local")
print(env_loader.get_variables())
