# coding=utf8

class BaseDPart(object):
    name = "BasePart"
    host = '127.0.0.1'
    port = 15000
    pass


class PP(BaseDPart):
    name = "PP"
    host = 'pp.ai.home.tokgo.cn'
    port = 15001
    pass


class SF(BaseDPart):
    name = "SF"
    host = 'sf.ai.home.tokgo.cn'
    port = 15002
    pass


class AL(BaseDPart):
    name = "AL"
    host = 'al.ai.home.tokgo.cn'
    port = 15003
    pass


class MB(BaseDPart):
    name = "MB"
    host = 'mb.ai.home.tokgo.cn'
    port = 15004
    pass


class EXT(BaseDPart):
    name = "EXT"
    host = 'ext.ai.home.tokgo.cn'
    port = 15005
    pass


class EV(BaseDPart):
    name = "EV"
    host = 'ev.ai.home.tokgo.cn'
    port = 15006
    pass


class MP(BaseDPart):
    name = "MP"
    host = 'mp.ai.home.tokgo.cn'
    port = 15007
    pass
