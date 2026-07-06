import socket      # Core library for managing network sockets and TCP/IP connections
import threading   # Enables concurrent connection processing so multiple browser tabs load simultaneously

# Global Network Infrastructure Parameters
PROXY_HOST = "127.0.0.1"  # Local loopback interface (localhost)
PROXY_PORT = 8888         # The port assigned to listen for intercepted browser traffic

# Worker function assigned to manage every distinct incoming client connection
def handle_client ( client_socket ) :
    try:
        # 1. Catch the initial application layer request packet from the browser (Buffer: 4096 Bytes)
        request = client_socket.recv ( 4096)
        if not request:
            return

        # 2. Convert raw byte payload into readable text formats to analyze content
        first_line = request.decode ( 'utf-8', errors='ignore' ) .split ( '\n')
        
        # [🔬 PRIMARY RESEARCH CHECKPOINT]: Output the intercepted headers straight to the screen.
        # If the destination uses plain HTTP, sensitive login variables display instantly here.
        print ( f"[🔍 INTERCEPTED NETWORK LOG]: {first_line}")
        
        # 3. Parse headers to programmatically locate the target web server's address
        url = first_line.split ( ' ') if len ( first_line.split ( ' ' ) ) > 1 else ""
        http_pos = url.find ( "://")
        temp = url[ ( http_pos + 3 ) :] if http_pos != -1 else url
        
        port_pos = temp.find ( ":")
        webserver_pos = temp.find ( "/")
        if webserver_pos == -1:
            webserver_pos = len ( temp)

        webserver = ""
        port = 80 # Default listening port designated for unencrypted HTTP traffic
        
        if port_pos == -1 or webserver_pos < port_pos:
            webserver = temp[:webserver_pos]
        else:
            webserver = temp[:port_pos]
            port = int (  ( temp[ ( port_pos + 1 ) :] ) [:webserver_pos - port_pos - 1])

        # 4. Open a fresh outbound TCP socket to bridge communication with the real web server
        server_socket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect (  ( webserver, port ) )
        
        # 5. Forward the original browser packet to the real live server
        server_socket.sendall ( request)

        # 6. Stream incoming server response packets directly back to the active browser instance
        while True:
            reply = server_socket.recv ( 4096)
            if len ( reply) > 0:
                client_socket.sendall ( reply) # Relay data payload back to client
            else:
                break # Terminate stream loop when data payload finishes transferring
                
        server_socket.close ( ) # Clean up server socket resource
    except Exception:
        pass # Silence exceptions to keep the core script engine running during structural shifts
    finally:
        client_socket.close ( ) # Terminate client socket thread session safely

# Core initialization function to bind sockets and activate listening sequences
def start_proxy (  ) :
    # Construct an IPv4 Internet Protocol socket running on standard TCP streams
    server = socket.socket ( socket.AF_INET, socket.SOCK_STREAM)
    
    # Establish ownership over local testing parameter boundaries (127.0.0.1:8888)
    server.bind (  ( PROXY_HOST, PROXY_PORT ) )
    
    # Listen actively for connection inputs (Maximum holding queue backlog = 5 requests)
    server.listen ( 5)
    print ( f"[*] Proxy engine active and listening on {PROXY_HOST}:{PROXY_PORT}")

    # Infinite engine execution loop designed to trap incoming connection queries indefinitely
    while True:
        # Acknowledge and securely capture incoming remote browser socket structures
        client_socket, addr = server.accept ( )
        
        # Instantly delegate the request packet processing workload to a new isolated worker thread
        client_thread = threading.Thread ( target=handle_client, args= ( client_socket, ) )
        client_thread.start ( )

# Main entry point declaration statement to trigger execution cycle
if __name__ == "__main__":
    start_proxy ( )
