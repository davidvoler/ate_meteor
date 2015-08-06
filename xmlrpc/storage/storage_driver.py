from jsonstore.store import EntryManager
from tornado.options import options


class StorageDriver(object):
    def __init__(self):
        self.em = EntryManager(options.storage_file_name)

    def create_default(self):
        return {
            'class_path': '',
            'yaml_path': ''
        }

    def get_tf_info(self):
        res = self.em.search(type='tf_info')
        if len(res) <= 0:
            info = self.em.create(type='tf_info',
                                  class_path='',
                                  yaml_path='')
            return info
        else:
            info = res[0]
            return info

    def save_tf_info(self, tf_info_d):
        res = self.em.search(type='tf_info')
        if len(res) <= 0:
            info = self.em.create(type='tf_info',
                                  class_path=tf_info_d['class_path'],
                                  yaml_path=tf_info_d['yaml_path'])
            return info
        else:
            info = self.em.update(tf_info_d, res[0])
            return info

    def list_profiles(self):
        res = self.em.search(type='profile')
        return res

    def delete_profile(self, id):
        res = self.em.delete(id)
        return res

    def create_profile(self, profile):
        res = self.em.create(profile)
        return res

    def update_profile(self, profile):
        res = self.em.search(type='profile', __id__=profile['__id__'])
        if len(res) <= 0:
            return self.create_profile(profile)
        else:
            updated_profile = self.em.update(profile, res[0])
            return updated_profile

    def list_groups(self):
        res = self.em.search(type='group')
        return res

    def delete_group(self, id):
        res = self.em.delete(id)
        return res

    def create_group(self, group):
        res = self.em.create(group)
        return res

    def update_group(self, group):
        res = self.em.search(type='group', __id__=group['__id__'])
        if len(res) <= 0:
            return self.create_group(group)
        else:
            updated_group = self.em.update(group, res[0])
            return updated_group

    def create_object(self, key, value):
        value['type'] = key
        res = self.em.create(value)
        return res

    def get_object(self, key):
        return self.em.search(type=key)[0]

    def delete_object(self, key):
        doc = self.em.search(type=key)[0]
        return self.em.delete(doc['__id__'])


storage_driver = None


def get_storage_driver():
    global storage_driver
    if not storage_driver:
        storage_driver = StorageDriver()
    return storage_driver
