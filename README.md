# 上海创智学院2025年PE考试

> 仅供学习和交流

## set up

~~~
pip install openai
~~~



## dataset

~~~python
val.jsonl:
{
    "user_id": 5737, // ⽤⼾编号
    "item_list": [ // ⽤⼾历史观看电影列表，按时间顺序排列，越靠后表⽰越近期观看
    [1836, "Last Days of Disco, The"], // [电影ID, 电影名称]
    [3565, "Where the Heart Is"],
    // ...
    ],
    "target_item": [1893, "Beyond Silence"], // ⽤⼾实际观看的下⼀部电影 [电影ID, 电影名称]
    "candidates": [ // 推荐系统召回阶段得到的候选电影列表
    [2492, "20 Dates"],
    [684, "Windows"],
    [1893, "Beyond Silence"], // 包含⽤⼾实际观看的下⼀部电影
    // ... 
    ]
}
~~~

## use your prompt

you can change the prompt with your prompt in prompt_and_parse.py, and the parse_output function in prompt_and_parse.py.



## eval

共有5个超参数，分别是：
- api_key: str, openai的api key，**必须提供**.
- base_url: str, 模型网站，默认https://api.deepseek.com.
- model_name: str, openai的模型名称，默认为deepseek-chat.
- num_epochs: int, 训练轮数，默认为5.
- temperature: float, 模型的温度参数，默认为0.0
- ndcg@k: int, 评估指标，默认k为10，即计算NDCG@10.
- is_multi_turn: bool, 是否多轮对话，默认为False，即单轮对话.

you can change the hyperparameters in eval.sh, then run the following command to evaluate the model:
~~~bash
bash eval.sh
~~~

or you can run the following command to evaluate the model:
~~~python
python eval.py --api_key <your_api_key> --model_name <your_model_name> --num_epochs <your_num_epochs> --temperature <your_temperature> --ndcg@k <your_ndcg@k> --is_multi_turn <your_is_multi_turn>
~~~


## result(NDCG@10)

~~~
=== Processing Epoch 1/5 ===
[Epoch 1] [1/10] sample_id=405 NDCG@10 = 0.31546
[Epoch 1] [2/10] sample_id=475 NDCG@10 = 1.00000
[Epoch 1] [3/10] sample_id=522 NDCG@10 = 1.00000
[Epoch 1] [4/10] sample_id=549 NDCG@10 = 0.35621
[Epoch 1] [5/10] sample_id=554 NDCG@10 = 1.00000
[Epoch 1] [6/10] sample_id=659 NDCG@10 = 0.50000
[Epoch 1] [7/10] sample_id=706 NDCG@10 = 0.38685
[Epoch 1] [8/10] sample_id=729 NDCG@10 = 0.43068
[Epoch 1] [9/10] sample_id=738 NDCG@10 = 0.43068
[Epoch 1] [10/10] sample_id=751 NDCG@10 = 0.63093
Epoch 1 average NDCG@10 = 0.60508

=== Processing Epoch 2/5 ===
[Epoch 2] [1/10] sample_id=405 NDCG@10 = 0.33333
[Epoch 2] [2/10] sample_id=475 NDCG@10 = 1.00000
[Epoch 2] [3/10] sample_id=522 NDCG@10 = 1.00000
[Epoch 2] [4/10] sample_id=549 NDCG@10 = 0.35621
[Epoch 2] [5/10] sample_id=554 NDCG@10 = 1.00000
[Epoch 2] [6/10] sample_id=659 NDCG@10 = 0.50000
[Epoch 2] [7/10] sample_id=706 NDCG@10 = 1.00000
[Epoch 2] [8/10] sample_id=729 NDCG@10 = 0.43068
[Epoch 2] [9/10] sample_id=738 NDCG@10 = 0.43068
[Epoch 2] [10/10] sample_id=751 NDCG@10 = 0.63093
Epoch 2 average NDCG@10 = 0.66818

=== Processing Epoch 3/5 ===
[Epoch 3] [1/10] sample_id=405 NDCG@10 = 0.31546
[Epoch 3] [2/10] sample_id=475 NDCG@10 = 1.00000
[Epoch 3] [3/10] sample_id=522 NDCG@10 = 1.00000
[Epoch 3] [4/10] sample_id=549 NDCG@10 = 0.35621
[Epoch 3] [5/10] sample_id=554 NDCG@10 = 1.00000
[Epoch 3] [6/10] sample_id=659 NDCG@10 = 0.50000
[Epoch 3] [7/10] sample_id=706 NDCG@10 = 1.00000
[Epoch 3] [8/10] sample_id=729 NDCG@10 = 0.38685
[Epoch 3] [9/10] sample_id=738 NDCG@10 = 0.43068
[Epoch 3] [10/10] sample_id=751 NDCG@10 = 0.63093
Epoch 3 average NDCG@10 = 0.66201

=== Processing Epoch 4/5 ===
[Epoch 4] [1/10] sample_id=405 NDCG@10 = 0.28906
[Epoch 4] [2/10] sample_id=475 NDCG@10 = 1.00000
[Epoch 4] [3/10] sample_id=522 NDCG@10 = 1.00000
[Epoch 4] [4/10] sample_id=549 NDCG@10 = 0.35621
[Epoch 4] [5/10] sample_id=554 NDCG@10 = 1.00000
[Epoch 4] [6/10] sample_id=659 NDCG@10 = 0.50000
[Epoch 4] [7/10] sample_id=706 NDCG@10 = 1.00000
[Epoch 4] [8/10] sample_id=729 NDCG@10 = 0.43068
[Epoch 4] [9/10] sample_id=738 NDCG@10 = 0.43068
[Epoch 4] [10/10] sample_id=751 NDCG@10 = 0.63093
Epoch 4 average NDCG@10 = 0.66376

=== Processing Epoch 5/5 ===
[Epoch 5] [1/10] sample_id=405 NDCG@10 = 0.31546
[Epoch 5] [2/10] sample_id=475 NDCG@10 = 1.00000
[Epoch 5] [3/10] sample_id=522 NDCG@10 = 1.00000
[Epoch 5] [4/10] sample_id=549 NDCG@10 = 0.35621
[Epoch 5] [5/10] sample_id=554 NDCG@10 = 1.00000
[Epoch 5] [6/10] sample_id=659 NDCG@10 = 0.50000
[Epoch 5] [7/10] sample_id=706 NDCG@10 = 0.43068
[Epoch 5] [8/10] sample_id=729 NDCG@10 = 0.43068
[Epoch 5] [9/10] sample_id=738 NDCG@10 = 0.43068
[Epoch 5] [10/10] sample_id=751 NDCG@10 = 0.63093
Epoch 5 average NDCG@10 = 0.60946

=== Final Results ===
Processed 5 epochs with 10 samples each
Overall average NDCG@10 across all epochs = 0.64170
~~~





