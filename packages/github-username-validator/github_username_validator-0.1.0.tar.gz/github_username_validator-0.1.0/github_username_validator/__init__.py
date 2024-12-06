import requests
import time

def validate_usernames(usernames, api_key):
    """
    Memvalidasi daftar username GitHub.

    Args:
        usernames (list): List username GitHub yang akan divalidasi.
        api_key (str): API key untuk autentikasi.

    Returns:
        list: List dictionary yang berisi hasil validasi setiap username.
    """
    valid_api_keys = ["masanto", "msdigital"]  # Ganti dengan API key yang valid

    if api_key not in valid_api_keys:
        return {"error": "API key tidak valid"}

    results = []
    for username in usernames:
        username = username.strip()
        if username:
            api_url = f"https://api.github.com/users/{username}"
            try:
                response = requests.get(api_url)

                # Periksa rate limit
                if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers:
                    remaining_requests = int(response.headers['X-RateLimit-Remaining'])
                    if remaining_requests == 0:
                        reset_time = int(response.headers['X-RateLimit-Reset'])
                        wait_time = reset_time - time.time()
                        print(f"Rate limit tercapai. Menunggu {wait_time:.2f} detik...")
                        time.sleep(wait_time)
                        response = requests.get(api_url)

                if response.status_code == 200:
                    data = response.json()
                    created_at = data.get('created_at')
                    results.append({
                        'username': username,
                        'created_at': created_at,
                        'valid': True
                    })
                else:
                    results.append({
                        'username': username,
                        'valid': False
                    })
            except requests.exceptions.RequestException as e:
                results.append({
                    'username': username,
                    'error': str(e)
                })
    return results