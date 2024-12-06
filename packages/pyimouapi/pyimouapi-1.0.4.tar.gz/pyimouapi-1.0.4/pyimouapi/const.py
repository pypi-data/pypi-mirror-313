# API Endpoints
API_ENDPOINT_ACCESS_TOKEN = "/openapi/accessToken"
API_ENDPOINT_LIST_DEVICE_DETAILS = "/openapi/listDeviceDetailsByPage"
API_ENDPOINT_CONTROL_DEVICE_PTZ = "/openapi/controlMovePTZ"
API_ENDPOINT_MODIFY_DEVICE_ALARM_STATUS = "/openapi/modifyDeviceAlarmStatus"
API_ENDPOINT_GET_DEVICE_ALARM_PARAM = "/openapi/getDeviceAlarmParam"
API_ENDPOINT_GET_DEVICE_STATUS = "/openapi/getDeviceCameraStatus"
API_ENDPOINT_SET_DEVICE_STATUS = "/openapi/setDeviceCameraStatus"
API_ENDPOINT_GET_DEVICE_NIGHT_VISION_MODE = "/openapi/getNightVisionMode"
API_ENDPOINT_SET_DEVICE_NIGHT_VISION_MODE = "/openapi/setNightVisionMode"
API_ENDPOINT_DEVICE_STORAGE = "/openapi/deviceStorage"
API_ENDPOINT_RESTART_DEVICE = "/openapi/restartDevice"
API_ENDPOINT_BIND_DEVICE_LIVE = "/openapi/bindDeviceLive"
API_ENDPOINT_GET_DEVICE_ONLINE = "/openapi/deviceOnline"
API_ENDPOINT_GET_DEVICE_LIVE_INFO = "/openapi/getLiveStreamInfo"
API_ENDPOINT_SET_DEVICE_SNAP = "/openapi/setDeviceSnapEnhanced"
API_ENDPOINT_GET_IOT_DEVICE_PROPERTIES = "/openapi/getIotDeviceProperties"
API_ENDPOINT_SET_IOT_DEVICE_PROPERTIES = "/openapi/setIotDeviceProperties"
API_ENDPOINT_DEVICE_SD_CARD_STATUS = "/openapi/deviceSdcardStatus"

# error_codes
ERROR_CODE_SUCCESS = "0"
ERROR_CODE_TOKEN_OVERDUE = "TK1002"
ERROR_CODE_INVALID_SIGN = "SN1001"
ERROR_CODE_INVALID_APP = "SN1004"
ERROR_CODE_DEVICE_OFFLINE = "DV1007"

# params key
PARAM_APP_ID = "appId"
PARAM_APP_SECRET = "appSecret"
PARAM_SYSTEM = "system"
PARAM_ACCESS_TOKEN = "accessToken"
PARAM_CURRENT_DOMAIN = "currentDomain"
PARAM_DEVICE_ID = "deviceId"
PARAM_CHANNEL_ID = "channelId"
PARAM_VER = "ver"
PARAM_SIGN = "sign"
PARAM_TIME = "time"
PARAM_NONCE = "nonce"
PARAM_PARAMS = "params"
PARAM_ID = "id"
PARAM_RESULT = "result"
PARAM_CODE = "code"
PARAM_MSG = "msg"
PARAM_DATA = "data"
PARAM_PAGE = "page"
PARAM_PAGE_SIZE = "pageSize"
PARAM_TOKEN = "token"
PARAM_PRODUCT_ID = "productId"
PARAM_CHANNEL_NUM = "channelNum"
PARAM_MODE = "mode"
PARAM_ENABLE_TYPE = "enableType"
PARAM_ENABLE = "enable"
PARAM_COUNT = "count"
PARAM_DEVICE_LIST = "deviceList"
PARAM_DEVICE_NAME = "deviceName"
PARAM_DEVICE_STATUS = "deviceStatus"
PARAM_DEVICE_ABILITY = "deviceAbility"
PARAM_DEVICE_VERSION = "deviceVersion"
PARAM_BRAND = "brand"
PARAM_DEVICE_MODEL = "deviceModel"
PARAM_CHANNEL_LIST = "channelList"
PARAM_CHANNEL_NAME = "channelName"
PARAM_CHANNEL_STATUS = "channelStatus"
PARAM_CHANNEL_ABILITY = "channelAbility"
PARAM_STREAM_ID = "streamId"
PARAM_OPERATION = "operation"
PARAM_DURATION = "duration"
PARAM_PROPERTIES = "properties"
PARAM_API_URL = "api_url"
PARAM_MOTION_DETECT = "motion_detect"
PARAM_MOBILE_DETECT = "mobile_detect"
PARAM_STATUS = "status"
PARAM_STORAGE_USED = "storage_used"
PARAM_NIGHT_VISION_MODE = "night_vision_mode"
PARAM_CURRENT_OPTION = "current_option"
PARAM_MODES = "modes"
PARAM_OPTIONS = "options"
PARAM_CHANNELS = "channels"
PARAM_USED_BYTES = "usedBytes"
PARAM_TOTAL_BYTES = "totalBytes"
PARAM_STREAMS = "streams"
PARAM_HLS = "hls"
PARAM_RESTART_DEVICE = "restart_device"
PARAM_URL = "url"
PARAM_CLOSE_CAMERA = "close_camera"
PARAM_WHITE_LIGHT = "white_light"
PARAM_AB_ALARM_SOUND = "ab_alarm_sound"
PARAM_AUDIO_ENCODE_CONTROL = "audio_encode_control"

# Configuration definitions
CONF_API_URL_SG = "openapi-sg.easy4ip.com"
CONF_API_URL_OR = "openapi-or.easy4ip.com"
CONF_API_URL_FK = "openapi-fk.easy4ip.com"
CONF_CLOSE_CAMERA = "CloseCamera"
CONF_WHITE_LIGHT = "WhiteLight"
CONF_AB_ALARM_SOUND = "AbAlarmSound"
CONF_AUDIO_ENCODE_CONTROL = "AudioEncodeControl"
CONF_NVM = "NVM"
CONF_PT = "PT"

PLATFORMS = [
    "select",
    "sensor",
    "switch",
    "camera",
    "button"
]

SWITCH_TYPE_ABILITY = {
    "close_camera": "CloseCamera",
    "white_light": "WhiteLight",
    "audio_encode_control": "AudioEncodeControl",
    "ab_alarm_sound": "AbAlarmSound"
}

SWITCH_TYPE_ENABLE = {
    "motion_detect": ["motionDetect", "mobileDetect"],
    "close_camera": ["closeCamera"],
    "white_light": ["whiteLight"],
    "audio_encode_control": ["audioEncodeControl"],
    "ab_alarm_sound": ["abAlarmSound"]
}

BUTTON_TYPE_PARAM_VALUE = {
    "ptz_up": 0,
    "ptz_down": 1,
    "ptz_left": 2,
    "ptz_right": 3
}

