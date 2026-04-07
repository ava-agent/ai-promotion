import requests
import json
from datetime import datetime

print('HF API Status Check Started...')
print(f'Check Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print()

# Check API endpoints status
endpoints = {
    'Homepage': 'https://huggingface.co',
    'Health Check': 'https://huggingface.co/api/health',
    'Models List': 'https://huggingface.co/api/models',
    'Organization Info': 'https://huggingface.co/api/organizations/IKUN-LLM',
    'Model Details': 'https://huggingface.co/api/models/ikun-2.5B'
}

status_results = {}
for name, url in endpoints.items():
    try:
        response = requests.get(url, timeout=10)
        status = 'OK' if response.status_code == 200 else f'Error ({response.status_code})'
        status_results[name] = {'url': url, 'status': status, 'response_time': response.elapsed.total_seconds()}
        print(f'{name}: {status} - Response Time: {response.elapsed.total_seconds():.2f}s')
    except Exception as e:
        status_results[name] = {'url': url, 'status': f'Connection Failed ({str(e)})', 'response_time': 0}
        print(f'{name}: Connection Failed ({str(e)})')

print()
print('API Status Summary:')
successful = sum(1 for result in status_results.values() if 'OK' in result['status'])
total = len(status_results)
print(f'Successful Endpoints: {successful}/{total} ({successful/total*100:.1f}%)')

print()
print('HF System Status Assessment:')
if successful == total:
    print('Perfect: All HF API endpoints are available')
elif successful >= total * 0.8:
    print('Good: HF API mostly normal with some issues')
else:
    print('Poor: HF API has multiple issues that need fixing')