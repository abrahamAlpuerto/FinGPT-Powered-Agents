Model
=====

The model combines a supervised learning component with an unsupervised learning component. The
supervised learning component processes the dataset and feeds this to a base model, while the
unsupervised component leverages diverse data sources to further enhance the model's capabilities.
These learned weights are then combined with the pre-trained base model.

.. image:: ../../img/Overview.png
  :width: 100%
  :align: center

For the fine-tuning process, the base model is optimized using the Low-Rank Adaptation (LoRA)
technique. By applying this method, the model's performance is refined, enabling it to better
adapt to specific tasks. In this experiment, the Llama 3.2 3B model serves as the foundational
base for the supervised and unsupervised learning.

.. image:: ../../img/Fine-tuning_Architecture.png
  :width: 50%
  :align: center
