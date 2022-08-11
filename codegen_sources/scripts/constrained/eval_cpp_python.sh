#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --time=2:00:00
#SBATCH --mem=80GB
#SBATCH --gres=gpu:1
#SBATCH --job-name=cpp_python_constraints
#SBATCH --output=constraints_cpp_python_%j.log

MODEL_PATH='models/transcoder_st/Online_ST_CPP_Python.pth'
DUMP_PATH='dump/transcoder_st_constraints/eval/cpp_python'
DATASET_PATH='dataset/transcoder/test'

python -m codegen_sources.model.train \
    --dump_path "$DUMP_PATH" \
    --exp_name online_st \
    --data_path "$DATASET_PATH" \
    --encoder_only false \
    --n_layers 0 \
    --n_layers_decoder 6 \
    --n_layers_encoder 6 \
    --emb_dim 1024 \
    --n_heads 8 \
    --dropout '0.1' \
    --lgs 'cpp_sa-python_sa' \
    --max_vocab 64000 \
    --max_len 512 \
    --reload_model "${MODEL_PATH},${MODEL_PATH}" \
    --optimizer 'adam_inverse_sqrt,warmup_updates=10000,lr=0.00003,weight_decay=0.01' \
    --amp 2 \
    --fp16 true \
    --max_batch_size 128 \
    --tokens_per_batch 4000 \
    --epoch_size 2500 \
    --max_epoch 10000000 \
    --clip_grad_norm 1 \
    --stopping_criterion 'valid_cpp_sa-python_sa_mt_comp_acc,25' \
    --validation_metrics 'valid_cpp_sa-python_sa_mt_comp_acc' \
    --has_sentence_ids 'valid|para,test|para' \
    --eval_bleu true \
    --eval_computation true \
    --generate_hypothesis true \
    --eval_st false \
    --eval_only true \
    --st_steps 'cpp_sa-python_sa' \
    --st_beam_size 20 \
    --lambda_st 1 \
    --robin_cache false \
    --st_sample_size 200 \
    --st_limit_tokens_per_batch true \
    --st_remove_proba '0.3' \
    --st_sample_cache_ratio '0.5' \
    --beam_size 20 \
    --constrained true \
    --correct_functions false