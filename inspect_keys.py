import json

with open('test_api_debug.py', 'r', encoding='utf-8') as f:
    content = f.read()
    # Extract the JSON part (crude but works for this file)
    start = content.find('[{')
    end = content.rfind('}]') + 2
    if start != -1 and end != -1:
        data = json.loads(content[start:end])
        if data:
            print("Keys available in match object:")
            print(list(data[0].keys()))
            print("\nSample values for some keys:")
            for k in ['tournament_name', 'event_status', 'event_type_type']:
                print(f"{k}: {data[0].get(k)}")
