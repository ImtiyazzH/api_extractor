import requests

def fetch_api_data(url):
    citations = []
    page = 1
    while True:
        response = requests.get(url, params={'page': page})
        print("Response status code:", response.status_code)
        response_text = response.content.decode('utf-8')
        print("Response content:", response_text)

        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            break
        
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            break

        # Assuming the actual items are under the "data" key
        if "data" not in data:
            print("No 'data' key in the response JSON")
            break

        items = data["data"]
        if not items:
            break

        for item in items:
            for source_item in item["source"]:
                if source_item["context"] in item["response"]:
                    citation = {
                        "id": item["id"],
                        "link": source_item["link"]
                    }
                    citations.append(citation)
                    break
        page += 1

    return citations

def main():
    url = "https://devapi.beyondchats.com/api/get_message_with_sources"
    citations = fetch_api_data(url)
    print("Citations found:", citations)

if __name__ == "__main__":
    main()
