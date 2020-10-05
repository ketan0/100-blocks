# 100 Blocks - Activity Tracking and Visualization
Inspired by the Tim Urban blog post entitled "100 Blocks a Day," I created a Messenger bot to poll me every 10 minutes about what I'm doing, and a couple python scripts to visualize my "100 Blocks" at the end of the day. You can read more about it [in my blog post](https://www.blog.ketan.me/posts/100-blocks/).

## Setup
Follow the tutorial at [Quick Start - Messenger Platform](https://developers.facebook.com/docs/messenger-platform/getting-started/quick-start), except use the starter code inside the [messenger-webhook](./messenger-webhook) directory of this repository instead of the provided starter code. In your deploy environment (such as Heroku,) specify the environment variables required by the webhook such as `PAGE_ACCESS_TOKEN` and `VERIFY_TOKEN` (the latter of which is a random string.) Finally, you'll have to create a table in DynamoDB that has "activity" as its primary index and "timestamp" as its sort index, and replace `DYNAMODB_TABLE_NAME` and `DYNAMODB_TABLE_REGION` with the appropriate values.

Visualization in Python (perhaps in Jupyter) can be run as follows (assuming you're in the [visualization](./visualization) directory.) You'll first need to [configure your AWS credentials locally.](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) Then load the data from DynamoDB into a Pandas table, and extract 10-minute blocks from the data:

```python
from utils import load_dynamo_table, extract_blocks
df = load_dynamo_table(DYNAMODB_TABLE_NAME)
blocks, activity_ids = extract_blocks(df)
```

Classic "100 Blocks" visualization:
```python
from hundred_blocks_viz import hundred_blocks_viz
hundred_blocks_viz(blocks, activity_ids)
```

Pie chart of your activities visualization:
```python
from pie_chart_viz import pie_chart_viz
pie_chart_viz(blocks, activity_ids)
```
