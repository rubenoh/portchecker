import csv
import socket
import time

retry = 2
delay = 2
timeout = 2
MESSAGE = "Package"

def get_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        #print("Hostname :  ",host_name) 
        return host_ip
        #print("IP : ",host_ip) 
    except: 
        host_ip = "Unable to get Hostname and IP"
        #print("Unable to get Hostname and IP") 
        return host_ip

def checkHost(ip, port):
        ipup = False
        for i in range(retry):
                if isOpenTCP(ip, port):
                        ipup = True
                        break
                else:
                        time.sleep(delay)
        return ipup

def isOpenTCP(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
                s.connect((ip, int(port)))
                s.shutdown(socket.SHUT_RDWR)
                return True
        except:
                return False
        finally:
                s.close()

def isOpenUDP(ip, port):
        sudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
        sudp.sendto(MESSAGE.encode(), (ip, int(port)))

def checkfunction():
        with open("hosts.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                line_count = 0
                aux_ip = []
                aux_port = []
                aux_protocol = []
                aux_proj = []
                aux_env = []
                aux_result = []
                for row in csv_reader:
                        ip = (f'{row[0]}')
                        port = (f'{row[1]}')
                        protocol = (f'{row[2]}')
                        proj = (f'{row[3]}')
                        env = (f'{row[4]}')
                        if protocol == "TCP" or protocol == "tcp":
                                if checkHost(ip, port):
                                        aux_ip.append(ip)
                                        aux_port.append(port)
                                        aux_protocol.append(protocol)
                                        aux_proj.append(proj)
                                        aux_env.append(env)
                                        aux_result.append("OK!")
                                else: 
                                        aux_ip.append(ip)
                                        aux_port.append(port)
                                        aux_protocol.append(protocol)
                                        aux_proj.append(proj)
                                        aux_env.append(env)
                                        aux_result.append("KO!")
                                line_count += 1
                        elif protocol == "UDP" or protocol == "udp":
                                isOpenUDP(ip, port)
                                aux_ip.append(ip)
                                aux_port.append(port)
                                aux_protocol.append(protocol)
                                aux_proj.append(proj)
                                aux_env.append(env)
                                aux_result.append("OK!  Package Sended")
                                line_count += 1
                        else:
                                aux_ip.append(ip)
                                aux_port.append(port)
                                aux_protocol.append(protocol)
                                aux_proj.append(proj)
                                aux_env.append(env)
                                aux_result.append("Protocol Error")
                                line_count += 1
                aux = ({'IP': aux_ip, 'Port': aux_port, 'Protocol': aux_protocol, "Project": aux_proj, "Environment": aux_env, "Status": aux_result})                      
        return aux

def function_troubleshoot(ip, port, protocol):
        aux_ip = []
        aux_port = []
        aux_protocol = []
        aux_result = []
        if protocol == "TCP" or protocol == "tcp":  
                if checkHost(ip, port):
                        aux_ip.append(ip)
                        aux_port.append(port)
                        aux_protocol.append(protocol)
                        aux_result.append("OK!")
                else: 
                        aux_ip.append(ip)
                        aux_port.append(port)
                        aux_protocol.append(protocol)
                        aux_result.append("KO!")
        elif protocol == "UDP" or protocol == "udp":
                isOpenUDP(ip, port)
                aux_ip.append(ip)
                aux_port.append(port)
                aux_protocol.append(protocol)
                aux_result.append("OK!  Package Sended")               
        else:
                aux_ip.append(ip)
                aux_port.append(port)
                aux_protocol.append(protocol)
                aux_result.append("Entry pattern error. try url in the following form: troubleshooting/?ip=<ipdir>&port=<portvalue>&protocol=<tcp or udp>")                 
        aux = ({'IP': aux_ip, 'Port': aux_port, 'Protocol': aux_protocol, "Status": aux_result})
        return aux