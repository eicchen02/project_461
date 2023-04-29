import requests

def main():
    # Test authenticate
    response = requests.put("http://127.0.0.1:8080/authenticate", json={'Secret': {'password': 'TestTest'},
                                                                        'User': {'isAdmin': True,
                                                                                 'name': 'Test'}})
    print(f'Authentication Test: {response}')
    
    response = requests.post("http://127.0.0.1:8080/package", headers={'X-Authorization': 'Test'}, json={'Content': '',
                                                                                                        'JSProgram': '', 
                                                                                                        'URL': 'https://github.com/cloudinary/cloudinary_npm'})
    print(f'Package Create Test: {response}')
if __name__ == "__main__":
    main()