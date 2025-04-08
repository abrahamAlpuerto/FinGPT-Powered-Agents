Dataset
=======

The source materials utilized include annual letters to Berkshire Hathaway shareholders,
transcripts of interviews and speeches, books and articles discussing Warren Buffett's
investment philosophy, as well as his public statements and market commentary. These materials
undergo a thorough data processing procedure, which involves text cleaning and normalization,
content categorization, quality filtering, and format standardization to ensure consistency
and reliability.


Source Materials
----------------

The raw data includes:

  - Annual letters to Berkshire Hathaway shareholders (1977-2021)
  - Transcripts of interviews and speeches
  - Books and articles about Buffett's investment philosophy
  - Public statements and market commentary


Data Processing
---------------

The raw data undergoes the following steps:

  - Text cleaning and normalization
  - Content categorization
  - Quality filtering
  - Format standardization


Structured Format
-----------------

Each processed entry adheres to this JSONL scheme:

.. code-block:: json

  {
    "context": "What is Warren Buffett's core investment philosophy?",  // Input query
    "target": "Buffett's investment philosophy is rooted in ..."        // Model response
  }

.. image:: ../../img/Data_Collection_Pipeline.png
  :width: 100%
  :align: center
