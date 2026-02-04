"""
Configuration settings for the hackathon project
"""
import os
from typing import Dict, List

# API Configuration
API_PORT = int(os.getenv("API_PORT", 8000))
API_HOST = os.getenv("API_HOST", "0.0.0.0")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Hackathon Evaluation Parameters
HACKATHON_METRICS = {
    "max_conversation_turns": 50,
    "target_engagement_time": 10,  # minutes
    "extraction_targets": {
        "upi": 2,
        "bank_accounts": 1,
        "links": 3,
        "phones": 1
    },
    "scoring_weights": {
        "engagement_duration": 0.3,
        "conversation_turns": 0.2,
        "extraction_completeness": 0.4,
        "realism_score": 0.1
    }
}

# Agent Configuration
AGENT_CONFIG = {
    "response_delay_range": (1.0, 5.0),  # seconds
    "typo_probability": 0.15,
    "confusion_probability": 0.2,
    "stalling_probability": 0.1,
    "max_conversation_history": 20,
    "persona_switch_interval": 10  # turns
}

# Detection Configuration
DETECTION_CONFIG = {
    "scam_threshold": 0.5,
    "urgency_weight": 0.3,
    "financial_weight": 0.4,
    "threat_weight": 0.3,
    "url_weight": 0.2,
    "minimum_keyword_matches": 2
}

# Memory Configuration
MEMORY_CONFIG = {
    "storage_backend": "file",  # file, redis, memory
    "session_timeout_hours": 24,
    "max_sessions": 1000,
    "cleanup_interval_minutes": 60
}

# Extraction Configuration
EXTRACTION_CONFIG = {
    "validate_upi": True,
    "validate_accounts": True,
    "check_suspicious_domains": True,
    "extract_context": True,
    "min_confidence_score": 0.6
}

# Mock Scammer API Configuration (for testing)
MOCK_SCAMMER_CONFIG = {
    "base_url": os.getenv("MOCK_SCAMMER_URL", "http://localhost:8080"),
    "api_key": os.getenv("MOCK_SCAMMER_KEY", "test_key"),
    "polling_interval": 1.0,
    "max_retries": 3
}

# Logging Configuration
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "scam_pot.log",
    "max_size_mb": 10,
    "backup_count": 5
}

def get_config() -> Dict:
    """Get all configuration as a dictionary"""
    return {
        "api": {
            "port": API_PORT,
            "host": API_HOST,
            "debug": DEBUG
        },
        "hackathon": HACKATHON_METRICS,
        "agent": AGENT_CONFIG,
        "detection": DETECTION_CONFIG,
        "memory": MEMORY_CONFIG,
        "extraction": EXTRACTION_CONFIG,
        "mock_scammer": MOCK_SCAMMER_CONFIG,
        "logging": LOG_CONFIG
    }

def validate_config() -> List[str]:
    """Validate configuration and return any issues"""
    issues = []
    
    if API_PORT < 1 or API_PORT > 65535:
        issues.append(f"Invalid API_PORT: {API_PORT}")
    
    if HACKATHON_METRICS["max_conversation_turns"] <= 0:
        issues.append("max_conversation_turns must be positive")
    
    if not (0 <= AGENT_CONFIG["typo_probability"] <= 1):
        issues.append("typo_probability must be between 0 and 1")
    
    if DETECTION_CONFIG["scam_threshold"] <= 0 or DETECTION_CONFIG["scam_threshold"] >= 1:
        issues.append("scam_threshold must be between 0 and 1")
    
    return issues