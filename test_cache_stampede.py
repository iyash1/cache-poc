import requests, json

host = "http://localhost:8000"

def generate_padded_data(user_record):
    user = {
        "id": user_record[0],
        "name": user_record[1],
        "email": user_record[2],
        "padding": "X" * 100000  # inflate size
    }

def get_user_record(user_id):
    response = requests.get(f'{host}/users/{user_id}')
    print(f"GET Response for user {user_id}:", response)
    return response.json()

def update_user_record(user_id, name):
    response = requests.put(f'{host}/users/{user_id}', params={'name': name})
    print(f"PUT Response for user {user_id}:", response)
    return response.json()

def add_user_record(name, email):
    response = requests.post(f'{host}/users/', params={'name': name, 'email': email})
    print(f"POST Response for user {name}:", response)
    return response.json()

if __name__ == "__main__":
    #  Read user records from JSON file
    user_records_json = json.load(open('users.json'))

    # Loop through user records to perform operations
    for i in range(1, 100):

        # Look for a user record in the system
        user = get_user_record(user_records_json[i]['id'])

        # if user is found, update the record from the JSON file
        if not user.get("error"):
            updated_user = update_user_record(user_records_json[i]['id'], user_records_json[i]['name'])

        # if user is not found, add the record from the JSON file
        if user.get("error"):
            new_user = add_user_record(user_records_json[i]['name'], user_records_json[i]['email'])

