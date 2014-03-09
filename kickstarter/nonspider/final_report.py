#!/bin/python2
from __future__ import division

# Report items:
# Total projects, time range
# Percent and total projects with feature over per-feature threshold
# Projects with feature over per-feature threshold per time period (20 periods)
# Correlation of each feature to epic feature, based on binary incidence
#   Binary because: Low incidence levels may be noise, and I don't expect any incidence to go above 4-5.
#   Any present feature may be indicative of a bad writeup/game, but I want to know if the way they are bad is related (correlated).
# Projects vs # features present, to see how many projects have no features

import datetime
from scipy.stats.stats import pearsonr
import pygal
import sqlite3

import common

db = common.connect_db()
db_test = db.cursor()
db.row_factory = sqlite3.Row
db_iterate = db.cursor()

def format_time(stamp):
    return datetime.datetime.fromtimestamp(stamp).strftime('(%Y) %m-%d')

total, oldest, newest = tuple(db.execute('SELECT COUNT(1), MIN(date), MAX(date) FROM projects').fetchone())
print('Total projects: {0}'.format(total))
print('Oldest project: {0}'.format(format_time(oldest)))
print('Newest project: {0}'.format(format_time(newest)))

features = {
    'epic': { 
        'threshold': 1, 
        'description': 'the word epic'
    },
    'roguelike': { 
        'threshold': 1,
        'description': 'the word roguelike'
    },
    'zombie': { 
        'threshold': 1,
        'description': 'the word zombie'
    },
    'genre': { 
        'threshold': 3,
        'description': '3 or more genres'
    },
    'names': { 
        'threshold': 3,
        'description': '3 or more dropped names'
    }
}
for feature in features.values():
    feature['incidence_count'] = 0
    feature['epic_correlation_pairs'] = []

time_bucket_count = 10
time_bucket_size = (newest - oldest) / time_bucket_count 
time_buckets = [{
    'start': oldest + index * time_bucket_size,
    'feature_count': dict(zip(features.keys(), [0] * len(features))),
    'count': 0
} for index in range(time_bucket_count)]

feature_counts = [0] * (len(features) + 1)

for project in db_iterate.execute('SELECT * FROM projects'):
    time_bucket = next(bucket for bucket in reversed(time_buckets) if project['date'] >= bucket['start'])
    time_bucket['count'] += 1

    # Count features over thresholds
    total_features = 0
    epic_present = False
    for feature in features.items():
        count = project['match_{0}_count'.format(feature[0])]
        if count >= feature[1]['threshold']:
            if feature[0] == 'epic':
                epic_present = True
            feature[1]['incidence_count'] += 1
            time_bucket['feature_count'][feature[0]] += 1
            total_features += 1

    # Separated to guarantee epic_present is set
    for feature in features.items():
        count = project['match_{0}_count'.format(feature[0])]
        feature_present = count >= feature[1]['threshold']
        feature[1]['epic_correlation_pairs'].append((1.0 if epic_present else 0.0, 1.0 if feature_present else 0.0))

    feature_counts[total_features] += 1

for feature in features.values():
    print('Projects featuring {0}: {1} / {2} - {3}%'.format(
        feature['description'], 
        feature['incidence_count'], 
        total, 
        100 * feature['incidence_count'] / total
    ))
    
for feature in features.values():
    x, y = zip(*feature['epic_correlation_pairs'])
    assert(len(x) == len(y))
    print('Correlation of {0} to {1}: {2}'.format(
        features['epic']['description'], 
        feature['description'], 
        pearsonr(x, y)
    ))

for feature in features.values():
    together = sum((1 if pair[0] == 1 and pair[1] == 1 else 0 for pair in feature['epic_correlation_pairs']))
    individually = sum((1 if pair[0] == 1 or pair[1] == 1 else 0 for pair in feature['epic_correlation_pairs']))
    print('Coincidence of {0} and {1}: {2} / {3} - %{4}'.format(
        features['epic']['description'], 
        feature['description'],
        together,
        individually,
        100 * together / individually
    ))

absolute_graph = pygal.Line(x_label_rotation = 20)
absolute_graph.title = 'Projects with features by date'
absolute_graph.x_labels = [format_time(bucket['start']) for bucket in time_buckets]
absolute_graph.add('Totals', [bucket['count'] for bucket in time_buckets])
for feature in features.items():
    absolute_graph.add(
        feature[1]['description'], 
        [bucket['feature_count'][feature[0]] for bucket in time_buckets]
    )
absolute_graph.render_to_file('features_absolute.svg')

percent_graph = pygal.Line(x_label_rotation = 20)
percent_graph.title = 'Projects with features by date (in %)'
percent_graph.x_labels = [format_time(bucket['start']) for bucket in time_buckets]
for feature in features.items():
    percent_graph.add(
        feature[1]['description'], 
        [(int(100 * (bucket['feature_count'][feature[0]] / bucket['count'])) if bucket['count'] > 0 else None) for bucket in time_buckets]
    )
percent_graph.render_to_file('features_percent.svg')

feature_histogram = pygal.Bar()
feature_histogram.title = 'Histogram of features per project'
feature_histogram.x_labels = map(str, range(6))
feature_histogram.add('Feature count', feature_counts)
feature_histogram.render_to_file('feature_histogram.svg')

