from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime, timezone
from zai import ZaiClient

load_dotenv()
# Get API key from environment
api_key = os.getenv("ZAI_API_KEY")

# Working endpoint
monitor_url = "https://api.z.ai/api/monitor/usage/quota/limit"
model_url = "https://api.z.ai/api/monitor/usage/model-usage"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(monitor_url, headers=headers)

print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    #print(json.dumps(data, indent=2))
    
    # Extract and display relevant information
    if data.get('success') and 'data' in data:
        limits = data['data'].get('limits', [])
        level = data['data'].get('level')
        print("\n" + "="*60)
        print(f"QUOTA SUMMARY for == {level} == rank acct")
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
                # The timestamp appears to be in milliseconds, convert from UTC to local time
                reset_time_utc = datetime.fromtimestamp(next_reset / 1000, tz=timezone.utc)
                reset_time_local = reset_time_utc.astimezone()
                print(f"  Next Reset (UTC): {reset_time_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")
                print(f"  Next Reset (Local): {reset_time_local.strftime('%Y-%m-%d %H:%M:%S %Z')}")
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

"""
print("\n" + "="*60)
print("MODEL USAGE ENDPOINT")
print("="*60)

# Try with different headers
print("\nMethod 1: GET with different headers")
"""

headers_v2 = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}
"""
response = requests.get(model_url, headers=headers_v2)
print(f"Status Code: {response.status_code}")
print(f"Response text: {response.text}")
print(f"Response headers: {dict(response.headers)}")
if response.text.strip():
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

print("\nMethod 2: POST with different headers and empty body")
response = requests.post(model_url, headers=headers_v2, json={})
print(f"Status Code: {response.status_code}")
print(f"Response text: {response.text}")
if response.text.strip():
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

print("\nMethod 3: Try with query parameters (correct format)")
"""
response = requests.get(model_url, headers=headers_v2, params={"startTime": "2026-03-01 00:00:00", "endTime": "2026-03-06 23:59:59"})
print(f"Status Code: {response.status_code}")
if response.text.strip():
    try:
        data = response.json()
        if data.get('success') and 'data' in data:
            usage_data = data['data']
            print("\n" + "="*60)
            print("MODEL USAGE SUMMARY")
            print("="*60)
            print(f"\nTotal Model Call Count: {usage_data.get('totalUsage', {}).get('totalModelCallCount', 0)}")
            print(f"Total Token Usage: {usage_data.get('totalUsage', {}).get('totalTokensUsage', 0):,}")
            
            # Show hourly breakdown (last 10 entries)
            x_time = usage_data.get('x_time', [])
            model_call_count = usage_data.get('modelCallCount', [])
            tokens_usage = usage_data.get('tokensUsage', [])
            
            print(f"\nHourly Breakdown (last 10 entries):")
            print(f"{'Time':<20} {'Calls':<10} {'Tokens':<15}")
            print("-" * 45)
            
            for i in range(max(0, len(x_time) - 10), len(x_time)):
                time = x_time[i] if i < len(x_time) else 'N/A'
                calls = model_call_count[i] if i < len(model_call_count) and model_call_count[i] is not None else 0
                tokens = tokens_usage[i] if i < len(tokens_usage) and tokens_usage[i] is not None else 0
                print(f"{time:<20} {calls:<10} {tokens:<15,}")
        else:
            print(json.dumps(data, indent=2))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

#print("\nMethod 4: Try with model parameter (glm-4.7 specific)")
response = requests.get(model_url, headers=headers_v2, params={"startTime": "2026-03-01 00:00:00", "endTime": "2026-03-06 23:59:59", "model": "glm-4.7"})
print(f"Status Code: {response.status_code}")
if response.text.strip():
    try:
        data = response.json()
        if data.get('success') and 'data' in data:
            usage_data = data['data']
            print("\n" + "="*60)
            print("GLM-4.7 SPECIFIC USAGE")
            print("="*60)
            print(f"\nTotal Model Call Count: {usage_data.get('totalUsage', {}).get('totalModelCallCount', 0)}")
            print(f"Total Token Usage: {usage_data.get('totalUsage', {}).get('totalTokensUsage', 0):,}")
            
            # Show hourly breakdown (last 10 entries)
            x_time = usage_data.get('x_time', [])
            model_call_count = usage_data.get('modelCallCount', [])
            tokens_usage = usage_data.get('tokensUsage', [])
            
            print(f"\nHourly Breakdown (last 10 entries):")
            print(f"{'Time':<20} {'Calls':<10} {'Tokens':<15}")
            print("-" * 45)
            
            for i in range(max(0, len(x_time) - 10), len(x_time)):
                time = x_time[i] if i < len(x_time) else 'N/A'
                calls = model_call_count[i] if i < len(model_call_count) and model_call_count[i] is not None else 0
                tokens = tokens_usage[i] if i < len(tokens_usage) and tokens_usage[i] is not None else 0
                print(f"{time:<20} {calls:<10} {tokens:<15,}")
        else:
            print(json.dumps(data, indent=2))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")