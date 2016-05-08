#include "mytask.h"

MyTask::MyTask(QString received)
{
    JSONcall.insert("UnParsed",received);

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
        robjJSON["code"] = -32700;
        robjJSON["message"] = "Parse error";
        robjJSON["id"] = "null";
        JSONresult["error"] = robjJSON;
        emit Result(QtJson::serialize(JSONresult));
        return;
    }

    if(batch)
    {
        QList<QVariant> batchResult;
        foreach(QVariant rpCall, parsedJSON.toList())
        {
            JSONcall = rpCall.toMap();
            processCall();
            batchResult << JSONresult;
        }
        if(answer) emit Result(QtJson::serialize(batchResult));
    }
    else
    {
        JSONcall = parsedJSON.toMap();
        processCall();
        if(answer) emit Result(QtJson::serialize(JSONresult));
    }

    qDebug() << "Task Done";
}

void MyTask::processCall()
{
    // set the version of the json rpc
    JSONresult["jsonrpc"] = "2.0";

    // Return the same message id if provided
    // if no id is provided, an answer will not be sent
    QVariant id = JSONcall["id"];
    answer = id.isValid();
    if(answer)
        JSONresult["id"] = id;

    // Save the parameters
    paramsJSON = JSONcall["params"].toMap();

    // Check what kind of function came in
    int method;
    method = qHash(JSONcall["method"].toString());
    switch(method)
    {

    // System control
    case SYSTEM_SETMODE:
        setMode();
        break;
    //case SETVERBOSE:
    //    setVerbose();
    //    break;
    case SYSTEM_SENDUART:
        busWrite();
        break;
    //case GETCURRENT:
    //    getCurrent();
    //    break;
    case SYSTEM_GETMODE:
        getMode();
        break;

    // Motor Control
    case MOTOR_SETMOTOR:
        setMotor();
        break;

    // Turret Control
    case TURRET_SETANGLE:
        setTurretAngle();
        break;
    case TURRET_FIREMISSILE:
        fireMissile();
        break;
    case TURRET_SETLASER:
        setLaser();
        break;

    // If none of the above is true, an unknown method is received
    default:
        robjJSON["code"] = -32601;
        robjJSON["message"] = "Method does not exist";
        JSONresult["error"] = robjJSON;
        answer = true;
        break;
    }
}

void MyTask::setMode()
{
    qDebug() << "Going to set the mode";

    QString mode = paramsJSON["mode"].toString();

    //TODO: set the actual mode

    JSONresult["status"] = "notImplemented";
}

void MyTask::setVerbose()
{
    qDebug() << "Going to change the verbosity level of client ";

    QString mode = paramsJSON["mode"].toString();

    //TODO: set the actual mode

    JSONresult["status"] = "notImplemented";
}

QVariantMap MyTask::busWrite()
{
    QVariantMap result;
    QVariantMap _result;

    QString dataType = paramsJSON["dataType"].toString();
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
        QByteArray data = paramsJSON["data"].toByteArray();
        qDebug() << "Going to write \"" << data << "\" to the bus";
        emit UARTsend(data);
    }
    else if(dataType == "hex")
    {
        bool ok;
        QString stringData = paramsJSON["data"].toString();
        stringData.toInt(&ok,16);
        if(ok)
        {
            QByteArray data = QByteArray::fromHex(stringData.toLatin1());
            qDebug() << "Going to write \"" << data << "\" to the bus";
            emit UARTsend(data);
        }
        else
        {
            _result["code"] = -32602;
            _result["message"] = "Parse error";
            result["error"] = _result;
        }
    }
    return result;
}

QVariantMap MyTask::getCurrent()
{
    qDebug() << "Going to send the current";
    QVariantMap result;


    //TODO: implement

    return result;
}

void MyTask::getMode()
{
    qDebug() << "Going to send the Mode";
    //emit(Result("{\"status\": \"notImplemented\"}"));
}

void MyTask::setMotor()
{
    qDebug() << "Going to set the motor speeds";
    //emit(Result("{\"status\": \"notImplemented\"}"));
}

void MyTask::setTurretAngle()
{
    qDebug() << "Going to set the turret angle";
    //emit(Result("{\"status\": \"notImplemented\"}"));
}

void MyTask::fireMissile()
{
    qDebug() << "Going to fire a missile";
    //emit(Result("{\"status\": \"notImplemented\"}"));
}

void MyTask::setLaser()
{
    qDebug() << "Going to set the laser";
    //emit(Result("{\"status\": \"notImplemented\"}"));
}

