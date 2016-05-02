#include "myuart.h"

MyUART::MyUART(QObject *parent) :
    QObject(parent)
{
    foreach (const QSerialPortInfo &serialPortInfo, QSerialPortInfo::availablePorts())
    {
        if(serialPortInfo.systemLocation() == "/dev/ttyS0")
        {
            serialPort = new QSerialPort(serialPortInfo);
            portInfo = const_cast<QSerialPortInfo*>(&serialPortInfo);
            break;
        }
    }

    serialPort->setBaudRate(QSerialPort::Baud9600);
    serialPort->setDataBits(QSerialPort::Data8);
    serialPort->setParity(QSerialPort::NoParity);
    //serialPort->stopBits(QSerialPort::OneAndHalfStop);
    //serialPort->flowControl(QSerialPort::NoFlowControl);
    serialPort->open(QIODevice::ReadWrite);

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
