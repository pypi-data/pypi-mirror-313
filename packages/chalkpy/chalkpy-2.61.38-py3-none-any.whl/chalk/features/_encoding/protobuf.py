from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb

PROTOBUF_TO_UNIT = {
    pb.TIME_UNIT_SECOND: "s",
    pb.TIME_UNIT_MILLISECOND: "ms",
    pb.TIME_UNIT_MICROSECOND: "us",
    pb.TIME_UNIT_NANOSECOND: "ns",
}


UNIT_TO_PROTOBUF = {
    "s": pb.TIME_UNIT_SECOND,
    "ms": pb.TIME_UNIT_MILLISECOND,
    "us": pb.TIME_UNIT_MICROSECOND,
    "ns": pb.TIME_UNIT_NANOSECOND,
}
