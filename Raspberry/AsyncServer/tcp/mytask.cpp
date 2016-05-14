#include "mytask.h"

MyTask::MyTask(QString received, uint mode)
{
    JSONcall.insert("UnParsed",received);
    this->mode = mode;
}

void MyTask::run()
{
    qDebug() << "Task Start";

    bool batch  = JSONcall["UnParsed"].toString().startsWith('[');
    bool jsonOk;
    QVariant parsedJSON = QtJson::parse(
            JSONcall["UnParsed"].toString(), jsonOk);

    // check if the received string is valid JSON
    if(!jsonOk)
    {
        qDebug() << "Invalid JSON string";
        answer = true;
        QVariantMap robjJSON;
        QVariantMap result;
        robjJSON["code"] = -32700;
        robjJSON["message"] = "Parse error";
        robjJSON["id"] = "null";
        result["error"] = robjJSON;
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

    qDebug() << "Task Done";
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
    QVariantMap paramsJSON = json["params"].toMap();

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
        setMode(paramsJSON, result);
        break;
    //case SETVERBOSE:
    //    setVerbose()paramsJSON;
    //    break;
    case SYSTEM_SENDUART:
        busWrite(paramsJSON, result);
        break;
    //case GETCURRENT:
    //    getCurrent(paramsJSON);
    //    break;
    case SYSTEM_GETMODE:
        getMode();
        break;

    // Motor Control
    case MOTOR_SETMOTOR:
        setMotor(paramsJSON, result);
        break;

    // Turret Control
    case TURRET_SETANGLE:
        setTurretAngle(paramsJSON, result);
        break;
    case TURRET_FIREMISSILE:
        fireMissile(paramsJSON, result);
        break;
    case TURRET_SETLASER:
        setLaser(paramsJSON, result);
        break;

    // If none of the above is true, an unknown method is received
    default:
        QVariantMap _result;
        _result["code"] = -32601;
        _result["message"] = "Method does not exist";
        result["error"] = _result;
        answer = true;
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
    qDebug() << "Going to set the mode";

    QString mode = params["mode"].toString();

    //TODO: set the actual mode
}

void MyTask::setVerbose(QVariantMap &params, QVariantMap &result)
{
    qDebug() << "Going to change the verbosity level of client ";

    QString mode = params["mode"].toString();

    //TODO: set the actual mode
}

void MyTask::busWrite(QVariantMap &params, QVariantMap &result)
{
    QVariantMap _result;

    QString dataType = params["dataType"].toString();
    if(dataType.isNull())
    {
        qDebug() << "Invalid parameter";
        answer = true;
        _result["code"] = -32700;
        _result["message"] = "Parse error";
        result["error"] = _result;
    }
    else if(dataType == "string")
    {
        QByteArray data = params["data"].toByteArray();
        result["result"] = "OK";
        emit UARTsend(data);
    }
    else if(dataType == "hex")
    {
        bool ok;
        QString stringData = params["data"].toString();
        stringData.toInt(&ok,16);
        if(ok)
        {
            QByteArray data = QByteArray::fromHex(stringData.toLatin1());
            result["result"] = "OK";
            emit UARTsend(data);
        }
        else
        {
            _result["code"] = -32602;
            _result["message"] = "Parse error";
            result["error"] = _result;
        }
    }
}

void MyTask::getCurrent(QVariantMap &result)
{
    qDebug() << "Going to send the current";

    //TODO: implement
}

void MyTask::getMode()
{
    qDebug() << "Going to send the Mode";
    //emit(Result("{\"status\": \"notImplemented\"}"));
}

void MyTask::setMotor(QVariantMap &params, QVariantMap &result)
{
    qDebug() << "Going to set the motor speeds";
    //emit(Result("{\"status\": \"notImplemented\"}"));
}

void MyTask::setTurretAngle(QVariantMap &params, QVariantMap &result)
{
    qDebug() << "Going to set the turret angle";
    //emit(Result("{\"status\": \"notImplemented\"}"));
}

void MyTask::fireMissile(QVariantMap &params, QVariantMap &result)
{
    qDebug() << "Going to fire a missile";
    //emit(Result("{\"status\": \"notImplemented\"}"));
}

void MyTask::setLaser(QVariantMap &params, QVariantMap &result)
{
    qDebug() << "Going to set the laser";
    //emit(Result("{\"status\": \"notImplemented\"}"));
}

