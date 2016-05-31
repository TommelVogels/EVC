#include <QTimer>
#include "myuart.h"
#include "globaldefines.h"
#include "json.h"

MyUART::MyUART(QObject *parent) :
    QObject(parent)
{
    foreach (const QSerialPortInfo &serialPortInfo, QSerialPortInfo::availablePorts())
    {
        if(serialPortInfo.systemLocation() == "/dev/ttyAMA0")
        {
            serialPort = new QSerialPort(serialPortInfo);
            portInfo = const_cast<QSerialPortInfo*>(&serialPortInfo);
            break;
        }
    }

    if(!serialPort->open(QIODevice::ReadWrite))
    {
        qDebug() << "UART: \tError: Unable to open port, error code" << serialPort->error();
        return;
    }
    if(!serialPort->setBaudRate(QSerialPort::Baud115200))
        qDebug() << "UART: \tError: Baud rate:" << serialPort->baudRate();
    if(!serialPort->setDataBits(QSerialPort::Data8))
        qDebug() << "UART: \tError: Data bits:" << serialPort->dataBits();
    if(!serialPort->setParity(QSerialPort::NoParity))
        qDebug() << "UART: \tError: Parity:" << serialPort->parity();
    if(!serialPort->setStopBits(QSerialPort::OneStop))
        qDebug() << "UART: \tError: Stop bits:" << serialPort->stopBits();
    if(!serialPort->setFlowControl(QSerialPort::NoFlowControl))
        qDebug() << "UART: \tError: Flow control:" << serialPort->flowControl();

    qDebug() << "UART: \tStarted without errors";
    connect(serialPort,SIGNAL(readyRead()),this,SLOT(serialReceived()));
    waitingForAck = false;

    QTimer::singleShot(500, this, SLOT(serialReceived()));

}

void MyUART::serialReceived()
{  
    if(qobject_cast<QTimer *>(QObject::sender()))
        qDebug() << "UART: \tTimeout";


    QByteArray data = serialPort->readAll();
    receivedData.append(data);
    qDebug() << "UART: \tReceived:" << QString(data.toHex());

    if(receivedData.length() < UART_LENGTH_POS + 1)
        return;

    int idx = receivedData.indexOf(0x5A);
    int len = receivedData[idx + UART_LENGTH_POS];
    if(idx > -1 && len > -1 && receivedData.length() >= idx + len)
    {
        QByteArray com = receivedData.mid(idx, len);
        qDebug() << "UART: \tFound command:" << QString(com.toHex());

        receivedData = receivedData.right(receivedData.length() - (idx + len));
        waitingForAck = false;
        writeData();
    } 
}

void MyUART::queueData(QByteArray data, uint function)
{
    if(data.length() == 0 || (function == 0 && data.length() < 3))
        return;

    if(function)
    {
        QByteArray uartComm;
        uartComm.append(UART_STARTBYTE);
        uartComm.append(data.length()+UART_OVERHEAD);
        uartComm.append(function);
        uartComm.append(data);
        uartComm.append(function ^ data[data.length()-1]);
        uartComm.append(UART_STOPBYTE);
        data = uartComm;
    }

    qDebug() << "UART: \tEnqueued:" << QString(data.toHex());
    queue.enqueue(data);
    writeData();
}

void MyUART::writeData()
{
    if(waitingForAck || queue.isEmpty())
        return;

    waitingForAck = true;
    QByteArray head = queue.dequeue();
    qDebug() << "UART: \tGoing to write" << QString(head.toHex()) << "to the bus";
    serialPort->write(head, head.length());

    //Send a notification
    QVariantMap json;
    json["jsonrpc"] = "2.0";
    json["notification"] = "UART";
    json["direction"] = "RA";
    uint verbosity = 0;

    quint8 function = head[UART_COMMANDID_POS];
    switch(function)
    {
    case UART_FIREALLT1:
        json["function"] = "fireAllT1";
        verbosity = V_TURRETMISSILE;
        break;
    case UART_FIREALLT2:
        json["function"] = "fireAllT2";
        verbosity = V_TURRETMISSILE;
        break;
    case UART_FIREALLT12:
        json["function"] = "fireAllT12";
        verbosity = V_TURRETMISSILE;
        break;
    case UART_FIREMISSILET1:
        json["function"] = "fireMissileT1";
        verbosity = V_TURRETMISSILE;
        break;
    case UART_FIREMISSILET2:
        json["function"] = "fireMissileT2";
        verbosity = V_TURRETMISSILE;
        break;
    case UART_FLIPLASER:
        json["function"] = "flipLaser";
        verbosity = V_TURRETLASER;
        break;
    case UART_LEFTMOTORSPEED:
        json["function"] = "leftMotorSpeed";
        verbosity = V_MOTORSPEED;
        break;
    case UART_RESETPERIPHERALS:
        json["function"] = "resetPeripherals";
        break;
    case UART_RIGHTMOTORSPEED:
        json["function"] = "rightMotorSpeed";
        verbosity = V_MOTORSPEED;
        break;
    case UART_TESTSEQUENCE:
        json["function"] = "testSequence";
        break;
    case UART_TURRETHORIZONTAL:
        json["function"] = "turretHorizontal";
        verbosity = V_TURRETANGLE;
        break;
    case UART_TURRETVERTICAL:
        json["function"] = "turretVertical";
        verbosity = V_TURRETANGLE;
        break;

    default:
        json["function"] = "unknown";
        break;
    }

    json["data"] = QString(head.mid(UART_DATA_POS,head.length()-UART_OVERHEAD).toHex());
    emit notification(QtJson::serialize(json), verbosity);
}
