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
        qDebug() << "uart error: Unable to open port, error code" << serialPort->error();
    if(!serialPort->setBaudRate(QSerialPort::Baud115200))
        qDebug() << "uart error: Baud rate:" << serialPort->baudRate();
    if(!serialPort->setDataBits(QSerialPort::Data8))
        qDebug() << "uart error: Data bits:" << serialPort->dataBits();
    if(!serialPort->setParity(QSerialPort::NoParity))
        qDebug() << "uart error: Parity:" << serialPort->parity();
    if(!serialPort->setStopBits(QSerialPort::OneAndHalfStop))
        qDebug() << "uart error: Stop bits:" << serialPort->stopBits();
    if(!serialPort->setFlowControl(QSerialPort::SoftwareControl))
        qDebug() << "uart error: Flow control:" << serialPort->flowControl();

    connect(serialPort,SIGNAL(readyRead()),this,SLOT(serialReceived()));

}

void MyUART::serialReceived()
{
    QByteArray data;
    data = serialPort->readAll();
    qDebug() << "UART: " << data;
}

void MyUART::writeData(QByteArray data)
{
    qDebug() << "Going to write \"" << data << "\" to the bus";
    serialPort->write(data, data.length());
}

void MyUART::getPortInfo()
{
    qDebug() << "Number of serial ports: " << QSerialPortInfo::availablePorts().count();

    foreach (const QSerialPortInfo &serialPortInfo, QSerialPortInfo::availablePorts())
    {
        qDebug() << "\nPort:" << serialPortInfo.portName();
        qDebug() << "Location:" << serialPortInfo.systemLocation();
        qDebug() << "Description:" << serialPortInfo.description();
        qDebug() << "Manufacturer:" << serialPortInfo.manufacturer();
        qDebug() << "Vendor Identifier:" << (serialPortInfo.hasVendorIdentifier() ? QByteArray::number(serialPortInfo.vendorIdentifier(), 16) : QByteArray());
        qDebug() << "Product Identifier:" << (serialPortInfo.hasProductIdentifier() ? QByteArray::number(serialPortInfo.productIdentifier(), 16) : QByteArray());
        qDebug() << "Busy:" << (serialPortInfo.isBusy() ? QObject::tr("Yes") : QObject::tr("No"));

        QSerialPort *port = new QSerialPort(serialPortInfo);
        if (port->open(QIODevice::ReadWrite)) {
            qDebug() << "Baud rate:" << port->baudRate();
            qDebug() << "Data bits:" << port->dataBits();
            qDebug() << "Stop bits:" << port->stopBits();
            qDebug() << "Parity:" << port->parity();
            qDebug() << "Flow control:" << port->flowControl();
            qDebug() << "Read buffer size:" << port->readBufferSize();
            port->close();
        } else {
            qDebug() << "Unable to open port, error code" << port->error();
        }
        delete port;
    }
}
