import numpy as np
import sklearn
import pandas as pd
from sklearn.metrics import auc
from sklearn.metrics import roc_auc_score

from gesund.core._metrics.classification.metrics.auc import AUC
from gesund.core._metrics.classification.metrics.stats_tables import StatsTables
from gesund.core._utils import ValidationUtils


class PlotStatsTables:
    def __init__(
        self, true, pred_logits, pred_categorical, class_mappings, meta_pred_true
    ):
        self.true = true
        self.pred_logits = pred_logits
        self.pred_categorical = pred_categorical
        self.class_mappings = class_mappings
        self.class_order = [int(i) for i in list(class_mappings.keys())]

        self.stats_tables = StatsTables(
            class_mappings=class_mappings,
        )
        self.auc = AUC(class_mappings)
        self.validation_utils = ValidationUtils(meta_pred_true)

    def training_validation_comparison_classbased_table(self):
        rename_statistics_dict = {
            "FP": "False Positive",
            "TP": "True Positive",
            "FN": "False Negative",
            "TN": "True Negative",
            "TPR": "Recall",
            "TNR": "Specificity (TNR)",
            "PPV": "Precision",
            "NPV": "Negative Predictive Value",
            "FPR": "False Positive Rate",
            "FNR": "False Negative Rate",
            "F1": "F1",
        }

        data = {}
        content_dict = {}
        (
            accuracy,
            micro_f1,
            macro_f1,
            macro_auc,
            micro_prec,
            macro_prec,
            micro_rec,
            macro_rec,
            macro_specificity,
            micro_specificity,
            matthews,
        ) = self.stats_tables.calculate_highlighted_overall_metrics(
            true=self.true,
            pred_categorical=self.pred_categorical,
            pred_logits=self.pred_logits,
        )

        data = {
            "accuracy": {"Validation": accuracy},
            "micro_f1": {"Validation": micro_f1},
            "macro_f1": {"Validation": macro_f1},
            "macro_auc": {"Validation": macro_auc},
            "micro_precision": {"Validation": micro_prec},
            "macro_precision": {"Validation": macro_prec},
            "micro_recall": {"Validation": micro_rec},
            "macro_recall": {"Validation": macro_rec},
        }
        payload_dict = {"type": "table", "data": data}
        return payload_dict

    def tp_tn_fp_fn(self, target_class=None, target_attribute_dict=None):
        """
        Calculates true positive, true negative, false positive, false negatives for the given class.
        :param target_class: Class to calculate metrics.
        :param true: True labels for samples
        :param pred_categorical: Prediction for samples
        :return: payload_dict
        """
        filtered_meta_pred_true = self.validation_utils.filter_attribute_by_dict(
            target_attribute_dict
        )
        true = filtered_meta_pred_true["true"]
        pred_categorical = filtered_meta_pred_true["pred_categorical"]

        sense_spec_dict = self.auc.calculate_sense_spec(true, pred_categorical)

        TP = sense_spec_dict["TP"]
        TN = sense_spec_dict["TN"]
        FP = sense_spec_dict["FP"]
        FN = sense_spec_dict["FN"]

        if target_class is not None:
            TP = TP[target_class]
            TN = TN[target_class]
            FP = FP[target_class]
            FN = FN[target_class]

        payload_dict = {
            "type": "square",
            "data": {"TP": TP, "TN": TN, "FP": FP, "FN": FN},
        }
        return payload_dict

    def highlighted_overall_metrics(
        self, target_attribute_dict=None, cal_conf_interval=True
    ):
        payload_dict = {}

        image_ids = self.true.index

        if target_attribute_dict:
            filtered_meta_pred_true = self.validation_utils.filter_attribute_by_dict(
                target_attribute_dict
            )

            image_ids = filtered_meta_pred_true.index

        (
            accuracy,
            micro_f1,
            macro_f1,
            macro_auc,
            micro_prec,
            macro_prec,
            micro_rec,
            macro_rec,
            macro_specificity,
            micro_specificity,
            matthews,
        ) = self.stats_tables.calculate_highlighted_overall_metrics(
            true=self.true.loc[image_ids],
            pred_categorical=self.pred_categorical.loc[image_ids],
            pred_logits=self.pred_logits.T.loc[image_ids].T,
            cal_conf_interval=cal_conf_interval,
        )
        if cal_conf_interval:
            data = {
                "Accuracy": {
                    "Validation": accuracy[0],
                    "Confidence_Interval": list(accuracy[1]),
                },
                "Micro F1": {
                    "Validation": micro_f1[0],
                    "Confidence_Interval": list(micro_f1[1]),
                },
                "Macro F1": {
                    "Validation": macro_f1[0],
                    "Confidence_Interval": list(macro_f1[1]),
                },
                "AUC": {
                    "Validation": macro_auc[0],
                    "Confidence_Interval": list(macro_auc[1]),
                },
                "Precision": {
                    "Validation": macro_prec[0],
                    "Confidence_Interval": list(macro_prec[1]),
                },
                "Sensitivity": {
                    "Validation": macro_rec[0],
                    "Confidence_Interval": list(macro_rec[1]),
                },
                "Specificity": {
                    "Validation": macro_specificity[0],
                    "Confidence_Interval": list(macro_specificity[1]),
                },
                "Matthews C C": {
                    "Validation": matthews[0],
                    "Confidence_Interval": list(matthews[1]),
                },
            }
        else:
            data = {
                "Accuracy": {"Validation": accuracy},
                "Micro F1": {"Validation": micro_f1},
                "Macro F1": {"Validation": macro_f1},
                "AUC": {"Validation": macro_auc},
                "Precision": {"Validation": macro_prec},
                "Sensitivity": {"Validation": macro_rec},
                "Specificity": {"Validation": macro_specificity},
                "Matthews C C": {"Validation": matthews},
            }

        payload_dict["type"] = "overall"
        payload_dict["data"] = data
        return payload_dict

    def statistics_classbased_table(self, target_attribute_dict=None):
        """
        Calculates True Positive,True Negative, False Positive, False Negative for an attribute filtered data.
        :param target_class: Class of interest to calculate ROC.
        :param target_attribute_dict: Dictionary of attribute-value pairs.
        If "Age" in meta_data, target_attribute_dict = {"Age:[10,30]} indicates  Age between 10 and 30.
        If "Gender" in meta_data, target_attribute_dict = {"Gender:"male"] indicates  male accuracy.
        :return: payload_dict
        """
        #  TO DO: Reduce nofilter/filtered/multifiltered functions to single one, which is possible.
        filtered_meta_pred_true = self.validation_utils.filter_attribute_by_dict(
            target_attribute_dict
        )
        true = filtered_meta_pred_true["true"]
        pred_categorical = filtered_meta_pred_true["pred_categorical"]
        sense_spec_dict = self.stats_tables.calculate_statistics_classbased_table(
            true, pred_categorical
        )

        # Get ROC AUC
        pred_logits = self.pred_logits[pred_categorical.index]
        class_aucs = self.auc.calculate_multiclass_roc_statistics(
            true, pred_logits, return_points=False, use_class_name=False
        )

        for key in ["Micro", "Macro"]:
            class_aucs.pop(key, None)
        for key in list(class_aucs.keys()):
            class_aucs[int(key)] = class_aucs.pop(key)

        data = dict()
        stats_table_validation = pd.DataFrame(sense_spec_dict)
        stats_table_validation["AUC"] = class_aucs.values()

        stats_table_validation_renamed = stats_table_validation.rename(
            index={int(k): v for k, v in self.class_mappings.items()}
        ).T.to_dict()
        stats_table_validation_dict_per_row = [
            {"Class": keys, **dict(stats_table_validation_renamed[keys])}
            for keys in stats_table_validation_renamed
        ]

        data["Validation"] = stats_table_validation_renamed

        payload_dict = {"type": "table", "data": data}
        return payload_dict

    def class_performances(self):
        data = {}
        metrics = ["Accuracy", "F1", "TPR", "TNR", "PPV"]
        rename_statistics_dict = {
            "FP": "False Positive",
            "TP": "True Positive",
            "FN": "False Negative",
            "TN": "True Negative",
            "TPR": "Sensitivity",
            "TNR": "Specificity",
            "PPV": "Precision",
            "NPV": "Negative Predictive Value",
            "FPR": "False Positive Rate",
            "FNR": "False Negative Rate",
            "F1": "F1",
        }

        sense_spec_dict = self.auc.calculate_sense_spec(
            self.true, self.pred_categorical
        )

        # Filter designed metrics
        sense_spec_dict = {i: sense_spec_dict[i] for i in metrics}

        # Rename Metrics

        common_metrics = set(sense_spec_dict.keys()).intersection(
            rename_statistics_dict.keys()
        )

        for key in common_metrics:
            sense_spec_dict[str(rename_statistics_dict[key])] = sense_spec_dict[key]
            sense_spec_dict.pop(key)

        # Rename classes
        for key_ in sense_spec_dict:
            for class_ in self.class_order:
                sense_spec_dict[key_][
                    self.class_mappings[str(class_)]
                ] = sense_spec_dict[key_][class_]
                sense_spec_dict[key_].pop(class_)

        data["Validation"] = sense_spec_dict

        payload_dict = {}
        payload_dict["type"] = "bar"
        payload_dict["data"] = data
        return payload_dict

    def blind_spot_metrics(self, target_attribute_dict=None):
        payload_dict = {}
        image_ids = self.true.index

        if target_attribute_dict:
            filtered_meta_pred_true = self.validation_utils.filter_attribute_by_dict(
                target_attribute_dict
            )

            image_ids = filtered_meta_pred_true.index

        blind_spot_metrics_dict = self.stats_tables.calculate_blind_spot_metrics(
            true=self.true.loc[image_ids],
            pred_categorical=self.pred_categorical.loc[image_ids],
            pred_logits=self.pred_logits.T.loc[image_ids].T,
        )

        return blind_spot_metrics_dict
