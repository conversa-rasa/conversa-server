from os.path import exists
import yaml

# Database import
from database.Database import Database


class Setup:

    database = None
    installation_path = None

    def __init__(self):
        current_setup = self.read_current_setup()

        if current_setup:
            self.installation_path = current_setup["installation_path"]
            self.database = Database(self.installation_path+"/conversa.db")

    def check_installation_path(self, path):

        config_exists = exists(path+'/config.yml')
        #endpoints_exists = exists(path+'/endpoints.yml')
        data_exists = exists(path+'/data')
        domain_exists = exists(path+'/domain.yml')

        if config_exists and data_exists and domain_exists:
            self.installation_path = path
            return True
        else:
            return False

    def install_conversa(self, password):

        # If installation file is valid
        if self.installation_path and exists(self.installation_path) and len(self.installation_path) > 0:

            # Create DB
            self.database = Database(self.installation_path+"/conversa.db")
            create_db_result = self.database.init_database(password)

            if not create_db_result:
                print("Failed to create DB")
                return False

            # Try to read current endpoints.yml config
            current_content = self.read_endpoints()

            # Try to write Conversa's endpoints.yml config
            try:
                with open(self.installation_path+'/endpoints.yml', 'w') as file:
                    try:
                        # Restore previous info
                        if current_content:
                            try:
                                yaml.dump(current_content, file)
                            except:
                                print("Error writing old endpoints.yml config")

                        # Write endpoints.yml config
                        db_config = {'tracker_store': {
                            'type': 'SQL', 'db': './conversa.db'}}
                        yaml.dump(db_config, file, sort_keys=False)

                        # Write config
                        with open('config.yml', 'w') as file:
                            try:
                                yaml.dump(
                                    {'installation_path': self.installation_path}, file)
                            except:
                                print("Error")

                        return True
                    except:
                        print("Error writing endpoints.yml config")
                        return False

            except:
                print("Error creating file")
                return False

    def read_endpoints(self):
        try:
            with open(self.installation_path+'/endpoints.yml') as file:
                try:
                    current_config = yaml.safe_load(file)
                    return current_config
                except yaml.YAMLError as exc:
                    print(exc)
                    return None
        except:
            print("No file")
            return None

    def read_current_setup(self):
        try:
            with open('config.yml') as file:
                try:
                    current_config = yaml.safe_load(file)
                    return current_config
                except yaml.YAMLError as exc:
                    print(exc)
                    return None
        except:
            print("No file")
            return None
    
    def is_first_run(self):
        try:
            if exists("./config.yml"):
                return False
            else:
                return True
        except:
            print("Error")
