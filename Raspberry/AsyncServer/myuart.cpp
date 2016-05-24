#include "myuart.h"


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
        qDebug() << "UART: \tError: Unable to open port, error code" << serialPort->error();
    if(!serialPort->setBaudRate(QSerialPort::Baud115200))
        qDebug() << "UART: \tError: Baud rate:" << serialPort->baudRate();
    if(!serialPort->setDataBits(QSerialPort::Data8))
        qDebug() << "UART: \tError: Data bits:" << serialPort->dataBits();
    if(!serialPort->setParity(QSerialPort::NoParity))
        qDebug() << "UART: \tError: Parity:" << serialPort->parity();
    if(!serialPort->setStopBits(QSerialPort::OneAndHalfStop))
        qDebug() << "UART: \tError: Stop bits:" << serialPort->stopBits();
    if(!serialPort->setFlowControl(QSerialPort::SoftwareControl))
        qDebug() << "UART: \tError: Flow control:" << serialPort->flowControl();

    connect(serialPort,SIGNAL(readyRead()),this,SLOT(serialReceived()));

}

void MyUART::serialReceived()
{
    QByteArray data;
    data = serialPort->readAll();
    qDebug() << "UART: \tReceived: \"" << data << "\"";
}

void MyUART::writeData(QByteArray data)
{
    qDebug() << "UART: \tGoing to write \"" << data << "\" to the bus";
    serialPort->write(data, data.length());
}

void MyUART::getPortInfo()
{
    qDebug() << "UART: \tNumber of serial ports: " << QSerialPortInfo::availablePorts().count();

    foreach (const QSerialPortInfo &serialPortInfo, QSerialPortInfo::availablePorts())
    {
        qDebug() << "UART: \tPort:" << serialPortInfo.portName();
        qDebug() << "UART: \tLocation:" << serialPortInfo.systemLocation();
        qDebug() << "UART: \tDescription:" << serialPortInfo.description();
        qDebug() << "UART: \tManufacturer:" << serialPortInfo.manufacturer();
        qDebug() << "UART: \tVendor Identifier:" << (serialPortInfo.hasVendorIdentifier() ? QByteArray::number(serialPortInfo.vendorIdentifier(), 16) : QByteArray());
        qDebug() << "UART: \tProduct Identifier:" << (serialPortInfo.hasProductIdentifier() ? QByteArray::number(serialPortInfo.productIdentifier(), 16) : QByteArray());
        qDebug() << "UART: \tBusy:" << (serialPortInfo.isBusy() ? QObject::tr("Yes") : QObject::tr("No"));

        QSerialPort *port = new QSerialPort(serialPortInfo);
        if (port->open(QIODevice::ReadWrite)) {
            qDebug() << "UART: \tBaud rate:" << port->baudRate();
            qDebug() << "UART: \tData bits:" << port->dataBits();
            qDebug() << "UART: \tStop bits:" << port->stopBits();
            qDebug() << "UART: \tParity:" << port->parity();
            qDebug() << "UART: \tFlow control:" << port->flowControl();
            qDebug() << "UART: \tRead buffer size:" << port->readBufferSize();
            port->close();
        } else {
            qDebug() << "UART: \tUnable to open port, error code" << port->error();
        }
        delete port;
    }
}
