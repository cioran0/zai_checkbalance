from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime

load_dotenv()
# Get API key from environment
api_key = os.getenv("ZAI_API_KEY")

# Working endpoint
monitor_url = "https://api.z.ai/api/monitor/usage/quota/limit"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(monitor_url, headers=headers)

print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
    
    # Extract and display relevant information
    if data.get('success') and 'data' in data:
        limits = data['data'].get('limits', [])
        
        print("\n" + "="*60)
        print("QUOTA SUMMARY")
        print("="*60)
        
        for limit in limits:
            limit_type = limit.get('type', 'Unknown')
            print(f"\n{limit_type}:")
            print(f"  Unit: {limit.get('unit')}")
            print(f"  Number: {limit.get('number')}")
            print(f"  Percentage: {limit.get('percentage')}%")
            
            # Convert timestamp to local time
            next_reset = limit.get('nextResetTime')
            if next_reset:
                # The timestamp appears to be in milliseconds
                reset_time = datetime.fromtimestamp(next_reset / 1000)
                print(f"  Next Reset: {reset_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            else:
                print(f"  Next Reset: N/A")
            
            if 'usageDetails' in limit:
                print(f"  Usage Details:")
                for detail in limit['usageDetails']:
                    model = detail.get('modelCode', 'Unknown')
                    usage = detail.get('usage', 0)
                    print(f"    - {model}: {usage}")
else:
    print(f"Error: {response.text}")

print("\n" + "="*60)
print("NOTE: The quota/limit endpoint provides general quota information")
print("but not model-specific token usage (like glm-4.7).")
print("="*60)
