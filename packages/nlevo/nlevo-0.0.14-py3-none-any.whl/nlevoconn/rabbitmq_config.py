from os import environ
from nlevoutils.constant import Exchange as x, RoutingKey as key


class RabbitMQConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False

        return cls._instance

    def __init__(self, override=False):
        if self.__initialized and not override:
            return

        self.RABBITMQ_HOST = environ.get('RABBITMQ_HOST', 'localhost')
        self.RABBITMQ_PORT = environ.get('RABBITMQ_PORT', 5672)
        self.RABBITMQ_USER = environ.get('RABBITMQ_USER', 'guest')
        self.RABBITMQ_PASSWORD = environ.get('RABBITMQ_PASSWORD', 'guest')

        self.CORE_BINDING_INFO = {x.BACKEND_TO_CORE: [key.SETUP_RESP,
                                                      key.CONNECT_REQ,
                                                      key.COMMAND_REQ,
                                                      #   key.REFRESH_REQ,
                                                      #   key.PACKET_CAPTURE_REQ,
                                                      #   key.MEDIA_MODE_REQ,
                                                      key.ON_OFF_CONTROL_REQ,
                                                      key.BLUETOOTH_CONNECTION_REQ,
                                                      key.REMOCON_PROPERTIES_REQ,
                                                      key.REMOCON_TRANSMIT_REQ,
                                                      key.NETWORK_EMULATION_REQ,
                                                      key.NETWORK_EMULATION_BATCH_REQ,
                                                      key.MONITORING_CONFIG_REQ,
                                                      key.MONITORING_CONTROL_REQ],
                                  x.MODULE_TO_CORE: [key.SETUP_REQ,
                                                     key.CONNECT_RESP,
                                                     key.COMMAND_RESP,
                                                     #  key.PACKET_CAPTURE_RESP,
                                                     #  key.MEDIA_MODE_RESP,
                                                     #  key.REFRESH_RESP,
                                                     key.ON_OFF_CONTROL_RESP,
                                                     key.BLUETOOTH_CONNECTION_RESP,
                                                     key.REMOCON_PROPERTIES_RESP,
                                                     key.REMOCON_TRANSMIT_RESP,
                                                     key.NETWORK_EMULATION_RESP,
                                                     key.NETWORK_EMULATION_BATCH_RESP,
                                                     key.MONITORING_CONFIG_RESP,
                                                     key.MONITORING_CONTROL_RESP,
                                                     #  key.MONITORING_DETECTED,
                                                     key.NETWORK_STATUS_RESP,
                                                     key.ADB_LOGCAT_RESP,
                                                     key.STB_RESOURCE_RESP]}
        self.BACKEND_BINDING_INFO = {x.TO_BACKEND: [key.SETUP_REQ,
                                                    key.CONNECT_RESP,
                                                    key.COMMAND_RESP,
                                                    # key.PACKET_CAPTURE_RESP,
                                                    # key.MEDIA_MODE_RESP,
                                                    # key.REFRESH_RESP,
                                                    key.ON_OFF_CONTROL_RESP,
                                                    key.BLUETOOTH_CONNECTION_RESP,
                                                    key.REMOCON_PROPERTIES_RESP,
                                                    key.REMOCON_TRANSMIT_RESP,
                                                    key.NETWORK_EMULATION_RESP,
                                                    key.NETWORK_EMULATION_BATCH_RESP,
                                                    key.MONITORING_CONFIG_RESP,
                                                    key.MONITORING_CONTROL_RESP,
                                                    key.MONITORING_DETECTED,
                                                    key.CONFIG_RESP,
                                                    key.LOUDNESS_RESP,
                                                    key.SMF_RESP,
                                                    key.NETWORK_STATUS_RESP,
                                                    key.ADB_LOGCAT_RESP,
                                                    key.STB_RESOURCE_RESP,
                                                    key.ANALYSIS_PROGRESS,
                                                    key.SMF_CONTROL_RESP,
                                                    key.GOTO_MENU_RESP]}
        self.NETWORK_CAPTURE_BINDING_INFO = {
            x.FOR_SYSTEM_SETUP: [key.SETUP_RESP]}
        self.NETWORK_CONTROL_BINDING_INFO = {x.FOR_SYSTEM_SETUP: [key.SETUP_RESP],
                                             x.FOR_DEVICE_ACT: [key.NETWORK_EMULATION_REQ,
                                                                key.NETWORK_EMULATION_BATCH_REQ]}
        self.DEVICE_CONTROL_BINDING_INFO = {x.FOR_SYSTEM_SETUP: [key.SETUP_RESP],
                                            x.FOR_DEVICE_ACT: [key.ON_OFF_CONTROL_REQ,
                                                               key.BLUETOOTH_CONNECTION_REQ,
                                                               key.REMOCON_PROPERTIES_REQ,
                                                               key.REMOCON_TRANSMIT_REQ]}
        self.MEDIA_BINDING_INFO = {x.FOR_SYSTEM_SETUP: [key.SETUP_RESP]}
        self.LOG_COLLECTOR_BINDING_INFO = {x.FOR_SYSTEM_SETUP: [key.SETUP_RESP],
                                           x.FOR_STB_ACT: [key.CONNECT_REQ,
                                                           key.COMMAND_REQ]}
        self.ANALYSIS_BINDING_INFO = {x.FOR_SYSTEM_SETUP: [key.SETUP_RESP],
                                      x.FOR_SMF_ACT: [key.SMF_CONTROL_REQ,
                                                      key.GOTO_MENU_REQ]}
        self.MONITORING_BINDING_INFO = {x.FOR_SYSTEM_SETUP: [key.SETUP_RESP],
                                        x.FOR_MONITORING_ACT: [key.MONITORING_CONFIG_REQ,
                                                               key.MONITORING_CONTROL_REQ]}

        self.__initialized = True
