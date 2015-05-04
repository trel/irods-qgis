####################################################

#  Author : Amit Juneja							   #
#  Date: 02/09/2015                                #
#  Description : Fix for error due to MSG_WAITALL  #
#				 variable in Windows               #

####################################################


def read_exactly(sock, size):
    buffer = ''
    while len(buffer) < size:
        data = sock.recv(size-len(buffer))
        if not data:
            break
        buffer+=data
    return buffer