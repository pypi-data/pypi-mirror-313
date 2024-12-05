import numpy as np
from typing import List, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TransactionMetrics:
    mean_amount: float
    std_dev: float
    transaction_density: float
    network_load: float
    system_capacity: float

class TransactionAnalytics:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def calculate_network_metrics(self, 
                                time_window: int = 3600) -> TransactionMetrics:
        """
        Calculate network metrics based on mathematical models.
        
        Args:
            time_window: Analysis window in seconds
        Returns:
            TransactionMetrics object with calculated values
        """
        transactions = self.db.get_transaction_history()
        
        # the section below calculates the μ and σ for transaction distribution
        amounts = [tx[3] for tx in transactions]  # amount is index 3
        mean_amount = np.mean(amounts)
        std_dev = np.std(amounts)
        
        # Calc. the transaction density function
        n = len(transactions)
        if n > 0:
            density = self._calculate_density(amounts, mean_amount, std_dev)
        else:
            density = 0.0
            
        # Calc. the network load
        current_time = datetime.utcnow().timestamp()
        load = self._calculate_network_load(
            transactions, 
            current_time, 
            time_window
        )
        
        # Calc. the system capacity
        capacity = self._calculate_system_capacity(
            transaction_rate=n/time_window,
            avg_tx_size=256,  # bytes
            available_memory=1e9  # 1GB for example
        )
        
        return TransactionMetrics(
            mean_amount=mean_amount,
            std_dev=std_dev,
            transaction_density=density,
            network_load=load,
            system_capacity=capacity
        )
    
    def _calculate_density(self, 
                         amounts: List[float], 
                         mean: float, 
                         std_dev: float) -> float:
        """
        Implements the probability density function:
        f(x) = (1/nσ√(2π)) * e^(-(x-μ)²/2σ²)
        """
        n = len(amounts)
        if std_dev == 0:
            return 0.0
            
        def pdf(x):
            return (1 / (n * std_dev * np.sqrt(2 * np.pi))) * \
                   np.exp(-(x - mean)**2 / (2 * std_dev**2))
                   
        return np.mean([pdf(x) for x in amounts])
    
    def _calculate_network_load(self, 
                              transactions: List[Tuple], 
                              current_time: float,
                              window: int,
                              base_load: float = 1.0,
                              decay_factor: float = 0.1) -> float:
        """
        Implements the network load function:
        L(t) = λ + ∑(i=1 to n) αᵢe^(-β(t-tᵢ))
        """
        load = base_load
        
        for tx in transactions:
            tx_time = datetime.fromisoformat(tx[4]).timestamp()  # timestamp is index 4
            if current_time - tx_time <= window:
                tx_weight = tx[3]  # amount as weight
                load += tx_weight * np.exp(-decay_factor * (current_time - tx_time))
                
        return load
    
    def _calculate_system_capacity(self,
                                 transaction_rate: float,
                                 avg_tx_size: int,
                                 available_memory: int,
                                 network_bandwidth: int = 1e6) -> float:
        """
        Implements the system capacity formula:
        C = min(Ct, Cm, Cn)
        """
        # The transaction processing capacity (tx/s)
        Ct = transaction_rate
        
        # set a memory-based capacity (tx/s)
        Cm = available_memory / (avg_tx_size * transaction_rate)
        
        # set a network-based capacity (tx/s)
        Cn = network_bandwidth / (avg_tx_size * transaction_rate)
        
        return min(Ct, Cm, Cn)
