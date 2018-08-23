#!/usr/bin/env sh

# Train BiLM on Mimic data
# Make sure that bin/train_elmo.py has been made executable

# source activate n2c2
export CUDA_VISIBLE_DEVICES=0

python bin/train_elmo.py \
    --train_prefix='/path/to/bilm-tf/mimic_data_*' \
    --vocab_file /path/to/bilm-tf/mimic_vocab.txt \
    --save_dir /path/to/bilm-tf/output

echo "Training done!"
