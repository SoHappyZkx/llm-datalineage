import argilla as rg

client = rg.Argilla(api_url="https://soulhappy-argilla-annotation.hf.space", api_key="dPbfgm4dt8obJJPNgTXmOf89-cPizsJRLO7o1YnVbm1S2UKWTQ4jbtqFh-kD7gOZu1wdoGMT-ivcYmIAQXnfbU4_rCL6fHVMV6zRibgbta8")
#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  huggingface api 
#xgYbnM-OOvB1K6BXDwwKJYMHJBr2Xl6QTUb4gKPer8rRvg4MdE1XckrhX2rTSlyPA3HCfPGejLOL_mc9hAeoLeFH1nnG26hgssfMkD8l3cg

settings = rg.Settings(
    guidelines="Classify the reviews as positive or negative.",
    fields=[
        rg.TextField(
            name="review",
            title="Text from the review",
            use_markdown=False,
        ),
    ],
    questions=[
        rg.LabelQuestion(
            name="my_label",
            title="In which category does this article fit?",
            labels=["positive", "negative"],
        )
    ],
)
dataset = rg.Dataset(
    name=f"zkx_first_dataset",
    settings=settings,
    client=client,
)
dataset.create()

records = [
    rg.Record(
        fields={
            "review": "This is a great product.",
        },
    ),
    rg.Record(
        fields={
            "review": "This is a bad product.",
        },
    ),
]
dataset.records.log(records)


print("dd")
#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

#xgYbnM-OOvB1K6BXDwwKJYMHJBr2Xl6QTUb4gKPer8rRvg4MdE1XckrhX2rTSlyPA3HCfPGejLOL_mc9hAeoLeFH1nnG26hgssfMkD8l3cg