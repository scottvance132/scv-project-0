def containsSpecChar(value):
    sc = '[@_!#$%^&*()<>?/\|}{~:]'
    for char in value:
        if char in sc:
            return True
    return False

