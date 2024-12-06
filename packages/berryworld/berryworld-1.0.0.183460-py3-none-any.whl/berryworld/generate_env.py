from .handy_mix import HandyMix
import yaml


class EnvVariables:
    """ Generate the environmental variables to be used by kubernetes """

    @staticmethod
    def generate_env_file(yaml_path='./environments/prd1/step01.yaml', env_path='./.env'):
        """ Save the data from the yaml file into a .env file to be used by decouple
        :param yaml_path: Path to Yaml file
        :param env_path: Path to destination file
        """
        # Read lines from .env file
        f = open(yaml_path, 'r')
        text_content = f.readlines()
        f.close()

        # Find starting index for env variables
        text_content = [str(elem).strip() for elem in text_content]
        first_ind = text_content.index('env:') + 1

        # Find last index for env variables
        boolean_list = ['value' in str(elem) for elem in text_content[::-1]]
        last_ind = len(text_content) - boolean_list.index(True)

        # Get the final variables set
        final_set = text_content[first_ind:last_ind]

        # Prepare .env file structure
        values_pairs = []
        for index in range(int(len(final_set) / 2)):
            value_pair_str = str(final_set[2 * index]).replace(" ", "").replace("-name:", "")
            value_pair_str += "="
            value_pair_str += str(final_set[2 * index + 1]).replace(" ", "").replace("value:", "").replace('"', "")

            values_pairs.append(value_pair_str)

        # Write value pairs to .env file
        f = open(env_path, "w")
        f.write('\n'.join(values_pairs))
        f.close()

    @staticmethod
    def generate_yaml_file(yaml_path='./environments/prd1/step01.yaml', env_path='./.env'):
        """ Save the data from the .env file into a yaml file to be used by kubernetes
        :param yaml_path: Path to Yaml file
        :param env_path: Path to destination file
        """
        # Read lines from yaml file
        f = open(yaml_path, 'r')
        yaml_content = f.readlines()
        f.close()

        # Read yaml content
        yaml_content_mod = [str(elem).strip() for elem in yaml_content]
        break_ind = yaml_content_mod.index('containers:')

        # Find the index where the env variables are to be inserted
        insert_ind = 0
        leading_spaces = len(yaml_content[break_ind]) - len(yaml_content[break_ind].lstrip())
        for ind in range(break_ind + 2, len(yaml_content)):
            if len(yaml_content[ind]) - len(yaml_content[ind].lstrip()) == leading_spaces:
                insert_ind = ind
                break

        # Read env file
        f = open(env_path, 'r')
        env_content = f.readlines()
        f.close()

        # Prepare value pairs for yaml file
        value_pairs_list = [str(elem).replace("\n", "").split("=") for elem in env_content]
        final_set = HandyMix().flatten_nested_list(value_pairs_list)

        values_pairs = []
        for index in range(int(len(final_set) / 2)):
            name = (leading_spaces + 4) * ' ' + '- name: ' + str(final_set[2 * index]) + '\n'
            value = (leading_spaces + 6) * ' ' + 'value: "' + str(final_set[2 * index + 1]) + '"\n'

            values_pairs.append(name)
            values_pairs.append(value)
        values_pairs.insert(0, "        env:\n")

        # Build the yaml file
        new_yaml_file = ''.join(yaml_content[:insert_ind])
        new_yaml_file += ''.join(values_pairs)
        new_yaml_file += ''.join(yaml_content[insert_ind:])

        # Write env variables to yaml file
        f = open(yaml_path, "w")
        f.write(new_yaml_file)
        f.close()

    @staticmethod
    def backup_env_yaml(yaml_path='./environments/prd1/step01.yaml', server='test', env_name='', sql=False,
                        postgres=False, sharepoint=False, bc=False, cds=False):
        """ Save the data from the yaml file into a .env file to be used by decouple
        :param yaml_path: Path to Yaml file
        :param server: Server type; dev, test or prod
        :param env_name: Name of environment variables
        :param sql: SQL Environment credentials type
        :param postgres: Postgres Environment credentials type
        :param sharepoint: SharePoint Environment credentials type
        :param bc: Business Central Environment credentials type
        :param cds: CDS Environment credentials type
        """
        yaml_credentials = {}
        env_name = env_name.upper()
        server = server.upper()
        stream = open(yaml_path, "r")
        docs = yaml.load_all(stream, yaml.FullLoader)
        for doc in docs:
            yaml_env = doc['spec']['template']['spec']['containers'][0]['env']
            creds_list = list(filter(lambda person: env_name in person['name'], yaml_env))
            creds_dict = {item['name']: item for item in creds_list}

            if sql:
                server_name = creds_dict[f"SQL_{env_name}_{server}"]
                db_name = creds_dict[f"SQL_{env_name}_DB_NAME"]
                user_name = creds_dict[f"SQL_{env_name}_USER_NAME"]
                password = creds_dict[f"SQL_{env_name}_PASSWORD"]
                yaml_credentials = {'server_name': server_name, 'db_name': db_name,
                                    'user_name': user_name, 'password': password}
                break

            if postgres:
                server_name = creds_dict[f"POSTGRESQL_{env_name}_{server}_SERVER_NAME"]
                db_name = creds_dict[f"POSTGRESQL_{env_name}_DB_NAME"]
                user_name = creds_dict[f"POSTGRESQL_{env_name}_USER_NAME"]
                password = creds_dict[f"POSTGRESQL_{env_name}_PASSWORD"]
                yaml_credentials = {'server_name': server_name, 'db_name': db_name,
                                    'user_name': user_name, 'password': password}
                break

            if sharepoint:
                client_id = creds_dict[f'SHAREPOINT_CLIENT_ID_{env_name}']['value']
                scopes = creds_dict[f'SHAREPOINT_SCOPES_{env_name}']['value']
                organisation_id = creds_dict[f'SHAREPOINT_ORG_{env_name}']['value']
                username = creds_dict[f'SHAREPOINT_USER_{env_name}']['value']
                password = creds_dict[f'SHAREPOINT_PASSWORD_{env_name}']['value']
                site_id = creds_dict[f'SHAREPOINT_SITE_ID_{env_name}']['value']
                site_name = creds_dict[f'SHAREPOINT_SITE_NAME_{env_name}']['value']
                api_version = creds_dict[f'SHAREPOINT_API_VERSION_{env_name}']['value']
                yaml_credentials = {'client_id': client_id, 'scopes': scopes, 'organisation_id': organisation_id,
                                    'username': username, 'password': password, 'site_id': site_id,
                                    'site_name': site_name, 'api_version': api_version}
                break

            if bc:
                scope = creds_dict["BC_AUTH_SCOPE"]
                client_id = creds_dict["BC_AUTH_CLIENT_ID"]
                client_secret = creds_dict["BC_AUTH_CLIENT_SECRET"]

                yaml_credentials = {'scope': scope, 'client_id': client_id, 'client_secret': client_secret}
                break

            if cds:
                server = creds_dict[f"CDS_ENV_SERVER_{env_name}"]
                organisation_id = creds_dict[f"CDS_ENV_ORG_{env_name}"]
                environment_prefix = creds_dict[f"CDS_ENV_PREFIX_{env_name}"]
                environment_url = creds_dict[f"CDS_ENV_URL_{env_name}"]
                environment_name = creds_dict[f"CDS_ENV_NAME_{env_name}"]

                yaml_credentials = {'server': server, 'environment_name': environment_name,
                                    'organisation_id': organisation_id, 'environment_prefix': environment_prefix,
                                    'environment_url': environment_url}
                break

        return yaml_credentials
