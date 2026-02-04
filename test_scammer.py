import requests
import json
import time
from typing import Dict, Any

class ScamPotTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session_counter = 0
    
    def test_single_message(self, message: str, session_id: str = None) -> Dict[str, Any]:
        """Test a single message"""
        if session_id is None:
            session_id = f"test_session_{self.session_counter}"
            self.session_counter += 1
        
        payload = {
            "session_id": session_id,
            "message": message
        }
        
        try:
            response = requests.post(f"{self.base_url}/chat", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "session_id": session_id, "message": message}
    
    def test_conversation_flow(self, messages: list, session_id: str = None) -> list:
        """Test a complete conversation flow"""
        if session_id is None:
            session_id = f"conv_test_{int(time.time())}"
        
        results = []
        for i, message in enumerate(messages):
            print(f"Turn {i+1}: Sending '{message}'")
            result = self.test_single_message(message, session_id)
            results.append(result)
            
            if "reply" in result:
                print(f"  Reply: {result['reply'][:50]}...")
                print(f"  Scam: {result.get('scam', False)}, Confidence: {result.get('scam_confidence', 0)}")
            
            time.sleep(0.5)  # Simulate thinking time
        
        return results
    
    def test_scam_scenarios(self):
        """Test various scam scenarios"""
        scenarios = {
            "upi_scam": [
                "Your bank account will be blocked within 2 hours",
                "Click this link to verify: https://secure-sbi.com/login",
                "Send ₹1 to 9876543210@okicici to confirm your account",
                "The transaction failed, try again with ₹10"
            ],
            "tech_support": [
                "Your computer has a virus",
                "Download TeamViewer from https://tinyurl.com/fake-teamviewer",
                "Share the 6-digit code showing on your screen",
                "Pay $50 for antivirus software to 123456789012"
            ],
            "lottery_scam": [
                "Congratulations! You won ₹50,00,000",
                "Claim your prize at http://lottery-claim.net",
                "Share your bank account number for transfer",
                "Pay processing fee of ₹5000 to account 987654321"
            ],
            "phishing": [
                "Your email password needs reset",
                "Click: http://gmail-verify.xyz to secure account",
                "Enter your current password on the page",
                "Check your email for OTP and share it here"
            ]
        }
        
        all_results = {}
        for scenario_name, messages in scenarios.items():
            print(f"\n{'='*50}")
            print(f"Testing: {scenario_name}")
            print(f"{'='*50}")
            
            results = self.test_conversation_flow(messages, f"scenario_{scenario_name}")
            all_results[scenario_name] = results
            
            # Summarize results
            scam_count = sum(1 for r in results if r.get('scam', False))
            print(f"\nSummary: {scam_count}/{len(messages)} messages detected as scam")
            
            # Show extractions
            extractions = []
            for r in results:
                if r.get('extracted'):
                    extractions.append(r['extracted'])
            print(f"Extractions: {extractions}")
        
        return all_results
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health")
            print(f"Health check: {response.json()}")
            
            # Test getting metrics for a session
            test_session = "test_session_0"
            response = requests.get(f"{self.base_url}/session/{test_session}/metrics")
            print(f"Session metrics: {response.json()}")
            
        except Exception as e:
            print(f"Metrics test failed: {e}")
    
    def run_comprehensive_test(self):
        """Run comprehensive test suite"""
        print("Starting comprehensive test of Agentic Honey-Pot System")
        print("="*60)
        
        # Test 1: Health check
        print("\n1. Testing system health...")
        self.test_metrics_endpoint()
        
        # Test 2: Individual scam messages
        print("\n2. Testing individual scam messages...")
        test_messages = [
            "Send money to 9876543210@paytm",
            "Your account 12345678901 is blocked",
            "Click http://fake-bank.com to verify",
            "Share OTP 123456 immediately"
        ]
        
        for msg in test_messages:
            result = self.test_single_message(msg)
            print(f"Message: {msg[:40]}...")
            print(f"  → Scam: {result.get('scam')}, Reply: {result.get('reply', '')[:40]}...")
        
        # Test 3: Full scam scenarios
        print("\n3. Testing complete scam scenarios...")
        scenario_results = self.test_scam_scenarios()
        
        # Test 4: Non-scam messages
        print("\n4. Testing non-scam messages...")
        non_scam_msgs = [
            "Hello, how are you?",
            "What's the weather today?",
            "Can you help me with something?",
            "Thanks for your help!"
        ]
        
        for msg in non_scam_msgs:
            result = self.test_single_message(msg, "non_scam_test")
            print(f"Non-scam: {msg} → Scam: {result.get('scam')}")
        
        print("\n" + "="*60)
        print("Comprehensive test complete!")
        
        return scenario_results

if __name__ == "__main__":
    # Change the port if your API runs on a different port
    tester = ScamPotTester("http://localhost:8000")
    
    # Run quick test
    print("Running quick test...")
    result = tester.test_single_message("Send ₹1000 to 1234567890@ybl")
    print(f"Test result: {json.dumps(result, indent=2)}")
    
    # Uncomment for comprehensive test
    # tester.run_comprehensive_test()