"""Structured output: ProviderStrategy ve ToolStrategy.

Serbest cumle yerine alanlari belli bir nesne isteriz.
Pydantic modeli hem belge hem dogrulama semasidir.
ToolStrategy modeli ozel bir tool cagirmaya zorlar.
ProviderStrategy ayni semayi modelin kendi yapisal cikti yoluna birakir.
"""

from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy, ToolStrategy
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

from labs.kit.models import make_tool_model


class JobMatch(BaseModel):
    """A job the agent recommends."""

    # description alanlari semaya girer. Model bu cumleleri gorur.
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    reason: str = Field(description="Why it matches the question")


def recommend_with_tool_strategy(question: str, model) -> JobMatch:
    """Cevap, adi JobMatch olan bir tool cagrisi olarak gelir."""

    agent = create_agent(
        model=model,
        tools=[],
        system_prompt=(
            "Return exactly one JobMatch and then stop. "
            "Every field is required. Example arguments: "
            '{"title":"Data Analyst","company":"Northwind","reason":"sql tag"}. '
            "For a Python question, choose Acme or Bright instead of the example."
        ),
        # ToolStrategy, JobMatch'i bir tool gibi cagirtir. Cevap semaya uymak zorundadir.
        response_format=ToolStrategy(JobMatch),
    )
    result = agent.invoke(
        {"messages": [HumanMessage(content=question)]},
        # Limit, model ornek JSON'u tekrar tekrar denerse donguyu keser.
        config={"recursion_limit": 12},
    )
    # structured_response, dogrulanmis Pydantic nesnesidir. Ham JSON degil.
    return result["structured_response"]


def recommend_with_provider_strategy(question: str, model) -> JobMatch:
    """Cevap, modelin semaya uygun iceriginden dogrudan nesneye cevrilir."""

    agent = create_agent(
        model=model,
        tools=[],
        system_prompt=(
            "Return one job that matches the schema, then stop. "
            "Choose from Acme Junior Python Developer, "
            "Bright Junior Python Intern, or Northwind Data Analyst."
        ),
        # ProviderStrategy, ayni semayi modelin kendi structured output yoluna verir.
        response_format=ProviderStrategy(JobMatch),
    )
    result = agent.invoke(
        {"messages": [HumanMessage(content=question)]},
        config={"recursion_limit": 12},
    )
    return result["structured_response"]


def main(model=None) -> JobMatch:
    chosen = model or make_tool_model()
    match = recommend_with_tool_strategy("A junior python role", chosen)
    print(match)
    return match


if __name__ == "__main__":
    main()
