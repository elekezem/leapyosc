from OSC import OSCServer
import sys
from time import sleep

message_count = 0

def log(msg):
    sys.stderr.write(str(msg))
    sys.stderr.flush()

def main(hostname="localhost",port="8000"):
    server = OSCServer((hostname, int(port)))
    server.timeout = 0
    run = True
    global message_count
    message_count = 0

    # this method of reporting timeouts only works by convention
    # that before calling handle_request() field .timed_out is 
    # set to False
    def handle_timeout(self):
        self.timed_out = True

    # funny python's way to add a method to an instance of a class
    import types
    server.handle_timeout = types.MethodType(handle_timeout, server)

    def user_callback(path, tags, args, source):
        log("%s %s\n" % (path, args))
        global message_count
        message_count += 1

    def quit_callback(path, tags, args, source):
        #global run
        run = False

    server.addMsgHandler( "default", user_callback )
    server.addMsgHandler( "/quit", quit_callback )

    # user script that's called by the game engine every frame
    def each_frame():
        log("Messages received: %s\n" % message_count)
        # clear timed_out flag
        server.timed_out = False
        # handle all pending requests then return
        while not server.timed_out:
            server.handle_request()

    # simulate a "game engine"
    print "Server running at %s:%s" % (hostname, port)
    while run:
        # do the game stuff:
        sleep(1)
        # call user script
        each_frame()

    server.close()


if __name__ == "__main__":
    main(*sys.argv[1:])