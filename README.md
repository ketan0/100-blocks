# 100 Blocks - Activity Tracking and Visualization
Inspired by the Tim Urban blog post entitled "100 Blocks a Day," I created a Messenger bot to poll me every 10 minutes about what I'm doing, and a couple python scripts to visualize my "100 Blocks" at the end of the day. You can read more about it [in my blog post](https://www.blog.ketan.me/posts/100-blocks/).

## Setup
Follow the tutorial at [Quick Start - Messenger Platform](https://developers.facebook.com/docs/messenger-platform/getting-started/quick-start), except use the starter code inside the [messenger-webhook](./messenger-webhook) directory of this repository instead of the provided starter code. In your deploy environment (such as Heroku,) specify the environment variables required by the webhook such as `PAGE_ACCESS_TOKEN` and `VERIFY_TOKEN` (the latter of which is a random string.) Finally, you'll have to create a table in DynamoDB that has "activity" as its primary index and "timestamp" as its sort index, and replace `DYNAMODB_TABLE_NAME` and `DYNAMODB_TABLE_REGION` with the appropriate values.

Visualization in Python (perhaps in Jupyter) can be run as follows (assuming you're in the [visualization](./visualization) directory.) You'll first need to [configure your AWS credentials locally.](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) Then load the data from DynamoDB into a Pandas table, and extract 10-minute blocks from the data:

```python
from utils import load_dynamo_table, extract_blocks
from config import DYNAMODB_TABLE_NAME, ACTIVITY_COLORS
from pytz import timezone
# lower bound on wakeup time (that way only get activities after sleep)
this_morning_naive = datetime.now().replace(
    hour=9, minute=0, second=0, microsecond=0
)
# convert to an "aware" datetime object (has a sense of timezone)
eastern = timezone('US/Eastern')
this_morning_aware = eastern.localize(this_morning_naive)
print(this_morning_aware)
last_morning_aware = this_morning_aware - timedelta(days=1)
print(last_morning_aware)
start_dt = this_morning_aware
end_dt = this_morning_aware + timedelta(days=1)
df = load_dynamo_table(DYNAMODB_TABLE_NAME,
                       start_dt=start_dt,
                       end_dt=end_dt)
blocks = extract_blocks(df)
```

Classic "100 Blocks" visualization:
```python
from hundred_blocks_viz import hundred_blocks_viz
hundred_blocks_viz(blocks, ACTIVITY_COLORS, day=start_dt)
```

Pie chart of your activities visualization:
```python
from pie_chart_viz import pie_chart_viz
pie_chart_viz(blocks, ACTIVITY_COLORS, day=start_dt)
```

Some more example usages can be seen in [viz_experiments](./visualization/viz_experiments.ipynb) Jupyter notebook. Not always using the most efficient ways to do things, but I'll get around to cleaning it up.
