#!/usr/bin/env -S rye run python

import os

import pandas as pd

from lastmile.lib.auto_eval import AutoEval, BuiltinMetrics

client = AutoEval(
    # This is the default and can be omitted
    api_token=os.environ.get("LASTMILE_API_TOKEN"),
)

input_df = pd.DataFrame(
    {
        "input": [
            "Can you tell me the weight limit for carry-on bags?",
            "What gate is my flight SA795 departing from?",
            "Can I bring my pet on the plane?",
        ],
        "output": [
            "The weight limit for carry-on bags is 7kg.",
            "Your flight SA795 is departing from JFK at 6:30PM.",
            "Yes, you can bring your pet, but it must fit under the seat in front of you and there is a pet fee.",
        ],
        "ground_truth": [
            "7kg",
            "SA795: JFK Terminal 4, Gate 42, 6:30PM departure",
            "Pets are not allowed on StrikeAir flights.",
        ],
    }
)


output_df = client.evaluate_data(input_df, BuiltinMetrics.FAITHFULNESS)
print(output_df)
#                                                input                                             output                                      ground_truth  Faithfulness_score
# 0  Can you tell me the weight limit for carry-on ...         The weight limit for carry-on bags is 7kg.                                               7kg            0.998831
# 1       What gate is my flight SA795 departing from?  Your flight SA795 is departing from JFK at 6:3...  SA795: JFK Terminal 4, Gate 42, 6:30PM departure            0.998952
# 2                   Can I bring my pet on the plane?  Yes, you can bring your pet, but it must fit u...        Pets are not allowed on StrikeAir flights.            0.000892
