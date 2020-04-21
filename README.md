####    SocketServer简化了网络服务器的编写
+   初始化类Handler，它是一个集成BaseRequestHandler的类中的handle方法决定了每一个链接过来的操作，类控制器类名可以是其他的，只要继承了BaseRequestHandle就行
    +   使用socketserver来实现异步服务端
        +   init():初始化套接字，地址，处理实例信息。
        +   handle()：定义如何控制每一个连接，相当于句柄。
        +   setup():在handle()之前执行，一般作为设置默认之外的连接配置。
        +   finish()：在handle之后执行。
        +   self.request 套接字对象，使用self.request.xxxxx调用套接字的函数
        +   self.server包含调用处理程序的实例
        +   self.client_address是客户端地址信息
        +   定义服务类型TCP：server=socketserver.TCPServer((HOST,PORT),Handler)
        +   UDP:server=socketserver.UDPServer((HOST,PORT),Handler)
        +   server.shutdown()：关闭服务
+   它有4个同步类：
    +   TCPServer
    +   UDPServer
    +   UnixStreamServer
    +   UnixDatagramServer
+   两个Mixin类，用来支持异步。
    +   ForkingMixIn
    +   ThreadingMixIn
+   组合得到
    +   class ForkingUDPServer(ForkingMixIn,UDPServer):pass
    +   class ForkingTCPServer(ForkingMixIn,TCPServer):pass
    +   class ThreadingUDPServer(ThreadingMixIn,UDPServer):pass
    +   class ThreadingTCPServer(ThreadingMixIn,TCPServer):pass
    +   fork是创建多进程，thread是创建多线程。
    +   fork需要操作系统支持，Windows不支持。
+   ThreadingUDPServer与ThreadingTCPServer类中的特有属性：
    +   daemon_threads=False #默认值是False表示创建的线程都不是daemon线程，改为True表示创建的所有线程都是daemon线程
    +   block_on_close=False #默认值为Fasle，如果为True，可以设置为守护线程3.7版本可以用
    +   <div class="table-box"><table>
<thead>
<tr>
<th align="left">方法</th>
<th align="left">含义</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><strong>server_address</strong></td>
<td align="left">服务器正在监听的地址和端口，在不同协议格式不一样。Internet协议上是一个元组(“127.0.0.1”,80)</td>
</tr>
<tr>
<td align="left"><strong>socket</strong></td>
<td align="left">服务器正在监听的套接字对象。socket</td>
</tr>
<tr>
<td align="left">request_queue_size</td>
<td align="left">请求队列的大小。如果处理单个请求需要很长时间，那么在服务器繁忙时到达的任何请求都会被放入队列中，直到request_queue_size请求为止。一旦队列满了，来自客户机的进一步请求将得到一个“连接被拒绝”错误。默认值通常是5，但是可以被子类覆盖。</td>
</tr>
<tr>
<td align="left">address_family</td>
<td align="left">服务器套接字所属的协议族。常见的例子是套接字。AF_INET socket.AF_UNIX。</td>
</tr>
<tr>
<td align="left">socket_type</td>
<td align="left">服务器使用的套接字类型;套接字。SOCK_STREAM套接字。SOCK_DGRAM是两个常见的值。</td>
</tr>
<tr>
<td align="left">timeout</td>
<td align="left">超时持续时间，以秒为单位度量，如果不需要超时，则为None。如果handle_request()在超时期间没有收到传入的请求，则调用handle_timeout()方法。</td>
</tr>
<tr>
<td align="left"><strong>handle_request()</strong></td>
<td align="left"><strong>处理单个请求，同步执行</strong><br>这个函数按顺序调用以下方法:get_request()、verify_request()和process_request()。如果处理程序类的用户提供的handle()方法引发异常，将调用服务器的handle_error()方法。如果在超时秒内没有收到任何请求，那么将调用handle_timeout()并返回handle_request()。</td>
</tr>
<tr>
<td align="left"><strong>server_forever(poll_interval=0.5)</strong></td>
<td align="left"><strong>异步执行，处理请求</strong>。每隔poll_interval秒轮询一次。<br>忽略timeout属性，还会调用service_actions()，在ForkingMixIn的子类中定义，可以用来清理僵尸进程。</td>
</tr>
<tr>
<td align="left"><strong>shutdown()</strong></td>
<td align="left">告诉serve_forever循环停止。并等待他结束。</td>
</tr>
<tr>
<td align="left"><strong>server_close()</strong></td>
<td align="left">关闭服务器</td>
</tr>
<tr>
<td align="left">finish_request(request,client_address)</td>
<td align="left">通过实例化RequestHandlerClass并调用它的handle()方法来处理请求</td>
</tr>
<tr>
<td align="left">server_bind()</td>
<td align="left">由服务器的构造函数调用，以将套接字绑定到所需的地址。可能会被覆盖。</td>
</tr>
<tr>
<td align="left">verify_request(request,client_address)</td>
<td align="left">必须返回一个布尔值;如果值为True，请求将被处理，如果值为False，请求将被拒绝。可以重写此函数来实现服务器的访问控制。默认实现总是返回True。</td>
</tr>
</tbody>
</table></div>

+   BaserRequestHandler类
<ol>
<li>是和用户连接的用户请求处理类的基类，</li>
<li><code>BaseRequestHandler(request,client_address,server)</code> #构造函数
<ul>
<li>request #是和客户端的连接的socket对象</li>
<li>client_address #是客户端地址</li>
<li>server #是TCPServer实例本身</li>
</ul>
</li>
<li>服务端Server实例接收用户请求后，最后会实例化这个类。它被初始化时，送入3个构造参数：request, client_address, server自身 以后就可以在BaseRequestHandler类的实例上使用以下属性：
<ul>
<li>self.request是和客户端的连接的socket对象</li>
<li>self.server是TCPServer实例本身</li>
<li>self.client_address是客户端地址</li>
</ul>
</li>
<li>这个类在初始化的时候，它会依次调用3个方法。子类可以覆盖这些方法。</li>
</ol>

+   运行服务端：
    +   持续运行一个serve_forever，即使一个连接报错了，但不会导致程序停止，而是会持续运行，与其他客户端通信
        +   server.serve_forever()
        +   serve.shutdown()
```
import socketserver

class MyServer(socketserver.BaseRequestHandler):
    #   集成一个socketserver的基础类来初始化我们自己的服务器
    def handle(self):
        #   写一个handle方法，必须叫这个名字要不不能够运行父类的pass
        #   self.request相当于一个conn
        self.request.recv(1024) # 收消息
        msg = '会用了不？'
        self.request.send(BytesWarning(msg,encode('utf-8')))    #   发一条
        self.request.close()    #   关闭连接
        #   拿到了我们对每个客户端的管道之后，我们就可以在这里写信息发送的逻辑了
```
+   SocketServer主要被抽象为两个主要的类，BaseServer类用于处理联结相关的网络操作，BaseRequestHandler用于处理数据相关的操作，SocketServer还提供了两个MixIn类，用于实际处理数据相关的操作。BaseRequestHandler类，用于实际处理数据相关的操作，SocketServer还提供了两个MixIn类，ThreadingMinIn和ForkingMixIn用于拓展多线程，多进程服务器。
+   BaseServer类
    +   server_activate
    +   serve_forever
    +   shutdown
    +   service_action
    +   handle_request
    +   handlerrequest_noblock
    +   handle_timeout
    +   verify_request
    +   process_request
    +   server_close
    +   finish_request
    +   shutdown_request
    +   close_request
    +   handle_error

[socketserver](https://www.cnblogs.com/double-W/p/10704680.html)
