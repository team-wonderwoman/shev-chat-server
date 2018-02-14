const_value = {
    'TTL' : 2592000,
    'HEADER_DOES_NOT_EXIST' : 'NO_token_in_header',
    'SESSION_EXIST' : 'Session_exist',
    'SESSION_CREATED' : 'Session_created',
    'TOKEN_DOES_NOT_EXIST' : 'Token does not exist',
    'INVITATION_LINK' : 'http://192.168.0.33:9000/api/group/invitation/',
    'PARTICIPATION_LINK': 'http://192.168.0.33:9000/api/group/join/',
    'CONFIRMATION_LINK' : 'http://192.168.0.24:8000/api/signup/',
}

status_code = {
    'SUCCESS' :{
            "code" : 0,
            "msg": "Request Succes",
            "": ""
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
    'LOGOUT_FAILURE' : {
        "code" : 3401,
        "msg" : "Logout Failure",
        "data" : ""
    },

    'USER_INFO_GET_SUCCESS' : {
        "code" : 4200,
        "msg" : "User information Retrieve",
        "data" : ""
    },
    'USER_INFO_GET_FAILURE' : {
        "code" : 4401,
        "msg" : "User information retrieve fail",
        "data" : ""
    },
    'USER_INFO_MODIFY_SUCCESS' : {
        "code" : 4202,
        "msg" : "User information modified",
        "data" : ""
    },
    'USER_INFO_MODIFY_FAILURE' : {
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
    'GROUP_MADE_FAILURE': {
        "code": 5400,
        "msg": "Group creation fail",
        "data": ""
    },
    'GROUP_LIST_FAILURE': {
        "code": 5401,
        "msg": "Cannot retrieve list of group",
        "data": ""
    },
    'GROUP_MEMBER_GET_FAILURE': {
        "code": 5402,
        "msg": "group memeberlist get fail",
        "data": ""
    },
    'GROUP_INVITATION_FAILURE': {
        "code": 5403,
        "msg": "Group invite Fail",
        "data": ""
    },
    'GROUP_INVITATION_ACTIVATE_FAILURE': {
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

}