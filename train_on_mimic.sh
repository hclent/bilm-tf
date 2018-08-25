#!/usr/bin/env sh

# Train BiLM on Mimic data
# Make sure that bin/train_elmo.py has been made executable

# source activate elmo
# echo $CUDA_VISIBLE_DEVICES

python bin/train_elmo.py \
    --train_prefix='/path/to/bilm-tf/mimic_*' \
    --vocab_file /path/to/bilm-tf/mimicvocab.txt \
    --save_dir /path/to/bilm-tf/output

echo "Training done!"
