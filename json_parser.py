'''
Parser of json files.
'''

def find_value(json_content: dict, user_key: str):
    '''
    Returns a value from the field given by a user.
    '''
    def investigate(section, key):
        '''
        Returns a value corresponding to a given key
    or (False, None) if the given key wasn't found.
        '''
        if isinstance(section, list):
            for sub_element in section:
                investigation_result, discovered_value = investigate(sub_element, key)
                if investigation_result:
                    return (True, discovered_value)

        elif isinstance(section, dict):
            if key in section:
                return (True, section[key])

            for sub_section_key in section:
                investigation_result, discovered_value = investigate(section[sub_section_key], key)
                if investigation_result:
                    return (True, discovered_value)

        return (False, None)

    investigation_conclusion = investigate(json_content, user_key)
    return investigation_conclusion

if __name__ == '__main__':
    import doctest
    doctest.testmod()
