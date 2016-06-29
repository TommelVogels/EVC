#ifndef GLOBALDEFINES_H
#define GLOBALDEFINES_H

#define SERVICE_NAME1        "evc.CommunicationInterface"
#define ECHO_OBJECT_PATH1    "/"

extern uint mode;

struct SystemState {
    uint operatingMode;
    int mototSpeedLeft;
    int motorSpeedRight;
    int turretHorizontal;
    int turretVertical;
    bool laser;
};

extern SystemState sysState;

enum EjsonErrors{
    JSON_PARSEERROR,
    JSON_PARAMERROR,
    JSON_INVALIDREQUEST,
    JSON_METHODNOTFOUND,
    JSON_INTERNALERROR,
    JSON_SERVERERROR,
};

enum EjsonFuncList{
    JSONRPC_VERSION         = 530966439LL,
    JSONRPC_GETMETHODS      = 2319619661LL,

    SYSTEM_SETMODE          = 3915231334LL,
    SYSTEM_GETMODE          = 1855121754LL,
    SYSTEM_SETVERBOSE       = 3649038303LL,
    SYSTEM_SENDUART         = 961744437LL,

    MOTOR_SETMOTOR          = 711497420LL,
    MOTOR_GETMOTORANGLE     = 1061487451LL,
    MOTOR_GETMOTORSPEED     = 1078168271LL,

    TURRET_SETANGLE         = 3291407567LL,
    TURRET_GETANGLE         = 3852520027LL,
    TURRET_SETLASER         = 3301190343LL,
    TURRET_GETLASER         = 3862302803LL,
    TURRET_FIREMISSILE      = 4091903506LL,
};

enum EuartInfo{
    UART_STARTBYTE_POS      = 0,
    UART_LENGTH_POS         = 1,
    UART_COMMANDID_POS      = 2,
    UART_DATA_POS           = 3,
    UART_OVERHEAD           = 4,
    UART_MINLENGTH          = 5,

    UART_STARTBYTE          = 0xA5,
    UART_STOPBYTE           = 0x5A,
};

enum EcommunicationCommands{
    UART_ERROR              = 0x01,
    UART_GETQUEUELENGTH     = 0x02,
    UART_RESETPERIPHERALS   = 0x03,
    UART_TESTSEQUENCE       = 0x04,

    UART_LEFTMOTORSPEED     = 0x11,
    UART_RIGHTMOTORSPEED    = 0x12,
    UART_BOTHMOTORSPEED     = 0x13,

    UART_BATTERYCURRENT     = 0x21,
    UART_SYSTEMCURRENT      = 0x22,

    UART_TURRETHORIZONTAL   = 0x31,
    UART_TURRETVERTICAL     = 0x32,
    UART_TURRETBOTHDIRS     = 0x39,
    UART_FIREMISSILET1      = 0x33,
    UART_FIREMISSILET2      = 0x34,
    UART_FIREALLT1          = 0x35,
    UART_FIREALLT2          = 0x36,
    UART_FIREALLT12         = 0x37,
    UART_FLIPLASER          = 0x38,
};

enum EVerbose{
    V_REMAINING             = 0b00000001,
    V_SYSTEMMODE            = 0b00000010,
    V_MOTORSPEED            = 0b00000100,
    V_TURRETANGLE           = 0b00001000,
    V_TURRETMISSILE         = 0b00010000,
    V_TURRETLASER           = 0b00100000,
    V_SYSTEMCURRENT         = 0b01000000,
};

enum EMode{
    MODE_MANUAL             = 1,
    MODE_AUTONOMOUS         = 2,
};


#endif // GLOBALDEFINES_H
