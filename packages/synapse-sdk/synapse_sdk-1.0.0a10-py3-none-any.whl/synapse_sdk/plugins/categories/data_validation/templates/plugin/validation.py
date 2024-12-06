def validate(data, assignment_id, **kwargs):
    errors = []
    if data.get('errors'):
        errors += data['errors']
    return errors
