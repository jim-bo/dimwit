from celery import Celery
import numpy as np
from sklearn.decomposition import PCA, FastICA
from datalayer import mongoctx
from bson.objectid import ObjectId
from sklearn.manifold import TSNE

app = Celery('tasks', broker='redis://localhost', backend='redis://localhost')

@app.task
def dim_survey(X, entry_id):

    # convert to numpy
    X = np.array(X)

    # run the reduction.
    X_pca = PCA(n_components=3).fit_transform(X)
    X_tsne = TSNE(n_components=3).fit_transform(X)
    X_ica = FastICA(n_components=3).fit_transform(X)

    # connect to db.
    with mongoctx() as db:

        # update the stuff.
        db['entry'].update(
            {
                '_id': ObjectId(entry_id)
            },
            {
                '$set': {
                    'pca': X_pca.tolist(),
                    'tsne': X_tsne.tolist(),
                    'ica': X_ica.tolist(),
                }
            }
        )