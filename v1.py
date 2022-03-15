# -*- coding: utf-8 -*-
"""CLUTRR_Dataset Loading Script.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1q9DdeHA5JbgTHkH6kfZe_KWHQOwHZA97
"""
# coding=utf-8
# Copyright 2019 The CLUTRR Datasets Authors and the HuggingFace Datasets Authors.
#
# CLUTRR is CC-BY-NC 4.0 (Attr Non-Commercial Inter.) licensed, as found in the LICENSE file.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""The CLUTRR (Compositional Language Understanding and Text-based Relational Reasoning) benchmark."""


import csv
import os
import textwrap

import numpy as np

import datasets
import json

_CLUTRR_CITATION = """\
@article{sinha2019clutrr,
  Author = {Koustuv Sinha and Shagun Sodhani and Jin Dong and Joelle Pineau and William L. Hamilton},
  Title = {CLUTRR: A Diagnostic Benchmark for Inductive Reasoning from Text},
  Year = {2019},
  journal = {Empirical Methods of Natural Language Processing (EMNLP)},
  arxiv = {1908.06177}
}
"""

_CLUTRR_DESCRIPTION = """\
CLUTRR (Compositional Language Understanding and Text-based Relational Reasoning),
 a diagnostic benchmark suite, is first introduced in (https://arxiv.org/abs/1908.06177) 
 to test the systematic generalization and inductive reasoning capabilities of NLU systems.
"""
_URL = "https://raw.githubusercontent.com/kliang5/CLUTRR_huggingface_dataset/main/"
_TASK = ["gen_train23_test2to10", "gen_train234_test2to10", "rob_train_clean_23_test_all_23", "rob_train_disc_23_test_all_23", "rob_train_irr_23_test_all_23","rob_train_sup_23_test_all_23"]

class v1(datasets.GeneratorBasedBuilder):
    """BuilderConfig for CLUTRR."""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name=task,
            version=datasets.Version("1.0.0"),
            description="",
        )
        for task in _TASK
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_CLUTRR_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "story": datasets.Value("string"),
                    "query": datasets.Value("string"),
                    "target": datasets.Value("int32"),
                    "clean_story": datasets.Value("string"),
                    "proof_state": datasets.Value("string"),
                    "f_comb": datasets.Value("string"),
                    "task_name": datasets.Value("string"),
                    "story_edges": datasets.Value("string"),
                    "edge_types": datasets.Value("string"),
                    "query_edge": datasets.Value("string"),
                    "genders": datasets.Value("string"),
                    "task_split": datasets.Value("string"),
                }
            ),
            # No default supervised_keys (as we have to pass both premise
            # and hypothesis as input).
            supervised_keys=None,
            homepage="https://www.cs.mcgill.ca/~ksinha4/clutrr/",
            citation=_CLUTRR_CITATION,
        )

    def _split_generators(self, dl_manager):
          """Returns SplitGenerators."""
          # dl_manager is a datasets.download.DownloadManager that can be used to
          # download and extract URLs

          task = str(self.config.name)
          urls_to_download = {
              "test": _URL + task + "/test.csv",
              "train": _URL + task + "/train.csv",
              "validation": _URL + task + "/validation.csv",
          }
          downloaded_files = dl_manager.download_and_extract(urls_to_download)
       

          return [
              datasets.SplitGenerator(
                  name=datasets.Split.TRAIN,
                  # These kwargs will be passed to _generate_examples
                  gen_kwargs={
                      "filepath": downloaded_files["train"],
                      "task": task,
                  },
              ),
              datasets.SplitGenerator(
                  name=datasets.Split.VALIDATION,
                  # These kwargs will be passed to _generate_examples
                  gen_kwargs={
                      "filepath": downloaded_files["validation"],
                      "task": task,
                  },
              ),
              datasets.SplitGenerator(
                  name=datasets.Split.TEST,
                  # These kwargs will be passed to _generate_examples
                  gen_kwargs={
                      "filepath": downloaded_files["test"],
                      "task": task,
                  },
              ),
          ]

    def _generate_examples(self, filepath, task):
      """Yields examples."""
      with open(filepath, encoding="utf-8") as f:
        reader = csv.reader(f)
        for id_, data in enumerate(reader):
          if id_ == 0:
            continue
          # yield id_, data
          # id_ += 1
          yield id_, {
              "id": data[1],
              "story": data[2],
              "query": data[3],
              "target": data[4],
              "clean_story": data[5],
              "proof_state": data[6],
              "f_comb": data[7],
              "task_name": data[8],
              "story_edges": data[9],
              "edge_types": data[10],
              "query_edge": data[11],
              "genders": data[12],
              "task_split": data[13],
            }