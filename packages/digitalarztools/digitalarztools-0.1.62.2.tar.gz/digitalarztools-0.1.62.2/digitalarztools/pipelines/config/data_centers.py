import os
import json
import sys

from cryptography.fernet import Fernet


class DataCenters:
    """
        To add the account in the digitalarztool module, you have to open the python console.
        Activate the venv environment and  open python in this environment. In console use following commands

        from digitalarztools.pipelines.config.data_centers import DataCenters
        DataCenters().set_up_account("EARTHEXPLORER")
     usage:
        To set earthsat account username and password
        DataCenters().set_up_account("NASA")
        To get earthsat account username and password
        DataCenters().get_server_account("NASA")

    """
    servers = ["EARTHEXPLORER", "NASA", "NASA_BEARER", "GLEAM", "FTP_WA", "MSWEP", "Copernicus", "VITO", "WAPOR"]
    key_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "wa_key.txt")
    json_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "keys.json")

    def create_key(self):
        # key_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "wa_key.txt")

        if os.path.exists(self.key_filename):
            os.remove(self.key_filename)

        f = open(self.key_filename, "w+")
        f.write(str(Fernet.generate_key().decode("utf-8")))
        f.close()

    def set_up_account(self, account="ALL"):
        if not os.path.exists(self.key_filename):
            self.create_key()

        f = open(self.key_filename, "r")
        key = f.read()
        f.close()

        cipher_suite = Fernet(key.encode('utf-8'))

        if os.path.exists(self.json_filename):

            # open json file
            with open(self.json_filename) as f:
                datastore = f.read()
            obj = json.loads(datastore)
            f.close()
        else:
            obj = {}

        if account == "ALL":
            Servers = self.servers
        else:
            Servers = [account]

        for Server in Servers:

            if Server != "WAPOR" and Server != "NASA_BEARER":
                account_name = input("Type in your account username for %s" % Server)
                pwd = input("Type in your password for %s" % Server)

                account_name_crypt = cipher_suite.encrypt(("%s" % account_name).encode('utf-8'))
                pwd_crypt = cipher_suite.encrypt(("%s" % pwd).encode('utf-8'))
                obj[Server] = ([str(account_name_crypt.decode("utf-8")), str(pwd_crypt.decode("utf-8"))])
            if Server == "WAPOR" or Server == "NASA_BEARER":
                API_Key = input("Type in your API key for %s" % Server)
                API_Key_crypt = cipher_suite.encrypt(("%s" % API_Key).encode('utf-8'))
                obj[Server] = [str(API_Key_crypt.decode("utf-8"))]

        # save extent in task
        with open(self.json_filename, 'w') as outfile:
            json.dump(obj, outfile)

    def get_server_account(self, server_name):
        # path = os.path.dirname(__file__)

        # key_file = os.path.join(path, "wa_key.txt")

        if not os.path.exists(self.key_filename):
            sys.exit("DataCenters().create_key()")

        # json_file = os.path.join(path, "keys.json")

        if not os.path.exists(self.json_filename):
            sys.exit("DataCenters().set_up_account()")

        f = open(self.key_filename, "r")
        key = f.read()
        f.close()

        cipher_suite = Fernet(key.encode('utf-8'))

        # open json file
        with open(self.json_filename) as f:
            datastore = f.read()
        obj = json.loads(datastore)
        f.close()

        if server_name != "WAPOR" and server_name != "NASA_BEARER":
            username_crypt, pwd_crypt = obj[server_name]
            username = cipher_suite.decrypt(username_crypt.encode("utf-8"))
            pwd = cipher_suite.decrypt(pwd_crypt.encode("utf-8"))
        else:
            username_crypt = obj[server_name]
            username = cipher_suite.decrypt(username_crypt[0].encode("utf-8"))
            pwd = b''

        return str(username.decode("utf-8")), str(pwd.decode("utf-8"))


if __name__ == "__main__":
    dc = DataCenters()
    res = dc.get_server_account("EARTHEXPLORER")
    print(res)