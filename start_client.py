from src.connection.tcp_client import *

if __name__ == '__main__':
    client = Client()
    print("Clientul a pornit.")

    client.check_status()