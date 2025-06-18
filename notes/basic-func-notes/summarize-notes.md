# distil "summarize functionality"
`summarize()` — the functionality that allows users to retrieve summarized data, trends, and other distilled information. these insights are presented in english or another natural language.

- converts raw or queried data into natural-language insight
- strips away abstraction and technical jargon
- output is human-readable, contextualized, and high-level
- not dependent on tracker functionality

## definitions
- **summary:** a concise, high-level description of the main patterns, statistics, or findings in the data
- **trend:** a general direction in which something is developing or changing, as observed in the data

---

## potential function signature

> ```python
def summarize(data, context=None, granularity='high') -> str:
    """
    summarizes the provided data into a human-readable insight
    - data: the dataset or query result to summarize
    - context: optional context or user preferences for tailoring the summary
    - granularity: level of detail ('high', 'medium', 'low')
    returns: a summary string
    """

### inputs
- `data`: the dataset or query result to be summarized
- `context`: (optional) user or application context for personalized summaries
- `granularity`: (optional) level of detail for the summary

### outputs
- returns a human-readable summary string

## edge case handling
- if data is empty, return "no data available to summarize."
- if data is highly variable, note the variability in the summary

## intended workflow
1. preprocess data: clean and validate the input data
2. analyze trends: identify key statistics, patterns, and trends
3. generate summary: convert findings into a natural-language summary
4. format output: ensure the summary is clear, concise, and contextualized

### high-level example
inputs:
- dataset: monthly sales data for 2024
- context: low
- granularity: low

output:
- "sales increased steadily throughout 2024, with a peak in july. the average monthly growth rate was 5%. the electronics category contributed most to the overall increase."

## extensibility
- add support for summaries in multiple languages
- allow user to specify summary format (bullet points, paragraph, etc.)
- integrate with visualization modules for graphical summaries

## related functions/see also
- `distill()` in distill-notes.md
- `track()` in track-notes.md
