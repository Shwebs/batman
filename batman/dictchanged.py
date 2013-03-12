import os
import ast

OLD_DICT_FILENAME = 'old_dict.txt'

def _old_dict_filename(persist_dir):
    return os.path.join(persist_dir, OLD_DICT_FILENAME)

def _write_old_dict(input, persist_dir):
    with open(_old_dict_filename(persist_dir), 'wc') as f:
        f.write(str(input))

def _load_old_dict(persist_dir):
    try:
        return ast.literal_eval(open(_old_dict_filename(persist_dir)).read())
    except IOError:
        return {}

def _dict_compare(d1, d2):
    """
    We care if one of two things happens:

      * d2 has added a new key
      * a (value for the same key) in d2 has a different value than d1

    We don't care if this stuff happens:

      * A key is deleted from the dict

    Should return a list of keys that either have been added or have a different value than they used to

    """
    keys_added = set(d2.keys()) - set(d1.keys())
    keys_changed = [k for k in d1.keys() if k in d2.keys() and d1[k] != d2[k]]
    return list(keys_added) + keys_changed

def changed_keys(new_dict, persist_dir):
    old_dict = _load_old_dict(persist_dir)
    _write_old_dict(new_dict, persist_dir)
    if old_dict:
        return _dict_compare(old_dict, new_dict)
    else:
        return new_dict.keys()