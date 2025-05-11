# author: lyyyyyyyo
# contact: 17857150773@163.com
# All rights reserved.
# All effects are subject to official evaluation. Self-made content is for study only and shall not be used for commercial purposes.
import json
from openai import OpenAI
from prompt_and_parse import construct_prompt, parse_output
import math
import argparse

# calculate the ndcg@k.
def calculate_ndcg_for_sample(predicted_list, ground_truth_item, k=10):
    
    predicted_list = predicted_list[:k]

    relevance = []
    for item_id in predicted_list:
        if item_id == ground_truth_item:
            relevance.append(1)
        else:
            relevance.append(0)

    dcg = 0.0
    for i, rel in enumerate(relevance):
        discount = math.log2(i + 2)
        dcg += rel / discount

    idcg = 1/ math.log2(1 + 1) 
    
    if idcg > 0:
        ndcg = dcg / idcg
    else:
        ndcg = 0.0

    return ndcg

def main():
    
    # input the num_epochs and api_key and base_url.
    # running the code: python main.py --api_key your_api_key --base_url your_base_url --model_name deepseek-chat
    parser = argparse.ArgumentParser(description='Calculate NDCG with OpenAI API')
    parser.add_argument('--num_epochs', type=int, default=5, help='The number of epochs')
    parser.add_argument('--api_key', type=str, required=True, help='Your OpenAI API key')
    parser.add_argument('--base_url', type=str, default='https://api.deepseek.com', help='The base URL for the API') # the official test is based on: https://api.deepseek.com.
    parser.add_argument('--model_name', type=str, default='deepseek-chat', help='The model name for the API') # the official test is based on: 'deepseek-chat'.
    parser.add_argument('--temperature', type=float, default=0.0, help='The temperature for the API, 测试必须采用0.0')
    parser.add_argument('--ndcg@k', type=int, default=10, help='官方评测指标为NDCG@10')
    parser.add_argument('--is_multi_turn', type=bool, default=False, help='是否多轮对话')   
    args = parser.parse_args()
    
    client = OpenAI(api_key=args.api_key, base_url=args.base_url)
    # read all samples.
    with open("val.jsonl", "r", encoding="utf-8") as f:
        lines = f.readlines()
    samples = [json.loads(line) for line in lines]

    epoch_ndcgs = []
    for epoch in range(1, args.num_epochs + 1):
        print(f"\n=== Processing Epoch {epoch}/{args.num_epochs} ===")
        print(f"you are running the model: {args.model_name}, base_url: {args.base_url}")
        print(f"you are using the temperature: {args.temperature} with is_multi_turn: {args.is_multi_turn}")
        total_ndcg = 0.0
        count = 0

        for idx, sample in enumerate(samples, start=1):
            messages = construct_prompt(sample)
            
            if args.is_multi_turn: # 单轮对话模式。
                response = client.chat.completions.create(
                    model=args.model_name,
                    messages=messages,
                    stream=False,
                    temperature=args.temperature
                )
            else: # 多轮对话模式。
                context = []
                for message in messages:
                    context.append(message)
                    response = client.chat.completions.create(
                    model=args.model_name,
                    messages=context,
                    stream=False,
                    temperature=args.temperature
                    )
                    context.append({"role": "assistant", "content": response.choices[0].message.content.strip()})
                    
            output_text = response.choices[0].message.content.strip()

            predicted_list = parse_output(output_text)
            
            ground_truth = sample["target_item"][0]
            ndcg = calculate_ndcg_for_sample(predicted_list, ground_truth, k=10)

            total_ndcg += ndcg
            count += 1

            # show the result.
            print(f"[Epoch {epoch}] [{idx}/{len(samples)}] sample_id={sample['user_id']} NDCG@10 = {ndcg:.5f}")

        avg_ndcg = total_ndcg / count if count > 0 else 0.0
        epoch_ndcgs.append(avg_ndcg)
        
        print(f"Epoch {epoch} average NDCG@10 = {avg_ndcg:.5f}")
    
    # show the average NDCG@10.
    final_avg_ndcg = sum(epoch_ndcgs) / len(epoch_ndcgs) if epoch_ndcgs else 0.0
    print(f"\n=== Final Results ===")
    print(f"Processed {args.num_epochs} epochs with {len(samples)} samples each")
    print(f"Overall average NDCG@10 across all epochs = {final_avg_ndcg:.5f}")

if __name__ == "__main__":
    main()