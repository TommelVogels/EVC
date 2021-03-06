#include "myclient.h"
#include "myserver.h"
#include "interfacecollection.h"
#include "json.h"

MyClient::MyClient(QObject *parent) :
    QObject(parent)
{
    QThreadPool::globalInstance()->setMaxThreadCount(15);
    setVerbose(0x0);
}

void MyClient::SetSocket(int Descriptor)
{
    socket = new QTcpSocket(this);

    InterfaceCollection *ic = qobject_cast<InterfaceCollection *>(this->parent());
    connect(socket,SIGNAL(disconnected()),ic->Server,SLOT(clientDisconnected()));
    connect(socket,SIGNAL(readyRead()),this,SLOT(readyRead()));

    socket->setSocketDescriptor(Descriptor);

    qDebug() << "TCP: \tClient connected";

}

void MyClient::disconnected()
{
    qDebug() << "TCP: \tClient disconnected";
}

void MyClient::readyRead()
{
    QString received = socket->readAll().simplified();

    if(received != "")
    {
        //qDebug() << "TCP: \tReceived: " << received;

        //Initialize a task
        MyTask *mytask = new MyTask(received, sysState);
        mytask->setAutoDelete(true);
        connect(mytask,SIGNAL(Result(QByteArray)),SLOT(sendData(QByteArray)), Qt::QueuedConnection);

        //Connect to the other interfaces
        InterfaceCollection *ic = qobject_cast<InterfaceCollection *>(this->parent());
        connect(mytask,SIGNAL(ChangeMode(uint)),SLOT(setMode(uint)),Qt::QueuedConnection);
        connect(mytask,SIGNAL(Verbose(uint)),SLOT(setVerbose(uint)), Qt::QueuedConnection);
        connect(mytask,SIGNAL(UARTsend(QByteArray,uint)),ic->Uart,SLOT(queueData(QByteArray,uint)), Qt::QueuedConnection);
        connect(mytask,SIGNAL(MotorSignal(bool,bool,int,int)),ic->Uart,SLOT(setMotor(bool,bool,int,int)), Qt::QueuedConnection);
        connect(mytask,SIGNAL(TurretAngleSignal(bool,bool,int,int)),ic->Uart,SLOT(setTurretAngle(bool,bool,int,int)), Qt::QueuedConnection);
        connect(mytask,SIGNAL(MissileSignal(bool,bool,bool)),ic->Uart,SLOT(fireMissile(bool,bool,bool)), Qt::QueuedConnection);
        connect(mytask,SIGNAL(LaserSignal(bool)),ic->Uart,SLOT(setLaser(bool)), Qt::QueuedConnection);

        //Start the task
        QThreadPool::globalInstance()->start(mytask);
    }
}

void MyClient::sendData(QByteArray rData)
{
    //Send the data straight to the client
    socket->write(rData.append("\r\n"));
}

void MyClient::setVerbose(uint level)
{
    verbositylevel = level;
}

void MyClient::setMode(uint level)
{
    sysState.operatingMode = level;
    QVariantMap notification;
    notification["jsonrpc"] = "2.0";
    notification["method"] = "System.SetMode";

    switch(level)
    {
    case MODE_AUTONOMOUS:
        notification["mode"] = "autonomous";
        break;
    case MODE_MANUAL:
        notification["mode"] = "manual";
        break;
    default:
        notification["mode"] = "unknown";
        break;
    }

    emit sendNotification(notification,V_SYSTEMMODE);
}
