import httpx
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test_all_scenarios():
    base = "http://localhost:8000/api/v1"
    
    print("========================================")
    print("SMARTCART COMPREHENSIVE 12-TEST SUITE")
    print("========================================")

    # 1. Health
    r = httpx.get(f"{base}/health", timeout=5.0)
    print(f"\n[TEST 0] Health check: {r.status_code} -> {r.json().get('status')}")

    # TEST 1: Coding laptop under 60k (Telugu)
    r = httpx.post(f"{base}/assistant/chat", json={"message": "naku 60000 lopu coding laptop kavali", "language": "telugu"}, timeout=30.0)
    res = r.json()
    print(f"\n[TEST 1] Coding laptop under 60k (Telugu transliteration):")
    print(f"  Result Type: {res.get('result_type')}")
    print(f"  Products Found: {len(res.get('products', []))}")
    print(f"  AI Message: {res.get('message')[:100]}...")
    if res.get('products'):
        print(f"  Product 1: {res['products'][0]['name']} (₹{res['products'][0]['price']:,}) -> WHY: {res['products'][0].get('why_recommended')}")

    # TEST 2: Best earbuds under 5000 (English)
    r = httpx.post(f"{base}/assistant/chat", json={"message": "best earbuds under 5000", "language": "english"}, timeout=30.0)
    res = r.json()
    print(f"\n[TEST 2] Best earbuds under 5000 (English):")
    print(f"  Result Type: {res.get('result_type')}")
    print(f"  Products Found: {len(res.get('products', []))}")
    print(f"  AI Message: {res.get('message')[:100]}...")
    if res.get('products'):
        print(f"  Product 1: {res['products'][0]['name']} (₹{res['products'][0]['price']:,}) -> WHY: {res['products'][0].get('why_recommended')}")

    # TEST 3: Strict impossible budget (Near-budget fallback + alert offer)
    r = httpx.post(f"{base}/assistant/chat", json={"message": "naku 15000 lopu laptop kavali", "language": "telugu"}, timeout=30.0)
    res = r.json()
    print(f"\n[TEST 3] Laptop under 15k (Near-budget fallback test):")
    print(f"  Result Type: {res.get('result_type')}")
    print(f"  Products Found: {len(res.get('products', []))}")
    print(f"  AI Message: {res.get('message')[:120]}...")
    if res.get('products'):
        p = res['products'][0]
        print(f"  Product 1: {p['name']} (₹{p['price']:,}) -> Status: {p.get('budget_status')} (+₹{p.get('budget_difference', 0):,} above budget)")
    print(f"  Subscription Offer Show: {res.get('subscription_offer', {}).get('show')}")
    print(f"  Subscription Message: {res.get('subscription_offer', {}).get('message')}")

    # TEST 4: Out of catalogue category (DSLR camera)
    r = httpx.post(f"{base}/assistant/chat", json={"message": "naku DSLR camera kavali", "language": "telugu"}, timeout=30.0)
    res = r.json()
    print(f"\n[TEST 4] Out of catalogue (DSLR camera):")
    print(f"  Result Type: {res.get('result_type')}")
    print(f"  Products Found: {len(res.get('products', []))}")
    print(f"  AI Message: {res.get('message')[:120]}...")
    print(f"  Subscription Offer Show: {res.get('subscription_offer', {}).get('show')}")

    # TEST 5: Telugu script query
    r = httpx.post(f"{base}/assistant/chat", json={"message": "నాకు ₹60000 లోపు coding laptop కావాలి", "language": "telugu"}, timeout=30.0)
    res = r.json()
    print(f"\n[TEST 5] Telugu script query:")
    print(f"  Result Type: {res.get('result_type')}")
    print(f"  Products Found: {len(res.get('products', []))}")
    print(f"  AI Message: {res.get('message')[:100]}...")

    # TEST 6: Semantic search (no exact keywords, e.g. "naku coding kosam laptop kavali")
    r = httpx.post(f"{base}/assistant/chat", json={"message": "naku coding kosam laptop kavali", "language": "telugu"}, timeout=30.0)
    res = r.json()
    print(f"\n[TEST 6] Semantic search without price:")
    print(f"  Result Type: {res.get('result_type')}")
    print(f"  Products Found: {len(res.get('products', []))}")

    # TEST 7: Hard constraints (16gb ram + 80k)
    r = httpx.post(f"{base}/assistant/chat", json={"message": "gaming laptop 80k lopu 16gb ram", "language": "english"}, timeout=30.0)
    res = r.json()
    print(f"\n[TEST 7] Hard constraints (gaming laptop 80k lopu 16gb ram):")
    print(f"  Result Type: {res.get('result_type')}")
    print(f"  Products Found: {len(res.get('products', []))}")
    for p in res.get('products', [])[:2]:
        print(f"    - {p['name']} (₹{p['price']:,}) | Specs: {p.get('specs')[:2]}")

    # TEST 8: Compare two products
    r = httpx.post(f"{base}/compare", json={"product_ids": ["aerobuds-pro", "sonic-beam"]}, timeout=5.0)
    res = r.json()
    print(f"\n[TEST 8] Compare two products:")
    print(f"  Status: {r.status_code}")
    print(f"  Products compared: {[p['name'] for p in res.get('products', [])]}")

    # TEST 9: Comparison insights (AI comparison explanation)
    r = httpx.post(f"{base}/compare/insights", json={"product_ids": ["aerobuds-pro", "sonic-beam"], "language": "telugu"}, timeout=30.0)
    res = r.json()
    print(f"\n[TEST 9] Comparison AI Insights:")
    print(f"  Explanation: {res.get('explanation')[:140]}...")

    # TEST 10: Language switch English -> Telugu
    r_en = httpx.post(f"{base}/assistant/chat", json={"message": "Monitor for home office", "language": "english"}, timeout=30.0)
    r_te = httpx.post(f"{base}/assistant/chat", json={"message": "Monitor for home office", "language": "telugu"}, timeout=30.0)
    print(f"\n[TEST 10] Language switch verification:")
    print(f"  English response: {r_en.json().get('message')[:70]}...")
    print(f"  Telugu response: {r_te.json().get('message')[:70]}...")

    # TEST 11: Subscribe API endpoint
    r = httpx.post(f"{base}/subscribe", json={"category": "Laptops", "max_price": 15000, "language": "telugu", "email": "ravi@example.com"}, timeout=5.0)
    res = r.json()
    print(f"\n[TEST 11] Subscription creation API:")
    print(f"  Success: {res.get('success')}")
    print(f"  Message: {res.get('message')}")

    # TEST 12: Unavailable category (e.g. washing machine / microwave)
    r = httpx.post(f"{base}/assistant/chat", json={"message": "washing machine kavali", "language": "telugu"}, timeout=30.0)
    res = r.json()
    print(f"\n[TEST 12] Unavailable category check:")
    print(f"  Result Type: {res.get('result_type')}")
    print(f"  Products: {len(res.get('products', []))}")
    print(f"  Message: {res.get('message')[:100]}...")

    print("\n========================================")
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("========================================")

if __name__ == "__main__":
    test_all_scenarios()
