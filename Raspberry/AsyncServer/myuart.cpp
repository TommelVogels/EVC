#include "myuart.h"
#include "globaldefines.h"
#include "json.h"

MyUART::MyUART(QObject *parent) :
    QObject(parent)
{
    // Set the timer
    timer = new QTimer(this);
    timer->setSingleShot(true);
    timer->setInterval(100000);
    connect(timer,SIGNAL(timeout()),this,SLOT(timeOut()));

    //Iterate over the available serial ports and pick the one that is needed.
    foreach (const QSerialPortInfo &serialPortInfo, QSerialPortInfo::availablePorts())
    {
        if(serialPortInfo.systemLocation() == "/dev/ttyAMA0")
        {
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

/** This function should be used to read incomming messages that are queued
 **/
QByteArray MyUART::pop()
{
    QByteArray dummy;
    return receivedQueue.size() > 0 ? receivedQueue.dequeue() : dummy;
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
    {
        timer->start();
        return;
    }

    //The received messages start with 0x5A, followed by the lenght of the message
    //If we have found a start byte, the length of the data and enough bytes to read
    //   the message, we'll try to decode
    int idx = receivedData.indexOf(UART_STARTBYTE);
    int len = receivedData[idx + UART_LENGTH_POS];
    if(idx > -1 && len > -1 && receivedData.length() >= idx + len)
    {
        //We found something that looks like a command
        QByteArray com = receivedData.mid(idx, len + UART_OVERHEAD);
        qDebug() << "UART: \tFound command:" << QString(com.toHex());

        //Cut the used part of the received data
        //We need to keep the rest as it might be part of a new message
        receivedData = receivedData.right(receivedData.length() - (idx + len));

        //Add the command to the received queue and dequeue if the size becomes to big
        receivedQueue.enqueue(com);
        if(receivedQueue.size() > 255) receivedQueue.dequeue();

        //Allow new command to be sent over UART
        waitingForAck = false;
        writeData();
    } 
    // If no message can be decoded directly, we start a timer and hope that
    // future data will complement it to a fully readable command.
    else
    {
        qDebug() << "UART: \tDid not find a command";
        timer->start();
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
 ** put in the queue. If there is already a command with the same function it gets
 ** replaced. A new message can only be sent if the previous is acknowledged.
 **
 ** the 'uint function' variable might be 0 (and is so by default). This means that
 ** it is assumed that the data does not need formatting. This is for examplethe case
 ** for the Dbus push(..) interface and the JSON PRC SendUART(..) interface.
 **/
void MyUART::queueData(QByteArray data, uint function)
{
    //If there is no function argument we need at least a data length equal to
    //the position of the command 'overhead', otherwise it cannot be valid
    if(function == 0 && data.length() < UART_MINLENGTH)
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



    //Replace command if there is a command with the same function
    for(int i = 0; i<queue.size(); i++)
    {
        QPair<QByteArray, uint> p = queue.at(i);
        if(p.second == function)
        {
            queue.replace(i,qMakePair(data, function));
            qDebug() << "UART: \tReplaced:" << QString(data.toHex());
            writeData();
            return;
        }
    }

    //There was no command with the same function;
    //Put the data in the queue and try to write it on the bus.
    //It depends on writeData if this happens immediately.
    queue.enqueue(qMakePair(data, function));
    qDebug() << "UART: \tEnqueued:" << QString(data.toHex());
    writeData();
}

void MyUART::setMotor(bool left, bool right, int l, int r)
{
    unsigned char c;
    QByteArray commandData;

    if(left && l > -256 && l < 256)
    {
        if(l>=0) c = 0x01;
        else c= 0x00;
        commandData.append(c);
        quint8 left8 = (quint8)abs(l);
        commandData.append(left8);
    }
    else left = false;

    if(right && r > -256 && r < 256)
    {
        if(r>=0) c = 0x01;
        else c= 0x00;
        commandData.append(c);
        quint8 right8 = (quint8)abs(r);
        commandData.append(right8);
    }
    else right = false;

    if(left && right) queueData(commandData,UART_BOTHMOTORSPEED);
    else if(left)     queueData(commandData,UART_LEFTMOTORSPEED);
    else if(right)    queueData(commandData,UART_RIGHTMOTORSPEED);
}

void MyUART::setTurretAngle(bool horizontal, bool vertical, int h, int v)
{
    QByteArray commandData;

    if(horizontal && h > -1 && h < 181)
        commandData.append((quint8)abs(h));
    else horizontal = false;

    if(vertical && v > -1 && v < 91)
        commandData.append((quint8)abs(v));
    else vertical = false;

    if(horizontal && vertical) queueData(commandData,UART_TURRETBOTHDIRS);
    else if(horizontal)        queueData(commandData,UART_TURRETHORIZONTAL);
    else if(vertical)          queueData(commandData,UART_TURRETVERTICAL);
}

void MyUART::fireMissile(bool t1, bool t2, bool all)
{
    QByteArray dummy;

    if(t1 && t2)    queueData(dummy,UART_FIREALLT12);
    else if(t1) {
        if(all)     queueData(dummy,UART_FIREALLT1);
        else        queueData(dummy,UART_FIREMISSILET1); }
    else if(t2) {
        if(all)     queueData(dummy,UART_FIREALLT2);
        else        queueData(dummy,UART_FIREMISSILET2); }
}

void MyUART::setLaser(bool on)
{
    unsigned char c;
    QByteArray commandData;

    c = on? 0x01 : 0x00;
    commandData.append(c);

    queueData(commandData,UART_FLIPLASER);
}

/** This function handles the actual sending of the data over uart
 ** in addition it sends a notification that it sent a command
 **/
void MyUART::writeData()
{
    //If we are still awaiting the ack of a previous message we won't do anything now
    if(waitingForAck || queue.isEmpty() )
        return;

    //We are going to send a new command, hence we get a command from the fifo,
    //send it, and wait for the ack
    waitingForAck = true;
    QPair<QByteArray, uint> headpair = queue.dequeue();
    QByteArray head = headpair.first;
    lastCommand = head;
    qDebug() << "UART: \tGoing to write" << QString(head.toHex()) << "to the bus";
    serialPort->write(head, head.length());
    timer->start();

    //Based on the type of message we will send a notification
    QVariantMap noti;
    noti["direction"] = "RA";
    noti["source"] = "UART";
    uint verbosity = 0;

    quint8 function = head[UART_COMMANDID_POS];
    switch(function)
    {
    case UART_FIREALLT1:
        noti["method"] = "Turret.FireMissile";
        noti["turret"] = 1;
        noti["amount"] = "all";
        verbosity = V_TURRETMISSILE;
        break;
    case UART_FIREALLT2:
        noti["method"] = "Turret.FireMissile";
        noti["turret"] = 2;
        noti["amount"] = "all";
        verbosity = V_TURRETMISSILE;
        break;
    case UART_FIREALLT12:
        noti["method"] = "Turret.FireMissile";
        noti["turret"] = 12;
        noti["amount"] = "all";
        verbosity = V_TURRETMISSILE;
        break;
    case UART_FIREMISSILET1:
        noti["method"] = "Turret.FireMissile";
        noti["turret"] = 1;
        noti["amount"] = "one";
        verbosity = V_TURRETMISSILE;
        break;
    case UART_FIREMISSILET2:
        noti["method"] = "Turret.FireMissile";
        noti["turret"] = 2;
        noti["amount"] = "one";
        verbosity = V_TURRETMISSILE;
        break;
    case UART_FLIPLASER:
        noti["method"] = "Turret.SetLaser";
        noti["on"] = head[UART_DATA_POS] ? true : false;
        verbosity = V_TURRETLASER;
        break;
    case UART_LEFTMOTORSPEED:
        noti["method"] = "Motor.SetMotor";
        if(head[UART_DATA_POS])
        noti["left"] = head[UART_DATA_POS] ?
                       head[UART_DATA_POS + 1] :
                     - head[UART_DATA_POS + 1] ;
        verbosity = V_MOTORSPEED;
        break;
    case UART_RESETPERIPHERALS:
        noti["method"] = "resetPeripherals";
        break;
    case UART_RIGHTMOTORSPEED:
        noti["method"] = "Motor.SetMotor";
        noti["right"] = head[UART_DATA_POS] ?
                        head[UART_DATA_POS + 1] :
                      - head[UART_DATA_POS + 1] ;
        verbosity = V_MOTORSPEED;
        break;
    case UART_BOTHMOTORSPEED:
        noti["method"] = "Motor.SetMotor";
        noti["left"]  = head[UART_DATA_POS]     ?
                        head[UART_DATA_POS + 1] :
                      - head[UART_DATA_POS + 1] ;
        noti["right"] = head[UART_DATA_POS + 2] ?
                        head[UART_DATA_POS + 3] :
                      - head[UART_DATA_POS + 3] ;
        verbosity = V_MOTORSPEED;
        break;
    case UART_TURRETHORIZONTAL:
        noti["method"] = "Turret.SetAngle";
        noti["horizontal"] = (int)head[UART_DATA_POS];
        verbosity = V_TURRETANGLE;
        break;
    case UART_TURRETVERTICAL:
        noti["method"] = "Turret.SetAngle";
        noti["vertical"] = (int)head[UART_DATA_POS];
        verbosity = V_TURRETANGLE;
        break;
    case UART_TURRETBOTHDIRS:
        noti["method"] = "Turret.SetAngle";
        noti["horizontal"] = (int)head[UART_DATA_POS];
        noti["vertical"]   = (int)head[UART_DATA_POS + 1];
        verbosity = V_TURRETANGLE;
        break;

    default:
        noti["method"] = "unknown";
        verbosity = V_REMAINING;
        break;
    }

    noti["data"] = QString(head.mid(UART_DATA_POS,head.length()-UART_MINLENGTH).toHex());
    emit notification(noti, verbosity);
}
