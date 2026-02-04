import requests
import json
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Test locales endpoint
print("=" * 60)
print("Testing API Endpoints")
print("=" * 60)

# 1. Get locales
print("\n1. Getting supported locales...")
response = requests.get("http://localhost:8000/locales")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# 2. Normalize Hindi text
print("\n2. Normalizing Hindi text: '₹250 on 12/03/2024'")
response = requests.post(
    "http://localhost:8000/normalize",
    json={"locale": "hi-IN", "text": "₹250 on 12/03/2024"}
)
print(f"Status: {response.status_code}")
result = response.json()
print(f"Original: {result['original_text']}")
print(f"Normalized: {result['normalized_text']}")
print(f"Tokens: {len(result['tokens'])} tokens found")

# 3. Normalize Tamil text
print("\n3. Normalizing Tamil text: '₹250'")
response = requests.post(
    "http://localhost:8000/normalize",
    json={"locale": "ta-IN", "text": "₹250"}
)
print(f"Status: {response.status_code}")
result = response.json()
print(f"Original: {result['original_text']}")
print(f"Normalized: {result['normalized_text']}")

# 4. Generate SSML
print("\n4. Generating SSML for Hindi text: '₹250'")
response = requests.post(
    "http://localhost:8000/generate_ssml",
    json={"locale": "hi-IN", "text": "₹250", "use_ssml": True}
)
print(f"Status: {response.status_code}")
result = response.json()
print(f"SSML Output:")
print(result['ssml'])

# 5. Test with numbers
print("\n5. Normalizing number: '123' in Hindi")
response = requests.post(
    "http://localhost:8000/normalize",
    json={"locale": "hi-IN", "text": "123"}
)
print(f"Status: {response.status_code}")
result = response.json()
print(f"Original: {result['original_text']}")
print(f"Normalized: {result['normalized_text']}")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
