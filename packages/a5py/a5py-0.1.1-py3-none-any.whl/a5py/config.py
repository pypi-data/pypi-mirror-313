import configparser
import os

config_path = os.path.join(os.environ["HOME"],".a5py.ini")

def read_config(file_path : str = config_path) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(file_path)

    # # Access sections and options
    # for section in config.sections():
    #     print(f"Section: {section}")
    #     for option in config.options(section):
    #         value = config.get(section, option)
    #         print(f"  {option} = {value}")

    return config

config = read_config()

# config path
config_path = os.path.join(os.environ["HOME"],".a5py.ini")

def create_ini_from_dict(config_dict, config_path = config_path):
    """
    Create an .ini configuration file from a dictionary.
    
    :param config_dict: Dictionary containing configuration data.
                        Format: {section: {key: value, ...}, ...}
    :param file_path: Path to the .ini file to be created.
    """
    config_in = configparser.ConfigParser()
    
    # Populate ConfigParser with sections and keys
    for section, options in config_dict.items():
        config_in[section] = options
    
    # Write the configuration to a file
    if os.path.exists(config_path):
        user_input = input("Configuration file already exists. Overwrite? y/n:").strip().lower()
        if user_input in ['y', 'yes']:
            with open(config_path, 'w') as configfile:
                config_in.write(configfile)
            print("Configuration file '%s' created successfully. Edit the file to modify the default configuration" % config_path)
        else:
            print("Configuration file not written")
    else:
        with open(config_path, 'w') as configfile:
            config_in.write(configfile)

# Default config
config_data = {
    "db_params": {
        "dbname": "a5",
        "username": "username",
        "password": "password",
        "host": "localhost",
        "port": 5432
    },
    "test_db_params": {
        "dbname": "a5_test",
        "username": "username",
        "password": "password",
        "host": "localhost",
        "port": 5432
    },
    "raster": {
        "path": os.path.join(os.environ["HOME"],"a5/data/raster"),
        "bbox.ulx": -70, 
        "bbox.uly": -10,
        "bbox.lrx":-40, 
        "bbox.lry": -40
    }
}

def run():
    create_ini_from_dict(config_data, config_path)
