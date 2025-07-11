# Fine-Tuning LLMs with LoRA

This project demonstrates how to fine-tune a Large Language Model (LLM) using LoRA (Low-Rank Adaptation) technique and then perform inference with the fine-tuned model.

## Project Overview

This project fine-tunes the `TinyLlama/TinyLlama-1.1B-Chat-v1.0` model using LoRA on a custom instruction-following dataset. The fine-tuned model can then be used for inference to generate responses to various instructions.

## Directory Structure

```text
fine_tuning_llms/
├── README.md              # This file
├── Data/
│   └── alpaca_data.json   # Training dataset in Alpaca format
└── src/
    ├── finetune.py        # Fine-tuning script
    └── infer.py           # Inference script
```

## Dataset Format

The training data (`Data/alpaca_data.json`) follows the Alpaca format:

```json
{
  "instruction": "What is photosynthesis?",
  "input": "",
  "output": "Photosynthesis is the process by which green plants convert sunlight into chemical energy."
}
```

Each entry contains:

- **instruction**: The task or question to be performed
- **input**: Additional context (often empty)
- **output**: The expected response

## Requirements

Create a virtual environment and install the required packages:

```bash
pip install torch transformers datasets peft accelerate
```

### Required Dependencies

- `torch`: PyTorch framework
- `transformers`: Hugging Face transformers library
- `datasets`: Hugging Face datasets library
- `peft`: Parameter-Efficient Fine-Tuning library for LoRA
- `accelerate`: Accelerate library for distributed training

## Usage

### 1. Fine-Tuning the Model

Run the fine-tuning script from the `src` directory:

```bash
cd src
python finetune.py
```

**What it does:**

- Loads the Alpaca dataset from `../Data/alpaca_data.json`
- Formats the data into instruction-response pairs
- Tokenizes the text with a maximum length of 512 tokens
- Applies LoRA configuration to the TinyLlama model
- Fine-tunes the model for 3 epochs
- Saves checkpoints in the `lora-tinyllama` directory

**LoRA Configuration:**

- Rank (r): 8
- Alpha: 32
- Dropout: 0.1
- Target: All linear layers for causal language modeling

**Training Parameters:**

- Batch size: 4 per device
- Epochs: 3
- Save strategy: Every epoch
- Mixed precision: Disabled (set `fp16=True` for GPU with FP16 support)

### 2. Running Inference

After fine-tuning, run the inference script:

```bash
cd src
python infer.py
```

**What it does:**

- Automatically detects and loads the latest checkpoint from `../lora-tinyllama`
- Falls back to the base model if no fine-tuned model is found
- Generates a response to a sample instruction
- Currently configured to translate "Good night" to German

**Inference Parameters:**

- Max new tokens: 15
- Temperature: 0.1 (low for focused responses)
- Sampling: Enabled

## Key Features

### Intelligent Model Loading

The `infer.py` script includes smart model detection:

1. Checks if the fine-tuned model directory exists
2. Finds all available checkpoints
3. Loads the latest checkpoint automatically
4. Falls back to the base model if no fine-tuned model is available

### LoRA (Low-Rank Adaptation)

This project uses LoRA for efficient fine-tuning:

- **Memory Efficient**: Only trains a small number of parameters
- **Fast Training**: Significantly faster than full fine-tuning
- **Preserves Base Model**: Original model weights remain unchanged
- **Easy Deployment**: LoRA adapters can be easily shared and loaded

## Customization

### Modifying the Training Data

1. Edit `Data/alpaca_data.json` with your own instruction-response pairs
2. Ensure each entry follows the Alpaca format
3. Run the fine-tuning script again

### Changing the Base Model

In `finetune.py`, modify the `model_id` variable:

```python
model_id = "your-preferred-model"  # e.g., "microsoft/DialoGPT-medium"
```

### Adjusting Training Parameters

In `finetune.py`, modify the `TrainingArguments`:

```python
args = TrainingArguments(
    output_dir="lora-tinyllama",
    per_device_train_batch_size=4,     # Adjust based on your GPU memory
    num_train_epochs=3,                # Increase for more training
    learning_rate=2e-4,                # Add custom learning rate
    # ... other parameters
)
```

### Customizing Inference Prompts

In `infer.py`, change the prompt:

```python
prompt = "### Instruction:\nYour custom instruction here.\n\n### Response:"
```

## Output

### Fine-tuning Output

The script will create a `lora-tinyllama` directory with:

- `checkpoint-{step}/`: Saved model checkpoints
- Training logs and metrics

### Inference Output

Example output:

```text
Found checkpoints: ['checkpoint-100', 'checkpoint-200', 'checkpoint-300']
Loading fine-tuned model from ../lora-tinyllama/checkpoint-300
Translation: Gute Nacht
```

## Troubleshooting

### Common Issues

1. **CUDA Out of Memory**: Reduce `per_device_train_batch_size` or `max_length`
2. **No Checkpoints Found**: Ensure fine-tuning completed successfully
3. **Import Errors**: Install all required dependencies
4. **Path Issues**: Run scripts from the `src` directory

### Performance Tips

1. **GPU Acceleration**: Set `fp16=True` in TrainingArguments if you have a compatible GPU
2. **Larger Batch Size**: Increase if you have more GPU memory
3. **More Epochs**: Increase `num_train_epochs` for better convergence

## Model Information

**Base Model**: TinyLlama/TinyLlama-1.1B-Chat-v1.0

- **Size**: 1.1 billion parameters
- **Type**: Causal language model optimized for chat
- **License**: Apache 2.0
- **Use Case**: Lightweight model suitable for resource-constrained environments

## Next Steps

1. **Experiment with different datasets**: Try domain-specific data
2. **Hyperparameter tuning**: Adjust LoRA rank, alpha, and training parameters
3. **Evaluation**: Implement metrics to evaluate model performance
4. **Deployment**: Deploy the fine-tuned model in a production environment
5. **Multi-turn conversations**: Extend to handle conversation history

## License

This project is for educational purposes. Please check the licenses of the base models and datasets used.

# About the Author

<div style="background-color: #f8f9fa; border-left: 5px solid #28a745; padding: 20px; margin-bottom: 20px; border-radius: 5px;">
  <h2 style="color: #28a745; margin-top: 0; font-family: 'Poppins', sans-serif;">Muhammad Atif Latif</h2>
  <p style="font-size: 16px; color: #495057;">Data Scientist & Machine Learning Engineer</p>
  
  <p style="font-size: 15px; color: #6c757d; margin-top: 15px;">
    Passionate about building AI solutions that solve real-world problems. Specialized in machine learning, 
    deep learning, and data analytics with experience implementing production-ready models.
  </p>
</div>

## Connect With Me

<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px;">
  <a href="https://github.com/m-Atif-Latif" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-Follow-212121?style=for-the-badge&logo=github" alt="GitHub">
  </a>
  <a href="https://www.kaggle.com/matiflatif" target="_blank">
    <img src="https://img.shields.io/badge/Kaggle-Profile-20BEFF?style=for-the-badge&logo=kaggle" alt="Kaggle">
  </a>
  <a href="https://www.linkedin.com/in/muhammad-atif-latif-13a171318" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin" alt="LinkedIn">
  </a>
  <a href="https://x.com/mianatif5867" target="_blank">
    <img src="https://img.shields.io/badge/Twitter-Follow-1DA1F2?style=for-the-badge&logo=twitter" alt="Twitter">
  </a>
  <a href="https://www.instagram.com/its_atif_ai/" target="_blank">
    <img src="https://img.shields.io/badge/Instagram-Follow-E4405F?style=for-the-badge&logo=instagram" alt="Instagram">
  </a>
  <a href="mailto:muhammadatiflatif67@gmail.com">
    <img src="https://img.shields.io/badge/Email-Contact-D14836?style=for-the-badge&logo=gmail" alt="Email">
  </a>
</div>

---