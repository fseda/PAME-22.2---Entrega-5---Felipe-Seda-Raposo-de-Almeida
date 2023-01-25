def validate_data(data):
    error = ''

    if not data['full_name']:
        error = { "error": "full_name is required" }

    if not data['birthday']:
        error = { "error": "birthday is required" }

    if not data['cpf']:
        error = { "error": "cpf is required" }

    if not data['phone_number']:
        error = { "error": "phone_number is required" }
    
    if not data['email']:
        error = { "error": "email is required" }
    
    if not data['password']:
        error = { "error": "password is required" }

    return error, 400