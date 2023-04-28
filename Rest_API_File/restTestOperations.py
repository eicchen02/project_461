import requests

def main():
    # Test authenticate
    response = requests.put("http://127.0.0.1:8080/authenticate", json={'Secret': {'password': 'TestTest'},
                                                                        'User': {'isAdmin': True,
                                                                                 'name': 'Test'}})
    print(response)

if __name__ == "__main__":
    main()