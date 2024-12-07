from ats_base.common import func

from ats_base.service import pro, em
from ats_case.case import base, asb
from ats_case.case.context import Context
from ats_case.common.error import MeterSecurityAuthenticationError


def establish(context: Context, protocol: str):
    exec('_{}(context, protocol)'.format(protocol))


def _gw698(context: Context, protocol: str, retry_times=3):
    try:
        # 1. 读取esam参数
        result = pro.encode(
            func.to_dict(protocol=protocol, comm_addr=context.meter.addr,
                         operation='get:request:normal_list',
                         element=['F1000200', 'F1000300', 'F1000400', 'F1000500', 'F1000600', 'F1000700'],
                         session_key=context.test_sn))
        frame = base.write(context, result.get('frame'))
        data = pro.decode(func.to_dict(protocol=protocol, frame=frame, session_key=context.test_sn))
        # 2. 协商密钥
        e_r = data.get('result')
        e_r['session_key'] = context.test_sn
        em.handle(protocol, 'negotiate', e_r)
        # 3. 连接
        result = pro.encode(
            func.to_dict(protocol=protocol, comm_addr=context.meter.addr,
                         operation='connect:request:symmetry',
                         element='',
                         parameter={
                             '期望的应用层协议版本号': 21,
                             '期望的协议一致性块': 'FFFFFFFFC0000000',
                             '期望的功能一致性块': 'FFFEC400000000000000000000000000',
                             '客户机发送帧最大尺寸(字节)': 512,
                             '客户机接收帧最大尺寸(字节)': 512,
                             '客户机接收帧最大窗口尺寸(个)': 1,
                             '客户机最大可处理APDU尺寸': 2000,
                             '期望的应用连接超时时间(秒)': 7200,
                             '认证请求对象': {
                                 '对称加密': {
                                     '密文1': asb.Session.get(context, 'em_data'),
                                     '客户机签名1': asb.Session.get(context, 'em_mac')
                                 }
                             }
                         },
                         session_key=context.test_sn))
        frame = base.write(context, result.get('frame'))
        data = pro.decode(func.to_dict(protocol=protocol, frame=frame, session_key=context.test_sn))
        # 4. 加密
        e_r = data.get('result')
        e_r['session_key'] = context.test_sn
        em.handle(protocol, 'secret', e_r)
        base.sleep(1)
    except Exception as e:
        retry_times -= 1
        if retry_times <= 0:
            raise MeterSecurityAuthenticationError('[表位:{}]{}'.format(context.meter.pos, str(e)))
        else:
            base.sleep(5)
            _gw698(context, protocol, retry_times)


def _dlms(context: Context, protocol: str, retry_times=3):
    try:
        # 1. snrm
        result = pro.encode(
            func.to_dict(protocol=protocol, comm_addr=context.meter.addr,
                         operation='snrm',
                         element='',
                         session_key=context.test_sn))
        frame = base.write(context, result.get('frame'))
        pro.decode(func.to_dict(protocol=protocol, frame=frame, session_key=context.test_sn))
        # 2. aarq
        result = pro.encode(
            func.to_dict(protocol=protocol, comm_addr=context.meter.addr,
                         operation='aarq',
                         element='',
                         parameter={
                             '应用上下文名': 'LN_Referencing_With_Ciphering',
                             '加密机制': 'HIGH_GMAC',
                             '用户信息': {
                                 '安全控制': 'SC_AE',
                                 '计数器': 0,
                                 '初始化': {
                                     '一致性提议': {'引用类型': 'LN_REFERENCING_PROPOSED'}
                                 }
                             }
                         },
                         session_key=context.test_sn))
        frame = base.write(context, result.get('frame'))
        pro.decode(func.to_dict(protocol=protocol, frame=frame, session_key=context.test_sn))
        # 3. rlrq
        result = pro.encode(
            func.to_dict(protocol=protocol, comm_addr=context.meter.addr,
                         operation='action:request:normal',
                         element={"000F0000280000FF01": "XXXXXXXX"},
                         session_key=context.test_sn))
        frame = base.write(context, result.get('frame'))
        pro.decode(func.to_dict(protocol=protocol, frame=frame, session_key=context.test_sn))
        base.sleep(1)
        # {'应用上下文名': 'LN_Referencing_No_Ciphering', '加密机制': 'LOW', '用户信息': {'初始化': {'一致性提议': {'引用类型':
        # 'LN_REFERENCING_PROPOSED'}}}}
    except Exception as e:
        retry_times -= 1
        if retry_times <= 0:
            raise MeterSecurityAuthenticationError('[表位:{}]{}'.format(context.meter.pos, str(e)))
        else:
            base.sleep(5)
            _dlms(context, protocol, retry_times)


def _dlt645(context: Context, retry_times=3):
    pass


def _cjt188(context: Context, retry_times=3):
    pass
