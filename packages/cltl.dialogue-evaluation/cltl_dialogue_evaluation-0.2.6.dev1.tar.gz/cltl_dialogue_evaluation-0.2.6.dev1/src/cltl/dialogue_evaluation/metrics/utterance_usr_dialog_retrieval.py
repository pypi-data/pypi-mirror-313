from transformers import RobertaForSequenceClassification, RobertaTokenizer, RobertaConfig

#Credits:
# This code was created by Thomas Bellucci

import numpy as np
import torch

class USR_CTX:
    def __init__(self, path=None):
        """ Load pretrained and finetuned RoBERTa model for ctx.

            params
            str path: path to stored model or None

            returns: None
        """
        self.__config = RobertaConfig.from_pretrained('adamlin/usr-topicalchat-ctx')
        self.__tokenizer = RobertaTokenizer.from_pretrained('adamlin/usr-topicalchat-ctx')

        if path is not None:
            self.__model = RobertaForSequenceClassification.from_pretrained(path, config=self.__config )
        else:
            self.__model = RobertaForSequenceClassification.from_pretrained('adamlin/usr-topicalchat-ctx', config=self.__config,  local_files_only=True)

        self.__device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.__model.to(self.__device)

    def MCtx(self, context, response):
        """ Scores an input consisting of a (context, response) pair using RoBERTa.

            params
            str context:  the context strings
            sre response: response to the context

            returns: score
        """
        # Concatenates and encodes context-response pair
        inputs = self.__tokenizer(context + " [SEP] " + response, return_tensors='pt') # TODO verify separator token used in paper (standard </s> gives bad results)

        inputs['input_ids'] = inputs['input_ids'].to(self.__device)
        inputs['attention_mask'] = inputs['attention_mask'].to(self.__device)

        # Forward pass
        outputs = self.__model(**inputs)
        logits = outputs.logits.detach().cpu().numpy()

        # Returns the softmax score of the positive class, i.e. P(y=1|context, response)
        outputs = np.exp(logits) / np.sum(np.exp(logits))
        return outputs[0][1]


if __name__ == "__main__":
    pairs = [('Do you have a cat?', 'I do not have a cat'),  # good
             ('Do you have a cat?', 'I like cats'),  # not as good
             ('Do you have a cat?', 'I like kittens'),  # worse
             ('Do you have a cat?', 'I want a turtle')]  # what are we even saying

    model_xtc = USR_CTX()
    model_uk = USR_CTX(path='adamlin/usr-topicalchat-uk')
    for context, response in pairs:
        score = model_xtc.MCtx(context, response)
        print('score:', score, '\t', context, response)
