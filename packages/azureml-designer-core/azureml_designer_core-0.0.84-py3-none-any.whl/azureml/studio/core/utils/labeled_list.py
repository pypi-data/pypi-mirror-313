class LabeledList:

    def __init__(self):
        self._index_to_name = list()
        self._name_to_index = dict()
        self._items = list()

    @property
    def names(self):
        return self._index_to_name

    def set_name(self, old_name, new_name):
        if old_name not in self.names:
            self.raise_key_not_exist_error(arg_name='old_name', key=old_name)

        if old_name == new_name:
            raise ValueError(f'Names "{new_name}" must not be the same.')

        self.validate_name(new_name)

        index = self.get_index(old_name)
        self._index_to_name[index] = new_name
        self._name_to_index[new_name] = self._name_to_index[old_name]
        del self._name_to_index[old_name]

    def get_index(self, name):
        if isinstance(name, list):
            return [self._get_index(x) for x in name]
        return self._get_index(name)

    def _get_index(self, name):
        if name in self._name_to_index:
            return self._name_to_index[name]
        self.raise_key_not_exist_error(arg_name='name', key=name)

    def get_name(self, index):
        if isinstance(index, list):
            return [self._get_name(x) for x in index]
        return self._get_name(index)

    def _get_name(self, index):
        if isinstance(index, int):
            self.validate_key(key=index, arg_name_in_error='index')
            return self._index_to_name[index]
        else:
            raise TypeError(f'Argument "index": Column index "{index}" is not an integer type.')

    def __iter__(self):
        yield from self._items

    def __contains__(self, item):
        return item in self._name_to_index or (isinstance(item, int) and 0 <= item < len(self))

    def __getitem__(self, key):
        self.validate_key(key)
        if isinstance(key, str):
            return self._items[self._name_to_index[key]]
        return self._items[key]

    def __setitem__(self, key, value):
        self.validate_key(key)
        if isinstance(key, str):
            self._items[self._name_to_index[key]] = value
        else:
            self._items[key] = value

    def append(self, name, item):
        self.validate_name(name)
        self._index_to_name.append(name)
        self._update_name_to_index(len(self._index_to_name)-1)
        self._items.append(item)

    def remove(self, key):
        self.validate_key(key)

        if isinstance(key, int):
            del self._index_to_name[key]
            del self._items[key]
            self._update_name_to_index(key)
        else:
            self._index_to_name.remove(key)
            del self._items[self._name_to_index[key]]
            self._update_name_to_index(self._name_to_index[key])

    def _update_name_to_index(self, start_index):
        for i in range(start_index, len(self._index_to_name)):
            name = self._index_to_name[i]
            self._name_to_index[name] = i

    def __len__(self):
        return len(self._index_to_name)

    def __eq__(self, other):
        if not isinstance(other, LabeledList):
            raise TypeError('Argument "other": Not labeled list.')

        return self.names == other.names and  \
            all(self[x] == other[y] for x, y in zip(self.names, other.names))

    def validate_key(self, key, arg_name_in_error='key'):
        if isinstance(key, str):
            if key not in self._name_to_index:
                self.raise_key_not_exist_error(arg_name=arg_name_in_error, key=key)
        elif isinstance(key, int):
            if not 0 <= key < len(self._items):
                raise KeyError(f'Argument "{arg_name_in_error}" is out of range from {0} to {len(self._items)-1}.')
        else:
            raise TypeError(f'Argument "{arg_name_in_error}": Invalid key type.')

    def validate_name(self, name):
        if name in self._name_to_index:
            raise KeyError(f'Name "{name}" already exists.')

        if not isinstance(name, str):
            raise TypeError(f'Argument "name": Column name "{name}" is not string.')

    def to_list(self):
        return [item.to_dict() for item in self._items]

    @staticmethod
    def raise_key_not_exist_error(arg_name, key):
        raise KeyError(f'Argument "{arg_name}": Key "{key}" does not exist.')

    @staticmethod
    def from_list(json_list, cls):
        if not isinstance(json_list, list):
            raise TypeError(f'List required, got "{type(json_list)}"')
        vals = LabeledList()
        for item in json_list:
            obj = cls.from_dict(item)
            vals.append(obj.name, obj)
        return vals

    @staticmethod
    def from_items(items):
        vals = LabeledList()
        for item in items:
            vals.append(item.name, item)
        return vals
