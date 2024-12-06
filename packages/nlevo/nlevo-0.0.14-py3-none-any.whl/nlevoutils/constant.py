# Remocon Type
IR = "ir"
BT = "bt"
LCD = "lcd"

ADB = "adb"
SSH = "ssh"

STATUS_IDLE = "idle"
STATUS_CAPTURING = "capturing"
STATUS_STREAMING = "streaming"
STATUS_COPY = "copy"
STATUS_PROCESS = "process"

# config
KEY_HW_CONFIG = "hardware_configuration"
KEY_COMMON_CONFIG = "common"
KEY_DEVICES_CONFIG = "devices"
KEY_CAPTURE_BOARD_CONFIG = "capture"
KEY_STREAMING_CONFIG = "streaming"
KEY_RECORDING_CONFIG = "recording"
KEY_NETWORK_CONFIG = "network"

KEY_TARGET_CONNECTION_INFO = "device_connection_info"
KEY_TARGET_STATUS_INFO = "device_status_info"
KET_ON_OFF_INFO = "on_off_info"
KEY_SYSTEM_STATUS_INFO = "status_info"

SSH_PORT = "ssh_port"
PRIVATE_IP = "private_ip"
PUBLIC_IP = "public_ip"
GATEWAY_IP = "gateway_ip"
DUT_IP = "dut_ip"
DUT_MAC = "dut_mac"
DUT_NET_STATE = "dut_net_state"
# COMMON fields
TIMEZONE = "timezone"
ROOT_FILE_PATH = "root_file_path"
# DEVICE fields
SERIAL_BAUD_RATE = "serial_baud_rate"
IR_REMOCON_PORT = "ir_remocon_port"
BT_REMOCON_PORT = "bt_remocon_port"
LCD = "lcd"
# CAPTURE fields
VIDEO_DEVICE = "video_device"
AUDIO_DEVICE = "audio_device"
WIDTH = "width"
HEIGHT = "height"
FPS = "fps"
AUDIO_GAIN = "audio_gain"
# STREAMING fields
RTSP_PUBLISH_URL = "rtsp_publish_url"
RTSP_PUBLISH_PORT = "rtsp_publish_port"
STREAMING_URL = "streaming_url"
WEBRTC_PORT = "webrtc_port"
HLS_PORT = "hls_port"
STREAMING_NAME = "streaming_name"
CRF = "crf"
# RECORDING fields
MAX_RECORDING_INTERVAL = "max_recording_interval"
SEGMENT_INTERVAL = "segment_interval"
# NETWORK fields
BR_NIC = "br_nic"
WAN_NIC = "wan_nic"
STB_NIC = "stb_nic"
STB_WAN_NIC = "stb_wan_nic"
STB_LAN_NIC = "stb_lan_nic"
ROTATION_INTERVAL = "rotation_interval"
PROVIDER = "provider"

# TARGET_CONNECTION_INFO
TARGET_MODE = "target_mode"
TARGET_HOST = "target_host"
TARGET_PORT = "target_port"
TARGET_USERNAME = "target_username"
TARGET_PASSWORD = "target_password"
TARGET_DURATION = "target_duration"

# TARGET_STATUS_INFO
TARGET_NAME = "target_name"
TARGET_MAC = "target_mac"
TARGET_IP = "target_ip"
TARGET_MODEL = "target_model"
TARGET_FIRMWARE_VER = "target_firmware_ver"
TARGET_UI_VER = "target_ui_ver"

# ON_OFF_INFO
DUT_POWER_TRANSIT = "enable_dut_power_transition"
DUT_HDMI_TRANSIT = "enable_dut_hdmi_transition"
DUT_WAN_TRANSIT = "enable_dut_wan_transition"
SENSOR_TIME = "sensor_time"

# SYSTEM_STATUS_INFO fields
REMOTE_CONTROL_TYPE = "remote_control_type"

COM_CPU_USAGE = "com_cpu_usage"
COM_RAM_USAGE = "com_ram_usage"
COM_SSD_USAGE = "com_ssd_usage"
SOM_CPU_USAGE = "som_cpu_usage"
SOM_RAM_USAGE = "som_ram_usage"
SOM_SSD_USAGE = "som_ssd_usage"
COM_TEMP_STATUS = "com_temperature"
SOM_TEMP_STATUS = "som_temperature"
MDIN_TEMP_STATUS = "mdin_temperature"

STREAMING_STATUS = "streaming"
RECORDING_STATUS = "recording"
CAPTURE_STATUS = "capture"
BT_STATUS = "bt"
BT_MAC = "bt_mac"
IR_STATUS = "ir"
NETWORK_STATUS = "network"

DUT_POWER = "enable_dut_power"
DUT_HDMI = "enable_dut_hdmi"
DUT_WAN = "enable_dut_wan"
DUT_LAN = "enable_dut_lan"
DUT_PWR = "enable_dut_power"

DNLD_LIMIT = "enable_download_limit"
UPLD_LIMIT = "enable_upload_limit"
PCKT_BLOCK = "enable_packet_block"

PACKET_DOWNLOAD = "download"
PACKET_UPLOAD = "upload"
PACKET_FILTER = "filter"
PACKET_BANDWIDTH = "packet_bandwidth"
PACKET_DELAY = "packet_delay"
PACKET_LOSS = "packet_loss"
PACKET_BLOCKS = "packet_blocks"

LOG_COLLECTOR_STATUS = "log_collector"
SHELL_STATUS = "shell"
SERVICE_STATUS = "service_status"

CONNECTED = "connected"
CONNECTING = "connecting"
DISCONNECTED = "disconnected"
STOP = "stop"


class ServiceType:
    SVC_CORE = "core"
    SVC_BACKEND = "backend"
    SVC_DEVCTRL = "devctrl"
    SVC_NETCTRL = "netctrl"
    SVC_BLOCKPARSER = "block_parser"
    SVC_MEDIA = "media"
    SVC_MONITORING = "monitoring"
    SVC_LOG_COLLECTOR = "log_collector"
    SVC_SHELL = "shell"
    SVC_NETCAP = "netcap"
    SVC_ANALYSIS = "analysis"


class MessageType:
    SETUP_REQ = "setup"
    SETUP_RESP = "setup_response"
    CONNECT_REQ = "connect"
    CONNECT_RESP = "connect_response"
    CONFIG_REQ = "config"
    CONFIG_RESP = "config_response"
    COMMAND_REQ = "command"
    COMMAND_RESP = "command_response"
    REFRESH_REQ = "refresh"
    REFRESH_RESP = "refresh_response"
    PACKET_CAPTURE_REQ = "packet_capture"
    PACKET_CAPTURE_RESP = "packet_capture_response"
    MEDIA_MODE_REQ = "media_mode"
    MEDIA_MODE_RESP = "media_mode_response"
    ON_OFF_CONTROL_REQ = "on_off_control"
    ON_OFF_CONTROL_RESP = "on_off_control_response"
    BLUETOOTH_CONNECTION_REQ = "bluetooth_connection"
    BLUETOOTH_CONNECTION_RESP = "bluetooth_connection_response"
    REMOCON_PROPERTIES_REQ = "remocon_properties"
    REMOCON_PROPERTIES_RESP = "remocon_properties_response"
    REMOCON_TRANSMIT_REQ = "remocon_transmit"
    REMOCON_TRANSMIT_RESP = "remocon_transmit_response"
    NETWORK_EMULATION_REQ = "network_emulation"
    NETWORK_EMULATION_RESP = "network_emulation_response"
    NETWORK_EMULATION_BATCH_REQ = "network_emulation_batch"
    NETWORK_EMULATION_BATCH_RESP = "network_emulation_batch_response"
    MONITORING_CONFIG_REQ = "monitoring_config"
    MONITORING_CONFIG_RESP = "monitoring_config_response"
    MONITORING_CONTROL_REQ = "monitoring_control"
    MONITORING_CONTROL_RESP = "monitoring_control_response"
    LOUDNESS_RESP = "loudness_response"
    SMF_RESP = "smf_response"
    NETWORK_STATUS_RESP = "network_status_response"
    ADB_LOGCAT_RESP = "adb_logcat_response"
    STB_RESOURCE_RESP = "stb_resource_response"
    ANALYSIS_PROGRESS = "analysis_progress"


class Exchange:
    NOT_EXCHANGE = ""
    BACKEND_TO_CORE = "x.back.core"
    BLOCK_TO_CORE = "x.block.core"
    MODULE_TO_CORE = "x.act.core"
    TO_BACKEND = "x.backend"

    FOR_SYSTEM_SETUP = "x.system.setup"
    FOR_STB_ACT = "x.stb"
    FOR_CAPTURE_ACT = "x.capture.action"
    FOR_RECORDING_ACT = "x.recording.action"
    FOR_MEDIA_ACT = "x.media"
    FOR_DEVICE_ACT = "x.device.control"
    FOR_MONITORING_ACT = "x.monitoring"
    FOR_SMF_ACT = "x.analysis.action"


class RoutingKey:
    # 초기 설정 값 요청 (core\exam_msg\setup.json)
    SETUP_REQ = "req.setup.conf"
    # 설정 값 응답 (core\exam_msg\setup_response.json)
    SETUP_RESP = "res.setup.conf"
    # stb 연결 명령 (core\exam_msg\connect.json)
    CONNECT_REQ = "req.stb.ctrl"
    # stb 연결 응답 (core\exam_msg\connect_response.json)
    CONNECT_RESP = "res.stb.ctrl"
    # stb 연결 설정 변경 (core\exam_msg\config.json)
    CONFIG_REQ = "req.stb.conf"
    # stb 연결 설정 응답 (core\exam_msg\config_response.json)
    CONFIG_RESP = "res.stb.conf"
    # stb 명령 (core\exam_msg\command.json)
    COMMAND_REQ = "req.stb.cmd"
    # stb 명령 응답 (core\exam_msg\command_response.json)
    COMMAND_RESP = "res.stb.cmd"
    # capture board 설정 (core\exam_msg\refresh.json)
    REFRESH_REQ = "req.refresh.ctrl"
    # capture board 설정 응답 (core\exam_msg\refresh_response.json)
    REFRESH_RESP = "res.refresh.ctrl"
    # capture 모드 변경 (core\exam_msg\packet_capture.json)
    PACKET_CAPTURE_REQ = "req.capture.ctrl"
    # capture 모드 변경 응답 (core\exam_msg\packet_capture_response.json)
    PACKET_CAPTURE_RESP = "res.capture.ctrl"
    # streaming/recoding 모드 변경 (core\exam_msg\media_mode.json)
    MEDIA_MODE_REQ = "req.media.ctrl"
    # recoding 모드 변경 응답 (core\exam_msg\media_mode_response.json)
    MEDIA_MODE_RESP = "res.media.ctrl"
    # HDMI, LAN 절체 (core\exam_msg\on_off_control.json)
    ON_OFF_CONTROL_REQ = "req.onoff.ctrl"
    # HDMI, LAN 절체 응답 (core\exam_msg\on_off_control_response.json)
    ON_OFF_CONTROL_RESP = "res.onoff.ctrl"
    # BT 연결 명령 (core\exam_msg\bluetooth_connection.json)
    BLUETOOTH_CONNECTION_REQ = "req.btconn.ctrl"
    # BT 연결 명령 응답 (core\exam_msg\bluetooth_connection_response.json)
    BLUETOOTH_CONNECTION_RESP = "res.btconn.ctrl"
    # 리모컨 설정 (core\exam_msg\remocon_properties.json)
    REMOCON_PROPERTIES_REQ = "req.remocon.conf"
    # 리모컨 설정 응답 (core\exam_msg\remocon_properties_response.json)
    REMOCON_PROPERTIES_RESP = "res.remocon.conf"
    # 리모컨 명령 (core\exam_msg\remocon_transmit.json)
    REMOCON_TRANSMIT_REQ = "req.transmit"
    # 리모컨 명령 응답 (core\exam_msg\remocon_transmit_response.json)
    REMOCON_TRANSMIT_RESP = "res.transmit"
    # network 제어 (core\exam_msg\network_emulation.json)
    NETWORK_EMULATION_REQ = "req.emulation.ctrl"
    # network 제어 응답 (core\exam_msg\network_emulation_response.json)
    NETWORK_EMULATION_RESP = "res.emulation.ctrl"
    # network 제어 (core\exam_msg\network_emulation_batch.json)
    NETWORK_EMULATION_BATCH_REQ = "req.batch.ctrl"
    # network 제어 응답 (core\exam_msg\network_emulation_batch_response.json)
    NETWORK_EMULATION_BATCH_RESP = "res.batch.ctrl"
    # 모니터링 설정 변경 (core\exam_msg\monitoring_config.json)
    MONITORING_CONFIG_REQ = "req.mon.conf"
    # 모니터링 설정 변경 응답
    MONITORING_CONFIG_RESP = "res.mon.conf"
    # 모니터링 제어
    MONITORING_CONTROL_REQ = "req.mon.ctrl"
    # 모니터링 제어 응답
    MONITORING_CONTROL_RESP = "res.mon.ctrl"
    # 모니터링 검출 결과
    MONITORING_DETECTED = "sts.mon.detect"
    # Loudness 수치 응답
    LOUDNESS_RESP = "res.loud"
    # SMF 완료 응답
    SMF_RESP = "res.smf"
    # network 상태 응답
    NETWORK_STATUS_RESP = "res.network.stat"
    # 실시간 logcat
    ADB_LOGCAT_RESP = "res.logcat"
    # 실기간 resource
    STB_RESOURCE_RESP = "res.resource"
    # 분석 진행률
    ANALYSIS_PROGRESS = "sts.analysis"
    # SMF 학습 실행
    SMF_CONTROL_REQ = "req.smf.ctrl"
    SMF_CONTROL_RESP = "res.smf.ctrl"
    # GOTO MENU 실행
    GOTO_MENU_REQ = "req.goto.ctrl"
    GOTO_MENU_RESP = "res.goto.ctrl"


class RedisDBEnum:
    DEFAULT: int = 0


class IRState:
    STATE_IDLE = "CURRENT_IR_STAT:1"
    STATE_FREQUENCY_DETECT = "CURRENT_IR_STAT:2"
    STATE_READ_CODE = "CURRENT_IR_STAT:3"
    STATE_IR_SEND = "CURRENT_IR_STAT:4"
