import os
from typing import List, Union
import yaml

class ApiKeyManager:
    """Manages API keys by setting them as environment variables and providing get/set methods."""
    
    def __init__(self, key_file_path: str, service_names: List[str]):
        """
        Initialize the ApiKeyManager by loading keys from a file and setting them as environment variables.
        
        Args:
            key_file_path (str): Path to the YAML file containing the API keys.
            service_names (List[str]): List of service names to set as environment variables.
        
        Raises:
            Exception: If there is an error loading the key file.
        """
        try:
            with open(key_file_path, encoding='utf-8') as file:
                self.keys = yaml.load(file, Loader=yaml.SafeLoader)

            for service_name in service_names:
                if service_name in self.keys:
                    os.environ[service_name] = self.keys[service_name]
                    print(f"{service_name}: {os.environ[service_name]}")
                else:
                    print(f"No API key found for {service_name}")
                
        except Exception as e:
            print(f"Error loading the key file: {e}")
            self.keys = {}

    def __getitem__(self, service_name: str) -> Union[str, None]:
        """
        Retrieve the API key for the given service name.
        
        Args:
            service_name (str): Name of the service to retrieve the API key for.
        
        Returns:
            str: The API key for the given service name.
            
        Raises:
            KeyError: If no API key is found for the given service name.
        """
        if service_name in self.keys:
            return self.keys[service_name]
        else:
            raise KeyError(f"No API key found for {service_name}")

    def __setitem__(self, service_name: str, key: str) -> None:
        """
        Set the API key for the given service name.
        
        Args:
            service_name (str): Name of the service to set the API key for.
            key (str): The API key to set for the given service name.
        """
        self.keys[service_name] = key
        os.environ[service_name] = key  # Automatically update the os.environ with the new key value.

