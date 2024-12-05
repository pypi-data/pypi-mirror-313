import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json

class AnalyticsDataGenerator:
    def __init__(self, db_connection):
        self.db = db_connection
        
    def generate_hourly_metrics(self, hours: int = 24) -> Dict[str, List[Any]]:
        """Generate hourly metrics for the dashboard"""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        # obtain transactions from database
        transactions = self.db.get_transaction_history()
        df = pd.DataFrame(transactions, columns=[
            'id', 'sender', 'receiver', 'amount', 'timestamp', 'status'
        ])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # generate hourly statistics
        hourly_stats = []
        current_time = start_time
        
        while current_time <= end_time:
            next_hour = current_time + timedelta(hours=1)
            mask = (df['timestamp'] >= current_time) & (df['timestamp'] < next_hour)
            hour_data = df[mask]
            
            # Calc. metrics
            success_rate = (
                len(hour_data[hour_data['status'] == 'confirmed']) / 
                len(hour_data) * 100 if len(hour_data) > 0 else 100
            )
            
            metrics = {
                'hour': current_time.hour,
                'transactions': len(hour_data),
                'amount': hour_data['amount'].mean() if len(hour_data) > 0 else 0,
                'networkLoad': self._calculate_network_load(hour_data),
                'successRate': success_rate
            }
            
            hourly_stats.append(metrics)
            current_time = next_hour
            
        return hourly_stats
    
    def generate_distribution_data(self) -> List[Dict[str, Any]]:
        """Generate transaction amount distribution data"""
        transactions = self.db.get_transaction_history()
        df = pd.DataFrame(transactions, columns=[
            'id', 'sender', 'receiver', 'amount', 'timestamp', 'status'
        ])
        
        # let's create amount ranges
        bins = [0, 250, 500, 750, float('inf')]
        labels = ['0-250', '251-500', '501-750', '751+']
        
        df['range'] = pd.cut(df['amount'], bins=bins, labels=labels)
        distribution = df['range'].value_counts()
        
        return [
            {'name': label, 'value': float(count)}
            for label, count in distribution.items()
        ]
    
    def _calculate_network_load(self, df: pd.DataFrame) -> float:
        """Calculate network load based on transaction volume and amounts"""
        if len(df) == 0:
            return 0.0
            
        # base-load calculation
        base_load = 10.0  # minimum network load
        tx_volume_factor = len(df) * 2  # each transaction contributes to load
        amount_factor = df['amount'].sum() * 0.01  # higher amounts = higher load
        
        # calc. total load with some randomness for realism
        total_load = base_load + tx_volume_factor + amount_factor
        total_load *= (1 + np.random.normal(0, 0.1))  # add 10% random variation
        
        # normalizing to 0-100 range
        return min(max(total_load, 0), 100)

    def generate_dashboard_data(self) -> str:
        """Generate complete dashboard dataset"""
        hourly_data = self.generate_hourly_metrics()
        distribution_data = self.generate_distribution_data()
        
        dashboard_data = {
            'hourly_metrics': hourly_data,
            'distribution': distribution_data,
            'summary': {
                'total_transactions': sum(h['transactions'] for h in hourly_data),
                'average_amount': np.mean([h['amount'] for h in hourly_data]),
                'average_load': np.mean([h['networkLoad'] for h in hourly_data])
            }
        }
        
        return json.dumps(dashboard_data, indent=2)
