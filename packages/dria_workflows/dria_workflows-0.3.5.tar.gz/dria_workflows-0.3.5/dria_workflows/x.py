from dria_workflows import *

prompt = """Instructions:
1. You have been given a STATEMENT and some KNOWLEDGE points.
2. Your goal is to try to find evidence that either supports or does not \
support the factual accuracy of the given STATEMENT.
3. To do this, you are allowed to issue ONE Google Search query that you think \
will allow you to find additional useful evidence.
4. Your query should aim to obtain new information that does not appear in the \
KNOWLEDGE. This new information should be useful for determining the factual \
accuracy of the given STATEMENT.
5. Format your final query by putting it in a markdown code block.

KNOWLEDGE:
{{search_results}}

STATEMENT:
{{atomic_fact}}"""


builder = WorkflowBuilder(query="thiery henry")
builder.search_step(
    id="search",
    search_query="{{query}}",
    n_results=5,
    outputs=[Push.new("search_results")],
)

flow = [
    Edge(source="search", target="_end"),
]
builder.flow(flow)
builder.set_return_value("search_results")
wf = builder.build()
print(wf.model_dump_json(exclude_none=True, exclude_unset=True, indent=2))