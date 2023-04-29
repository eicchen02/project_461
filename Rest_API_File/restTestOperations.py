import requests

def main():
    # Test authenticate
    response = requests.put("http://127.0.0.1:8080/authenticate", json={'Secret': {'password': 'TestTest'},
                                                                        'User': {'isAdmin': True,
                                                                                 'name': 'Test'}})
    print(f'Authentication Test: {response.json()}\n')
    
    response = requests.post("http://127.0.0.1:8080/package", headers={'X-Authorization': 'Test'}, json={'Content': '',
                                                                                                        'JSProgram': '', 
                                                                                                        'URL': 'https://github.com/cloudinary/cloudinary_npm'})
    print(f'Package Create Test, Grabbing JSON: {response.json()}')
    if(response.status_code == 201):
        data = response.json()['data']
        print(f'Package Create Test, Grabbing data: {data}')
        metadata = response.json()['metadata']
        print(f'Package Create Test, Grabbing metadata: {metadata}\n')
    else:
        print(f'The package was not uploaded, due to a error code {response.status_code}')
if __name__ == "__main__":
    main()