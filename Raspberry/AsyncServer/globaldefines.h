#ifndef GLOBALDEFINES_H
#define GLOBALDEFINES_H

#define SERVICE_NAME1        "evc.CommunicationInterface"
#define ECHO_OBJECT_PATH1    "/"

extern uint mode;

enum EjsonKeywords{
    JSONRPC_VERSION         = 530966439LL,
    JSONRPC_GETMETHODS      = 2319619661LL,

    SYSTEM_SETMODE          = 3915231334LL,
    SYSTEM_GETMODE          = 1855121754LL,
    SYSTEM_SETVERBOSE       = 0LL,
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

enum EcommunicationCommands{
    UART_STARTBYTE          = 0x5A,
    UART_STOPBYTE           = 0xA5,

    UART_ERROR              = 0x01,
    UART_GETQUEUELENGTH     = 0x02,
    UART_RESETPERIPHERALS   = 0x03,
    UART_TESTSEQUENCE       = 0x04,

    UART_TURRETHORIZONTAL   = 0x31,
    UART_TURRETVERTICAL     = 0x32,
    UART_FIREMISSILET1      = 0x33,
    UART_FIREMISSILET2      = 0x34,
    UART_FIREALLT1          = 0x35,
    UART_FIREALLT2          = 0x36,
    UART_FIREALLT12         = 0x37,
    UART_FLIPLASER          = 0x38,
};

enum EVerbose{
    V_SYSTEMMODE            = 0b00000001,
    V_MOTORSPEED            = 0b00000010,
    V_MOTORANGLE            = 0b00000100,
    V_TURRETANGLE           = 0b00001000,
    V_TURRETMISSILE         = 0b00010000,
    V_TURRETLASER           = 0b00100000,
};

enum EMode{
    MODE_MANUAL             = 1,
    MODE_AUTONOMOUS         = 2,
};


#endif // GLOBALDEFINES_H
