# server.py
import flwr as fl
from flwr.server import ServerConfig

def main():
    strategy = fl.server.strategy.FedAvg(
        min_fit_clients=5,
        min_available_clients=5,
    )
    # Create a ServerConfig object with num_rounds set to 20
    config = ServerConfig(num_rounds=20)
    fl.server.start_server(server_address="127.0.0.1:8080", strategy=strategy, config=config)

if __name__ == "__main__":
    main()
