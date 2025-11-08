"""
Adaptive Defense System using AI/ML
"""
import logging
from typing import List, Dict
from datetime import datetime
import random

logger = logging.getLogger(__name__)


class AdaptiveDefense:
    """AI-powered adaptive defense mechanism"""
    
    def __init__(self):
        self.threat_history = []
        self.defense_rules = []
        self.learning_data = []
    
    def analyze_threat_pattern(self, threats: List[Dict]) -> Dict:
        """Analyze threat patterns using ML"""
        logger.info("Analyzing threat patterns")
        
        if not threats:
            return {
                "pattern": "normal",
                "confidence": 0.95,
                "recommendations": []
            }
        
        # Placeholder for actual ML analysis
        # In production, use scikit-learn, TensorFlow, or PyTorch
        
        threat_types = [t.get("threat_type", "unknown") for t in threats]
        most_common = max(set(threat_types), key=threat_types.count) if threat_types else "none"
        
        analysis = {
            "pattern": most_common,
            "confidence": 0.85,
            "threat_count": len(threats),
            "timestamp": datetime.utcnow().isoformat(),
            "recommendations": self._generate_recommendations(threats)
        }
        
        return analysis
    
    def _generate_recommendations(self, threats: List[Dict]) -> List[str]:
        """Generate defense recommendations"""
        recommendations = []
        
        if len(threats) > 10:
            recommendations.append("Increase firewall strictness")
            recommendations.append("Enable rate limiting")
        
        if any(t.get("severity") == "critical" for t in threats):
            recommendations.append("Immediate security audit required")
            recommendations.append("Isolate affected nodes")
        
        return recommendations
    
    def predict_next_threat(self) -> Dict:
        """Predict potential future threats"""
        logger.info("Predicting next threat")
        
        # Placeholder for actual predictive model
        threat_types = ["ddos", "intrusion", "malware", "data_breach"]
        
        prediction = {
            "predicted_threat": random.choice(threat_types),
            "confidence": round(random.uniform(0.6, 0.95), 2),
            "time_window": "next_24_hours",
            "timestamp": datetime.utcnow().isoformat(),
            "preventive_actions": [
                "Strengthen authentication",
                "Update firewall rules",
                "Increase monitoring frequency"
            ]
        }
        
        return prediction
    
    def optimize_defense_strategy(self, current_state: Dict) -> Dict:
        """Optimize defense strategy based on current state"""
        logger.info("Optimizing defense strategy")
        
        optimization = {
            "strategy": "adaptive",
            "adjustments": [],
            "priority": "high",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        cpu_usage = current_state.get("cpu_usage", 0)
        memory_usage = current_state.get("memory_usage", 0)
        
        if cpu_usage > 80:
            optimization["adjustments"].append({
                "component": "scanning",
                "action": "reduce_frequency",
                "reason": "high_cpu_usage"
            })
        
        if memory_usage > 80:
            optimization["adjustments"].append({
                "component": "logging",
                "action": "compress_logs",
                "reason": "high_memory_usage"
            })
        
        return optimization
    
    def learn_from_incident(self, incident: Dict):
        """Learn from security incidents to improve defense"""
        logger.info(f"Learning from incident: {incident.get('type', 'unknown')}")
        
        self.learning_data.append({
            "incident": incident,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Update defense rules based on learning
        new_rule = {
            "trigger": incident.get("type"),
            "action": "block",
            "source": incident.get("source_ip"),
            "created": datetime.utcnow().isoformat()
        }
        
        self.defense_rules.append(new_rule)
        logger.info(f"New defense rule created: {new_rule}")
