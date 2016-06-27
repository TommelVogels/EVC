#include "mytask.h"
#include <QRegularExpression>
#include <QRegularExpressionMatch>

void MyTask::getError(uint error, QVariantMap &result)
{
    QVariantMap _result;
    answer = true;

    switch(error)
    {
    case JSON_INVALIDREQUEST:
        _result["code"] = -32600;
        _result["message"] = "Invalid request";
        result["error"] = _result;
        break;
    case JSON_PARAMERROR:
        _result["code"] = -32602;
        _result["message"] = "Parse error";
        result["error"] = _result;
        break;
    case JSON_PARSEERROR:
        _result["code"] = -32602;
        _result["message"] = "Parse error";
        result["error"] = _result;
        break;
    case JSON_METHODNOTFOUND:
        _result["code"] = -32601;
        _result["message"] = "Method does not exist";
        result["error"] = _result;
        break;
    }
}

MyTask::MyTask(QString received, SystemState sysState)
{
    JSONcall.insert("UnParsed",received);
    this->system = sysState;
}

void MyTask::run()
{
    bool batch  = JSONcall["UnParsed"].toString().startsWith('[');
    bool jsonOk;
    QVariant parsedJSON = QtJson::parse(
            JSONcall["UnParsed"].toString(), jsonOk);

    // check if the received string is valid JSON
    if(!jsonOk)
    {
        qDebug() << "TCP: \tInvalid JSON string";
        answer = true;
        QVariantMap result;
        getError(JSON_PARSEERROR, result);
        emit Result(QtJson::serialize(result));
        return;
    }

    if(batch)
    {
        QList<QVariant> batchResult;
        foreach(QVariant rpCall, parsedJSON.toList())
        {
            QVariantMap result;
            processCall(rpCall.toMap(), result);
            batchResult << result;
        }
        if(answer) emit Result(QtJson::serialize(batchResult));
    }
    else
    {
        QVariantMap result;
        processCall(parsedJSON.toMap(), result);
        if(answer) emit Result(QtJson::serialize(result));
    }

    //qDebug() << "TCP: \tTask Done";
}

void MyTask::processCall(QVariantMap json, QVariantMap &result)
{
    // set the version of the json rpc
    result["jsonrpc"] = "2.0";

    // Return the same message id if provided
    // if no id is provided, an answer will not be sent
    QVariant id = json["id"];
    answer = id.isValid();
    if(answer)
        result["id"] = id;

    // Save the parameters
    QVariant paramsJSON = json["params"];
    QVariantMap paramsMap;
    QVariantList paramsList;

    // Check what kind of function came in
    int method;
    method = qHash(json["method"].toString());
    switch(method)
    {
    // JSON RPC
    case JSONRPC_VERSION:
        result["result"] = "0.1";
        break;
    case JSONRPC_GETMETHODS:
        getMethods(result);
        break;

    // System control
    case SYSTEM_SETMODE:
        paramsMap = paramsJSON.toMap();
        setMode(paramsMap, result);
        break;
    case SYSTEM_SETVERBOSE:
        paramsList = paramsJSON.toList();
        setVerbose(paramsList, result);
        break;
    case SYSTEM_SENDUART:
        paramsMap = paramsJSON.toMap();
        busWrite(paramsMap, result);
        break;
    //case GETCURRENT:
    //    getCurrent(paramsJSON);
    //    break;
    case SYSTEM_GETMODE:
        getMode(result);
        break;

    // Motor Control
    case MOTOR_SETMOTOR:
        paramsMap = paramsJSON.toMap();
        if(system.operatingMode == MODE_MANUAL)
            setMotor(paramsMap, result);
        else
            getError(JSON_INVALIDREQUEST, result);
        break;

    // Turret Control
    case TURRET_SETANGLE:
        paramsMap = paramsJSON.toMap();
        setTurretAngle(paramsMap, result);
        break;
    case TURRET_FIREMISSILE:
        paramsMap = paramsJSON.toMap();
        fireMissile(paramsMap, result);
        break;
    case TURRET_SETLASER:
        paramsMap = paramsJSON.toMap();
        setLaser(paramsMap, result);
        break;

    // If none of the above is true, an unknown method is received
    default:
        getError(JSON_METHODNOTFOUND,result);
        break;
    }
}

void MyTask::getMethods(QVariantMap &result)
{
    QStringList methods{
        "JSONRPC.Version",
        "JSONRPC.GetMethods",

        "System.SetMode",
        "System.GetMode",
        "System.SetVerbose",
        "System.SendUart",

        "Motor.SetMotor",
        "Motor.GetMotorAngle",
        "Motor.GetMotorSpeed",

        "Turret.SetAngle",
        "Turret.GetAngle",
        "Turret.SetLaser",
        "Turret.GetLaser",
        "Turret.FireMissile"
    };
    result["result"] = methods;
}

void MyTask::setMode(QVariantMap &params, QVariantMap &result)
{
    QString mode = params["mode"].toString();

    if(mode.isEmpty() || mode.isNull())
    {
        getError(JSON_INVALIDREQUEST, result);
        return;
    }

    if(mode.toLower() == "autonomous")
    {
        result["result"] = "OK";
        qDebug() << "TCP: \tGoing to set the mode";
        emit ChangeMode(MODE_AUTONOMOUS);
    }
    else if(mode.toLower() == "manual")
    {
        result["result"] = "OK";
        qDebug() << "TCP: \tGoing to set the mode";
        emit ChangeMode(MODE_MANUAL);
    }
    else
    {
        getError(JSON_PARAMERROR, result);
    }
}

void MyTask::setVerbose(QVariantList &params, QVariantMap &result)
{
    uint vlevel = 0;

    if(params.contains("mode"))          vlevel |= V_SYSTEMMODE;
    if(params.contains("motorSpeed"))    vlevel |= V_MOTORSPEED;
    if(params.contains("turretAngle"))   vlevel |= V_TURRETANGLE;
    if(params.contains("turretMissile")) vlevel |= V_TURRETMISSILE;
    if(params.contains("laser"))         vlevel |= V_TURRETLASER;

    result["result"] = "OK";
    qDebug() << "TCP: \tGoing to change the verbosity level of client ";
    emit Verbose(vlevel);
}

void MyTask::busWrite(QVariantMap &params, QVariantMap &result)
{
    QString dataType = params["dataType"].toString();
    if(dataType == "string")
    {
        QByteArray data = params["data"].toByteArray();
        result["result"] = "OK";
        emit UARTsend(data);
    }
    else if(dataType == "hex")
    {
        QString stringData = params["data"].toString();
        QRegularExpression hexMatcher("^[\\dABCDEF]+$");
        QRegularExpressionMatch match = hexMatcher.match(stringData);
        if(!match.hasMatch())
            getError(JSON_PARAMERROR,result);
        else
        {
            QByteArray data = QByteArray::fromHex(stringData.toLatin1());
            result["result"] = "OK";
            qDebug() << "TCP: \tGoing to write to the bus";
            emit UARTsend(data);
        }
    }
    else
    {
        getError(JSON_PARSEERROR,result);
    }
}

void MyTask::getCurrent(QVariantMap &result)
{
    qDebug() << "TCP: \tGoing to send the current";

    //TODO: implement
}

void MyTask::getMode(QVariantMap &result)
{
    switch(system.operatingMode)
    {
    case MODE_MANUAL:
        result["result"] = "manual";
        break;
    case MODE_AUTONOMOUS:
        result["result"] = "autonomous";
        break;
    default:
        return;
    }
    qDebug() << "TCP: \tGoing to send the Mode";
}

void MyTask::setMotor(QVariantMap &params, QVariantMap &result)
{
    bool paramError = false;
    bool left_ok = false, right_ok = false;
    int left, right;
    QString checkstr;

    checkstr = params["left"].toString();
    if(!checkstr.isEmpty() && !checkstr.isNull())
    {
        left = checkstr.toShort(&left_ok,10);
        if(!left_ok) paramError = true;
    }

    checkstr = params["right"].toString();
    if(!checkstr.isEmpty() && !checkstr.isNull())
    {
        right = checkstr.toShort(&right_ok,10);
        if(!right_ok) paramError = true;
    }

    if(paramError)
    {
        getError(JSON_PARAMERROR, result);
        return;
    }

    qDebug() << "TCP: \tGoing to set the motor";
    emit MotorSignal(left_ok,right_ok,left,right);
    result["result"] = "OK";
}

void MyTask::setTurretAngle(QVariantMap &params, QVariantMap &result)
{
    bool paramError = false;
    bool hori_ok = false, vert_ok = false;
    int hori, vert;
    QString checkstr;

    checkstr = params["horizontal"].toString();
    if(!checkstr.isEmpty() && !checkstr.isNull())
    {
        hori = checkstr.toShort(&hori_ok,10);
        if(!hori_ok) paramError = true;
    }

    checkstr = params["vertical"].toString();
    if(!checkstr.isEmpty() && !checkstr.isNull())
    {
        vert = checkstr.toShort(&vert_ok,10);
        if(!vert_ok) paramError = true;
    }

    if(paramError)
    {
        getError(JSON_PARAMERROR, result);
        return;
    }

    qDebug() << "TCP: \tGoing to set the turret angle";
    emit TurretAngleSignal(hori_ok,vert_ok,hori,vert);
    result["result"] = "OK";
}

void MyTask::fireMissile(QVariantMap &params, QVariantMap &result)
{
    int turret = params["turret"].toInt();
    QString amount = params["amount"].toString();

    if(amount != "one" && amount != "all")
    {
        getError(JSON_PARAMERROR, result);
        return;
    }

    bool all = (amount == "all");
    bool t1 = ((turret == 1) | (turret == 12));
    bool t2 = ((turret == 2) | (turret == 12));

    qDebug() << "TCP: \tGoing to fire";
    emit MissileSignal(t1,t2,all);
    result["result"] = "OK";
}

void MyTask::setLaser(QVariantMap &params, QVariantMap &result)
{
    QString checkstr = params["on"].toString();

    if(checkstr != "true" && checkstr != "false")
    {
        getError(JSON_PARAMERROR, result);
        return;
    }

    qDebug() << "TCP: \tGoing to set the laser";
    emit LaserSignal((checkstr == "true"));
    result["result"] = "OK";
}

