from flask import Flask, render_template, jsonify, request
import torch
from backend.model import SRC, TRG, Seq2Seq, Encoder, Decoder
import spacy

app = Flask(__name__)

# Load your trained model
def load_model():
    INPUT_DIM = len(SRC.vocab)
    OUTPUT_DIM = len(TRG.vocab)
    ENC_EMB_DIM = 256
    DEC_EMB_DIM = 256
    HID_DIM = 512
    N_LAYERS = 2
    ENC_DROPOUT = 0.5
    DEC_DROPOUT = 0.5
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    enc = Encoder(INPUT_DIM, ENC_EMB_DIM, HID_DIM, N_LAYERS, ENC_DROPOUT)
    dec = Decoder(OUTPUT_DIM, DEC_EMB_DIM, HID_DIM, N_LAYERS, DEC_DROPOUT)
    model = Seq2Seq(enc, dec, DEVICE).to(DEVICE)
    
    model.load_state_dict(torch.load('translation_model.pt', map_location=DEVICE))
    model.eval()
    
    return model

model = load_model()

# Translation function
def translate_sentence(sentence, src_field, trg_field, model, device, max_len=50):
    model.eval()
    
    if isinstance(sentence, str):
        nlp = spacy.load('zh_core_web_sm')
        tokens = [token.text.lower() for token in nlp(sentence)]
    else:
        tokens = [token.lower() for token in sentence]
        
    tokens = [src_field.init_token] + tokens + [src_field.eos_token]
    src_indexes = [src_field.vocab.stoi[token] for token in tokens]
    src_tensor = torch.LongTensor(src_indexes).unsqueeze(1).to(device)
    
    with torch.no_grad():
        hidden, cell = model.encoder(src_tensor)
        
    trg_indexes = [trg_field.vocab.stoi[trg_field.init_token]]
    
    for i in range(max_len):
        trg_tensor = torch.LongTensor([trg_indexes[-1]]).to(device)
        
        with torch.no_grad():
            output, hidden, cell = model.decoder(trg_tensor, hidden, cell)
            
        pred_token = output.argmax(1).item()
        trg_indexes.append(pred_token)
        
        if pred_token == trg_field.vocab.stoi[trg_field.eos_token]:
            break
            
    trg_tokens = [trg_field.vocab.itos[i] for i in trg_indexes]
    
    return trg_tokens[1:]

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data['text']
    src_lang = data['from']
    trg_lang = data['to']
    
    # Here you would select the appropriate model based on language pair
    # For simplicity, we'll use our Chinese-English model
    
    translation = translate_sentence(text, SRC, TRG, model, 'cpu')
    translation = ' '.join(translation[:-1])  # Remove <eos> token
    
    return jsonify({'translation': translation})

if __name__ == "__main__":
    app.run(debug=True)