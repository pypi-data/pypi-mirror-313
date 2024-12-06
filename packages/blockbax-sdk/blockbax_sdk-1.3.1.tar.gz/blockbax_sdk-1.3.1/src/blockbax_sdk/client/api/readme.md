# Blockbax API

## Batching

Batching works by ordering all timestamps per ingestion ID. Before this happens the ingestion IDs are split by subject type. Ingestion ID's that cannot be split this way are put together in their own separate bucket.

Older versions called the `get_subjects` methods each time `send_measurements` is called. Newer versions will use a best effort mechanism to split this ingestion IDs and determine which subject they belong, group the ingestions per subject and order per timestamp. Then batches are created per subject per metric from oldest to newest measurement until the batch is full. Before measurements are added to the batch a check is performed if all measurements in the subject can be added to this particular batch, if not the batch is then stored in a queue and a new batch is created.

To improve efficiencies a method is needed to be as greedy as possible to fill a batch, a possible way to do this is to not only sort per timestamp but also per ingestion list size per subject and start of with the most ingestions for the oldest timestamps per subject.

## Working

The main issue that batching has to fix is the split up a large batch of N measurements into batches with a maximum of 500 measurements.

Because of the streaming nature of Blockbax there are two other problems that batching has to fix: order and grouping per subject

First and foremost, measurements need to be send in order, this does not mean that the batch needs to be in order but that there cannot be measurements from and earlier time in a later batch. Secondly Because measurements for one subject are usually depended on each other later in the streaming pipeline it is important that measurements for one subject that are relatively close in time to each other are send together in one batch.

To illustrate, with a max batch size of 3:

| Time | Subject 1 Metric 1 | Subject 1 Metric 2 | Subject 1 Metric 3 | Subject 2 Metric 1 | Subject 2 Metric 2 | Subject 2 Metric 3 |
| ---- | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| 0    | 1                  | 2                  | 3                  | 1                  | 2                  | 3                  |
| 1    | -                  | -                  | -                  | 1                  | 2                  | 3                  |
| 2    | 1                  | 2                  | 3                  | -                  | -                  | -                  |
| 3    | 1                  | -                  | -                  | 1                  | 2                  | 3                  |
| 4    | x                  | 2                  | 3                  | -                  | -                  | 3                  |
| 5    | x                  | x                  | -                  | 1                  | -                  | -                  |
| 6    | -                  | -                  | -                  | 1                  | -                  | -                  |

Batches:

| Batch number | Batch                  |
| ------------ | ---------------------- |
| 1            | S1M1T0, S1M2T0, S1M3T0 |
| 2            | S2M1T0, S2M2T0, S2M3T0 |
| 3            | S2M1T1, S2M2T1, S2M3T1 |
| 4            | S1M1T2, S1M2T2, S1M3T2 |
| 5            | -                      |
| 6            | -                      |
| 7            | -                      |
