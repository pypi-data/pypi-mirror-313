import os
from dotenv import load_dotenv, find_dotenv


class EnvManager:
    @classmethod
    def _set_env_vars(cls):
        """
        Internal method to load environment variables based on the environment type.
        """
        is_dev_env = os.getenv("FLASK_DEV_ENV")
        env_file = ".env.dev" if is_dev_env else ".env.prod"

        env_file_path = find_dotenv(env_file, usecwd=True)
        if env_file_path:
            load_dotenv(env_file_path, override=False)
        else:
            raise FileNotFoundError(
                f"Environment file not found: {env_file}. Searched in the project root."
            )

    @classmethod
    def _validate_env_vars(cls):
        """
        Internal method to validate that all required environment variables are set.
        """
        example_file = find_dotenv(".env.example", usecwd=True)
        if not example_file:
            raise FileNotFoundError(
                "The '.env.example' file is missing in the project root. "
                "This file is required to validate environment variables."
            )

        required_keys = []
        with open(example_file, "r") as file:
            for line in file:
                # Ignoring comments and blank lines
                line = line.strip()
                if line and not line.startswith("#"):
                    key = line.split("=")[0].strip()
                    required_keys.append(key)

        missing_keys = [key for key in required_keys if not os.getenv(key)]
        if missing_keys:
            raise ValueError(
                f"The following required environment variables are missing: {', '.join(missing_keys)}"
            )

    @classmethod
    def initialize(cls):
        """
        Public class method to initialize and validate environment variables.
        Call this method at the start of your project.
        """
        try:
            cls._set_env_vars()
            cls._validate_env_vars()
        except Exception as e:
            raise Exception(f"Error initializing environment variables: {str(e)}")
