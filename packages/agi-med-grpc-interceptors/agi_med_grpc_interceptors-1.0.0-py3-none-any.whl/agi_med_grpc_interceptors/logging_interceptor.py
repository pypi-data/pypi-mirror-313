from typing import Callable, Iterator, TypeVar, NoReturn
from uuid import uuid4

import grpc
from grpc import (
    HandlerCallDetails,
    RpcMethodHandler,
    ServerInterceptor,
    unary_unary_rpc_method_handler,
    unary_stream_rpc_method_handler,
    stream_unary_rpc_method_handler,
    stream_stream_rpc_method_handler,
)
from loguru import logger

# Типы для запросов и ответов
ReqType = TypeVar("ReqType")
RespType = TypeVar("RespType")


class LoggingInterceptor(ServerInterceptor):
    def intercept_service(
        self, continuation: Callable[[HandlerCallDetails], RpcMethodHandler], handler_call_details: HandlerCallDetails
    ) -> RpcMethodHandler:
        full_method: str = handler_call_details.method
        handler: RpcMethodHandler = continuation(handler_call_details)

        def new_handler(request: ReqType | Iterator[ReqType], context: grpc.ServicerContext) -> RpcMethodHandler:
            headers: dict[str, str] = {
                key.replace("-", "_"): value
                for key, value in dict(context.invocation_metadata() or {}).items()
                if value
            }
            with logger.contextualize(uuid=uuid4(), **headers):
                method_type: str = self._get_method_type(handler)
                if handler.unary_unary:
                    return self._handle_method(handler.unary_unary, request, context, method_type, full_method)
                elif handler.unary_stream:
                    return self._handle_method(handler.unary_stream, request, context, method_type, full_method)
                elif handler.stream_unary:
                    return self._handle_method(handler.stream_unary, request, context, method_type, full_method)
                else:  # FYI handler.stream_stream:
                    return self._handle_method(handler.stream_stream, request, context, method_type, full_method)

        # Создание соответствующего обработчика в зависимости от типа вызова
        return self._create_method_handler(handler, new_handler)

    @staticmethod
    def _create_method_handler(handler: RpcMethodHandler, new_handler: Callable) -> RpcMethodHandler:
        """Создает новый обработчик исходя из типа вызова."""
        if handler.unary_unary:
            return unary_unary_rpc_method_handler(
                new_handler,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )
        elif handler.unary_stream:
            return unary_stream_rpc_method_handler(
                new_handler,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )
        elif handler.stream_unary:
            return stream_unary_rpc_method_handler(
                new_handler,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )
        else:  # FYI: handler.stream_stream
            return stream_stream_rpc_method_handler(
                new_handler,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )

    @staticmethod
    def _get_method_type(handler: RpcMethodHandler) -> str:
        """Определяет тип RPC метода по атрибутам обработчика."""
        if handler.unary_unary:
            return "unary-unary"
        elif handler.unary_stream:
            return "unary-stream"
        elif handler.stream_unary:
            return "stream-unary"
        else:  # FYI handler.stream_stream:
            return "stream-stream"

    def _handle_method(
        self,
        method: Callable,
        request: ReqType | Iterator[ReqType],
        context: grpc.ServicerContext,
        method_type: str,
        path: str,
    ) -> RespType | Iterator[RespType]:
        """Обрабатывает любой тип gRPC метода (unary или stream) с логированием."""
        try:
            self._log_method_call(method_type, path)
            if "stream" in method_type.split("-")[1]:
                # Потоковый ответ (unary-stream или stream-stream)
                return self._handle_stream_response(method, request, context, method_type, path)
            else:
                # Одиночный ответ (unary-unary или stream-unary)
                response: RespType = method(request, context)
                self._log_method_completion(method_type, path)
                return response
        except Exception as e:
            return self.exception_handler(method_type, path, e, request)

    def _handle_stream_response(
        self,
        method: Callable,
        request: ReqType | Iterator[ReqType],
        context: grpc.ServicerContext,
        method_type: str,
        path: str,
    ) -> Iterator[RespType]:
        """Генерирует потоковый ответ с логированием."""
        try:
            response_iterator = method(request, context)
            for response in response_iterator:
                yield response
            self._log_method_completion(method_type, path)
        except Exception as e:
            yield self.exception_handler(method_type, path, e, request)

    @staticmethod
    def _log_method_call(method_type: str, path: str) -> None:
        """Логирует начало вызова метода."""
        logger.info(f"Handling {method_type} gRPC call: {path}")

    @staticmethod
    def _log_method_completion(method_type: str, path: str) -> None:
        """Логирует завершение вызова метода."""
        logger.info(f"Completed {method_type} gRPC call: {path}")

    @staticmethod
    def _log_method_error(method_type: str, path: str, ex: Exception, request: ReqType | Iterator[ReqType]) -> None:
        """Логирует ошибку, возникшую во время вызова метода."""
        logger.error(f"Exception in {method_type} gRPC call: {path}, request: {request}")
        logger.exception(ex)

    def exception_handler(
        self, method_type: str, path: str, ex: Exception, request: ReqType | Iterator[ReqType]
    ) -> RespType | NoReturn:
        self._log_method_error(method_type, path, ex, request)
        raise ex
