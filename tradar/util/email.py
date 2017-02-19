def send_email(message, sender=None, recipients=[]):
    '''Dummy function, to be implemented later'''
    # TODO: Implement actual email sending
    print('''
    [BEGIN EMAIL]
    From: %(sender)s
    To: %(recipients)s

    %(message)s

    [END EMAIL]
    ''' % {
        'sender': sender,
        'message': message,
        'recipients': ', '.join([r for r in recipients])
    })
