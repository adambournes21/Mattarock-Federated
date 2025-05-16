# server.py
import flwr as fl
from flwr.server import ServerConfig
import matplotlib.pyplot as plt          # NEW
# -------------------------------------------------------------------------

# containers to collect per‑round numbers
loss_hist, acc_hist, prec_hist, rec_hist, f1_hist = ([] for _ in range(5))

def weighted_avg(metrics):
    """metrics = [(num_examples, {'accuracy': .., 'precision': .., ...}), ...]"""
    tot = {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0}
    total_examples = 0
    for n, m in metrics:
        total_examples += n
        for k in tot:
            tot[k] += n * m[k]
    return {k: v / total_examples for k, v in tot.items()}

# --- small subclass that logs every round --------------------------------
class FedAvgLog(fl.server.strategy.FedAvg):
    def aggregate_evaluate(self, rnd, results, failures):
        loss, metrics = super().aggregate_evaluate(rnd, results, failures)
        if loss is not None:                           # store loss
            loss_hist.append((rnd, loss))
        if metrics:                                    # store metrics
            acc_hist.append ((rnd, metrics["accuracy"]))
            prec_hist.append((rnd, metrics["precision"]))
            rec_hist.append ((rnd, metrics["recall"]))
            f1_hist.append  ((rnd, metrics["f1"]))
        return loss, metrics

def main():
    strategy = FedAvgLog(
        min_fit_clients=5,
        min_available_clients=5,
        evaluate_metrics_aggregation_fn=weighted_avg,
    )
    cfg = ServerConfig(num_rounds=15)
    fl.server.start_server(
        server_address="127.0.0.1:8080",   # keyword arg
        strategy=strategy,
        config=cfg,
    )
    # ------------- plot after training finishes --------------------------
    if loss_hist:                          # avoid crashing on early stop
        rounds, loss  = zip(*loss_hist)
        _, acc   = zip(*acc_hist)
        _, prec  = zip(*prec_hist)
        _, recall= zip(*rec_hist)
        _, f1    = zip(*f1_hist)

        fig, axes = plt.subplots(1, 5, figsize=(20, 4), constrained_layout=True)
        axes[0].plot(rounds, loss,  marker="o"); axes[0].set_title("Loss")
        axes[1].plot(rounds, acc,   marker="o"); axes[1].set_title("Accuracy")
        axes[2].plot(rounds, prec,  marker="o"); axes[2].set_title("Precision")
        axes[3].plot(rounds, recall,marker="o"); axes[3].set_title("Recall")
        axes[4].plot(rounds, f1,    marker="o"); axes[4].set_title("F1")

        for ax in axes:
            ax.set_xlabel("Round"); ax.grid(alpha=0.4)
        axes[0].set_ylabel("Value")
        plt.suptitle("FedAvg — 15 Rounds (global metrics)")
        plt.show()

if __name__ == "__main__":
    main()
