import pytest

from metagpt.exp_pool.context_builders.base import BaseContextBuilder
from metagpt.exp_pool.context_builders.simple import (
    SIMPLE_CONTEXT_TEMPLATE,
    SimpleContextBuilder,
)


class TestSimpleContextBuilder:
    @pytest.fixture
    def context_builder(self):
        return SimpleContextBuilder()

    @pytest.mark.asyncio
    async def test_build_with_experiences(self, context_builder, mocker):
        # Mock the format_exps method
        mock_exps = "Mocked experiences"
        mocker.patch.object(BaseContextBuilder, "format_exps", return_value=mock_exps)

        req = "Test request"
        result = await context_builder.build(req=req)

        expected = SIMPLE_CONTEXT_TEMPLATE.format(req=req, exps=mock_exps)
        assert result == expected

    @pytest.mark.asyncio
    async def test_build_without_experiences(self, context_builder, mocker):
        # Mock the format_exps method to return an empty string
        mocker.patch.object(BaseContextBuilder, "format_exps", return_value="")

        req = "Test request"
        result = await context_builder.build(req=req)

        assert result == req

    @pytest.mark.asyncio
    async def test_build_without_req(self, context_builder, mocker):
        # Mock the format_exps method
        mock_exps = "Mocked experiences"
        mocker.patch.object(BaseContextBuilder, "format_exps", return_value=mock_exps)

        result = await context_builder.build()

        expected = SIMPLE_CONTEXT_TEMPLATE.format(req="", exps=mock_exps)
        assert result == expected
