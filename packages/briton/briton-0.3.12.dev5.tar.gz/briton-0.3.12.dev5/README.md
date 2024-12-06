# Briton

The python side of Briton. Briton server is written in C++ for high performance
and provides a grpc endpoint for interaction. A major function of this python
libarary is to provide easier interaction with the Briton Server. e.g. there's
logic to startup the Briton server and ensure it's healthy. It also provides
adapters for using Briton from Truss. For certain features, such as draft model
based speculative decoding, a subtantial chunk of the implementation is in this
library.
