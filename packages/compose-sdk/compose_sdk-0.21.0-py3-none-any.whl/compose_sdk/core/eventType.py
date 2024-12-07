class SDK_TO_SERVER_EVENT_TYPE:
    APP_ERROR = "aa"
    INITIALIZE = "ab"
    RENDER_UI = "ac"
    FORM_VALIDATION_ERROR = "ad"
    RERENDER_UI = "ae"
    PAGE_CONFIG = "af"
    EXECUTION_EXISTS_RESPONSE = "ag"
    INPUT_VALIDATION_ERROR = "ah"
    FILE_TRANSFER = "ai"
    LINK = "aj"
    FORM_SUBMISSION_SUCCESS = "ak"
    RELOAD_PAGE = "al"
    CONFIRM = "am"
    TOAST = "an"
    RERENDER_UI_V2 = "ao"
    SET_INPUTS = "ap"
    CLOSE_MODAL = "aq"
    UPDATE_LOADING = "ar"


class SERVER_TO_SDK_EVENT_TYPE:
    START_EXECUTION = "aa"
    ON_CLICK_HOOK = "ab"
    ON_SUBMIT_FORM_HOOK = "ac"
    FILE_TRANSFER = "ad"
    CHECK_EXECUTION_EXISTS = "ae"
    ON_ENTER_HOOK = "af"
    ON_SELECT_HOOK = "ag"
    ON_FILE_CHANGE_HOOK = "ah"
    ON_TABLE_ROW_ACTION_HOOK = "ai"
    ON_CONFIRM_RESPONSE_HOOK = "aj"
    BROWSER_SESSION_ENDED = "ak"
    ON_CLOSE_MODAL = "al"


class EventType:
    SdkToServer = SDK_TO_SERVER_EVENT_TYPE
    ServerToSdk = SERVER_TO_SDK_EVENT_TYPE
