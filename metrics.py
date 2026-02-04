"""
Metrics tracking for hackathon evaluation
"""
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json
import os
from collections import defaultdict

class HackathonMetrics:
    def __init__(self):
        self.metrics_file = "hackathon_metrics.json"
        self._initialize_metrics()
    
    def _initialize_metrics(self):
        """Initialize metrics storage"""
        if not os.path.exists(self.metrics_file):
            base_metrics = {
                "total_sessions": 0,
                "total_messages": 0,
                "scam_sessions": 0,
                "total_engagement_time": 0,
                "extraction_counts": defaultdict(int),
                "conversation_lengths": [],
                "session_metrics": {},
                "start_time": datetime.now().isoformat(),
                "last_update": datetime.now().isoformat()
            }
            self._save_metrics(base_metrics)
    
    def _load_metrics(self) -> Dict:
        """Load metrics from file"""
        try:
            with open(self.metrics_file, 'r') as f:
                return json.load(f)
        except:
            return self._initialize_metrics()
    
    def _save_metrics(self, metrics: Dict):
        """Save metrics to file"""
        # Convert defaultdict to regular dict for JSON serialization
        if "extraction_counts" in metrics and isinstance(metrics["extraction_counts"], defaultdict):
            metrics["extraction_counts"] = dict(metrics["extraction_counts"])
        
        with open(self.metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)
    
    def update_session_metrics(self, session_id: str, metrics: Dict):
        """Update metrics for a specific session"""
        all_metrics = self._load_metrics()
        
        # Update overall metrics
        all_metrics["total_sessions"] += 1
        all_metrics["total_messages"] += metrics.get("message_count", 0)
        
        if metrics.get("is_scam", False):
            all_metrics["scam_sessions"] += 1
        
        all_metrics["total_engagement_time"] += metrics.get("engagement_duration", 0)
        
        # Update extraction counts
        extractions = metrics.get("extractions", {})
        for key, items in extractions.items():
            if items:
                all_metrics["extraction_counts"][key] = all_metrics["extraction_counts"].get(key, 0) + len(items)
        
        # Track conversation length
        all_metrics["conversation_lengths"].append(metrics.get("message_count", 0))
        
        # Keep only last 1000 conversation lengths
        if len(all_metrics["conversation_lengths"]) > 1000:
            all_metrics["conversation_lengths"] = all_metrics["conversation_lengths"][-1000:]
        
        # Store session-specific metrics
        all_metrics["session_metrics"][session_id] = {
            **metrics,
            "timestamp": datetime.now().isoformat()
        }
        
        all_metrics["last_update"] = datetime.now().isoformat()
        self._save_metrics(all_metrics)
    
    def get_overall_metrics(self) -> Dict[str, Any]:
        """Get overall system metrics"""
        metrics = self._load_metrics()
        
        # Calculate derived metrics
        avg_conversation_length = 0
        if metrics["conversation_lengths"]:
            avg_conversation_length = sum(metrics["conversation_lengths"]) / len(metrics["conversation_lengths"])
        
        scam_rate = 0
        if metrics["total_sessions"] > 0:
            scam_rate = (metrics["scam_sessions"] / metrics["total_sessions"]) * 100
        
        avg_engagement = 0
        if metrics["total_sessions"] > 0:
            avg_engagement = metrics["total_engagement_time"] / metrics["total_sessions"]
        
        return {
            "total_sessions": metrics["total_sessions"],
            "total_messages": metrics["total_messages"],
            "scam_sessions": metrics["scam_sessions"],
            "scam_rate_percentage": round(scam_rate, 2),
            "avg_conversation_length": round(avg_conversation_length, 2),
            "avg_engagement_minutes": round(avg_engagement, 2),
            "total_extractions": dict(metrics.get("extraction_counts", {})),
            "extraction_efficiency": self._calculate_extraction_efficiency(metrics),
            "system_uptime_hours": self._calculate_uptime_hours(metrics),
            "active_sessions": len(metrics.get("session_metrics", {}))
        }
    
    def get_session_leaderboard(self, top_n: int = 10) -> List[Dict]:
        """Get leaderboard of best sessions by extraction score"""
        metrics = self._load_metrics()
        session_data = metrics.get("session_metrics", {})
        
        scored_sessions = []
        for session_id, data in session_data.items():
            score = self._calculate_session_score(data)
            scored_sessions.append({
                "session_id": session_id,
                "score": score,
                "message_count": data.get("message_count", 0),
                "extractions": data.get("extractions", {}),
                "engagement_duration": data.get("engagement_duration", 0),
                "timestamp": data.get("timestamp", "")
            })
        
        # Sort by score descending
        scored_sessions.sort(key=lambda x: x["score"], reverse=True)
        return scored_sessions[:top_n]
    
    def _calculate_session_score(self, session_data: Dict) -> float:
        """Calculate score for a session (for hackathon evaluation)"""
        score = 0.0
        
        # Points for conversation length
        message_count = session_data.get("message_count", 0)
        score += min(message_count * 0.1, 2.0)  # Max 2 points for length
        
        # Points for extractions
        extractions = session_data.get("extractions", {})
        if extractions.get("upi"):
            score += len(extractions["upi"]) * 0.5
        if extractions.get("bank_accounts"):
            score += len(extractions["bank_accounts"]) * 0.7
        if extractions.get("suspicious_domains"):
            score += len(extractions["suspicious_domains"]) * 0.3
        
        # Points for engagement duration
        engagement = session_data.get("engagement_duration", 0)
        score += min(engagement * 0.05, 1.0)  # Max 1 point for duration
        
        return round(score, 2)
    
    def _calculate_extraction_efficiency(self, metrics: Dict) -> Dict[str, float]:
        """Calculate extraction efficiency metrics"""
        total_scam_sessions = metrics.get("scam_sessions", 0)
        if total_scam_sessions == 0:
            return {"upi_efficiency": 0.0, "account_efficiency": 0.0, "overall_efficiency": 0.0}
        
        extraction_counts = metrics.get("extraction_counts", {})
        
        upi_efficiency = (extraction_counts.get("upi", 0) / total_scam_sessions) * 100
        account_efficiency = (extraction_counts.get("bank_accounts", 0) / total_scam_sessions) * 100
        
        total_extractions = sum(extraction_counts.values())
        overall_efficiency = (total_extractions / total_scam_sessions) * 100
        
        return {
            "upi_efficiency": round(upi_efficiency, 2),
            "account_efficiency": round(account_efficiency, 2),
            "overall_efficiency": round(overall_efficiency, 2)
        }
    
    def _calculate_uptime_hours(self, metrics: Dict) -> float:
        """Calculate system uptime in hours"""
        start_time_str = metrics.get("start_time")
        if not start_time_str:
            return 0.0
        
        try:
            start_time = datetime.fromisoformat(start_time_str)
            uptime = datetime.now() - start_time
            return round(uptime.total_seconds() / 3600, 2)
        except:
            return 0.0

# Initialize metrics tracker
metrics_tracker = HackathonMetrics()

# Convenience functions
def update_metrics(session_id: str, is_scam: bool, extractions: Dict):
    """Update metrics for a session"""
    metrics_tracker.update_session_metrics(session_id, {
        "is_scam": is_scam,
        "extractions": extractions,
        "message_count": 1,  # This should be incremented per message
        "engagement_duration": 0.5  # Estimated 30 seconds per message
    })

def get_conversation_metrics(session_id: str) -> Dict:
    """Get metrics for a specific conversation"""
    metrics = metrics_tracker._load_metrics()
    return metrics.get("session_metrics", {}).get(session_id, {})

def get_leaderboard(top_n: int = 10) -> List[Dict]:
    """Get hackathon leaderboard"""
    return metrics_tracker.get_session_leaderboard(top_n)

def get_system_stats() -> Dict:
    """Get overall system statistics"""
    return metrics_tracker.get_overall_metrics()