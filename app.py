from flask import Flask, request, send_file, jsonify, render_template
from diffusers import StableDiffusionPipeline, DiffusionPipeline
import torch
import io
from flask_cors import CORS


app = Flask(__name__, template_folder="templates")
# 防止 OPTIONS 請求導致真的請求沒有送出
CORS(app)

@app.route("/")
def index():
    return render_template("cover.html")

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")

@app.route("/diary")
def diary():
    date = request.args.get("date")
    return render_template("diary.html", date=date)

pipe1 = pipe2 = pipe3 = pipe4 = pipe5 = None

def load_all_models():
    global pipe1, pipe2, pipe3, pipe4, pipe5
    print("正在載入模型...")

    try:
        pipe1 = DiffusionPipeline.from_pretrained("xyn-ai/anything-v4.0").to("cuda")
        pipe1.safety_checker = lambda images, clip_input: (images, [False] * len(images))
        print("pipe1 (anything-v4.0) 載入成功")
    except Exception as e:
        print("pipe1 載入失敗:", e)

    try:
        pipe2 = StableDiffusionPipeline.from_pretrained("nitrosocke/mo-di-diffusion", torch_dtype=torch.float16).to("cuda")
        print("pipe2 (mo-di-diffusion) 載入成功")
    except Exception as e:
        print("pipe2 載入失敗:", e)

    try:
        pipe3 = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16).to("cuda")
        print("pipe3 (sd-v1-4) 載入成功")
    except Exception as e:
        print("pipe3 載入失敗:", e)

    try:
        pipe4 = StableDiffusionPipeline.from_pretrained("Fictiverse/Stable_Diffusion_PaperCut_Model", torch_dtype=torch.float16).to("cuda")
        print("pipe4 (PaperCut) 載入成功")
    except Exception as e:
        print("pipe4 載入失敗:", e)

    try:
        pipe5 = StableDiffusionPipeline.from_pretrained("prompthero/openjourney-v4", torch_dtype=torch.float16).to("cuda")
        print("pipe5 (Openjourney) 載入成功")
    except Exception as e:
        print("pipe5 載入失敗:", e)

# image 是一個 PIL.Image.Image 物件，Flask 不能直接回傳這個類型
def image_to_response(image):
    # 建立一塊記憶體
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    # 前端會收到一張圖片
    return send_file(buf, mimetype="image/png")


# Post request 根據日記文字產生圖片
@app.route("/generate", methods=["POST"])
def generate_from_prompt():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    # 預設是 model1
    model_id = str(data.get("model", "1")).strip()
    print(f"正在使用model{model_id}")
    if not prompt:
        return jsonify({"error": "尚未填寫日記"}), 400

    model_map = {
        "1": pipe1,
        "2": pipe2,
        "3": pipe3,
        "4": pipe4,
        "5": pipe5
    }
    # 預設使用 pipe1
    pipe = model_map.get(model_id, pipe1)
    if pipe is None:
        return jsonify({"error": f"模型 {model_id} 尚未成功載入"}), 500
    if model_id == 1:
        prompt = "Use Cute Anime Style to generate" + prompt
    elif model_id == 2:
        prompt = "Use modern Disney Style to generate" + prompt
    elif model_id == 3:
        prompt = "Use Photorealistic Style to generate" + prompt
    elif model_id == 4:
        prompt = "Use Papercut Illustration to generate" + prompt
    else:
        prompt = "Use Master Painting Style to generate" + prompt

    image = pipe(prompt, num_inference_steps=30, guidance_scale=7.5).images[0]
    return image_to_response(image)


if __name__ == '__main__':
    load_all_models()
    print("所有模型準備完成，啟動 Flask server，日記開始使用")
    # 接收來自任何 IP 的請求
    app.run(host="0.0.0.0", port=5000, debug=True)
