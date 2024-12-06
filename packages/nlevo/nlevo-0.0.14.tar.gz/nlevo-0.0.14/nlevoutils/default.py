import nlevoutils.constant as const

# KEY_HW_CONFIG
# HW_CONFIG = {
#     const.REMOTE_CONTROL_TYPE: const.IR,
#     const.DUT_POWER: True,
#     const.DUT_HDMI: True,
#     const.DUT_WAN: True,
#     const.ENABLE_NETWORK_EMULATION: True,
#     const.PACKET_BANDWIDTH: 0,
#     const.PACKET_DELAY: 0.0,
#     const.PACKET_LOSS: 0.0,
#     const.PACKET_BLOCKS: [],
#     const.SSH_PORT: 22,
#     const.PRIVATE_IP: "",
#     const.PUBLIC_IP: "",
#     const.GATEWAY_IP: "",
#     const.DUT_IP: "",
#     const.DUT_MAC: "00:00:00:00:00:00",
#     const.DUT_NET_STATE: False
# }
# KEY_COMMON_CONFIG
COMMON_CONFIG = {
    const.TIMEZONE: "Asia/Seoul",
    const.ROOT_FILE_PATH: "./data"
}
# KEY_DEVICES_CONFIG
DEVICES_CONFIG = {
    const.SERIAL_BAUD_RATE: 115200,
    const.IR_REMOCON_PORT: "/dev/ttyUSBIR",
    const.BT_REMOCON_PORT: "/dev/ttyUSBBT",
    const.LCD: True
}
# KEY_CAPTURE_BOARD_CONFIG
CAPTURE_BOARD_CONFIG = {
    const.VIDEO_DEVICE: "/dev/video0",
    const.AUDIO_DEVICE: "hw:1",
    const.WIDTH: 1920,
    const.HEIGHT: 1080,
    const.FPS: 60,
    const.AUDIO_GAIN: 90
}
# KEY_STREAMING_CONFIG
STREAMING_CONFIG = {
    const.RTSP_PUBLISH_URL: "localhost",
    const.RTSP_PUBLISH_PORT: 8554,
    const.STREAMING_URL: "localhost",
    const.WEBRTC_PORT: 8889,
    const.HLS_PORT: 8888,
    const.STREAMING_NAME: "live",
    const.CRF: 23
}
# KEY_RECORDING_CONFIG
RECORDING_CONFIG = {
    const.MAX_RECORDING_INTERVAL: 14400,
    const.SEGMENT_INTERVAL: 10
}
# KEY_NETWORK_CONFIG
NETWORK_CONFIG = {
    const.BR_NIC: "br0", # Fixed?
    const.WAN_NIC: "eth-wan",
    const.STB_NIC: "eth-stb-wan",
    const.STB_LAN_NIC: "eth-stb-lan",
    const.STB_WAN_NIC: "eth-stb-wan",
    const.SEGMENT_INTERVAL: 10,
    const.ROTATION_INTERVAL: 1800,
    const.PROVIDER: "sk"
}
# KEY_TARGET_CONNECTION_INFO
TARGET_CONNECTION_INFO = {
    const.TARGET_MODE: const.ADB,
    const.TARGET_HOST: "",
    const.TARGET_PORT: 0,
    const.TARGET_USERNAME: "",
    const.TARGET_PASSWORD: "",
    const.TARGET_DURATION: 10
}
# KEY_TARGET_STATUS_INFO
TARGET_STATUS_INFO = {
    const.TARGET_NAME: "",
    const.TARGET_MAC: "00:00:00:00:00:00",
    const.TARGET_IP: "",
    const.TARGET_MODEL: "",
    const.TARGET_FIRMWARE_VER: "",
    const.TARGET_UI_VER: ""
}
# KET_ON_OFF_INFO
ON_OFF_INFO = {
    const.DUT_POWER_TRANSIT: False,
    const.DUT_HDMI_TRANSIT: False,
    const.DUT_WAN_TRANSIT: False,
    const.SENSOR_TIME: 0
}
# KEY_SYSTEM_STATUS_INFO
SYSTEM_STATUS_INFO = {
    # System Status
    # idle = "streaming" /service_state "blockparser"
    # "analyzing"/"streaming"/"recording"
    const.SERVICE_STATUS: const.STREAMING_STATUS,
    
    const.REMOTE_CONTROL_TYPE: const.IR,

    const.COM_TEMP_STATUS: 0,
    const.SOM_TEMP_STATUS: 0,
    const.MDIN_TEMP_STATUS: 0,

    const.COM_CPU_USAGE: 0,
    const.COM_RAM_USAGE: 0,
    const.COM_SSD_USAGE: 0,
    const.SOM_CPU_USAGE: 0,
    const.SOM_RAM_USAGE: 0,
    const.SOM_SSD_USAGE: 0,

    # Capture Board Status(Media)
    const.STREAMING_STATUS: const.STATUS_IDLE,  # STATUS_STREAMING
    const.RECORDING_STATUS: const.STATUS_IDLE,  # STATUS_COPY/STATUS_PROCESS

    # Network Capture Status(NetCap)
    const.CAPTURE_STATUS: const.STATUS_IDLE,  # STATUS_CAPTURING

    # Network Control Config(NetCtrl)
    const.DUT_POWER: True,
    const.DUT_HDMI: True,
    const.DUT_WAN: True,
    const.DUT_LAN: True,
    const.DUT_PWR: True,
    
    # Network Emulation(NetCtrl)
    const.DNLD_LIMIT: True,
    const.UPLD_LIMIT: True,
    const.PCKT_BLOCK: True,
    const.NETWORK_STATUS: {
        const.PACKET_DOWNLOAD: {
            const.PACKET_BANDWIDTH: 1000.0,
            const.PACKET_DELAY: 0.0,
            const.PACKET_LOSS: 0.0
        },
        const.PACKET_UPLOAD: {
            const.PACKET_BANDWIDTH: 1000.0,
            const.PACKET_DELAY: 0.0,
            const.PACKET_LOSS: 0.0
        }
    },
    const.PACKET_BLOCKS: [],

    # IR Remocon Status(DevCtrl)
    const.IR_STATUS: const.IRState.STATE_IDLE,

    # Bluetooth connection status(DevCtrl)
    const.BT_STATUS: const.DISCONNECTED,
    const.BT_MAC: "",

    # Log Collector status(LogCollector)
    # /log_connection_status const.CONNECTING/const.CONNECTED
    const.LOG_COLLECTOR_STATUS: const.DISCONNECTED,

    # Shell(LogCollector)
    const.SHELL_STATUS: const.DISCONNECTED,

    const.PRIVATE_IP: ""
}
