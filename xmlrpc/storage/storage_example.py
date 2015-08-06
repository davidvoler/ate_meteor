__author__ = 'davidl'

from jsonstore.store import EntryManager
import datetime


def get_tf_info():
    em = EntryManager('../../tf.db')
    res = em.search(type='tf_info')
    if len(res) <= 0:
        r = em.create(type='tf_info', class_path='tf.hor.hr.ForCor', updated=str(datetime.datetime.now()))
        return r
    else:
        info = res[0].copy()
        info['updated'] = str(datetime.datetime.now())
        em.update(info, res[0])
        return info
