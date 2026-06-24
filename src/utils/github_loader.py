import requests

def get_code_from_github_file(url : str) -> str :
    if "github.com" not in url or "/blob/" not in url :
        raise ValueError("Enter a valid github file url")
    
    raw_url = url.replace("github.com", "raw.githubusercontent.com")
    raw_url = raw_url.replace("/blob/", "/")

    response = requests.get(raw_url)

    if response.status_code != 200 :
        raise Exception("Failed to fetch file from the given github url.")
    
    return response.text