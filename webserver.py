from socket import * #soket dasar dari komunikasi
import sys           #Memanggil modul ke dalam program 

serverSocket = socket(AF_INET, SOCK_STREAM) #Mengaitkan nomor port server 

# Prepare a server socket
serverPort = 6789                    #Nomor Port 
serverSocket.bind(('', serverPort))  #Pintu pertama untuk menunggu client
serverSocket.listen(1)               #Untuk menunggu permintaan koneksi tcp dari klien 

while True:
    # Establish the connection
    print('Ready to serve...')                          #Memprint string
    connectionSocket, addr = serverSocket.accept()      #Berguna untuk menghubungkan client socket dengan socket server 
    try:
        message = connectionSocket.recv(1024).decode()  #Menerima pesan HTTP dari soket.Lalu mengubah pesan menjadi string
        filename = message.split()[1]                   #berguna untuk memisahkan string dan indeks 2 dari string disimpan ke var filename
        f = open(filename[1:], 'rb')                    #mode 'rb' (read binary) untuk membuka file dalam mode biner.
        outputdata = f.read()                           #berguna untuk membaca seluruh isi file 

        # Determine the content type based on the file extension
        if filename.endswith('.html'):                                         
            content_type = "text/html"                                          #membuka konten tipe text
        elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
            content_type = "image/jpeg"                                         #membuka konten tipe jpeg
        elif filename.endswith('.png'):
            content_type = "image/png"                                          #membuka konten tipe png
        else:
            content_type = "text/html"                                          # Default content type jika tidak terdapat kondisi yang sesuai

        # Send HTTP headers with the appropriate content type
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())                       #Mengirim HTTP response header line ke client
        connectionSocket.send(f"Content-Type: {content_type}\r\n\r\n".encode())     #Memberitahu clinet tipe konten yang dikirim adalah HTML

        # Send the content of the requested file to the client
        connectionSocket.sendall(outputdata)        #Berguna untuk mengirimkan semua data yang ada dalam variabel outputdata melalui soket yang sudah terbentuk.
        connectionSocket.send("\r\n".encode())      #Mengirim newline terakhir ke client sebagai akhir dari HTTP response
        connectionSocket.close()                    #Menutup koneksi socket dengan client
    except IOError:
        # Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())                            #Mengirim respon status line ke client bahwa file tidak ditemukan  
        connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())                       #Menunjukan bahwa tipe konten adalah text/html
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())  #Mengirim pesan body HTTP ke client berisi pesan yang diminta tidak ditemukan 
        connectionSocket.close()                                                                #Menutup koneksi socket dengan client

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
