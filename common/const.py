const_value = {
    'TTL': 300,
    'HEADER_DOES_NOT_EXIST': 'NO_token_in_header',
    'SESSION_EXIST': 'Session_exist',
    'SESSION_CREATED': 'Session_created',
    'SESSION_DOES_NOT_EXIST': 'Session does not exist',
    'SESSION_EXPIRE': 'Session expired',
    'TOKEN_DOES_NOT_EXIST': 'Token does not exist',
    'INVITATION_LINK' : 'http://192.168.0.24:9000/api/group/invitation/',
    'PARTICIPATION_LINK': 'http://192.168.0.24:9000/api/group/join/',
    'CONFIRMATION_LINK' : 'http://192.168.0.24:8000/api/accounts/signup/',
}

status_code = {
    'SUCCESS' :{
            "code" : 1,
            "msg": "Request Sucess",
            "data": ""
    },

    'FAIL': {
        "code": 0,
        "msg": "Request Failure",
        "data": ""
    },

    'SIGNUP_SUCCESS' : {
        "code": 1200,
        "msg": "SignUp Success",
        "data": ""
    },

    'SIGNUP_WRONG_PARAMETER': {
        "code": 1401,
        "msg": "SignUp Wrong Parameter",
        "data": ""
    },

    'SIGNUP_INVALID_EMAIL' : {
        "code": 1402,
        "msg": "SignUp Invalid Email",
        "data": ""
    },

    'USER_SIGNOUT_SUCCESS': {
        "code": 1203,
        "msg": "User signout success",
        "data": ""
    },
    'USER_SIGNOUT_FAIL': {
        "code": 1403,
        "msg": "User signout failure",
        "data": ""
    },


    'LOGIN_SUCCESS' : {
        "code" : 2200,
        "msg" : "Login success",
        "data" : ""
    },
    'LOGIN_WRONG_PARAMETER' : {
        "code" : 2401,
        "msg" : "Login Wrong Parameter",
        "data" : ""
    },
    'LOGIN_INVALID_EMAIL' : {
        "code" : 2402,
        "msg" : "Login Invalid Email",
        "data" : ""
    },
    'LOGIN_INVALID_PASSWORD': {
        "code": 2403,
        "msg": "Login Invalid Password",
        "data": ""
    },
    'LOGIN_SESSION_EXISTS' : {
        "code" : 2304,
        "msg" : "Session Exists",
        "data" : ""
    },

    'LOGOUT_SUCCESS' : {
        "code" : 3200,
        "msg" : "Logout Success",
        "data" : ""
    },
    'LOGOUT_FAIL' : {
        "code" : 3401,
        "msg" : "Logout Failure",
        "data" : ""
    },

    'USER_INFO_GET_SUCCESS' : {
        "code" : 4200,
        "msg" : "User information Retrieve",
        "data" : ""
    },
    'USER_INFO_GET_FAIL' : {
        "code" : 4401,
        "msg" : "User information retrieve fail",
        "data" : ""
    },
    'USER_INFO_MODIFY_SUCCESS' : {
        "code" : 4202,
        "msg" : "User information modified success",
        "data" : ""
    },
    'USER_INFO_MODIFY_FAIL' : {
        "code" : 4403,
        "msg" : "User information modification failure",
        "data" : ""
    },


    'GROUP_MADE_SUCCESS' : {
        "code" : 5200,
        "msg" : "New Group is made",
        "data" : ""
    },
    'GROUP_LIST_SUCCESS' : {
        "code" : 5201,
        "msg" : "Group list is retreived",
        "data" : ""
    },
    'GROUP_MEMBER_GET_SUCCESS': {
        "code": 5202,
        "msg": "group memeberlist get success",
        "data": ""
    },
    'GROUP_INVITATION_SUCCESS': {
        "code": 5203,
        "msg": "Group invite Success",
        "data": ""
    },
    'GROUP_INVITATION_ACTIVATE_SUCCESS': {
        "code": 5204,
        "msg": "Activation Success",
        "data": ""
    },
    'GROUP_DELETE_SUCCESS': {
        "code": 5205,
        "msg": "Group Delete Success",
        "data": ""
    },
    'GROUP_EXIT_SUCCESS': {
        "code": 5206,
        "msg": "Group Exit Success",
        "data": ""
    },
    'GROUP_GET_DETAIL_SUCCESS': {
        "code": 5207,
        "msg": "Get Group detail Success",
        "data": ""
    },
    'GROUP_MADE_FAIL': {
        "code": 5400,
        "msg": "Group creation fail",
        "data": ""
    },
    'GROUP_LIST_FAIL': {
        "code": 5401,
        "msg": "Cannot retrieve list of group",
        "data": ""
    },
    'GROUP_MEMBER_GET_FAIL': {
        "code": 5402,
        "msg": "group memeberlist get fail",
        "data": ""
    },
    'GROUP_INVITATION_FAIL': {
        "code": 5403,
        "msg": "Group invite Fail",
        "data": ""
    },
    'GROUP_INVITATION_ACTIVATE_FAIL': {
        "code": 5404,
        "msg": "Activation Fail",
        "data": ""
    },
    'GROUP_DELETE_FAIL': {
        "code": 5405,
        "msg": "Group Delete Fail",
        "data": ""
    },
    'GROUP_EXIT_FAIL': {
        "code": 5406,
        "msg": "Group Exit Fail",
        "data": ""
    },
    'GROUP_GET_DETAIL_FAIL': {
        "code": 5407,
        "msg": "Get Group detail Fail",
        "data": ""
    },



    'TOPIC_MADE_SUCCESS': {
    "code": 6200,
    "msg": "New Topic is made",
    "data": ""
    },
    'TOPIC_LIST_SUCCESS': {
        "code": 6201,
        "msg": "Topic list is retreived",
        "data": ""
    },
    'TOPIC_MEMBER_GET_SUCCESS': {
        "code": 6202,
        "msg": "Topic memeberlist get success",
        "data": ""
    },
    'TOPIC_INVITATION_SUCCESS': {
        "code": 6203,
        "msg": "Topic invite Success",
        "data": ""
    },
    'TOPIC_INVITATION_ACTIVATE_SUCCESS': {
        "code": 6204,
        "msg": "Activation Success",
        "data": ""
    },
    'TOPIC_DELETE_SUCCESS': {
        "code": 6205,
        "msg": "Topic Delete Success",
        "data": ""
    },
    'TOPIC_EXIT_SUCCESS': {
        "code": 6206,
        "msg": "Topic Exit Success",
        "data": ""
    },
    'TOPIC_GET_DETAIL_SUCCESS': {
        "code": 6207,
        "msg": "Get Topic detail Success",
        "data": ""
    },
    'TOPIC_MODIFY_SUCCESS': {
        "code": 6208,
        "msg": "Get Topic modify Success",
        "data": ""
    },
    'TOPIC_MADE_FAIL': {
        "code": 6400,
        "msg": "Topic creation fail",
        "data": ""
    },
    'TOPIC_LIST_FAIL': {
        "code": 6401,
        "msg": "Cannot retrieve list of Topic",
        "data": ""
    },
    'TOPIC_MEMBER_GET_FAIL': {
        "code": 6402,
        "msg": "Topic memeberlist get fail",
        "data": ""
    },
    'TOPIC_INVITATION_FAIL': {
        "code": 6403,
        "msg": "Topic invite Fail",
        "data": ""
    },
    'TOPIC_INVITATION_ACTIVATE_FAIL': {
        "code": 6404,
        "msg": "Activation Fail",
        "data": ""
    },
    'TOPIC_DELETE_FAIL': {
        "code": 6405,
        "msg": "Topic Delete Fail",
        "data": ""
    },
    'TOPIC_EXIT_FAIL': {
        "code": 6406,
        "msg": "Topic Exit Fail",
        "data": ""
    },
    'TOPIC_GET_DETAIL_FAIL': {
        "code": 6407,
        "msg": "Get Topic detail Fail",
        "data": ""
    },
    'TOPIC_MODIFY_FAIL': {
        "code": 6408,
        "msg": "Get Topic modify Fail",
        "data": ""
    },


    'CHAT_MADE_SUCCESS': {
        "code": 7200,
        "msg": "New Chat is made",
        "data": ""
    },
    'CHAT_LIST_SUCCESS': {
        "code": 7201,
        "msg": "Chat list is retreived",
        "data": ""
    },
    'CHAT_MEMBER_GET_SUCCESS': {
        "code": 7202,
        "msg": "Chat memeberlist get success",
        "data": ""
    },
    'CHAT_INVITATION_SUCCESS': {
        "code": 7203,
        "msg": "Chat invite Success",
        "data": ""
    },
    'CHAT_INVITATION_ACTIVATE_SUCCESS': {
        "code": 7204,
        "msg": "Activation Success",
        "data": ""
    },
    'CHAT_DELETE_SUCCESS': {
        "code": 7205,
        "msg": "Chat Delete Success",
        "data": ""
    },
    'CHAT_EXIT_SUCCESS': {
        "code": 7206,
        "msg": "Chat Exit Success",
        "data": ""
    },
    'CHAT_GET_DETAIL_SUCCESS': {
        "code": 7207,
        "msg": "Get Chat detail Success",
        "data": ""
    },
    'CHAT_MADE_FAIL': {
        "code": 7400,
        "msg": "Chat creation fail",
        "data": ""
    },
    'CHAT_LIST_FAIL': {
        "code": 7401,
        "msg": "Cannot retrieve list of Chat",
        "data": ""
    },
    'CHAT_MEMBER_GET_FAIL': {
        "code": 7402,
        "msg": "Chat memeberlist get fail",
        "data": ""
    },
    'CHAT_INVITATION_FAIL': {
        "code": 7403,
        "msg": "Chat invite Fail",
        "data": ""
    },
    'CHAT_INVITATION_ACTIVATE_FAIL': {
        "code": 7404,
        "msg": "Activation Fail",
        "data": ""
    },
    'CHAT_DELETE_FAIL': {
        "code": 7405,
        "msg": "Chat Delete Fail",
        "data": ""
    },
    'CHAT_EXIT_FAIL': {
        "code": 7406,
        "msg": "Chat Exit Fail",
        "data": ""
    },
    'CHAT_GET_DETAIL_FAIL': {
        "code": 7407,
        "msg": "Get Chat detail Fail",
        "data": ""
    },
}