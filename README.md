## Disclaimer
This is insane task. Because technology is not ready for production use.
Because browser just start support it.
Chrome start support it 22Jan2022 and only 22% of users update to this version.
https://caniuse.com/webtransport
Right now any server can't support WebTransport even HTTP/3



# Test assignemt

## Part 1
I have tried to test the feature but have no luck. Because I can't find any lib that can test http3 and WebTransport


## Part2

### Question
> Make the communication channel secure or suggest what security measures you would implement given more time.
### Answer:
> We could send data via datagram or if we want more secure way use stream.
Datagrams are ideal for sending and receiving data that does not require strong delivery guarantees. Both connections are using HTTP/3 so it's already secured.
_________________________________________________________________________________________________________________________________________________

### Question
> Provide a plan for Kubernetes deployment
### Answer
```
1. Containerize the client and server applications. Or in my case for simple JS we could use S3
2. Define the Kubernetes deployment manifests
3. Create the Kubernetes cluster
4. Deploy the server application
5. Deploy the client application. Or just copy to S3
6. Expose the server application
7. Test the deployment
```
_________________________________________________________________________________________________________________________________________________
### Question
> Provide a plan/design for an auto-recovery mechanism for both sides (in case of a temporary connection failure). Feel free to implement that if you have enough time.
### Answer
> Let`s imagine that we are already deploy our service. In this case I suppose we will use docker
> We can use healthcheck feature

_________________________________________________________________________________________________________________________________________________
### Question:
> Can you think of a way for the client to auto-discover the server without the need to point it to the exact server endpoint?
### Answer:
>  DNS-SD and mDNS is solve this problem

