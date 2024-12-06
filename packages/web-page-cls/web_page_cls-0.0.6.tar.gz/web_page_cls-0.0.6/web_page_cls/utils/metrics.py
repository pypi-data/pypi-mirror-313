"""
Collect LLM outputs and calc metrics
"""
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sn
from colorama import Fore, Style
from colorama import init as colorama_init
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

colorama_init()


class LLMMetrics:
    """
    Collect LLM outputs and calc metrics
    """

    def __init__(self, labels: list[str], strict_check=False) -> None:
        """
        strict_check: if True compare true_label == llm_output. Else: true_label in llm_output:list[str]
        """
        self.labels = list(labels)  # copy, or append UNK will change original list
        self.labels.append('UNK')
        self.strict_check = strict_check

        self.label2id = {label: i for i, label in enumerate(self.labels)}

        self.y_true = []
        self.y_pred = []

    def add_llm_str_output_and_true_value(self, llm_output: str, true_value: str):
        """
        llm_str_output has to be parsed, not valid json
        """
        pass

    def add_y_pred_strict_check(self, llm_output: list[str], true_value: str):
        """
        Strict comparison
        """
        is_parsed = False
        if isinstance(llm_output, list):
            if len(llm_output) == 1:
                if llm_output[0] == true_value:
                    self.y_pred.append(self.label2id[true_value])
                    is_parsed = True
                else:
                    for label in self.labels:
                        if label == llm_output[0]:
                            # grab first
                            self.y_pred.append(self.label2id[label])
                            is_parsed = True
                            break
        if not is_parsed:
            self.y_pred.append(self.label2id['UNK'])

    def add_y_pred_soft_check(self, llm_output: list[str], true_value: str):
        """
        Soft comparison
        """
        is_parsed = False
        if isinstance(llm_output, list):
            if len(llm_output) != 0:
                if true_value in llm_output:
                    self.y_pred.append(self.label2id[true_value])
                    is_parsed = True
                else:
                    for label in self.labels:
                        if label in llm_output:
                            # grab first
                            self.y_pred.append(self.label2id[label])
                            is_parsed = True
                            break

        elif isinstance(llm_output, str):
            if true_value == llm_output:
                self.y_pred.append(self.label2id[true_value])
                is_parsed = True
            else:
                for label in self.labels:
                    if label == llm_output:
                        # grab first
                        self.y_pred.append(self.label2id[label])
                        is_parsed = True
                        break
        if not is_parsed:
            self.y_pred.append(self.label2id['UNK'])

    def add_llm_strict_output_and_true_value(self, llm_output: list[str], true_value: str):
        """
        llm_dict_output in json valid format. May be {}, if strictjson cant handle it
        """
        if self.strict_check:
            self.add_y_pred_strict_check(llm_output, true_value)
        else:
            self.add_y_pred_soft_check(llm_output, true_value)

        self.y_true.append(self.label2id[true_value])

    def get_report(self):
        """
        Return all metrics to console. UNK - last label: not included, it's LLM error
        """

        # if self.is_all_labels_in_pred():

        return classification_report(self.y_true,
                                     self.y_pred, target_names=self.labels, labels=list(
                                         self.label2id.values())[:-1],
                                     zero_division=0.0)

    def save_confusion_matrix(self, image_path=None):
        """
        Save confusion matrix as image 
        """
        cm = confusion_matrix(self.y_true,
                              self.y_pred, labels=list(self.label2id.values())[:-1])

        fig, ax = plt.subplots(figsize=(16, 14))
        im = ax.imshow(cm, interpolation='nearest',
                       cmap=plt.cm.Blues)
        ax.figure.colorbar(im, ax=ax)

        ax.set(xticks=np.arange(cm.shape[1]),
               yticks=np.arange(cm.shape[0]),
               xticklabels=self.labels[:-1], yticklabels=self.labels[:-1],
               title='Confusion Matrix')

        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")

        if image_path is None:
            image_path = os.path.join(os.path.dirname(
                __file__), 'confusion_matrix.png')

        plt.savefig(image_path, dpi=300)


if __name__ == '__main__':

    y_true = [13]

    y_pred = [13]

    print(classification_report(y_true, y_pred, labels=[
          str(f'label {x}') for x in range(14)]))
