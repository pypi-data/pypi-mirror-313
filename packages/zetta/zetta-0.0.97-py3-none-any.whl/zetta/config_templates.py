# Copyright ZettaBlock Labs 2024

lf_template = """# Code framework configuration
framework: llama-factory


# Base model configurations
base_model:
  version_id: model_version_vi68JFrIAoKpsjy71i9qe02Q


# Base datasets configuration
base_datasets:
  # Known datasets. Simply specify dataset name if it is available in [dataset_info.json](https://github.com/hiyouga/LLaMA-Factory/blob/main/data/dataset_info.json).
  # - name: alpaca_gpt4_en
  #   source: huggingface
  #   path: llamafactory/alpaca_gpt4_en
  # Custom datasets on ZettaHub. Specify the gitea path and dataset description according to https://github.com/hiyouga/LLaMA-Factory/blob/main/data/README.md.
  - name: mllm_demo
    version_id: dataset_version_tlMJt8mYRtxj10re5FWiUvku
    formatting: sharegpt
    columns:
      messages: messages
      images: images
    tags:
      role_tag: role
      content_tag: content
      user_tag: user
      assistant_tag: assistant


# Output model configurations
output_model_name: "{}"


# Fine-tune parameters configurations (compatible with llama-factory framework)
### method
stage: sft
do_train: true
finetuning_type: lora
lora_target: all

### dataset
template: llava
cutoff_len: 1024
max_samples: 1000
overwrite_cache: true
preprocessing_num_workers: 4

### output
output_dir: saves/phi3-4k/lora/sft
logging_steps: 10
save_steps: 500
plot_loss: true
overwrite_output_dir: true

### train
per_device_train_batch_size: 8
gradient_accumulation_steps: 1
learning_rate: 1.0e-5
num_train_epochs: 1.0
weight_decay: 0.1
lr_scheduler_type: cosine
warmup_ratio: 0.1
bf16: true
ddp_timeout: 180000000

### eval
eval_on_start: False
val_size: 0.1
per_device_eval_batch_size: 1
eval_strategy: steps
eval_steps: 100
"""
