```shell
mkdir -p $GOPATH/src/google.golang.org
cd $GOPATH/src/google.golang.org
git clone https://github.com/grpc/grpc-go.git grpc
git clone https://github.com/google/go-genproto.git genproto

mkdir -p $GOPATH/src/golang.org/x
cd $GOPATH/src/golang.org/x
git clone https://github.com/golang/net.git
git clone https://github.com/golang/text.git

go install google.golang.org/grpc
```