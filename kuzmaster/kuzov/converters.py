class SlugPkConverter:
    regex = "\d+_\d+"

    def to_python(self, value):
        p_keys = {'auto_pk': int(value.split('_')[0]), 'client_pk': int(value.split('_')[1])}
        return p_keys
    
    def to_url(self, value):
        pass
