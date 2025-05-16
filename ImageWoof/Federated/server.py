import flwr as fl

def main():
    # Use Flower's FedAvg strategy.
    strategy = fl.server.strategy.FedAvg(
        min_fit_clients=5,
        min_available_clients=5,
    )
    
    # Start the Flower server on localhost:8080 for 20 rounds.
    fl.server.start_server(
        server_address="127.0.0.1:8080",
        strategy=strategy,
        config=fl.server.ServerConfig(num_rounds=10)
    )

if __name__ == "__main__":
    main()
