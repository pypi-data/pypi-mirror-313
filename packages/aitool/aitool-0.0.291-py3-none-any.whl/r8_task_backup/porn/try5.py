# -*- coding: UTF-8 -*-
import os
x = list(os.scandir('/Users/bytedance/PycharmProjects/aitool/application/aigc/core_element'))
y = [_.path for _ in x]
y.sort()
for p in y:
    print(p)


    def classify_score(self, tokenizer, messages: List[dict], stream=False, generation_config: Optional[GenerationConfig] = None, target_tokens=[92347, 93224], max_new_tokens=None):
        generation_config = generation_config or self.generation_config
        if max_new_tokens:
            generation_config.max_new_tokens = max_new_tokens
        input_ids = build_chat_input(self, tokenizer, messages, generation_config.max_new_tokens)

        outputs = self.generate(input_ids, generation_config=generation_config, output_scores=True, return_dict_in_generate=True)
        response = tokenizer.decode(outputs['sequences'][0][len(input_ids[0]):], skip_special_tokens=True)
        scores = torch.stack(outputs.scores, dim=1).softmax(-1)

        target_token_scores = dict()
        for target_token_id in target_tokens:
            target_token_scores[target_token_id] = scores[..., target_token_id].flatten().tolist()[0]
        return response, outputs, target_token_scores


def get_scores_baichuan(model, tokenizer, instruction, input, history, target_words=['是', '否']):
    message = []
    if history:
        for q, a in history:
            message.append({'role': 'user', 'content': q})
            message.append({'role': 'assistant', 'content': a})
    prompt = f'{instruction}\n{input}'
    message.append({'role': 'user', 'content': prompt})
    target_tokens = [tokenizer.encode_plus(target_word, add_special_tokens=False).input_ids[0] for target_word in target_words]
    response, output, target_token_scores= model.classify_score(tokenizer, message, max_new_tokens=3, target_tokens=target_tokens)
    ret = dict()
    for target_word in target_words:
        target_word_id = tokenizer.encode_plus(target_word, add_special_tokens=False).input_ids[0]
        ret[target_word] = target_token_scores.get(target_word_id, 0)
    return ret