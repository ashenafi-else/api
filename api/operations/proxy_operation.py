from elsecommon.marshalling import marshall
from elsepublic.api.dto.proxy_operation_dto import ProxyOpParamsDTO
from elsepublic.api.serializers.proxy_operation_serializer import ProxyOpParamsSerializer
from elsecommon.transports.router import Router


@marshall(expect=ProxyOpParamsSerializer)
def proxy_operation(params: ProxyOpParamsDTO, **context: dict) -> None:
    """
    Proxy operation for calling other operations via uri

    Parameters
    ----------
    params: lsepublic.api.dto.proxy_operation_dto.ProxyOpParamsDTO
        Input operation parameters
    **context
        Context data
    """
    operation = Router[params.operation]
    serializer = operation.interface.expect_serializer_class(data=params.operation_params)
    serializer.is_valid(raise_exception=True)
    params_dto = serializer.to_entity()
    operation(params_dto, **context)
