from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel
from pymediasoup.device import RtpCapabilities
from pymediasoup.models.transport import DtlsFingerprint, IceCandidate
from pymediasoup.rtp_parameters import (
    RTX,
    MediaKind,
    RtcpFeedback,
    RtcpParameters,
    RtpCodecCapability,
    RtpCodecParameters,
    RtpEncodingParameters,
    RtpHeaderExtension,
    RtpHeaderExtensionParameters,
    RtpParameters,
)
from pymediasoup.sctp_parameters import SctpCapabilities, SctpParameters
from pymediasoup.transport import (
    DtlsParameters,
    IceParameters,
    RTCIceServer,
    SctpStreamParameters,
)

from huddle01.proto.rtc.sctp_stream_parameters_pb2 import (
    ProtoSctpStreamParameters,
)

from .proto.client.app_data_pb2 import (
    AppData as ProtoAppData,
)
from .proto.client.app_data_pb2 import (
    Value as ProtoAppDataValue,
)
from .proto.rtc.rtp_capabilities_pb2 import ProtoRtpCapabilities
from .proto.rtc.rtp_parameters_pb2 import (
    ProtoCodecParameters,
    ProtoEncodings,
    ProtoHeaderExtensionParameters,
    ProtoRtcpFeedback,
    ProtoRtpParameters,
)
from .proto.rtc.rtp_parameters_pb2 import (
    RtcpParameters as ProtoRtcpParameters,
)
from .proto.rtc.sctp_capabilities_pb2 import ProtoNumSctpStreams, ProtoSctpCapabilities
from .proto.rtc.sdp_info_pb2 import (
    ProtoDtlsFingerPrints,
    ProtoDtlsParameters,
    ProtoIceParameters,
    ProtoTransportSDPInfo,
)

DirectionType = Literal["sendrecv", "sendonly", "recvonly", "inactive"]

priority: Optional[Literal["very-low", "low", "medium", "high"]] = None


def validate_priority(
    priority: str,
) -> Optional[Literal["very-low", "low", "medium", "high"]]:
    if priority in ("very-low", "low", "medium", "high"):
        return priority
    return None


def validate_direction(direction: str) -> Optional[DirectionType]:
    if direction in ("sendrecv", "sendonly", "recvonly", "inactive"):
        return direction  # type: ignore
    return None


def parse_ice_parameters(ice_parameters: ProtoIceParameters) -> IceParameters:
    parsed_ice_parameters = IceParameters(
        usernameFragment=ice_parameters.usernameFragment,
        password=ice_parameters.password,
        iceLite=ice_parameters.iceLite,
    )

    return parsed_ice_parameters


class MediasoupSDPInfo(BaseModel):
    iceParameters: IceParameters
    iceCandidates: List[Union[IceCandidate, dict]]
    dtlsParameters: DtlsParameters
    sctpParameters: Optional[SctpParameters]
    iceServers: Optional[List[RTCIceServer]] = None
    iceTransportPolicy: Optional[Literal["all", "relay"]] = None
    additionalSettings: Optional[dict] = None
    proprietaryConstraints: Any = None
    appData: Optional[dict] = {}


def parse_sdp_info(sdp_info: ProtoTransportSDPInfo) -> MediasoupSDPInfo:
    """
    Parse the ProtoTransportSDPInfo object into a MediasoupSDPInfo object
    """
    ice_candidates: List[Union[IceCandidate, dict]] = []

    for proto_candidate in sdp_info.iceCandidates:
        protocol = "udp" if proto_candidate.protocol == "udp" else "tcp"

        type = (
            "host"
            if proto_candidate.type == "host"
            else "srflx"
            if proto_candidate.type == "srflx"
            else "prflx"
            if proto_candidate.type == "prflx"
            else "relay"
        )

        tcp_type = (
            "active"
            if proto_candidate.tcpType == "active"
            else "passive"
            if proto_candidate.tcpType == "passive"
            else "so"
        )

        ice_candidate = IceCandidate(
            foundation=proto_candidate.foundation,
            ip=proto_candidate.ip,
            port=proto_candidate.port,
            priority=proto_candidate.priority,
            protocol=protocol,
            type=type,
            tcpType=tcp_type,
        )

        ice_candidates.append(ice_candidate)

    dtls_parameters = parse_from_proto_dtls(sdp_info.dtlsParameters)

    parsed_sdp_info = MediasoupSDPInfo(
        iceCandidates=ice_candidates,
        dtlsParameters=dtls_parameters,
        sctpParameters=SctpParameters(
            port=sdp_info.sctpParameters.port,
            OS=sdp_info.sctpParameters.OS,
            MIS=sdp_info.sctpParameters.MIS,
            maxMessageSize=sdp_info.sctpParameters.maxMessageSize,
        ),
        iceParameters=IceParameters(
            iceLite=sdp_info.iceParameters.iceLite,
            password=sdp_info.iceParameters.password,
            usernameFragment=sdp_info.iceParameters.usernameFragment,
        ),
    )

    return parsed_sdp_info


def parse_from_proto_dtls(dtlsParameters: ProtoDtlsParameters) -> DtlsParameters:
    """
    Parse the ProtoDtlsParameters object into a DtlsParameters object
    """
    dtls_fingerprints: List[DtlsFingerprint] = []

    for proto_fingerprint in dtlsParameters.fingerprints:
        dtls_fingerprint = DtlsFingerprint(
            algorithm=proto_fingerprint.algorithm, value=proto_fingerprint.value
        )

        dtls_fingerprints.append(dtls_fingerprint)

    dtls_role = (
        "auto"
        if dtlsParameters.role == "auto"
        else "client"
        if dtlsParameters.role == "client"
        else "server"
    )

    dtls_parameters: DtlsParameters = DtlsParameters(
        fingerprints=dtls_fingerprints, role=dtls_role
    )

    return dtls_parameters


def parse_to_proto_dtls(dtlsParameters: DtlsParameters) -> ProtoDtlsParameters:
    """
    Parse the DtlsParameters object into a ProtoDtlsParameters object
    """
    proto_fingerprints: List[ProtoDtlsFingerPrints] = []

    for fingerprint in dtlsParameters.fingerprints:
        proto_fingerprint = ProtoDtlsFingerPrints(
            algorithm=fingerprint.algorithm, value=fingerprint.value
        )
        proto_fingerprints.append(proto_fingerprint)

    proto_dtls_parameters = ProtoDtlsParameters(
        role=dtlsParameters.role, fingerprints=proto_fingerprints
    )

    return proto_dtls_parameters


def parse_from_proto_rtp_parameters(
    proto_rtp_parameters: ProtoRtpParameters,
) -> RtpParameters:
    """
    Parse the ProtoRtpParameters object into a Mediasoup RtpParameters object
    """
    codecs: List[RtpCodecParameters] = []
    header_extensions: List[RtpHeaderExtensionParameters] = []
    encodings: List[RtpEncodingParameters] = []
    mid: Optional[str] = proto_rtp_parameters.mid
    rtcp: Optional[RtcpParameters] = None

    if proto_rtp_parameters.rtcp:
        rtcp = RtcpParameters(
            cname=proto_rtp_parameters.rtcp.cname,
            reducedSize=True if proto_rtp_parameters.rtcp.reducedSize else False,
            mux=True if proto_rtp_parameters.rtcp.mux else False,
        )

    for codec in proto_rtp_parameters.codecs:
        if codec is None:
            continue

        rtcp_feedback: List[RtcpFeedback] = []

        for feedback in codec.rtcpFeedback:
            proto_feedback = RtcpFeedback(
                type=feedback.type, parameter=feedback.parameter
            )
            rtcp_feedback.append(proto_feedback)

        parameters: dict = {}

        if codec.parameters:
            for key, value in codec.parameters.items():
                parameters.update({key: value})

        codec = RtpCodecParameters(
            mimeType=codec.mimeType,
            clockRate=codec.clockRate,
            channels=codec.channels if codec.channels else None,
            payloadType=codec.payloadType,
            rtcpFeedback=rtcp_feedback,
            parameters=parameters,
        )

        codecs.append(codec)

    for proto_header_extension in proto_rtp_parameters.headerExtensions:
        parameters: dict = {}

        if proto_header_extension.parameters:
            for key, value in proto_header_extension.parameters.items():
                parameters.update({key: value})

        header_extension_parameters = RtpHeaderExtensionParameters(
            id=proto_header_extension.id,
            encrypt=True if proto_header_extension.encrypt else False,
            parameters=parameters,
            uri=proto_header_extension.uri,
        )

        header_extensions.append(header_extension_parameters)

    for proto_encoding in proto_rtp_parameters.encodings:
        rtx = RTX(ssrc=proto_encoding.rtx.ssrc)

        encoding: RtpEncodingParameters = RtpEncodingParameters(
            ssrc=proto_encoding.ssrc,
            rid=proto_encoding.rid,
            codecPayloadType=proto_encoding.codecPayloadType,
            rtx=rtx,
            dtx=True if proto_encoding.dtx else False,
            scalabilityMode=proto_encoding.scalabilityMode,
            scaleResolutionDownBy=proto_encoding.scaleResolutionDownBy,
            maxBitrate=proto_encoding.maxBitrate,
            maxFramerate=proto_encoding.maxFramerate,
            adaptivePtime=None,
            priority=None,
            networkPriority=None,
        )

        encodings.append(encoding)

    rtp_parameters = RtpParameters(
        encodings=encodings,
        codecs=codecs,
        headerExtensions=header_extensions,
        mid=mid,
        rtcp=rtcp,
    )

    return rtp_parameters


def parse_to_proto_rtp_parameters(rtp_parameters: RtpParameters) -> ProtoRtpParameters:
    """
    Parse the Mediasoup RtpParameters object into a ProtoRtpParameters object
    """
    proto_codecs: List[ProtoCodecParameters] = []
    proto_header_extensions: List[ProtoHeaderExtensionParameters] = []
    proto_encodings: List[ProtoEncodings] = []
    proto_rtcp: Optional[ProtoRtcpParameters] = None

    if rtp_parameters.rtcp:
        proto_rtcp = ProtoRtcpParameters(
            cname=rtp_parameters.rtcp.cname if rtp_parameters.rtcp.cname else None,
            reducedSize=True if rtp_parameters.rtcp.reducedSize else False,
            mux=True if rtp_parameters.rtcp.mux else False,
        )

    for codec in rtp_parameters.codecs:
        if codec is None:
            continue

        rtcp_feedback: List[ProtoRtcpFeedback] = []

        for feedback in codec.rtcpFeedback:
            proto_feedback = ProtoRtcpFeedback(
                type=feedback.type, parameter=feedback.parameter
            )
            rtcp_feedback.append(proto_feedback)

        proto_codec = ProtoCodecParameters(
            mimeType=codec.mimeType,
            clockRate=codec.clockRate,
            channels=codec.channels if codec.channels else None,
            payloadType=codec.payloadType,
            rtcpFeedback=rtcp_feedback,
            parameters=codec.parameters,
        )

        proto_codecs.append(proto_codec)

    for header_extension in rtp_parameters.headerExtensions:
        proto_header_extension = ProtoHeaderExtensionParameters(
            uri=header_extension.uri,
            id=header_extension.id,
            encrypt=True if header_extension.encrypt else False,
            parameters=header_extension.parameters,
        )
        proto_header_extensions.append(proto_header_extension)

    for encoding in rtp_parameters.encodings:
        rtx = ProtoEncodings.ProtoRTX(ssrc=encoding.rtx.ssrc) if encoding.rtx else None

        proto_encoding = ProtoEncodings(
            ssrc=encoding.ssrc,
            rid=encoding.rid,
            codecPayloadType=encoding.codecPayloadType,
            rtx=rtx,
            dtx=True if encoding.dtx else False,
            scalabilityMode=encoding.scalabilityMode,
            scaleResolutionDownBy=encoding.scaleResolutionDownBy,
            maxBitrate=encoding.maxBitrate,
            active=True,
            maxFramerate=encoding.maxFramerate,
        )
        proto_encodings.append(proto_encoding)

    proto_rtp_parameters = ProtoRtpParameters(
        mid=rtp_parameters.mid,
        codecs=proto_codecs,
        headerExtensions=proto_header_extensions,
        encodings=proto_encodings,
        rtcp=proto_rtcp,
    )

    return proto_rtp_parameters


def parse_router_rtp_capabilities(
    rtp_capabilities: ProtoRtpCapabilities,
) -> RtpCapabilities:
    """
    Parse the ProtoRtpCapabilities object into a RtpCapabilities object
    """
    # Create a new RtpCapabilities object
    parsed_router_rtp_capabilities = RtpCapabilities(
        codecs=[], headerExtensions=[], fecMechanisms=[]
    )

    # Mapping codecs from ProtoRtpCapabilities to RtpCapabilities
    if rtp_capabilities.codecs:
        for proto_codec in rtp_capabilities.codecs:
            kind: MediaKind = "audio" if proto_codec.kind == "audio" else "video"

            rtcp_feedback: List[RtcpFeedback] = [
                RtcpFeedback(type=feedback.type, parameter=feedback.parameter)
                for feedback in proto_codec.rtcpFeedback
            ]

            codec: RtpCodecCapability = RtpCodecCapability(
                mimeType=proto_codec.mimeType,
                clockRate=proto_codec.clockRate,
                channels=proto_codec.channels if proto_codec.channels > 0 else None,
                kind=kind,
                preferredPayloadType=proto_codec.preferredPayloadType,
                rtcpFeedback=rtcp_feedback,
            )

            # Fixing the codec parameters: converting certain string values to numbers (and back to strings)
            if proto_codec.parameters:
                for key, value in proto_codec.parameters.items():
                    if key == "packetization-mode" and value == "1":
                        value = int(value)

                    codec.parameters.update({key: value})

            parsed_router_rtp_capabilities.codecs.append(codec)

    # Mapping headerExtensions (if any)
    if rtp_capabilities.headerExtensions:
        for proto_ext in rtp_capabilities.headerExtensions:
            kind: MediaKind = "audio" if proto_ext.kind == "audio" else "video"

            direction: Optional[DirectionType] = validate_direction(proto_ext.direction)

            header_ext: RtpHeaderExtension = RtpHeaderExtension(
                kind=kind,
                uri=proto_ext.uri,
                preferredId=proto_ext.preferredId,
                preferredEncrypt=proto_ext.preferredEncrypt,
                direction=direction,
            )

            parsed_router_rtp_capabilities.headerExtensions.append(header_ext)

    return parsed_router_rtp_capabilities


def parse_to_proto_sctp_capabilities(
    sctp_capabilities: SctpCapabilities,
) -> ProtoSctpCapabilities:
    """
    Parse the SctpParameters object into a ProtoSctpCapabilities object
    """
    num_streams = ProtoNumSctpStreams(
        MIS=sctp_capabilities.numStreams.MIS, OS=sctp_capabilities.numStreams.OS
    )

    proto_sctp_capabilities = ProtoSctpCapabilities(numStreams=num_streams)

    return proto_sctp_capabilities


def parse_to_sctp_parameters(
    proto_sctp_parameters: ProtoSctpStreamParameters,
) -> SctpStreamParameters:
    return SctpStreamParameters(
        streamId=proto_sctp_parameters.streamId,
        ordered=proto_sctp_parameters.ordered,
        maxPacketLifeTime=proto_sctp_parameters.maxPacketLifeTime
        if proto_sctp_parameters.maxPacketLifeTime > 0
        else None,
        maxRetransmits=proto_sctp_parameters.maxRetransmits
        if proto_sctp_parameters.maxRetransmits > 0
        else None,
        label=None,
        protocol=None,
    )


def parse_to_proto_sctp_parameters(
    sctp_parameters: SctpStreamParameters,
) -> ProtoSctpStreamParameters:
    return ProtoSctpStreamParameters(
        streamId=sctp_parameters.streamId,
        ordered=sctp_parameters.ordered or False,
        maxPacketLifeTime=sctp_parameters.maxPacketLifeTime,
        maxRetransmits=sctp_parameters.maxRetransmits,
    )


def parse_to_proto_app_data(dict: Dict[str, str]):
    """
    Parse the AppData object into a ProtoAppData object
    """

    appData: Dict[str, ProtoAppDataValue] = {}

    for key, value in dict.items():
        appData[key] = ProtoAppDataValue(string_value=value)

    return ProtoAppData(appData=appData)
