"""Constants for petkit_api"""

from enum import StrEnum


class Region(StrEnum):

    US = "https://api.petkt.com/latest/"
    ASIA = "https://api.petktasia.com/latest/"
    CN = "https://api.petkit.cn/6/"


class Endpoint(StrEnum):

    BLE_CANCEL = "ble/cancel"
    BLE_CONNECT = "ble/connect"
    BLE_DEVICES = "ble/ownSupportBleDevices"
    BLE_POLL = "ble/poll"
    CALL_PET = "callPet"
    CANCEL_FEED = "cancelRealtimeFeed"
    CONTROL_DEVICE = "controlDevice"
    CONTROL_WF = "ble/controlDevice"
    DEVICE_DETAIL = "device_detail"
    DEVICE_DATA = "deviceData"
    DEVICE_RECORD = "getDeviceRecord"
    DEVICE_RECORD_RELEASE = "getDeviceRecordRelease"
    DEVICE_ROSTER = "discovery/device_roster_v2"
    FAMILY_LIST = "group/family/list"
    FEEDER_DESICCANT_RESET = "desiccantReset"
    FRESH_ELEMENT_CALIBRATION = "food_reset"
    FRESH_ELEMENT_CANCEL_FEED = "cancel_realtime_feed"
    FRESH_ELEMENT_DESICCANT_RESET = "feeder/desiccant_reset"
    FRESH_ELEMENT_MANUAL_FEED = "feeder/save_dailyfeed"
    FRESH_ELEMENT_SETTING = "feeder/update"
    LOGIN = "user/login"
    MANUAL_FEED = "saveDailyFeed"
    MAX_ODOR_RESET = "deodorantReset"
    MINI_DESICCANT_RESET = "feedermini/desiccant_reset"
    MINI_MANUAL_FEED = "feedermini/save_dailyfeed"
    MINI_SETTING = "feedermini/update"
    PET_PROPS = "pet/updatepetprops"
    REFRESH_HOME = "discovery/refreshHome"
    RESTORE_DAILY_FEED = "restoreDailyFeed"
    REMOVE_DAILY_FEED = "removeDailyFeed"
    REPLENISHED_FOOD = "added"
    SOUND_LIST = "soundList"
    SAVE_FEED = "saveFeed"
    STATISTIC = "statistic"
    STATISTIC_RELEASE = "statisticRelease"
    UNIT = "app/saveunit"
    UPDATE_SETTING = "updateSettings"
    USER_DETAILS = "user/details2"


class FeederSetting(StrEnum):

    AUTO_PRODUCT = "autoProduct"
    AUTO_UPGRADE = "autoUpgrade"
    CAMERA = "camera"
    CAMERA_CONFIG = "cameraConfig"
    CHILD_LOCK = "manualLock"
    CLOUD_UPLOAD = "upload"
    CONTROL_SETTINGS = "controlSettings"
    DETECT_CONFIG = "detectConfig"
    DETECT_INTERVAL = "detectInterval"
    DETECT_MULTI_RANGE = "detectMultiRange"
    DISPENSE_TONE = "feedSound"
    DISPENSING_NOTIFY = "feedNotify"
    DO_NOT_DISTURB = "disturbMode"
    EAT_NOTIFY = "eatNotify"
    EAT_SENSITIVITY = "eatSensitivity"
    FEED_PICTURE = "feedPicture"
    FEED_TONE = "feedTone"
    FRESH_ELEMENT_CHILD_LOCK = "settings.manualLock"
    FRESH_ELEMENT_INDICATOR_LIGHT = "settings.lightMode"
    HIGHLIGHT = "highlight"
    INDICATOR_LIGHT = "lightMode"
    LIVE_ENCRYPT = "liveEncrypt"
    LOW_BATTERY_NOTIFY = "lowBatteryNotify"
    MICROPHONE = "microphone"
    MIN_EAT_DURATION = "shortest"
    MINI_CHILD_LOCK = "settings.manualLock"
    MINI_INDICATOR_LIGHT = "settings.lightMode"
    MOVE_NOTIFY = "moveNotify"
    MOVE_SENSITIVITY = "moveSensitivity"
    NIGHT_VISION = "night"
    PET_EAT_NOTIFY = "eatNotify"
    PET_SENSITIVITY = "petSensitivity"
    PET_VISIT_NOTIFY = "petNotify"
    PRE_LIVE = "preLive"
    REFILL_FOOD_NOTIFY = "foodNotify"
    SELECTED_SOUND = "selectedSound"
    SHORTAGE_ALARM = "foodWarn"
    SMART_FRAME = "smartFrame"
    SOUND_ENABLE = "soundEnable"
    SURPLUS = "surplus"
    SURPLUS_CONTROL = "surplusControl"
    SURPLUS_STANDARD = "surplusStandard"
    SYSTEM_SOUND = "systemSoundEnable"
    TIME_DISPLAY = "timeDisplay"
    VOLUME = "volume"


class Header(StrEnum):

    ACCEPT = "*/*"
    X_TIMEZONE = "-5.0"
    ACCEPT_LANG = "en-US;q=1, it-US;q=0.9"
    ENCODING = "gzip, deflate"
    API_VERSION = "11.2.1"
    CONTENT_TYPE = "application/x-www-form-urlencoded"
    AGENT = "PETKIT/11.2.1 (iPhone; iOS 15.1; Scale/3.00)"
    TZ = "America/New_York"
    CLIENT = "ios(15.1;iPhone14,3)"
    LOCALE = "en_US"


class FeederCommand(StrEnum):

    START_CALIBRATION = "Start calibration"
    STOP_CALIBRATION = "Stop calibration"


class LitterBoxCommand(StrEnum):

    LIGHT_ON = "light_on"
    ODOR_REMOVAL = "start_odor"
    PAUSE_CLEAN = "stop_clean"
    POWER = "power"
    RESET_DEODOR = "reset_deodorizer"
    RESUME_CLEAN = "continue_clean"
    START_CLEAN = "start_clean"
    START_MAINTENANCE = "start_maintenance"
    EXIT_MAINTENANCE = "exit_maintenance"
    PAUSE_MAINTENANCE_EXIT = "pause_maintenance_exit"
    RESUME_MAINTENANCE_EXIT = "resume_maintenance_exit"
    DUMP_LITTER = "dump_litter"
    PAUSE_LITTER_DUMP = "pause_litter_dump"
    RESUME_LITTER_DUMP = "resume_litter_dump"
    RESET_MAX_DEODOR = "reset_max_deodorizer"


class LitterBoxCommandKey(StrEnum):

    CONTINUE = "continue_action"
    END = "end_action"
    POWER = "power_action"
    START = "start_action"
    STOP = "stop_action"


class LitterBoxCommandType(StrEnum):

    CONTINUE = "continue"
    END = "end"
    POWER = "power"
    START = "start"
    STOP = "stop"


class LitterBoxSetting(StrEnum):

    AUTO_CLEAN = "autoWork"
    AUTO_ODOR = "autoRefresh"
    AVOID_REPEAT_CLEAN = "avoidRepeat"
    CHILD_LOCK = "manualLock"
    CLEAN_INTERVAL = "autoIntervalMin"
    CONT_ROTATION = "downpos"
    DEEP_CLEAN = "deepClean"
    DEEP_REFRESH = "deepRefresh"
    DELAY_CLEAN_TIME = "stillTime"
    DISABLE_LIGHT_WEIGHT = "underweight"
    DISPLAY = "lightMode"
    DO_NOT_DISTURB = "disturbMode"
    ENHANCED_ADSORPTION = "bury"
    KITTEN_MODE = "kitten"
    PERIODIC_CLEAN = "fixedTimeClear"
    PERIODIC_ODOR = "fixedTimeRefresh"
    SAND_TYPE = "sandType"


class PetSetting(StrEnum):

    WEIGHT = "weight"


class PurifierSetting(StrEnum):

    LIGHT = "lightMode"
    SOUND = "sound"


class PurifierCommand(StrEnum):

    POWER = "power"
    AUTO_MODE = "auto_mode"
    SILENT_MODE = "silent_mode"
    STANDARD_MODE = "standard_mode"
    STRONG_MODE = "strong_mode"


class PurifierCommandKey(StrEnum):

    POWER = "power_action"
    MODE = "mode_action"


class PurifierCommandType(StrEnum):

    POWER = "power"
    MODE = "mode"


class FountainCommand(StrEnum):

    PAUSE = "Pause"
    NORMAL_TO_PAUSE = "Normal To Pause"
    SMART_TO_PAUSE = "Smart To Pause"
    NORMAL = "Normal"
    SMART = "Smart"
    RESET_FILTER = "Reset Filter"
    DO_NOT_DISTURB = "Do Not Disturb"
    DO_NOT_DISTURB_OFF = "Do Not Disturb Off"
    FIRST_BLE_CMND = "First BLE Command"
    SECOND_BLE_CMND = "Second BLE Command"
    LIGHT_LOW = "Light Low"
    LIGHT_MEDIUM = "Light Medium"
    LIGHT_HIGH = "Light High"
    LIGHT_ON = "Light On"
    LIGHT_OFF = "Light Off"


TIMEOUT = 5 * 60

CLIENT_DICT = {
    "locale": "en-US",
    "source": "app.petkit-ios-oversea",
    "platform": "ios",
    "osVersion": "15.1",
    "timezone": "-5.0",
    "timezoneId": "America/New_York",
    "version": "11.2.1",
    "token": "",
    "name": "iPhone14,3",
}

ASIA_REGIONS = [
    "AF",
    "AL",
    "AZ",
    "BH",
    "BD",
    "BT",
    "BN",
    "KH",
    "CN",
    "CY",
    "VA",
    "HK",
    "IN",
    "ID",
    "IR",
    "IQ",
    "IL",
    "JP",
    "JO",
    "KZ",
    "KP",
    "KR",
    "KW",
    "KG",
    "LA",
    "LB",
    "LU",
    "MO",
    "MY",
    "MV",
    "MN",
    "MM",
    "NP",
    "OM",
    "PK",
    "PH",
    "QA",
    "SA",
    "SG",
    "SY",
    "TW",
    "TJ",
    "TH",
    "TL",
    "TM",
    "AE",
    "VN",
    "YE",
]

AUTH_ERROR_CODES = {
    122: "PetKit username/email or password is incorrect",
    5: "Login session expired. Your account can only be signed in on one device.",
    125: "Unregistered e-mail address. The region selected may not be the correct one associated with your account.",
}

BLUETOOTH_ERRORS = {3003: "Bluetooth connection failed. Retrying on next update."}

SERVER_ERROR_CODES = {
    1: "PetKit servers are busy. Please try again later.",
    99: "PetKit servers are undergoing maintenance. Please try again later.",
}

BLE_HEADER = [-6, -4, -3]
FEEDER_LIST = ["D3", "D4", "D4s", "D4H", "D4sh", "Feeder", "FeederMini"]
LITTER_LIST = ["T3", "T4", "T6"]
PURIFIER_LIST = ["K2"]
WATER_FOUNTAIN_LIST = ["W5", "Ctw3"]

LB_CMD_TO_KEY = {
    LitterBoxCommand.LIGHT_ON: LitterBoxCommandKey.START,
    LitterBoxCommand.POWER: LitterBoxCommandKey.POWER,
    LitterBoxCommand.START_CLEAN: LitterBoxCommandKey.START,
    LitterBoxCommand.PAUSE_CLEAN: LitterBoxCommandKey.STOP,
    LitterBoxCommand.RESUME_CLEAN: LitterBoxCommandKey.CONTINUE,
    LitterBoxCommand.ODOR_REMOVAL: LitterBoxCommandKey.START,
    LitterBoxCommand.RESET_DEODOR: LitterBoxCommandKey.START,
    LitterBoxCommand.START_MAINTENANCE: LitterBoxCommandKey.START,
    LitterBoxCommand.EXIT_MAINTENANCE: LitterBoxCommandKey.END,
    LitterBoxCommand.PAUSE_MAINTENANCE_EXIT: LitterBoxCommandKey.STOP,
    LitterBoxCommand.RESUME_MAINTENANCE_EXIT: LitterBoxCommandKey.CONTINUE,
    LitterBoxCommand.DUMP_LITTER: LitterBoxCommandKey.START,
    LitterBoxCommand.PAUSE_LITTER_DUMP: LitterBoxCommandKey.STOP,
    LitterBoxCommand.RESUME_LITTER_DUMP: LitterBoxCommandKey.CONTINUE,
    LitterBoxCommand.RESET_MAX_DEODOR: LitterBoxCommandKey.START,
}

LB_CMD_TO_TYPE = {
    LitterBoxCommand.LIGHT_ON: LitterBoxCommandType.START,
    LitterBoxCommand.POWER: LitterBoxCommandType.POWER,
    LitterBoxCommand.START_CLEAN: LitterBoxCommandType.START,
    LitterBoxCommand.PAUSE_CLEAN: LitterBoxCommandType.STOP,
    LitterBoxCommand.RESUME_CLEAN: LitterBoxCommandType.CONTINUE,
    LitterBoxCommand.ODOR_REMOVAL: LitterBoxCommandType.START,
    LitterBoxCommand.RESET_DEODOR: LitterBoxCommandType.START,
    LitterBoxCommand.START_MAINTENANCE: LitterBoxCommandType.START,
    LitterBoxCommand.EXIT_MAINTENANCE: LitterBoxCommandType.END,
    LitterBoxCommand.PAUSE_MAINTENANCE_EXIT: LitterBoxCommandType.STOP,
    LitterBoxCommand.RESUME_MAINTENANCE_EXIT: LitterBoxCommandType.CONTINUE,
    LitterBoxCommand.DUMP_LITTER: LitterBoxCommandType.START,
    LitterBoxCommand.PAUSE_LITTER_DUMP: LitterBoxCommandType.STOP,
    LitterBoxCommand.RESUME_LITTER_DUMP: LitterBoxCommandType.CONTINUE,
    LitterBoxCommand.RESET_MAX_DEODOR: LitterBoxCommandType.START,
}

LB_CMD_TO_VALUE = {
    LitterBoxCommand.LIGHT_ON: 7,
    LitterBoxCommand.START_CLEAN: 0,
    LitterBoxCommand.PAUSE_CLEAN: 0,
    LitterBoxCommand.RESUME_CLEAN: 0,
    LitterBoxCommand.ODOR_REMOVAL: 2,
    LitterBoxCommand.RESET_DEODOR: 6,
    LitterBoxCommand.START_MAINTENANCE: 9,
    LitterBoxCommand.EXIT_MAINTENANCE: 9,
    LitterBoxCommand.PAUSE_MAINTENANCE_EXIT: 9,
    LitterBoxCommand.RESUME_MAINTENANCE_EXIT: 9,
    LitterBoxCommand.DUMP_LITTER: 1,
    LitterBoxCommand.PAUSE_LITTER_DUMP: 1,
    LitterBoxCommand.RESUME_LITTER_DUMP: 1,
    LitterBoxCommand.RESET_MAX_DEODOR: 8,
}

PUR_CMD_TO_KEY = {
    PurifierCommand.POWER: PurifierCommandKey.POWER,
    PurifierCommand.AUTO_MODE: PurifierCommandKey.MODE,
    PurifierCommand.SILENT_MODE: PurifierCommandKey.MODE,
    PurifierCommand.STANDARD_MODE: PurifierCommandKey.MODE,
    PurifierCommand.STRONG_MODE: PurifierCommandKey.MODE,
}

PUR_CMD_TO_TYPE = {
    PurifierCommand.POWER: PurifierCommandType.POWER,
    PurifierCommand.AUTO_MODE: PurifierCommandType.MODE,
    PurifierCommand.SILENT_MODE: PurifierCommandType.MODE,
    PurifierCommand.STANDARD_MODE: PurifierCommandType.MODE,
    PurifierCommand.STRONG_MODE: PurifierCommandType.MODE,
}

PUR_CMD_TO_VALUE = {
    PurifierCommand.AUTO_MODE: 0,
    PurifierCommand.SILENT_MODE: 1,
    PurifierCommand.STANDARD_MODE: 2,
    PurifierCommand.STRONG_MODE: 3,
}

FOUNTAIN_COMMAND_TO_CODE = {
    FountainCommand.DO_NOT_DISTURB: "221",
    FountainCommand.DO_NOT_DISTURB_OFF: "221",
    FountainCommand.LIGHT_ON: "221",
    FountainCommand.LIGHT_OFF: "221",
    FountainCommand.LIGHT_LOW: "221",
    FountainCommand.LIGHT_MEDIUM: "221",
    FountainCommand.LIGHT_HIGH: "221",
    FountainCommand.PAUSE: "220",
    FountainCommand.RESET_FILTER: "222",
    FountainCommand.NORMAL: "220",
    FountainCommand.NORMAL_TO_PAUSE: "220",
    FountainCommand.SMART: "220",
    FountainCommand.SMART_TO_PAUSE: "220",
}

FOUNTAIN_DND_COMMANDS = [
    FountainCommand.DO_NOT_DISTURB,
    FountainCommand.DO_NOT_DISTURB_OFF,
]
FOUNTAIN_LIGHT_BRIGHTNESS = [
    FountainCommand.LIGHT_LOW,
    FountainCommand.LIGHT_MEDIUM,
    FountainCommand.LIGHT_HIGH,
]
FOUNTAIN_LIGHT_POWER = [FountainCommand.LIGHT_ON, FountainCommand.LIGHT_OFF]
FOUNTAIN_MODE = [
    FountainCommand.NORMAL,
    FountainCommand.SMART,
    FountainCommand.NORMAL_TO_PAUSE,
    FountainCommand.SMART_TO_PAUSE,
]
FOUNTAIN_SETTINGS_COMMANDS = [
    FountainCommand.DO_NOT_DISTURB,
    FountainCommand.DO_NOT_DISTURB_OFF,
    FountainCommand.LIGHT_LOW,
    FountainCommand.LIGHT_MEDIUM,
    FountainCommand.LIGHT_HIGH,
    FountainCommand.LIGHT_ON,
    FountainCommand.LIGHT_OFF,
]

MIN_FEED_AMOUNT = 0
MAX_FEED_AMOUNT = 10
TOKEN_EXPIRATION_TIME = 3600
BLE_POLL_INTERVAL = 420
BLE_CONNECT_ATTEMPT = 4
