#include <QtCore/QCoreApplication>
#include "myserver.h"

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    QStringList arguments = QCoreApplication::arguments();

    int port = 0;
    if(argc > 1)
        port = arguments[1].toInt();

    MyServer Server;
    Server.StartServer(port?port:1234);

    return a.exec();
}
