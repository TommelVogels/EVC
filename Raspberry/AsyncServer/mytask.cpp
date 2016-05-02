#include "mytask.h"

MyTask::MyTask(QString received)
{
    receivedJSON.insert("UnParsed",received);
}

void MyTask::run()
{
    qDebug() << "Task Start";

    // convert the JSON string to QVariantMap
    bool jsonOk = false;
    receivedJSON = QtJson::parse(
            receivedJSON["UnParsed"].toString(),
            jsonOk).toMap();

    // notify the client that this is a reply
    sendJSON["type"] = "reply";

    // check if the received string is valid JSON
    if(!jsonOk)
    {
        qDebug() << "Invalid JSON string";
        sendJSON["status"] = "jsonFail";
        finalize();
        return;
    }

    // Return the same message id if provided
    QVariant id = receivedJSON["id"];
    if(id.isValid()) sendJSON["id"] = id;

    // Save the parameters
    paramsJSON = receivedJSON["params"].toMap();

    // Check what kind of function came in
    int method;
    method = qHash(receivedJSON["method"].toString());
    switch(method)
    {

    // System control
    case SETMODE:
        setMode();
        break;
    case SETVERBOSE:
        setVerbose();
        break;
    case BUSWRITE:
        busWrite();
        break;
    case GETCURRENT:
        getCurrent();
        break;
    case GETMODE:
        getMode();
        break;

    // Motor Control
    case SETMOTOR:
        setMotor();
        break;

    // Turret Control
    case SETTURRETANGLE:
        setTurretAngle();
        break;
    case FIREMISSILE:
        fireMissile();
        break;
    case SETLASER:
        setLaser();
        break;

    // If none of the above is true, an unknown method is received
    default:
        sendJSON["status"] = "unknownMethod";
        break;
    }

    qDebug() << "Task Done";

    finalize();
}

void MyTask::finalize()
{
    if(sendJSON["status"].isNull())
        sendJSON["status"] = "OK";
    emit Result(QtJson::serialize(sendJSON));
}

void MyTask::setMode()
{
    qDebug() << "Going to set the mode";

    QString mode = paramsJSON["mode"].toString();

    //TODO: set the actual mode

    sendJSON["status"] = "notImplemented";
}

void MyTask::setVerbose()
{
    qDebug() << "Going to change the verbosity level of client ";

    QString mode = paramsJSON["mode"].toString();

    //TODO: set the actual mode

    sendJSON["status"] = "notImplemented";
}

void MyTask::busWrite()
{
    qDebug() << "Going to write to the bus";

    QByteArray data = paramsJSON["data"].toByteArray();
    emit UARTsend(data);

    sendJSON["status"] = "OK";
}

void MyTask::getCurrent()
{
    qDebug() << "Going to send the current";

    //TODO:

    QVariantMap result;

    sendJSON["result"] = result;
    sendJSON["status"] = "notImplemented";
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

