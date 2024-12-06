#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#
#
#   Summer 2023, BRACE2 Team
#   Berkeley, CA
#
#----------------------------------------------------------------------------#
import sys
import logging

from threading import Thread
from django.db import models

from apps.events.models import Event
from apps.inventory.models import Asset
from .daemon import LiveEvaluation

class Evaluation(models.Model):
    id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, null=True)
    evaluation_data = models.JSONField(default=dict)

    @classmethod
    def create(cls, event: Event, asset: Asset, data: dict = None):
        evaluation = cls()
        evaluation.event = event
        evaluation.asset = asset
        evaluation.save()

        if data is not None:
            evaluation.evaluation_data = data["evaluation_data"]
            evaluation.save()
        else:
            Thread(target=evaluate, args=(event, evaluation)).start()

        return evaluation


def evaluate(event, evaluation)->"Evaluation":

    daemon = LiveEvaluation(event, event.asset.predictors, evaluation)

    # assignPredictorMetrics?
    predictions = daemon.assignMetricPredictors(event)

    #with multiprocessing.dummy.Pool(3) as pool:
        # for predictor_name, run_id in pool.imap_unordered(
        #         self.runPredictor,
        #         predictions.items()
        #     ):
    if True:
        for predictor_name, run_id in map(
                daemon.runPredictor,
                predictions.items()
            ):

            print(f">>> {predictor_name} run complete.", file=sys.stderr)
            for mname in predictions[predictor_name][1]:
                print(f">>> Retrieving {predictor_name}/{mname}.", file=sys.stderr)
                data = daemon.predictors[predictor_name].getMetricData(run_id, mname)
                daemon.setMetricData(mname, predictor_name, data)

            print(f">>> Completed {predictor_name}.", file=sys.stderr)


    daemon.save()
    return evaluation

