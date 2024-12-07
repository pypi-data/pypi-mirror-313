from ray import serve


class MockNetInference:
    model_id = None

    @serve.multiplexed()
    async def get_model(self, model_id: str):
        return model_id

    async def __call__(self):
        model_id = await self.get_model(serve.get_multiplexed_model_id())
        message = 'hello datamaker!!!'
        return {'model_id': model_id, 'message': message}
