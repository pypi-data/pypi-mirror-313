from toloka.a9s.client.base.client import AsyncBaseFunctionsClient
from toloka.a9s.client.models.function import FunctionFormStrict, FunctionViewV0Strict
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncFunctionsClient(AsyncBaseFunctionsClient):
    async def get(self, name: str) -> FunctionViewV0Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'/api/v0/function/{name}',
        )
        return FunctionViewV0Strict.model_validate(response.json())

    async def update(self, name: str, function_data: FunctionFormStrict) -> FunctionViewV0Strict:
        if name != function_data.name:
            raise ValueError("Function name can't be changed")

        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'/api/v0/function/{name}',
            body=model_dump_a9s(function_data),
        )
        return FunctionViewV0Strict.model_validate(response.json())

    async def create(self, function_data: FunctionFormStrict) -> FunctionViewV0Strict:
        response = await self.client.make_retriable_request(
            method='POST',
            url='/api/v0/function',
            body=model_dump_a9s(function_data),
        )
        return FunctionViewV0Strict.model_validate(response.json())
