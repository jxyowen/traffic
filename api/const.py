
class GeneratorEnum():
    STATUS_IDLE = 'idle'
    STATUS_TRANSMITITING = 'transmititing'
    STATUS_ERROR = 'error'

    MODE_NORMAL = 'normal'
    MODE_LOOP = 'loop'


class SwitchEnum():
    TYPE_HUAWEI = 'huawei'
    TYPE_H3C = 'h3c'


class VLANEnum():
    MODE_NONE = 'none'
    MODE_ACCESS = 'access'
    MODE_TRUNK = 'trunk'
    MODE_HYBRID = 'hybrid'

    STATUS_IDLE = 'idle'
    STATUS_USED = 'used'

    TRAFFIC_OFF = 'off'
    TRAFFIC_ON = 'on'
