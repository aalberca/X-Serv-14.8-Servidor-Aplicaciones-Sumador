#!/usr/bin/python

"""
webApp class
 Root for hierarchy of classes implementing web applications
 Copyright Jesus M. Gonzalez-Barahona and Gregorio Robles (2009-2015)
 jgb @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - February 2015
"""

import socket
import random


class webApp:
    """Root of a hierarchy of classes implementing web applications
    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""

        return None  #podriamos poner "aaaaaaaaaa" da igual

    def process(self, parsedRequest):
        """Process the relevant elements of the request.
        Returns the HTTP code for the reply, and an HTML page.
        """

        return ("200 OK", "<html><body><h1>It works!</h1></body></html>")

    def __init__(self, hostname, port):
        """Initialize the web application."""

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)

        primer = 0
        while True:
            print 'Waiting for connections'
            (recvSocket, address) = mySocket.accept()
            print 'HTTP request received (going to parse and process):'
            request = recvSocket.recv(2048)
            print request
            try:
                parsedRequest = self.parse(request)
            except ValueError:
                continue
            (returnCode, htmlAnswer, primer) = self.process(parsedRequest, primer)
            print 'Answering back...'
            recvSocket.send("HTTP/1.1 " + returnCode + " \r\n\r\n"
                            + htmlAnswer + "\r\n")
            recvSocket.close()


class calcuApp(webApp):
    def parse(self, request):
        #try:
        loquequiero = int(request.split()[1][1:])
        #except ValueError:
            #print 'ERROOOOOOR'

        return loquequiero

    def process(self, parsedRequest, primer):
        if (primer == 0):
            primer = parsedRequest
            respuesta = "<html><body><h1>Dame otro numero!</h1></body></html>"
        else:
            resultado = primer + parsedRequest
            respuesta = "<html><body><h1>" + str(primer) + "+" + str(parsedRequest) + "=" + str(resultado) + "</h1></body></html>"
            primer = 0
        return ("200 OK", respuesta, primer)


if __name__ == "__main__":
    testWebApp = calcuApp("localhost", 1234)
