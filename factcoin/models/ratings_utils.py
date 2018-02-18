from django.db.models import Avg

import numpy as np

import factcoin

DOCUMENT_SCORE_RATIO = 0.5
VOTES_SCORE_RATIO = 0.5


def update_rating(document):
    Rating = factcoin.models.ratings.Rating
    Vote = factcoin.models.votes.Vote

    last_rating = Rating.objects.filter(document=document).last()
    document_score = document.get_evaluation()
    votes = Vote.objects.filter(document=document)
    votes_score = votes.aggregate(Avg('score'))["score__avg"]
    score = DOCUMENT_SCORE_RATIO * document_score + VOTES_SCORE_RATIO * votes_score
    rating = Rating.objects.create(parent=last_rating, document=document, score=score)
    return rating


def get_neighbours_score(document):
    connections = document.connections
    print (connections)
    ratings = []
    weights = []

    for connection in connections:
        other = connection.get_other(document)
        if other.rating_score:
            ratings.append(other.rating_score)
            weights.append(connection.score)

    score = 0.0
    if ratings:
        score = np.mean(np.array(ratings) * np.array(weights))
    return score
