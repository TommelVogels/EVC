#include "myuart.h"
#include "globaldefines.h"
#include "json.h"

MyUART::MyUART(QObject *parent) :
    QObject(parent)
{
    // Set the timer
    timer = new QTimer(this);
    timer->setSingleShot(true);
    timer->setInterval(500);
    connect(timer,SIGNAL(timeout()),this,SLOT(timeOut()));

    //Iterate over the available serial ports and pick the one that is needed.
    foreach (const QSerialPortInfo &serialPortInfo, QSerialPortInfo::availablePorts())
    {
        if(serialPortInfo.systemLocation() == "/dev/ttyAMA0")
        {
            qDebug() << "found";
            serialPort = new QSerialPort(serialPortInfo);
            portInfo = const_cast<QSerialPortInfo*>(&serialPortInfo);
            break;
        }
    }

    //Try to open the device and try to set all the correct settings
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
}

/** This function is automatically invoked when data is
 ** sent to the raspberry over uart
 **/
void MyUART::serialReceived()
{  
    //A timer is set when something is received, but does not hold a valid command (yet)
    //If new data comes in we disable the timer and check again
    timer->stop();

    //Read all data and append it to the existing data
    QByteArray data = serialPort->readAll();
    receivedData.append(data);
    qDebug() << "UART: \tReceived:" << QString(data.toHex());

    //If the data is to short we cannot do anything with it. It is kept
    //in memory so that combined with future data it hopfully will form a command
    if(receivedData.length() < UART_LENGTH_POS + 1)
        return;

    //The received messages start with 0x5A, followed by the lenght of the message
    //If we have found a start byte, the length of the data and enough bytes to read
    //   the message, we'll try to decode
    int idx = receivedData.indexOf(0x5A);
    int len = receivedData[idx + UART_LENGTH_POS];
    if(idx > -1 && len > -1 && receivedData.length() >= idx + len)
    {
        //We found something that looks like a command
        QByteArray com = receivedData.mid(idx, len);
        qDebug() << "UART: \tFound command:" << QString(com.toHex());

        //Cut the used part of the received data
        //We need to keep the rest as it might be part of a new message
        receivedData = receivedData.right(receivedData.length() - (idx + len));
        waitingForAck = false;
        writeData();
    } 
    // If no message can be decoded directly, we start a timer and hope that
    // future data will complement it to a fully readable command.
    else
    {
        timer->start();
        waitingForAck = false;
        writeData();
    }
}

/** This function is fired automatically when the timer times out.
 ** It means that there is unreadable data in the receivedData variable.
 ** The only thing that we can do is reset the variable and hope for the best.
 **/
void MyUART::timeOut()
{
    qDebug() << "UART: \tTimer timed out";
    receivedData = "";
    waitingForAck = false;
    writeData();
}

/** When some other program (via IPC or RPC) wants to send data over UART, it is
 ** queued in a fifo. A new message can only be sent if the previous is acknowledged.
 **
 ** the 'uint function' variable might be 0 (and is so by default). This means that
 ** it is assumed that the data does not need formatting. This is for examplethe case
 ** for the Dbus push(..) interface and the JSON PRC SendUART(..) interface.
 **/
void MyUART::queueData(QByteArray data, uint function)
{
    //If there is no function argument we need at least a data length equal to
    //the position of the command 'overhead', otherwise it cannot be valid
    if(data.isNull() || (function == 0 && data.length() < UART_OVERHEAD))
        return;

    //If function is defined we format the command.
    if(function)
    {
        QByteArray uartComm;
        quint8 len = (quint8)(data.length()+1);
        quint8 commID = (quint8)(function);
        uartComm.append((quint8)(UART_STARTBYTE));
        uartComm.append(len);
        uartComm.append(commID);
        uartComm.append(data);
        quint8 checksum = commID ^ len;
        if(data.length() > 0)
            for(int i = 0; i<data.length(); i++)
                checksum ^= (quint8)data[i];
        uartComm.append(checksum);
        uartComm.append((quint8)(UART_STOPBYTE));
        data = uartComm;
    }

    qDebug() << "UART: \tEnqueued:" << QString(data.toHex());

    //Put the data in the queue and try to write it on the bus.
    //It depends on writeData if this happens immediately.
    queue.enqueue(data);
    writeData();
}

/** This function handles the actual sending of the data over uart
 ** in addition it sends a notification that it sent a command
 **/
void MyUART::writeData()
{
    //If we are still awaiting the ack of a previous message we won't do anything now
    if(/*waitingForAck ||*/ queue.isEmpty() )
        return;

    //We are going to send a new command, hence we get a command from the fifo,
    //send it, and wait for the ack
    qDebug() << "fts";
    waitingForAck = true;
    QByteArray head = queue.dequeue();
    lastCommand = head;
    qDebug() << "UART: \tGoing to write" << QString(head.toHex()) << "to the bus";
    serialPort->write(head, head.length());

    //Based on the type of message we will send a notification
    QVariantMap json;
    json["jsonrpc"] = "2.0";
    json["direction"] = "RA";
    json["source"] = "UART";
    uint verbosity = 0;

    quint8 function = head[UART_COMMANDID_POS];
    switch(function)
    {
    case UART_FIREALLT1:
        json["method"] = "fireAllT1";
        verbosity = V_TURRETMISSILE;
        break;
    case UART_FIREALLT2:
        json["method"] = "fireAllT2";
        verbosity = V_TURRETMISSILE;
        break;
    case UART_FIREALLT12:
        json["method"] = "fireAllT12";
        verbosity = V_TURRETMISSILE;
        break;
    case UART_FIREMISSILET1:
        json["method"] = "fireMissileT1";
        verbosity = V_TURRETMISSILE;
        break;
    case UART_FIREMISSILET2:
        json["method"] = "fireMissileT2";
        verbosity = V_TURRETMISSILE;
        break;
    case UART_FLIPLASER:
        json["method"] = "flipLaser";
        verbosity = V_TURRETLASER;
        break;
    case UART_LEFTMOTORSPEED:
        json["method"] = "leftMotorSpeed";
        verbosity = V_MOTORSPEED;
        break;
    case UART_RESETPERIPHERALS:
        json["method"] = "resetPeripherals";
        break;
    case UART_RIGHTMOTORSPEED:
        json["method"] = "rightMotorSpeed";
        verbosity = V_MOTORSPEED;
        break;
    case UART_TESTSEQUENCE:
        json["method"] = "testSequence";
        break;
    case UART_TURRETHORIZONTAL:
        json["method"] = "turretHorizontal";
        verbosity = V_TURRETANGLE;
        break;
    case UART_TURRETVERTICAL:
        json["method"] = "turretVertical";
        verbosity = V_TURRETANGLE;
        break;

    default:
        json["method"] = "unknown";
        break;
    }

    json["data"] = QString(head.mid(UART_DATA_POS,head.length()-UART_OVERHEAD).toHex());
    emit notification(QtJson::serialize(json), verbosity);
}
