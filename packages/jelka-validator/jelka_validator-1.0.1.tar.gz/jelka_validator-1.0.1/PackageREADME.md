# Jelka validator

Decoder for data stream sent to x-mas tree and simulation.

Exposes `DataReader` class at toplevel. It serielizes bytes from input
into python `list of tuples of 3 integers`.

There is also `datawriter.DataWriter` that can be used for writing frames in required format
to stdout. It deals with headers so you don't have to.
