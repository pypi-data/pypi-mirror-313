import os


def set_env_vars(env_vars):
    """Set environment variables for the grpc server"""

    original_env_vars = os.environ.copy()
    for key, value in env_vars.items():
        os.environ[key] = value
    return original_env_vars


def reset_env_vars(env_vars, original_env_vars):
    """Reset environment variables for the grpc server to original state"""

    for key in env_vars.keys():
        del os.environ[key]

    for key, value in original_env_vars.items():
        os.environ[key] = value
