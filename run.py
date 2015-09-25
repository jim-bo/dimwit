from eve import Eve
from tasks import dim_survey

# create application.
app = Eve()

# define hooks
def hook_dim_survey(items):

    # loop over each entry.
    for item in items:

        print item.keys()

        # run the async task.
        dim_survey.delay(item['data'], item['_id'])

# register hooks.
app.on_inserted_entry += hook_dim_survey

# run the application.
app.run(debug=True)