from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer

from .config import settings

app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained(settings.tokenizer)
model = AutoModelForCausalLM.from_pretrained(
    settings.model, pad_token_id=tokenizer.eos_token_id)


class AIResponse(BaseModel):
    """A container for generated text"""
    generated_text: str
    text_length: int


class Return(BaseModel):
    """A response model"""
    status: str
    ai_results: List[AIResponse]


@app.get("/email_generator", response_model=Return)
def read_root(sender: str = "me", to: str = "Thomas", subject: str = "I want to have dinner with you", token_count: int = 128, temperature: float = 0.6, n_gen: int = 1):

    seed = "From: {} \n To: {} \n Subject: {}\n\n".format(sender, to, subject)
    prompt = seed+"Dear,\n\n"

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    gen_tokens = model.generate(
        input_ids,
        max_length=token_count,
        no_repeat_ngram_size=2,
        num_return_sequences=n_gen,
        early_stopping=True,
        temperature=temperature
    )
    texts = tokenizer.batch_decode(gen_tokens)
    ai = Return(status="success", ai_results=[AIResponse(
        generated_text=x.replace(seed, ""), text_length=len(x.replace(seed, ""))) for x in texts])

    return ai


@app.get("/email_replier", response_model=Return)
def read_root(sender: str = "me", to: str = "Thomas", input: str = "topic1 \\n topic2 \\n topic3", token_count: int = 128, temperature: float = 0.6, n_gen: int = 1):

    input = input.replace(",", "\n")
    seed = "From: {} \n To: {} \n {}".format(sender, to, input)
    prompt = seed+"Dear,\n\n"

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    gen_tokens = model.generate(
        input_ids,
        max_length=token_count,
        no_repeat_ngram_size=2,
        num_return_sequences=n_gen,
        early_stopping=True,
        temperature=temperature
    )
    texts = tokenizer.batch_decode(gen_tokens)
    ai = Return(status="success", ai_results=[AIResponse(
        generated_text=x.replace(seed, ""), text_length=len(x.replace(seed, ""))) for x in texts])

    return ai
