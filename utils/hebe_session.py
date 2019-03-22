# -*- coding: utf-8 -*-
'''
@File  : cache_util.py
@Date  : 19-3-12 下午6:33
'''
import time
from config.config import cache
from utils.sqls import ConMysql
from config.config import SESSION_CACHE_KEY, SESSION_UID_CACHE_KEY, \
    UID_UDID_CACHE_KEY

class HebeSession(object):
    def __init__(self, db: ConMysql):
        self.db = db

    def get_session_id_from_db(self, user_id):
        """

        :param user_id:
        :return:
        """
        sql = '''
        SELECT *
        FROM user_session
        WHERE user_id=%s
        ''' % user_id
        row = self.db.query_one(sql)
        if row:
            return row['session_id']
        return None

    def get_session_uid_cache(self, uid):
        return cache('session').get(SESSION_UID_CACHE_KEY % uid)

    def get_session_by_uid(self, uid, cache_flag):
        """

        :param uid:
        :param cache_flag:
        :return: dict
        """
        if cache_flag:
            rv = self.get_session_uid_cache(uid)
            if rv:
                return rv

        sid = self.get_session_id_from_db(uid)
        if sid:
            if cache_flag:
                self.set_session_uid_cache(uid, sid)
            return {'sid': sid}
        return dict()

    def set_session_uid_cache(self, uid, sid):
        cache('session').set(SESSION_UID_CACHE_KEY % uid,
                             {'sid': sid}, timeout=30 * 86400)

    def insert_user_session(self, uid, sid):
        sql = '''
        INSERT INTO user_session
        (user_id, session_id, create_time)
        VALUES
        (%(uid)s, %(sid)s, %(now)s)
        ''' % {
            "uid": uid,
            "sid": sid,
            "now": int(time.time())
        }
        self.db.execute_sql(sql)

    def update_session_by_uid(self, uid, sid):
        sql = '''
        UPDATE user_session
        SET session_id='%(sid)s'
        WHERE user_id=%(uid)s
        ''' % {
            "sid": sid,
            "uid": uid
        }
        self.db.execute_sql(sql)

    def set_user_session(self, uid, sid):
        rv = self.get_session_by_uid(uid, cache_flag=False)
        if rv:
            self.update_session_by_uid(uid, sid)
        else:
            # 根据sessionid 把之前的对应删除，然后再插入
            p = dict(session_id=sid)
            sql = """
                    DELETE FROM user_session 
                    WHERE session_id = '%s'
                """ % p
            self.db.execute_sql(sql)
            self.insert_user_session(uid, sid)
        self.set_session_uid_cache(uid, sid)

    def get_session_info(self, sid):
        """
        :param sid: SessionID
        :return: {'uid','udid'}
        """
        if not sid:
            raise Exception('sid error: no sid')

        data = self.get_sid_info(sid)
        if not data:
            rv = self.get_session_by_sid(sid)
            if rv:
                uid = rv.get("user_id","")
                value = {'udid': '', 'uid': uid}
                self.set_sid_info_cache(sid=sid, udid='', uid=uid)
                self.set_user_session(uid, sid)
                return value
            return dict()
        return data

    def get_session_by_sid(self, sid):
        sql = '''
        SELECT * FROM user_session
        WHERE session_id='%s'
        ORDER BY update_time DESC
        ''' % sid
        rs = self.db.query_one(sql)
        return rs

    def get_device_info_by_uid(self, user_id):
        """

        :param user_id:
        :return:
        """
        sql = """
            SELECT * FROM user_match
            WHERE user_id = %s
            ORDER BY id DESC LIMIT 1
            """ % user_id
        rv = self.db.query_one(sql)
        return rv

    def get_sid_info_from_db(self, sid):
        """

        :param sid:
        :return: dict
        """
        info = dict()
        # 先获取session
        db_session = self.get_session_by_sid(sid)
        if not db_session:
            return info

        uid = db_session['user_id']
        info['user_id'] = uid

        # 用户登录时， 不应该从数据库里补udid。
        # udid是和用户设备相关的，例如用户在A设备和在B设备，udid是不一样的，
        # 所以用户重新登录时，让用户重新绑定证书一次是应该的

        # # 查找udid
        # info['udid'] = get_udid_by_uid(uid)

        # idfa
        device = self.get_device_info_by_uid(uid)
        info['idfa'] = ''
        if device:
            info['idfa'] = device['idfa']

        return info

    def set_uid_udid_cache(self, uid, udid):
        cache('session').set(UID_UDID_CACHE_KEY %
                             uid, udid, timeout=30 * 86400)

    def set_sid_info_cache(self, sid, udid, uid, **kwargs):
        value = {'udid': udid, 'uid': uid}
        idfa = kwargs.get('idfa', None)
        if idfa:
            value['idfa'] = idfa
        return cache('session').set(SESSION_CACHE_KEY % sid,
                                    value, timeout=365 * 86400)

    def get_sid_info_cache(self, sid):
        return cache('session').get(SESSION_CACHE_KEY % sid)

    def update_uid_udid(self, cached_uid, sid, udid):
        sqla = """
            insert into t_dieid_uid (uid, dieid) 
            VALUES (%(uid)s, '%(udid)s') 
            ON DUPLICATE KEY 
            UPDATE dieid = '%(udid)s', uid = %(uid)s;
        """ % {
            'uid': cached_uid,
            'udid': udid
        }
        # sqla = """
        #     insert into t_dieid_uid (uid, dieid)
        #     VALUES (%(uid)s, %(udid)s)
        #     ON DUPLICATE
        #     KEY UPDATE dieid = %(udid)s, uid = %(uid)s;
        #     """ % {
        #     "uid": cached_uid,
        #     "udid": udid
        # }
        cnt = self.db.execute_sql(sqla)
        print("cnt______________->>>>%s" % cnt)
        if cnt > 0:
            # 有变更时记录下来
            sqlb = """
                    insert into v4_uid_udid_log (uid, udid, sid) 
                    VALUES (%(uid)s, '%(udid)s', '%(sid)s');
                 """ % {
                "uid": cached_uid,
                "udid": udid,
                "sid": sid
            }
            self.db.execute_sql(sqlb)
            self.set_uid_udid_cache(cached_uid, udid)
        return cnt

    def get_sid_info(self, sid):
        # from cache
        rv = self.get_sid_info_cache(sid)
        if rv:
            return rv

        # from db
        rv = self.get_sid_info_from_db(sid)
        if rv:
            udid = rv.get('udid', '')
            user_id = rv.get('user_id', 0)
            idfa = rv.get('idfa', '')
            # set cache
            self.set_sid_info_cache(
                sid=sid,
                udid=udid,
                uid=user_id,
                idfa=idfa
            )
            return {
                'sid': sid,
                'udid': udid,
                'uid': user_id,
                'idfa': idfa
            }

        return {}

    def bind_sid_udid(self, sid, udid):
        """
        绑定 SessionID, UDID
        redis 记录
        db 记录
        log 记录
        :return:
        """
        idfa="A624A1D7-E227-431A-8413-E50638B56C0A"
        if not udid or not sid:
            return False

        session_info = self.get_sid_info(sid)
        if not session_info:
            # 若 session_info 不存在，则直接保存到 cache 并返回
            return self.set_sid_info_cache(sid=sid, udid=udid, uid=0)

        cached_udid = session_info.get('udid', '')
        if udid and cached_udid == udid:
            # 若 已经缓存中 UDID 与当前相同，则不做处理
            return True

        cached_uid = session_info.get('uid', 0)
        """
        CHANGE LOG
            2019-03-11
            绑定证书时，idfa关系保持。用户在更换设备关系时，证书需要重新绑定，
            但是绑定证书时如果没有保留设备和用户关系就会死循环
        """
        cache_idfa = session_info.get('idfa',"")
        if cached_uid:
            # 若 缓存中已存在 uid，则记录当前 uid 和 udid 关系到数据库，缓存并返回
            self.update_uid_udid(cached_uid, sid, udid)
            return self.set_sid_info_cache(sid=sid, udid=udid,
                                                     uid=cached_uid,
                                                     idfa=cache_idfa)
        return self.set_sid_info_cache(sid=sid, udid=udid, uid=0,
                                                 idfa=cache_idfa)
print(cache('session').get(SESSION_CACHE_KEY%"9b21a3ff5b4346f68f1b9a53ba7e5e34"))