SYSTEM_1 = """\
You will be provided with the contents of a file along with its metadata. \
Provide a summary of the contents. The purpose of the summary is to organize \
files based on their content. To this end provide a concise but informative summary. \
Make the summary as specific to the file as possible. Along with the summary \
provide 3 Tags that accurately describe the high-level content of the file.

Write your response a JSON object with the following schema:

```json
{
    "summary": "Concise summary of the content",
    "tags": ["Tag 1", "Tag 2", "Tag 3"]
}
```

For example:

```json
{
    "summary": "A tutorial on using machine learning for data analysis.",
    "tags": ["machine learning", "data analysis", "tutorial"]
}
```"""

USER_1 = """\
{DOC_JSON}"""

SUMMARIZE_DOC = [
    {"role": "system", "content": SYSTEM_1},
    {"role": "user", "content": USER_1},
]